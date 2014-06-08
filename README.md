Flask-JIRA-Helper
=================

A simple JIRA extension for Flask. Supports basic authentication and OAuth.

Supported Platforms
-------------------

* OSX and Linux.
* Python 2.7
* [Flask](http://flask.pocoo.org/) 0.10.1
* [JIRA](http://jira-python.readthedocs.org/en/latest/) 0.21

Probably works on other versions too.

Quickstart
----------

Install:
```bash
pip install Flask-JIRA-Helper
```

Example:
```python
# example.py
from flask import Flask
from flask.ext.jira import JIRA

app = Flask(__name__)
app.config['JIRA_SERVER'] = 'https://jira.mycompany.com'
app.config['JIRA_USER'] = 'jdoe'
app.config['JIRA_PASSWORD'] = 'SuperSecretP@ssw0rd'
jira = JIRA(app)

print jira.projects()
```

Factory Example
---------------

```python
# extensions.py
from flask.ext.jira import JIRA

jira = JIRA()
```

```python
# application.py
from flask import Flask
from extensions import jira

def create_app():
    app = Flask(__name__)
    app.config['JIRA_SERVER'] = 'https://jira.mycompany.com'
    app.config['JIRA_USER'] = 'service'
    app.config['JIRA_PASSWORD'] = 'SuperSecretP@ssw0rd'
    jira.init_app(app)
    return app
```

```python
# manage.py
from application import create_app

app = create_app()
app.run()
```

Configuration
-------------

`Flask-JIRA-Helper` subclasses `jira.client.JIRA` and adds the init_app() method for delayed initialization (for
applications that instantiate extensions in a separate file, but run init_app() in the same file Flask() was
instantiated).

The following config settings are searched for in the Flask application's configuration dictionary:
* `JIRA_SERVER` -- URL to JIRA server.
* `JIRA_USER` -- HTTP Basic authentication user name.
* `JIRA_PASSWORD` -- HTTP Basic authentication password.
* `JIRA_TOKEN` -- OAuth authentication access token.
* `JIRA_SECRET` -- OAuth authentication access token secret.
* `JIRA_CONSUMER` -- OAuth authentication consumer key.
* `JIRA_CERT` -- OAuth authentication key certificate data.
