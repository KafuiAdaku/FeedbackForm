#!/usr/bin/python3
"""This module contains view functions for `admin` blueprint"""
from flask import (
        Blueprint,
        flash,
        redirect,
        request,
        render_template,
        url_for)

from flask_login import login_required, current_user
from sqlalchemy import text

from feedback_form.blueprints.admin.models import Dashboard
from feedback_form.blueprints.user.decorators import role_required
from feedback_form.blueprints.user.models import User
from feedback_form.blueprints.admin.forms import (
        SearchForm,
        BulkDeleteForm,
        UserForm
        )

admin = Blueprint("admin", __name__, template_folder="templates",
                  url_prefix="/admin")


@admin.before_request
@login_required
@role_required("admin")
def before_request():
    """Protects all admin endpoints"""
    pass


# **********Dashboard***********
@admin.route("")
def dashboard():
    group_and_count_users = Dashboard.group_and_count_users()

    return render_template("admin/page/dashboard.html",
                           group_and_count_users=group_and_count_users)


# **********Users***************
@admin.route("/users", defaults={"page": 1})
@admin.route("/users/page/<int:page>")
def users(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = User.sort_by(request.args.get("sort", "created_on"),
                           request.args.get("direction", "desc"))
    order_values = f"{sort_by[0]} {sort_by[1]}"

    search_expr = User.search(request.args.get('q', ''))
    print(f"Search Expression: {search_expr}")

    if search_expr is not None:
        paginated_users = User.query.filter(search_expr)\
                .order_by(User.role.asc(), text(order_values))\
                .paginate(page=page, per_page=50, error_out=True)
    else:
        paginated_users = User.query\
                .order_by(User.role.asc(), text(order_values))\
                .paginate(page=page, per_page=50, error_out=True)

    return render_template("admin/user/index.html", form=search_form,
                           bulk_form=bulk_form, users=paginated_users)


@admin.route("/users/edit/<int:id>", methods=["GET", "POST"])
def users_edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if User.is_last_admin(user, request.form.get("role"),
                              request.form.get("active")):
            flash("You are the last admin, you cannot do that", "error")
            return redirect(url_for("admin.users"))

        form.populate_obj(user)

        if not user.username:
            user.username = None

        user.save()

        flash("User has been saved successfully.", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/user/edit.html", form=form, user=user)


@admin.route("users/bulk_delete", methods=["POST"])
def users_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = User.get_bulk_action_ids(request.form.get("scope"),
                                       request.form.getlist("bulk_ids"),
                                       omit_ids=[current_user.id],
                                       query=request.form.get("q"))
        delete_account = User.bulk_delete(ids)

        flash(f"{delete_account} user(s) were scheduled to be deleted.",
              "success")

    else:
        flash("No users were deleted,something went wrong", "error")

    return redirect(url_for("admin.users"))
