from forge_symposia.server import env
from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from forge_symposia.server.models import indexDB
import os
import pathlib

RESOURCE_METHODS = ['GET']

DOMAIN = DomainConfig({
    'events': ResourceConfig(indexDB.AssetState),
    'acquireTx': ResourceConfig(indexDB.AcquireAssetTx),
    'tx': ResourceConfig(indexDB.Tx)
}).render()


JWT_SECRET_KEY = 'python-starter-secret-key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + env.INDEX_DB


SQLALCHEMY_BINDS = {
    'app_db': "sqlite:///" + env.APP_DB
}