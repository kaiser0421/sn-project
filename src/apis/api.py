from http import HTTPStatus

from flask import request, jsonify, Blueprint
from datetime import datetime, timedelta

from tools.validation import signupValidation
from tools.tool import verifyUserPassword
from models.user import findUser, saveUser, getUserPassword, updateUser
from exceptions import exception
from constants import message, constant

user_api = Blueprint("user", __name__)

@user_api.errorhandler(exception.InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

@user_api.errorhandler(exception.ServerError)
def server_error(e):
    return jsonify(e.to_dict()), e.status_code

@user_api.errorhandler(exception.DatabaseError)
def database_error(e):
    return jsonify(e.to_dict()), e.status_code

@user_api.route("/signup/", methods=["POST"])
def signup():
    """Create Account
    Username must be between 3 and 32 characters in length.
    Passwords must be between 8 and 32 characters in length to include: one uppercase character, one lowercase character and one number.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
                example: Test01
              password:
                type: string
                example: Test01Password

    responses:
      200:
        description: success is a boolean field indicating the outcome of the account creation process
        schema:
            type: object
            properties:
              success:
                type: boolean
      400:
        description: success is a boolean field indicating the outcome of the account creation process, reason is a string field indicating the reason for a failed account creation process
        schema:
            type: object
            properties:
              success:
                type: boolean
                example: false
              reason:
                type: string
                example: "Passwords must be between 8 and 32 characters in length. Passwords must be to include: one uppercase character, one number, "
    """
    if not request or not request.json:
        raise exception.InvalidAPIUsage(message.INPUT_INVALID)

    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        raise exception.InvalidAPIUsage(message.INPUT_INVALID)

    # validate username, password
    valid, msg = signupValidation(username, password)
    if not valid:
        raise exception.InvalidAPIUsage(msg)

    # check if a user exists
    doesExists = findUser(username)
    if doesExists:
        raise exception.InvalidAPIUsage(message.USER_DOES_EXIST)

    # save new user to database
    else:
        saveUser(username, password, datetime.now())

    return jsonify({"success": True}), HTTPStatus.OK

@user_api.route("/signin/", methods=["POST"])
def signin():
    """Account sign in
    Username is a string representing the username of the account being accessed.
    Passwords is a string representing the password being used to access the account.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
                example: Test01
              password:
                type: string
                example: Test01Password

    responses:
      200:
        description: success is a boolean field indicating the outcome of the account creation process
        schema:
            type: object
            properties:
              success:
                type: boolean
      400:
        description: success is a boolean field indicating the outcome of the account creation process, reason is a string field indicating the reason for a failed account creation process
        schema:
            type: object
            properties:
              success:
                type: boolean
                example: false
              reason:
                type: string
                example: "The username and/or password you specified are not correct."
    """
    if not request or not request.json:
        raise exception.InvalidAPIUsage(message.INPUT_INVALID)

    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        raise exception.InvalidAPIUsage(message.INPUT_INVALID)

    # get user password
    ok, user = getUserPassword(username)
    if not ok:
        raise exception.InvalidAPIUsage(message.USER_DOES_NOT_EXIST)
    
    retryPeriod = user.updated_on + timedelta(minutes=constant.VERIFY_RETRY_PERIOD_MINTUES)
    isTimeLimitExceeded = datetime.now() < retryPeriod
    isRetryLimitExceeded = user.password_retry >= constant.VERIFY_RETRY_LIMIT
    # number of retries exceeded in retry period time(mintue)
    if  isRetryLimitExceeded and isTimeLimitExceeded:
        raise exception.InvalidAPIUsage(message.SIGNIN_TRY_LATER)
    
    # verify user password
    else:
        verify = verifyUserPassword(password, user.password)
        if not verify:
            # reset password_retry and updated_on
            if user.password_retry >= 1 and datetime.now() > retryPeriod:
                user.password_retry = 1  # reset retry to 1
                user.updated_on = datetime.now()
                updateUser(user.id, user.password_retry, user.updated_on)
            # counting retry
            else:
                user.password_retry += 1
                updateUser(user.id, user.password_retry, None) 
            raise exception.InvalidAPIUsage(message.PASSWORD_INCORRECT)

    return jsonify({"success": True}), HTTPStatus.OK
