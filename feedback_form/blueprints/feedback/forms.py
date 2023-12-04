from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired


class FeedbackForm(FlaskForm):
    employee_feedback = SelectField('Select Employee', validators=[InputRequired()])
    service_feedback = SelectField('How was the service?', choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ], default='good', validators=[InputRequired()])

    additional_comments = TextAreaField('Additional Comments')
    submit_button = SubmitField('Submit Feedback')
