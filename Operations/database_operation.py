import logging as log
import datetime

from random import randint
from Config_and_Log import logs, config
from Operations.Mail.mail import send_mail

logs.initialize_logger("database_operation")


def replace_tag_data(mysql, full_response):
    log.debug("inside replace_tag_data function.")

    try:
        # replace * with department name which is coming from context variable.
        department_name = str(full_response['context']).replace("_", " ")
        full_response['message'] = str(full_response['message']).replace("*", department_name)

        str_rv = ""
        if (str(full_response['message']).find("#")) > (-1):
            temp_store = str(full_response['message']).split('#')
            tags = temp_store[1::2]

            for tag in tags:
                if tag != "" and str(full_response['context']) != "":
                    cur = mysql.get_db().cursor()
                    result = cur.execute("SELECT status FROM " + full_response['context'] +
                                         " WHERE tag = '" + tag + "'")

                    if result > 0:
                        rv = cur.fetchall()
                    else:
                        cur.execute("SELECT status FROM Administration WHERE tag = '" + tag + "'")
                        rv = cur.fetchall()

                    for row in rv:
                        str_rv = ''.join(map(str, row))

                    cur.close()
                    temp_replace = "#" + tag + "#"
                    full_response['message'] = str(full_response['message']).replace(temp_replace, str_rv)

            return full_response['message']

        else:
            return full_response['message']

    except Exception as e:
        log.error("Error in replace_tag_data. Error message: %s", e)


def total_response_update(mysql, role):
    log.debug("Inside total_response function.")
    try:
        cur = mysql.get_db().cursor()
        result = cur.execute("UPDATE `Manager` SET `total_response` = `total_response` + 1" +
                             " WHERE `role` = '" + str(role) + "'")
        mysql.get_db().commit()
        cur.close()

        if result > 0:
            return True
        else:
            log.debug("No role is there: " + str(role))
            return False

    except Exception as e:
        log.error("Failed Sql operation in total_response. Error message: %s", e)
        return None


def login_check(mysql, username, password):
    log.debug("inside login_check function.")
    try:
        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT `role` FROM `Manager` WHERE `username` = '" + str(username) +
                             "' and `password` = '" + str(password) + "'")

        if result > 0:
            role = cur.fetchone()[0]
            log.debug("User verified with role: " + str(role))
            cur.close()

            return str(role)
        else:
            log.debug("No user is there with username: " + str(username))
            return False

    except Exception as e:
        log.error("Failed Sql operation in login_check. Error message: %s", e)
        return None


def forgot_password(mysql, username):
    log.debug("inside forgot_password function.")
    try:
        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT `email` FROM `Manager` WHERE `username` = '" + str(username) + "'")
        if result > 0:
            log.debug("Sending mail to the user to reset password.")

            email = cur.fetchone()[0]

            while True:
                random_id = randint(1000, 999999)
                result = cur.execute("SELECT `username` FROM `Manager` WHERE `random_id` = " + str(random_id))
                if result > 0:
                    rows = cur.fetchall()
                    for row in rows:
                        if row != random_id:
                            break
                        else:
                            continue
                else:
                    break

            cur.execute("UPDATE `Manager` SET `random_id` = " + str(random_id) +
                        ", `create_time` = '" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                        "' WHERE `username` = '" + str(username) + "'")
            mysql.get_db().commit()
            cur.close()

            message_link = str(config.browser_config['url']) + "reset_password?id=" + str(random_id)
            message = str(config.email['h_above']) + message_link + str(config.email['h_below'])

            status = send_mail(email, "Reset Your Password", message)
            if status is not None:
                return True
            else:
                return None

        else:
            log.debug("No user is there with username: " + str(username))
            return False

    except Exception as e:
        log.error("Failed Sql operation in forgot_password. Error message: %s", e)
        return None


def get_username(mysql, id_):
    log.debug("inside get_username function.")
    try:
        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT `username` FROM `Manager` WHERE `random_id` = " + str(id_))

        if result > 0:
            username = cur.fetchone()[0]
            log.debug("User verified with role: " + str(username))
            cur.close()
            return str(username)

        else:
            log.debug("No user is there with username with id: " + str(id_))
            return False

    except Exception as e:
        log.error("Failed Sql operation in get_username. Error message: %s", e)
        return None


def reset_password_db(mysql, username, password):
    log.debug("inside reset_password function.")
    try:
        cur = mysql.get_db().cursor()
        result = cur.execute("UPDATE `Manager` SET `password` = '" + str(password) + "', `random_id` = " + str("NULL") +
                             ", `create_time` = " + str("NULL") + " WHERE `username` = '" + str(username) + "'")
        mysql.get_db().commit()
        cur.close()

        if result > 0:
            log.debug("Password is updated for username: " + str(username))
            return True
        else:
            log.debug("No user is there with username: " + str(username))
            return False

    except Exception as e:
        log.error("Failed Sql operation in reset_password. Error message: %s", e)
        return None


