from flask import Blueprint, redirect, flash, render_template, url_for, current_app, request
from flask_login import current_user, login_user

from . import login_manager
from .forms import RegisterForm, LoginForm
from .models import db, User

auth_bp = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User()
            user.email = form.email.data
            user.name = form.name.data
            user.set_password(form.password.data)
            
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                flash('Error occured when registering user.')
                return redirect(current_app.config.get('BASE_URL') + \
                    url_for('auth.register'))
            
            login_user(user)  # Log in as newly created user
            
            return redirect(current_app.config.get('BASE_URL') + \
                url_for('dashboard_bp.dashboard'))
        
        flash('A user already exists with that email address.')
    
    return render_template(
        'register.jinja2',
        title='Create an Account',
        base_url=current_app.config.get('BASE_URL'),
        form=form
    )

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(current_app.config.get('BASE_URL') + \
            url_for('dashboard_bp.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or current_app.config.get('BASE_URL') + \
                    url_for('dashboard_bp.dashboard'))
        
        flash('Invalid username/password combination.')
        return redirect(current_app.config.get('BASE_URL') + \
            url_for('auth_bp.login'))
    
    return render_template(
        'login.jinja2',
        form=form,
        title='Log In',
        base_url=current_app.config.get('BASE_URL')
    )

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(current_app.config.get('BASE_URL') + \
        url_for('auth_bp.login'))