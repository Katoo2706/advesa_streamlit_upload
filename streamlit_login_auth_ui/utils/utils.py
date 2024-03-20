import re
import json
from trycourier import Courier
import secrets
from passlib.hash import pbkdf2_sha256
import requests
from pymongo import MongoClient

import logging

logger = logging.getLogger(__name__)


def check_usr_pass(db_conn: MongoClient, username: str, password: str) -> bool:
    """
    Authenticates the username and password.
    """

    user_data = db_conn['users'].find_one(
        {"username": username}
    )

    if user_data and pbkdf2_sha256.verify(hash=user_data["password"], secret=password):
        return True
    return False


def load_lottieurl(url: str) -> None:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass


def check_advesa_email(email_sign_up: str) -> bool:
    """
    Check if that emails belong to Advesa
    :param email_sign_up: Advesa email
    :return: bool
    """

    return True if email_sign_up[-10:] == "advesa.com" else False


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = r'^[A-Za-z_][A-Za-z0-9_]*'

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(cli, email_sign_up: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    user_data = cli['users'].find_one({
        "email": email_sign_up
    })
    if user_data:
        return False
    return True


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_usr(cli, username_sign_up: str):
    """
    Checks if the username already exists (since username needs to be unique),
    also checks for non - empty username.
    """
    user_data = cli['users'].find_one({
        "username": username_sign_up
    })
    if user_data:
        return False
    return True


def register_new_usr(db_conn: MongoClient, name_sign_up: str, email_sign_up: str, username_sign_up: str,
                     password_sign_up: str) -> None:
    """
    Saves the information of the new user in the _secret_auth.json file.
    """
    new_usr_data = {'username': username_sign_up, 'name': name_sign_up, 'email': email_sign_up,
                    'password': pbkdf2_sha256.hash(password_sign_up)}

    db_conn['users'].insert_one(new_usr_data)

    logger.info(f"201: Created user {username_sign_up}")

    # with open("_secret_auth_.json", "r") as auth_json:
    #     authorized_user_data = json.load(auth_json)
    #
    # with open("_secret_auth_.json", "w") as auth_json_write:
    #     authorized_user_data.append(new_usr_data)
    #     json.dump(authorized_user_data, auth_json_write)


def check_username_exists(user_name: str) -> bool:
    """
    Checks if the username exists in the _secret_auth.json file.
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['username'])

    if user_name in authorized_user_data_master:
        return True
    return False


def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the _secret_auth.json file.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['email'] == email_forgot_passwd:
                return True, user['username']
    return False, None


def get_email(db_conn: MongoClient, username: str) -> [bool, str]:
    """
    Get email from username if email exists in _secret_auth_.json
    :param db_conn:
    :param username: username to login
    :return: email address as string
    """
    user_data = db_conn['users'].find_one({
        "username": username
    })
    if user_data:
        return True, user_data.get("email")
    return False, None


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(auth_token: str, username_forgot_passwd: str, email_forgot_passwd: str, company_name: str,
                         random_password: str) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(auth_token=auth_token)

    resp = client.send_message(
        message={
            "to": {
                "email": email_forgot_passwd
            },
            "content": {
                "title": company_name + ": Login Password!",
                "body": "Hi! " + username_forgot_passwd + "," + "\n" + "\n" + "Your temporary login password is: " + random_password + "\n" + "\n" + "{{info}}"
            },
            "data": {
                "info": "Please reset your password at the earliest for security reasons."
            }
        }
    )


def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

    with open("_secret_auth_.json", "w") as auth_json_:
        for user in authorized_users_data:
            if user['email'] == email_:
                user['password'] = pbkdf2_sha256.hash(random_password)
        json.dump(authorized_users_data, auth_json_)


def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """
    Authenticates the password entered against the username when 
    resetting the password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['email'] == email_reset_passwd:
                try:
                    if pbkdf2_sha256.verify(user['password'], current_passwd) == True:
                        return True
                except:
                    pass
    return False

# Author: quan.ngo@advesa.com
