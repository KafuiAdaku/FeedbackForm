from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    url_for,
    render_template
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required)

from feedback_form.blueprints.user.decorators import anonymous_required
from lib.safe_next_url import safe_next_url
from feedback_form.blueprints.user.models import User

from feedback_form.blueprints.feedback.forms import FeedbackForm, ContactForm
# from feedback_form.blueprints.feedback.email import send_feedback_email
from feedback_form.extensions import mail, db
from feedback_form.blueprints.feedback.models import Review, Employee

feedback = Blueprint('feedback', __name__, template_folder='templates')

@feedback.route('/feedback', methods=['GET', 'POST'])
@login_required
def index():
    form = FeedbackForm()

    """ fetch employees from database"""
    employees = Employee.query.all()

    # Create a list of tuples from the employee data
    employee_data = [(str(employee.id),
                      employee.employee_name) for employee in employees]
    
    # Set choices for the form
    form.employee_feedback.choices = employee_data

    if form.validate_on_submit():
        """ to avoid circular imports """
        # from feedback_form.tasks import send_async_email

        username = current_user.username
        user_email = current_user.email
        
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

        # send_async_email.delay(selected_employee.employee_name,
        #                        service_feedback, additional_comments)
        from feedback_form.blueprints.feedback.tasks import \
               deliver_feedback_email
        deliver_feedback_email(
                user_email,
                additional_comments,
                selected_employee.id,
                service_feedback)


        flash('Your feedback has been successfully submitted!', 'success')
        return redirect(url_for('page.success_page'))
    return render_template('feedback/index.html', form=form)


@feedback.route('/contact', methods=['GET', 'POST'])
@anonymous_required()
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        """send email on form submission"""
        # from feedback_form.tasks import send_async_email_contact
        
        # send_async_email_contact.delay(
        #     form.name.data,
        #     form.email.data,
        #     form.message.data
        # )

        from feedback_form.blueprints.feedback.tasks import \
                deliver_contact_email
        deliver_contact_email(request.form.get("name"),
                              request.form.get("email"),
                              request.form.get("message")
                              )
        flash('Your message has been successfully sent!', 'success')
        return redirect(url_for('page.success_page'))

    return render_template('feedback/contact.html', form=form)
