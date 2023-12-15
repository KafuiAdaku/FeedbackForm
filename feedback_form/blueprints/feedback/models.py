from datetime import datetime
from feedback_form.extensions import db

# User model
# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255))
    # Add other user-related fields as needed

class Employee(db.Model):
    """
    Model representing employee information.

    Fields:
        - id (int): Primary key for the 'employees' table.
        - employee_name (str): Employee's name.
    """
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(255))

class Review(db.Model):
    """
    Model representing feedback reviews.

    Fields:
        - id (int): Primary key for the 'reviews' table.
        - employee_feedback (str): Feedback on the employee's performance.
        - service_feedback (str): Feedback on the service provided.
        - additional_comments (str): Additional comments provided in the review.
        - created_at (datetime): Timestamp indicating when the review was created.
        - user_id (int): Foreign key referencing the 'id' column in the 'users' table.
        - user (relationship): Relationship to the User model.
        - employee_id (int): Foreign key referencing the 'id' column in the 'employees' table.
        - employee (relationship): Relationship to the Employee model.
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    employee_feedback = db.Column(db.String(255))
    service_feedback = db.Column(db.String(255))
    additional_comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    employee = db.relationship('Employee', backref=db.backref('reviews', lazy='dynamic'))
