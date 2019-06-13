from os import environ
from os import path
from forge_symposia.server import env

MONGO_URI = environ.get(
        'MONGO_URI') or 'mongodb://127.0.0.1:27017/forge-python-starter'
# Let's just use the local mongod instance. Edit as needed.

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

active_token = {
    'item_title': 'token',
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'token'
    },
    'schema': {
        'token': {
            'type': 'string',
            'unique': True,
        },
        'status': {
            'type': 'string'
        },
        'sessionToken': {
            'type': 'string'
        }
    }
}

user = {
    'item_title': 'user',
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'additional_lookup': {
        'url': 'regex("did:[\w]+:[\w]+")',
        'field': 'did'
    },
    'schema': {
        'did': {
            'type': 'string',
            'unique': True,
        },
        'name': {
            'type': 'string',
            'unique': True,
        },
        'email': {
            'type': 'string'
        },
        'mobile':{
            'type':'string'
        },
    }
}

DOMAIN = {'user': user, 'token': active_token}

JWT_SECRET_KEY='python-starter-secret-key'
SQLALCHEMY_DATABASE_URI='sqlite:///' + env.INDEX_DB
