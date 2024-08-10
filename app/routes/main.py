from typing import List

from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

from app.decorators import login_required
from app.models import Request

bp: Blueprint = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index() -> ResponseReturnValue:
    requests: List[Request] = Request.query.all()
    return render_template('index.html', requests=requests)
