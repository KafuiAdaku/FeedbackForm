from datetime import datetime
from feedback_form.extensions import db
from feedback_form.blueprints.user.models import User

# User model
# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255))
#     Add other user-related fields as needed


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
        - additional_comments (str): Additional comments in the review.
        - created_at (datetime): Timestamp for when the review was created.
        - user_id (int): Foreign key referencing 'id' column in 'users' table.
        - user (relationship): Relationship to the User model.
        - employee_id (int): Foreign key referencing 'id' column in 'employees'
          table.
        - employee (relationship): Relationship to the Employee model.
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    employee_feedback = db.Column(db.String(255))
    service_feedback = db.Column(db.String(255))
    additional_comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                        ondelete='CASCADE'))
    user = db.relationship('User',
                           backref=db.backref('reviews', lazy='dynamic',
                                              cascade='all, delete-orphan'))

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id',
                            ondelete='CASCADE'))
    employee = db.relationship('Employee',
                               backref=db.backref('reviews', lazy='dynamic',
                                                  cascade='all, delete-orphan')
                               )
