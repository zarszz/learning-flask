from typing import Union, List

from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from flask.typing import ResponseReturnValue

from app import db
from app.decorators import login_required
from app.models import Request

bp = Blueprint('requests', __name__)


@bp.route('/requests/new', methods=['GET'])
@login_required
def create_request() -> Union[ResponseReturnValue, str]:
    return render_template("create_request.html")


@bp.route('/requests', methods=['GET', 'POST'])
@login_required
def list_requests() -> ResponseReturnValue:
    if request.method == 'POST':
        # TODO: change user_id base on current users
        user_id: int = session['user_id']
        new_approval_request = Request(requester_id=user_id)
        db.session.add(new_approval_request)
        db.session.commit()

        flash("Request created successfully")
        return redirect(url_for("requests.view_request", id=new_approval_request.id))

    requests: List[Request] = Request.query.all()
    return render_template('list_requests.html', requests=requests)


@bp.route('/requests/<int:id>', methods=['GET'])
@login_required
def view_request(id: int) -> str:
    request_data: Request = Request.query.get_or_404(id)
    return render_template('view_request.html', request=request_data)
