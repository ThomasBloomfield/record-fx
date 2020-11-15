from flask import Blueprint, render_template
from ...plotlydash.dashboard import url_base

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def home():
   return render_template('page/home.html')

@page.route('/terms')
def terms():
    return render_template('page/terms.html')


@page.route('/privacy')
def privacy():
    return render_template('page/privacy.html')


@page.route('/faqs')
def faqs():
    return render_template('page/faqs.html')

@page.route('/dashboard')
def dashboard():
	return render_template('page/dashboard.html',
		dash_url=url_base
		)