def dashboard_get_tag_data(mysql, department, response, tag_name):
    log.debug("inside dashboard_get_tag_data function.")

    try:
        str_rv = ""
        tags = None
        response_edit = response
        response_edited_modal = response
        response_edit_modal = response
        i = 0

        if (str(response).find("#")) > (-1):
            temp_store = str(response).split('#')
            tags = temp_store[1::2]

            for tag in tags:
                i += 1
                if tag != "" and str(department) != "":
                    cur = mysql.get_db().cursor()
                    result = cur.execute("SELECT status FROM " + department +
                                         " WHERE tag = '" + tag + "'")

                    if result > 0:
                        rv = cur.fetchall()
                        for row in rv:
                            str_rv = ''.join(map(str, row))

                    cur.close()
                    temp_replace = "#" + tag + "#"

                    response_edit = str(response_edit).replace(temp_replace, str(config.dashboard['tag_start']) +
                                                               str(department) + "-" + str(tag) +
                                                               str(config.dashboard['tag_mid']) + str_rv +
                                                               str(config.dashboard['tag_end']))

                    response_edited_modal = str(response_edited_modal).\
                        replace(temp_replace, str(config.dashboard['tag_edited_modal_start']) +
                                str(department) + "-" + str(tag) + str(config.dashboard['tag_edited_modal_mid']) +
                                str_rv + str(config.dashboard['tag_edited_modal_end']))

                    response_edit_modal = str(response_edit_modal).replace(temp_replace,
                                                                           str(config.dashboard['tag_edit_modal_start'])
                                                                           + str(department) + "-" + str(tag) +
                                                                           str(config.dashboard['tag_edit_modal_mid'])
                                                                           + str_rv +
                                                                           str(config.dashboard['tag_edit_modal_end']))

                    response = str(response).replace(temp_replace, str_rv)

        res = {'main_tag': tag_name, 'tags': tags, 'response_edit': response_edit,
               'response_edited_modal': response_edited_modal, 'response_edit_modal': response_edit_modal}

        return res

    except Exception as e:
        log.error("Error in dashboard_get_tag_data. Error message: %s", e)
        return None


def get_total_responses(mysql, role):
    log.debug("inside get_total_responses function.")
    try:
        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT `total_response` FROM `Manager` WHERE `role` = '" + str(role) + "'")

        if result > 0:
            total_response = cur.fetchone()[0]
            log.debug("User verified with role: " + str(role))
            cur.close()
            return str(total_response)

        else:
            log.debug("No user is there with role: " + str(role))
            return False

    except Exception as e:
        log.error("Failed Sql operation in get_total_responses. Error message: %s", e)
        return None


def get_table_name(mysql):
    log.debug("inside get_table_name function.")

    try:
        res = []
        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'BitBot'")

        if result > 0:
            rows = cur.fetchall()
            log.debug("Table name fetched from database: BitBot")
            cur.close()

            for row in rows:
                res.append(row[0])

            return res

        else:
            log.debug("No database named BitBot found.")
            return False

    except Exception as e:
        log.error("Failed Sql operation in get_table_name. Error message: %s", e)
        return None


def get_update_data(mysql, department, data_list):
    log.debug("Inside get_update_data function.")

    try:
        data_list = eval(data_list)
        cur = mysql.get_db().cursor()
        for tag, value in data_list.items():
            result = cur.execute("UPDATE `" + department + "` SET `status` = '" + str(value) +
                                 "' WHERE `tag` = '" + str(tag) + "'")

            if result <= 0:
                log.debug("No data updated for department: " + str(department))

        mysql.get_db().commit()
        cur.close()

        log.debug("Data is updated for department: " + str(department))
        return True

    except Exception as e:
        log.error("Error in get_update_data. Error message: %s", e)
        return None


def get_update_email(mysql, department, email):
    log.debug("Inside get_update_email function.")

    try:
        cur = mysql.get_db().cursor()
        result = cur.execute("UPDATE `Manager` SET `email` = '" + str(email) +
                             "' WHERE `role` = '" + str(department) + "'")

        mysql.get_db().commit()
        cur.close()

        if result > 0:
            log.debug("Email updated for department: " + str(department))
            return True
        else:
            log.debug("Not available department: " + str(department))
            return None

    except Exception as e:
        log.error("Error in get_update_email. Error message: %s", e)
        return None


def get_update_password(mysql, role, old_password, new_password):
    log.debug("Inside get_update_email function.")

    try:
        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT `username` FROM `Manager` WHERE `password` = '" + str(old_password) + "'")

        if result > 0:
            cur = mysql.get_db().cursor()
            result = cur.execute("UPDATE `Manager` SET `password` = '" + str(new_password) +
                                 "' WHERE `role` = '" + str(role) + "'")

            mysql.get_db().commit()
            cur.close()

            if result > 0:
                log.debug("Password updated for department: " + str(role))
                return {'message': 'Password Successfully updated.', 'color': 'light-green'}
            else:
                log.debug("Not available department: " + str(role))
                return {'message': 'Failed. Same password is already exist.', 'color': 'red'}

        else:
            log.debug("No user is there having incoming password with role: " + str(role))
            return {'message': 'Failed. Incorrect old password.', 'color': 'red'}

    except Exception as e:
        log.error("Error in get_update_email. Error message: %s", e)
        return None
