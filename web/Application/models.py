from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    email = db.Column(
        db.String(63),
        unique=True,
        nullable=False
    )
    name = db.Column(
        db.String(63),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(255),
        primary_key=False,
        unique=False,
        nullable=False
	)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    __table_args__ = (
        {'mysql_charset':'utf8'}
    )
    
    def __repr__(self):
        return f'<User {self.id}>'

class FileDetail(db.Model):
    __tablename__ = 'file_detail'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    filename = db.Column(
        db.String(255),
        unique=False,
        nullable=False
	)
    owner = db.Column(
        db.ForeignKey('user.id', name='user_id_fk'),
        nullable=False
    )
    signed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint('filename', 'owner', name='filename_owner_uc'),
        {'mysql_charset':'utf8'}
    )
    
    def __repr__(self):
        return f'<FileDetail {self.id}>'