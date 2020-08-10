import pytest


error_map = {
    "empty_login": "Login is not given.",
    "short_login": "Login is too short for now.",
    "not_email_or_phone": "Please enter correct email address or phone.",
    "incorrect_login_or_password": "Login or password is incorrect!",
    "empty_password": "Password is not given.",
    "short_password": "The entered password must be not less than 6 symbols."
}


def test_valid_login_and_password(app):
    if app.session.is_signed_in():
        app.session.logout()
    app.session.sign_in(app.session.login, app.session.password)
    if app.session.is_signed_in():
        if not app.session.is_signed_in_as(app.session.login):
            raise Exception("Error: Signed in as another user")
    else:
        raise Exception("User is not signed in")


def test_logout(app):
    if not app.session.is_signed_in():
        app.session.sign_in(app.session.login, app.session.password)
    app.session.logout()
    if app.session.is_signed_in():
        raise Exception("Error: Logout doesn't work")


invalid_login_data = [
    {"login": "", "err": error_map['empty_login']},
    {"login": "1", "err": error_map['short_login']},
    {"login": "123456", "err": error_map['not_email_or_phone']},
    {"login": "12@example.com", "err": error_map['incorrect_login_or_password']}, # не существующий в базе логин
    {"login": "+7(555)12345", "err": error_map['not_email_or_phone']} # не соответствует допустимому формату
]


@pytest.mark.parametrize("data", invalid_login_data)
def test_invalid_login_with_valid_password_feedback(app, data):
    if app.session.is_signed_in():
        app.session.logout()
    app.session.sign_in(data['login'], app.session.password)
    if app.session.is_signed_in():
        raise Exception("Error: Signed in with invalid login")
    login_feedback, _ = app.session.get_login_and_password_invalid_feedback()
    assert login_feedback == data['err']


invalid_password_data = [
    {"password": "", "err": error_map['empty_password']},
    {"password": "1", "err": error_map['short_password']},
    {"password": "654321", "err": error_map['incorrect_login_or_password']}
]


@pytest.mark.parametrize("data", invalid_password_data)
def test_invalid_password_with_valid_login_feedback(app, data):
    if app.session.is_signed_in():
        app.session.logout()
    app.session.sign_in(app.session.login, data['password'])
    if app.session.is_signed_in():
        raise Exception("Error: Signed in with invalid password")
    login_feedback, password_feedback = app.session.get_login_and_password_invalid_feedback()
    if password_feedback:
        assert password_feedback == data['err']
    elif login_feedback and data['err'] == error_map['incorrect_login_or_password']:
        assert login_feedback == data['err']
    else:
        raise Exception("Invalid feedback")


invalid_login_and_password_data = [
    {"login": "", "password": "", "login_err": error_map['empty_login'], "password_err": error_map['empty_password']},
    {"login": "1", "password": "1", "login_err": error_map['short_login'], "password_err": error_map['short_password']},
    {"login": "12@example.com", "password": "654321", "login_err": error_map['incorrect_login_or_password'], "password_err": ""},
    {"login": "11111111", "password": "1", "login_err": error_map['not_email_or_phone'], "password_err": error_map['short_password']}
]


@pytest.mark.parametrize("data", invalid_login_and_password_data)
def test_invalid_login_with_invalid_password_feedback(app, data):
    if app.session.is_signed_in():
        app.session.logout()
    app.session.sign_in(data['login'], data['password'])
    if app.session.is_signed_in():
        raise Exception("Error: Signed in with invalid login and password")
    login_feedback, password_feedback = app.session.get_login_and_password_invalid_feedback()
    assert login_feedback == data['login_err']
    assert password_feedback == data['password_err']
