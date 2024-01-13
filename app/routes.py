from flask import render_template, request, jsonify
from app import app, db
from app.models import User
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for {form.email.data}!', 'info')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        flash('Test')
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        
        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'}), 201

@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify({'users': user_list})

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.username = data['username']
    user.email = data['email']
    db.session.commit()

    return jsonify({'message': 'User updated successfully'})

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})
