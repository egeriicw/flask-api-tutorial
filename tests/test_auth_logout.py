""" Unit tests for api.auth_logout API endpoint"""

from http import HTTPStatus

from src.flask_api_tutorial.models.token_blacklist import BlacklistedTokens

from tests.util import WWW_AUTH_NO_TOKEN, register_user, login_user, logout_user

SUCCESS = "successfully logged out."
TOKEN_BLACKLISTED = "Token blacklisted. Please log in again."
WWW_AUTH_BLACKLISTED_TOKEN = ' '.join((f'{WWW_AUTH_NO_TOKEN},',
                                       'error="invalid token",',
                                       f'error_description="{TOKEN_BLACKLISTED}"'))


def test_logout(client):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    blacklist = BlacklistedTokens.query.all()
    assert len(blacklist) == 0
    response = logout_user(client, access_token)
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    blacklist = BlacklistedTokens.query.all()
    assert len(blacklist) == 1
    assert access_token == blacklist[0].token


def test_logout_token_blacklisted(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = logout_user(client, access_token)
    assert response.status_code == HTTPStatus.OK
    response = logout_user(client, access_token)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json and response.json["message"] == TOKEN_BLACKLISTED
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == WWW_AUTH_BLACKLISTED_TOKEN
