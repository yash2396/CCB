from Operations.database_operation import *

import os
import logging as log

from flask import Flask, request, render_template, session, send_from_directory, jsonify, redirect, url_for
from flaskext.mysql import MySQL

from Config_and_Log import logs, config
from main_controller import bot_controller, dashboard_controller

logs.initialize_logger("BitBot")


app = Flask(__name__)

app.secret_key = "BitBotByYard"

app.config['MYSQL_DATABASE_HOST'] = config.sql['host']
app.config['MYSQL_DATABASE_USER'] = config.sql['user']
app.config['MYSQL_DATABASE_PASSWORD'] = config.sql['password']
app.config['MYSQL_DATABASE_DB'] = config.sql['database']
mysql = MySQL(app)


@app.route('/response', methods=['GET', 'POST'])
def bot_response():
    log.debug("Inside bot_response function.")
    show_details = True

    if request.method == 'POST':
        input_message = request.form['input_message']
        user_id = request.form['userID']
        selected_language = request.form['selected_language']

        context = session['context']

        log.debug("Received parameters: " + str(input_message) + " : " + str(user_id) + " : " + str(selected_language) +
                  " : " + str(context))

        res = bot_controller(input_message, user_id, selected_language, context, show_details, mysql)

        if type(res) is not tuple:
            session['context'] = res['context']
        else:
            return "", 500

        return jsonify(res)

    else:
        log.error("Error in bot_response. Sending Internal Error 500.")
        return "", 500


@app.route('/tts', methods=['GET', 'POST'])
def tts():
    log.debug("Inside tts function.")
    filename = request.args['filename']
    
    if filename is not None:
        return send_from_directory(os.path.dirname(__file__) + '/Speech', filename)
    else:
        log.error("Error in tts function. Sending Internal Error 500.")
        return "", 500


@app.route('/lang', methods=['GET', 'POST'])
def lang():
    log.debug("Inside lang function.")

    if request.method == 'POST':
        set_language = request.form['selected_language']
        return render_template('lang/' + set_language + '.json')
    else:
        log.error("Error in lang function. Sending default english.")
        return render_template('lang/en-US.json')


@app.route('/bitbot')
def bitbot():
    log.debug("Inside index function.")
    session.pop('context', None)
    session['context'] = ""
    return render_template('bitbot.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    log.debug("Inside login function.")

    error = None
    alert_color = 'red'
    if request.method == 'POST':
        flag = request.form['flag']
        username = request.form['username']

        if flag == "login":
            password = request.form['password']
            role = login_check(mysql, username, password)
            if role:
                session['role'] = role
                print(role)
                return redirect(url_for('dashboard'))
            elif not role:
                error = "Invalid Username or Password."
            else:
                error = "System error. Try again or contact administration."

        elif flag == 'forgot':
            status = forgot_password(mysql, username)
            if status is not None:
                error = "Mail has been sent to your email id."
                alert_color = 'light-green'
            elif not status:
                error = "Invalid Username."
            else:
                error = "System error. Try again or contact administration."

    return render_template('login.html', error=error, alert_color=alert_color)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    log.debug("Inside reset_password function.")
    error = None
    alert_color = "red"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        status = reset_password_db(mysql, username, str(password))
        if status:
            error = "Password successfully reset."
            alert_color = "light-green"
        else:
            error = "Failed to reset password. Link is expired or using last password."

    elif request.method == 'GET':
        id_ = request.args['id']
        username = get_username(mysql, id_)

        if (username is None) or (not username):
            error = "System error. Link is expired. Try again later."
        else:
            return render_template('reset_password.html', username=username)

    return render_template('login.html', error=error, alert_color=alert_color)


@app.route('/logout')
def logout():
    session.pop('role', None)
    return render_template('login.html', error="Logged out successfully.", alert_color="light-green")


@app.route('/dashboard')
def dashboard():
    log.debug("Inside dashboard function.")

    if "role" in session:
        res = dashboard_controller(mysql, session['role'])

        if res is not None:
            return render_template('dashboard.html', role=session['role'], res=res)
        else:
            error = "System Error. Try Again."

    else:
        error = "Please login."

    return render_template('login.html', error=error, alert_color="red")


@app.route('/update-data', methods=['GET', 'POST'])
def update_data():
    log.debug("Inside update_data function.")
    if request.method == 'POST':
        department = request.form['department']
        full_data = request.form['full_data']

        if "role" in session:
            status = get_update_data(mysql, department, full_data)
            if status is not None:
                return "Updated Successfully."
            else:
                return "", 500
        else:
            return "", 401

    else:
        return "", 500


@app.route('/update-email', methods=['GET', 'POST'])
def update_email():
    log.debug("Inside update_email function.")
    if request.method == 'POST':
        department = request.form['department']
        email = request.form['email']

        if "role" in session:
            if str(session['role']) == "Administration":
                status = get_update_email(mysql, department, email)
                if status is not None:
                    return "Updated Successfully."
                else:
                    return "", 500
            else:
                return "", 401
        else:
            return "", 401

    else:
        return "", 500


@app.route('/update-password', methods=['GET', 'POST'])
def update_password():
    log.debug("Inside update_password function.")
    if request.method == 'POST':
        role = request.form['role']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        if "role" in session:
            if str(session['role']) == role:
                status = get_update_password(mysql, role, old_password, new_password)
                if status is not None:
                    return jsonify(status)
                else:
                    return "", 500
            else:
                return "", 401
        else:
            return "", 401

    else:
        return "", 500


@app.route('/test')
def test():
    res = dashboard_controller(mysql, "Physiotherapy")

    if res is not None:
        return render_template('dashboard.html', role="Physiotherapy", res=res)


if __name__ == '__main__':
    app.run()
