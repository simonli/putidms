from __future__ import with_statement
from flask import Blueprint, request, render_template
from datetime import datetime
from putidms.forms.login_form import LoginForm

mod = Blueprint('index', __name__)


@mod.route('/')
def index():
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return 'Hello World. - %s' % date_str


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            print "*"*50
            return form.username.data
    return render_template('login.html',form=form)
