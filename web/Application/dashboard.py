from flask import Blueprint, render_template, current_app
from flask import redirect, url_for, flash, send_from_directory
from flask_login import login_required, logout_user, current_user

from .forms import UploadForm

from os.path import join, isfile, basename, splitext
from werkzeug.utils import secure_filename

from .models import FileDetail
from . import db

from .forms import ViewForm, MergeForm, DeleteForm, ReorderForm

import requests
import json

from datetime import datetime
from re import sub
from string import punctuation

dashboard_bp = Blueprint(
    'dashboard_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@dashboard_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(current_app.config.get('BASE_URL') + \
        url_for('auth_bp.login'))

@dashboard_bp.route('/', methods=['GET', 'POST'])
@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template(
        'dashboard.jinja2',
        title='Dashboard',
        base_url=current_app.config.get('BASE_URL')
    )

@dashboard_bp.route('/upload', methods=['GET', 'POST'])
@login_required 
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        redirect_url = current_app.config.get('BASE_URL') + \
            url_for('dashboard_bp.upload')
        
        f = form.upload.data
        
        file_detail = FileDetail()
        file_detail.filename = \
            add_extension(process_filename(secure_filename(f.filename)))
        file_detail.owner = current_user.id
        
        result = add_to_db(file_detail)
        if not result:
            return redirect(redirect_url)
        
        try:
            f.save(get_standard_filepath(file_detail))
        except:
            return redirect(redirect_url)
        
        result = commit_to_db()
        if not result:
            return redirect(redirect_url)

        
        flash('File uploaded successfully.')
    
    return render_template(
        'upload.jinja2',
        title='Upload',
        base_url=current_app.config.get('BASE_URL'),
        form=form
    )

@dashboard_bp.route('/uploads/<int:file_detail_id>')
def obtain_file(file_detail_id):
    file_detail = check_file(FileDetail.query.filter_by(
        id=file_detail_id
    ).first())
    if not file_detail:
        return 'File does not exist', 404
    
    return send_from_directory(current_app.config.get('STORAGE_PATH'), \
        get_standard_filename(file_detail))

@dashboard_bp.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    form = ViewForm()
    form.filename.choices = \
        populate_filename_choices(current_user.id)
    
    file_detail=None
    if form.validate_on_submit():
        file_detail = check_file(FileDetail.query.filter_by(
            id=form.filename.data
        ).first())
        if not file_detail:
            flash('Unable to retrieve file.')
    
    return render_template(
        'view.jinja2',
        title='View',
        base_url=current_app.config.get('BASE_URL'),
        form=form,
        file_detail=file_detail,
        client_id=None # current_app.config.get('EMBED_API_ID')
    )

@dashboard_bp.route('/merge', methods=['GET', 'POST'])
@login_required
def merge():
    form = MergeForm()
    
    form.first_filename.choices = \
        populate_filename_choices(current_user.id)
    form.second_filename.choices = \
        populate_filename_choices(current_user.id)
    
    if form.validate_on_submit():
        redirect_url = current_app.config.get('BASE_URL') + \
            url_for('dashboard_bp.merge')
        
        first_file_detail = check_file(FileDetail.query.filter_by(
            id=form.first_filename.data
        ).first())
        if not first_file_detail:
            flash(f'File {form.first_filename.data} absent.')
        
        second_file_detail = check_file(FileDetail.query.filter_by(
            id=form.second_filename.data
        ).first())
        if not second_file_detail:
            flash(f'File {form.first_filename.data} absent.')
        
        if not first_file_detail or not second_file_detail:
            flash('Unable to merge requested files.')
            return redirect(redirect_url)
        
        merged_file_detail = FileDetail()
        merged_file_detail.filename = \
            add_extension(process_filename(secure_filename(
                f'merged_{get_timestamp()}' \
                    f'_{process_filename(first_file_detail.filename)}' \
                        f'_{process_filename(second_file_detail.filename)}'
            )))
        merged_file_detail.owner = current_user.id

        result = add_to_db(merged_file_detail)
        if not result:
            return redirect(redirect_url)

        data = {
            'file1': get_standard_filepath(first_file_detail),
            'file2': get_standard_filepath(second_file_detail),
            'output': get_standard_filepath(merged_file_detail)
        }
        
        response = post(current_app.config.get('MERGE'), data=data)
        if not response.get('status', False):
            flash('Merge failure. Please retry.')
            rollback_db()
            return redirect(redirect_url)
        
        flash('Merge process initiated.')
        
        result = commit_to_db()
        if not result:
            return redirect(redirect_url)
        
        flash(f'{merged_file_detail.filename} will be available ' \
            'after process is successfully completed.')
    
    return render_template(
        'merge.jinja2',
        title='Merge',
        base_url=current_app.config.get('BASE_URL'),
        form=form
    )

@dashboard_bp.route('/split', methods=['GET', 'POST'])
@login_required
def split():
    return render_template(
        'split.jinja2',
        title='Split',
        base_url=current_app.config.get('BASE_URL')
    )

@dashboard_bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeleteForm()
    
    form.filename.choices = \
        populate_filename_choices(current_user.id)
    
    if form.validate_on_submit():
        redirect_url = current_app.config.get('BASE_URL') + \
                url_for('dashboard_bp.delete')
        
        try:
            page = int(form.page.data)
        except:
            flash('Page number must be an integer.')
            redirect(redirect_url)

        file_detail = check_file(FileDetail.query.filter_by(
            id=form.filename.data
        ).first())
        if not file_detail:
            flash(f'File {form.filename.data} absent.')
            return redirect(redirect_url)
        
        modified_file_detail = FileDetail()
        modified_file_detail.filename = \
            add_extension(process_filename(secure_filename(
                f'modified_{get_timestamp()}' \
                    f'_{process_filename(file_detail.filename)}'
            )))
        modified_file_detail.owner = current_user.id
        
        result = add_to_db(modified_file_detail)
        if not result:
            return redirect(redirect_url)
        
        data = {
            'file': get_standard_filepath(file_detail),
            'page': page,
            'output': get_standard_filepath(modified_file_detail)
        }
        
        response = post(current_app.config.get('DELETE'), data=data)
        if not response.get('status', False):
            flash('Page delete failure. Please retry.')
            rollback_db()
            return redirect(redirect_url)
        
        flash('Page deletion process initiated.')
        
        result = commit_to_db()
        if not result:
            return redirect(redirect_url)
        
        flash(f'{modified_file_detail.filename} will be available ' \
            'after process is successfully completed.')

    return render_template(
        'delete.jinja2',
        title='Delete',
        base_url=current_app.config.get('BASE_URL'),
        form=form
    )

@dashboard_bp.route('/reorder', methods=['GET', 'POST'])
@login_required
def reorder():
    form = ReorderForm()
    
    form.filename.choices = \
        populate_filename_choices(current_user.id)
    
    if form.validate_on_submit():
        redirect_url = current_app.config.get('BASE_URL') + \
            url_for('dashboard_bp.reorder')

        try:
            pages = [int(page.strip()) for page in form.pages.data.split(',')]
        except:
            flash('Invalid page input.')
            return redirect(redirect_url)
        
        file_detail = check_file(FileDetail.query.filter_by(
            id=form.filename.data
        ).first())
        if not file_detail:
            flash(f'File {form.filename.data} absent.')
            return redirect(redirect)
        
        reordered_file_detail = FileDetail()
        reordered_file_detail.filename = \
            add_extension(process_filename(secure_filename(
                f'reordered_{get_timestamp()}' \
                    f'_{process_filename(file_detail.filename)}'
            )))
        reordered_file_detail.owner = current_user.id

        result = add_to_db(reordered_file_detail)
        if not result:
            return redirect(redirect_url)

        data = {
            'file': get_standard_filepath(file_detail),
            'pages': pages,
            'output': get_standard_filepath(reordered_file_detail)
        }
        
        response = post(current_app.config.get('REORDER'), data=data)
        if not response.get('status', False):
            flash('Page reorder failure. Please retry.')
            rollback_db()
            return redirect(redirect_url)
        
        flash('Page reorder process initiated.')
        
        result = commit_to_db()
        if not result:
            return redirect(redirect_url)
        
        flash(f'{reordered_file_detail.filename} will be available ' \
            'after process is successfully completed.')
    
    return render_template(
        'reorder.jinja2',
        title='Reorder',
        base_url=current_app.config.get('BASE_URL'),
        form=form
    )

@dashboard_bp.route('/sign', methods=['GET', 'POST'])
@login_required
def sign():
    return render_template(
        'sign.jinja2',
        title='Sign',
        base_url=current_app.config.get('BASE_URL')
    )

def rollback_db():
    db.session.rollback()
    return False

def add_to_db(entity, flush=True):
    try:
        db.session.add(entity)
        if flush:
            db.session.flush()
    except:
        flash('Add to database failed.')
        return rollback_db()
    
    return True

def commit_to_db():
    try:
        db.session.commit()
    except:
        flash('Commit to database failed.')
        return rollback_db()
    
    return True

def add_extension(filename, ext='pdf'):
    filename = splitext(basename(filename))[0]
    return f'{filename}.{ext}'

def get_timestamp():
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

def process_filename(filename):
    if not filename:
        return f'unnamed_{get_timestamp()}'
    
    filename = splitext(basename(filename))[0]
    for punc in punctuation:
        filename = filename.replace(punc, ' ')
    filename = sub(' +', '_', filename)

    return filename[:60] if len(filename) > 60 else filename

def get_standard_filename(file_detail):
    return f'{file_detail.id}.pdf'

def get_standard_filepath(file_detail):
    path = join(current_app.config.get('STORAGE_PATH'), \
        get_standard_filename(file_detail))
    return path

def populate_filename_choices(owner):
    file_details = FileDetail.query.filter_by(
        owner=owner
    ).all()
    
    return [(file_detail.id, file_detail.filename) \
        for file_detail in file_details \
            if check_file(file_detail)]

def check_file(file_detail):
    if file_detail and isfile(get_standard_filepath(file_detail)):
        return file_detail
    return None

def post(endpoint, data=None, files=None, headers=None, as_dict=True):
    response = requests.post(endpoint, data=data, files=files, headers=headers)
    response = response.json()
    
    if as_dict and isinstance(response, str):
        return json.loads(response)
    return response