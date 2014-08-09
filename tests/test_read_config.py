from flask.ext.jira import read_config
import pytest


def test_basic_auth():
    config = dict(JIRA_SERVER='127.0.0.1', JIRA_USER='userA', JIRA_PASSWORD='passWord')
    expected = dict(options=dict(server='127.0.0.1'), basic_auth=('userA', 'passWord'))
    actual = read_config(config, 'JIRA')
    assert expected == actual


def test_oauth():
    config = dict(JIRA_SERVER='127.0.0.1', JIRA_TOKEN='token', JIRA_SECRET='secret', JIRA_CONSUMER='consumer',
                  JIRA_CERT='cert')
    expected = dict(options=dict(server='127.0.0.1'), oauth=dict(access_token='token', access_token_secret='secret',
                                                                 consumer_key='consumer', key_cert='cert'))
    actual = read_config(config, 'JIRA')
    assert expected == actual


def test_oauth_priority():
    config = dict(JIRA_SERVER='127.0.0.1', JIRA_TOKEN='token', JIRA_SECRET='secret', JIRA_CONSUMER='consumer',
                  JIRA_CERT='cert', JIRA_USER='userA', JIRA_PASSWORD='passWord')
    expected = dict(options=dict(server='127.0.0.1'), oauth=dict(access_token='token', access_token_secret='secret',
                                                                 consumer_key='consumer', key_cert='cert'))
    actual = read_config(config, 'JIRA')
    assert expected == actual


def test_oauth_partial():
    config = dict(JIRA_SERVER='127.0.0.1', JIRA_TOKEN='token')
    expected = dict(options=dict(server='127.0.0.1'), oauth=dict(access_token='token', access_token_secret=None,
                                                                 consumer_key=None, key_cert=None))
    actual = read_config(config, 'JIRA')
    assert expected == actual


def test_prefix():
    config = dict(JIRA_SERVER='127.0.0.1', JIRA_USER='userA', JIRA_PASSWORD='passWord', JIRA2_SERVER='127.0.0.2',
                  JIRA2_USER='userB', JIRA2_PASSWORD='passWord')

    expected = dict(options=dict(server='127.0.0.1'), basic_auth=('userA', 'passWord'))
    actual = read_config(config, 'JIRA')
    assert expected == actual

    expected = dict(options=dict(server='127.0.0.2'), basic_auth=('userB', 'passWord'))
    actual = read_config(config, 'JIRA2')
    assert expected == actual


def test_incomplete():
    config = dict(JIRA_SERVER='127.0.0.1', JIRA_USER='userA')
    with pytest.raises(ValueError):
        read_config(config, 'JIRA')
