from flask import Blueprint, redirect, url_for, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    flash('Authorization is disabled. Proceeding as guest.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    flash('Registration is disabled.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/logout')
def logout():
    flash('You have been logged out (dummy action).', 'info')
    return redirect(url_for('main.index'))
