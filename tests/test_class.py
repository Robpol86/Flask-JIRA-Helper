from flask import current_app
from requests import ConnectionError
import pytest

from flask.ext.jira import JIRA


def test_kill_session():
    jira = JIRA()
    assert jira.kill_session() == jira

    with pytest.raises(AttributeError):
        jira.original_kill_session()
    assert jira.kill_session != jira.original_kill_session

    with pytest.raises(AttributeError):
        jira.init_app(None)  # This will restore kill_session() and then crash later since app=None.

    with pytest.raises(AttributeError):
        jira.kill_session()
    assert jira.kill_session == jira.original_kill_session


def test_ignore_initial_connection_failure():
    current_app.config.update(dict(JIRA_SERVER='http://127.0.0.1', JIRA_USER='userA', JIRA_PASSWORD='passWord'))

    with pytest.raises(ConnectionError):
        JIRA(current_app)

    current_app.extensions.pop('jira')
    current_app.config['JIRA_IGNORE_INITIAL_CONNECTION_FAILURE'] = True
    jira = JIRA(current_app)
    assert current_app.extensions['jira'].jira == jira
