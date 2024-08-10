import datetime
from datetime import datetime

from flask import Blueprint, redirect, session, url_for, flash, render_template
from flask.typing import ResponseReturnValue

from app import db
from app.decorators import login_required, role_required
from app.models import Request, ApprovalLevel

bp = Blueprint('approvals', __name__)


@bp.route('/requests/<int:id>/approve', methods=['POST'])
@login_required
@role_required('Approver')
def approve_request(id: int) -> ResponseReturnValue:
    request_data: Request = Request.query.get_or_404(id)
    current_level: int = request_data.current_approval_level

    approval_level: ApprovalLevel = ApprovalLevel.query.filter_by(request_id=1, level=current_level).first()
    if approval_level and approval_level.status == 'pending':
        approval_level.status = 'approved'
        approval_level.approved_by = session['user_id']
        approval_level.approved_at = datetime.utcnow()

        request_data.current_approval_level += 1
        db.session.commit()

        flash("Request approved successfully")
    else:
        flash("Unable to approve request")
    return redirect(url_for("requests.view_request", id=id))


@bp.route('/requests/<int:id>/reject', methods=['POST'])
@login_required
@role_required('Approver')
def reject_request(id: int) -> ResponseReturnValue:
    request_data: Request = Request.query.get_or_404(id)
    current_level: int = request_data.current_approval_level

    approval_level: ApprovalLevel = ApprovalLevel.query.filter_by(request_id=id, level=current_level).first()

    if approval_level and approval_level.status == 'pending':
        approval_level.status = 'rejected'
        approval_level.approved_by = session['user_id']  # This should be fetched from the logged-in user's session
        approval_level.approved_at = datetime.utcnow()

        request_data.status = 'rejected'
        db.session.commit()

        flash('Request rejected successfully!')
    else:
        flash('Unable to reject request.')

    return redirect(url_for('requests.view_request', id=id))
