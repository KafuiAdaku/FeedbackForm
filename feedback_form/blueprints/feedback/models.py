from datetime import datetime
from feedback_form.extensions import db

from datetime import datetime
from feedback_form.extensions import db

# User model
# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255))
    # Add other user-related fields as needed

# Employee model
class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(255))
    # Add other employee-related fields as needed

# Review model with relationships
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    employee_feedback = db.Column(db.String(255))
    service_feedback = db.Column(db.String(255))
    additional_comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    employee = db.relationship('Employee', backref=db.backref('reviews', lazy='dynamic'))
