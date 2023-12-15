from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    url_for,
    render_template
)

from feedback_form.blueprints.feedback.forms import FeedbackForm, ContactForm
from feedback_form.extentions import mail, db
from feedback_form.blueprints.feedback.models import Review, Employee

feedback = Blueprint('feedback', __name__, template_folder='templates')

@feedback.route('/feedback', methods=['GET', 'POST'])
def index():
    """
    Endpoint to handle feedback form submissions.

    :return: Rendered template or redirect to success page upon successful submission.
    """
    form = FeedbackForm()

    """ fetch employees from database"""
    employees = Employee.query.all()

    employee_data = [(str(employee.id),
                      employee.employee_name) for employee in employees]
    
    form.employee_feedback.choices = employee_data

    if form.validate_on_submit():
        # Importing inside the function to avoid circular imports
        from feedback_form.tasks import send_async_email
        
        employee_id = form.employee_feedback.data
        service_feedback = form.service_feedback.data
        additional_comments = form.additional_comments.data

        # Fetch the selected employee
        selected_employee = Employee.query.get(int(employee_id))

        # Create a Review instance and add it to the database
        review_entry = Review(
            employee_feedback=selected_employee.employee_name,
            service_feedback=service_feedback,
            additional_comments=additional_comments,
            employee=selected_employee
        )
        db.session.add(review_entry)
        db.session.commit()

        # Send asynchronous email notification
        send_async_email.delay(selected_employee.employee_name,
                               service_feedback, additional_comments)

        flash('Your feedback has been successfully submitted!', 'success')
        return redirect(url_for('page.success_page'))
    return render_template('feedback/index.html', form=form)


@feedback.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Endpoint to handle contact form submissions.

    :return: Rendered template or redirect to success page upon successful submission.
    """
    form = ContactForm()

    if form.validate_on_submit():
        """send email on form submission"""
        from feedback_form.tasks import send_async_email_contact
        
        send_async_email_contact.delay(
            form.name.data,
            form.email.data,
            form.message.data
        )

        flash('Your message has been successfully sent!', 'success')
        return redirect(url_for('page.success_page'))

    return render_template('feedback/contact.html', form=form)