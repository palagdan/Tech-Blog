from flask import Blueprint,render_template


groups = Blueprint('groups', __name__)


@groups.route('/groups')
def groups_page():
    return render_template('groups/groups.html')