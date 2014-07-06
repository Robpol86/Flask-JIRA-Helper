"""JIRA support for Flask without breaking PyCharm inspections.

https://github.com/Robpol86/Flask-JIRA-Helper
https://pypi.python.org/pypi/Flask-JIRA-Helper
"""
from jira import client


__author__ = '@Robpol86'
__license__ = 'MIT'
__version__ = '0.1.2'


def read_config(app, prefix):
    """Generate a dictionary compatible with jira.client.JIRA.__init__() keyword arguments from data in the Flask
    application's configuration values relevant to JIRA. If both basic and OAuth settings are specified, OAuth
    authentication takes precedence.

    Usage:
    config = read_config(app, prefix)
    jira = JIRA(**config)

    Positional arguments:
    app -- Flask application instance.
    prefix -- Prefix used in config key names in the Flask app's configuration.

    Returns:
    Dictionary with parsed data, compatible with jira.client.JIRA.__init__() keyword arguments.
    """
    # Get all relevant config values from Flask application.
    suffixes = ('SERVER', 'USER', 'PASSWORD', 'TOKEN', 'SECRET', 'CONSUMER', 'CERT')
    config_server, config_user, config_password, config_token, config_secret, config_consumer, config_cert = [
        app.config.get('{}_{}'.format(prefix, suffix)) for suffix in suffixes
    ]
    result = dict(options=dict(server=config_server))
    # Gather authentication data.
    basic = (config_user, config_password)
    oauth = dict(
        access_token=config_token,
        access_token_secret=config_secret,
        consumer_key=config_consumer,
        key_cert=config_cert,
    )
    # Apply authentication data.
    if any(oauth.values()):
        result['oauth'] = oauth
    elif all(basic):
        result['basic_auth'] = basic
    else:
        raise ValueError('No/incomplete JIRA authentication settings specified in the Flask config.')
    # Done.
    return result


class _JIRAState(object):
    """Remembers the configuration for the (jira, app) tuple. Modeled from SQLAlchemy."""

    def __init__(self, jira, app):
        self.jira = jira
        self.app = app


class JIRA(client.JIRA):
    """JIRA extension for Flask applications.

    Relevant configuration settings from the Flask app config:
    JIRA_SERVER -- URL to JIRA server.
    JIRA_USER -- HTTP Basic authentication user name.
    JIRA_PASSWORD -- HTTP Basic authentication password.
    JIRA_TOKEN -- OAuth authentication access token.
    JIRA_SECRET -- OAuth authentication access token secret.
    JIRA_CONSUMER -- OAuth authentication consumer key.
    JIRA_CERT -- OAuth authentication key certificate data.

    The above settings names are based on the default config prefix of 'JIRA'. If the config_prefix is 'JIRA_SYSTEM' for
    example, then JIRA_SERVER will be JIRA_SYSTEM_SERVER, and so on.
    """
    def __init__(self, app=None, config_prefix=None):
        """If app argument provided then initialize JIRA using application config values.

        If no app argument provided you should do initialization later with init_app method.

        Keyword arguments:
        app -- Flask application instance.
        config_prefix -- Prefix used in config key names in the Flask app's configuration. More info in
            self.init_app()'s docstring.
        """
        self.original_kill_session = self.kill_session
        self.kill_session = lambda x: None  # JIRA calls this even when no session was created. Disabling for now.
        if app is not None:
            self.init_app(app, config_prefix)

    def init_app(self, app, config_prefix=None):
        """Actual method to read JIRA settings from app configuration and initialize the JIRA instance.

        Positional arguments:
        app -- Flask application instance.

        Keyword arguments:
        config_prefix -- Prefix used in config key names in the Flask app's configuration. Useful for applications which
            maintain two authenticated sessions with a JIRA server. Default is 'JIRA'. Will be converted to upper case.
            Examples:
                JIRA_SYSTEM_SERVER = 'http://jira.mycompany.com'
                JIRA_SYSTEM_USER = 'system_account'
                JIRA_SERVER = 'http://jira.mycompany.com'
                JIRA_TOKEN = '<token for oauthing users>'
        """
        # Restore self.kill_session().
        self.kill_session = self.original_kill_session

        # Normalize the prefix and add this instance to app.extensions.
        config_prefix = (config_prefix or 'JIRA').rstrip('_').upper()
        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        if config_prefix.lower() in app.extensions:
            raise ValueError('Already registered config prefix {0!r}.'.format(config_prefix))
        app.extensions[config_prefix.lower()] = _JIRAState(self, app)

        # Read config.
        args = read_config(app, config_prefix)

        # Initialize fully.
        super(JIRA, self).__init__(**args)
