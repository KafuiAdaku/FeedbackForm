from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email


class FeedbackForm(FlaskForm):
    """
    Form for collecting feedback information.

    Fields:
        - employee_feedback (SelectField): Dropdown for selecting an employee.
        - service_feedback (SelectField): Dropdown for rating the service.
        - additional_comments (TextAreaField): Text area for additional comments.
        - submit_button (SubmitField): Button to submit feedback.
    """
    employee_feedback = SelectField('Select Employee', validators=[InputRequired()])
    service_feedback = SelectField('How was the service?', choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ], default='good', validators=[InputRequired()])

    additional_comments = TextAreaField('Additional Comments')
    submit_button = SubmitField('Submit Feedback')


class ContactForm(FlaskForm):
    """
    Form for collecting contact information and messages.

    Fields:
        - name (StringField): Input field for the user's name.
        - email (StringField): Input field for the user's email.
        - message (TextAreaField): Text area for the user's message.
        - submit_button (SubmitField): Button to send the message.
    """
    name = StringField('Your Name', validators=[InputRequired()])
    email = StringField('Your Email', validators=[InputRequired(), Email()])
    message = TextAreaField('Your Message', validators=[InputRequired()])
    submit_button = SubmitField('Send Message')