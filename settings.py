"""Created on 12-09-2019."""
import os

VERSION = '1.0'


class Config(object):
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    PORT = 8080
    PROTOCOL = "http"
    HOST = 'localhost'
    DB_ENGINE = 'sqlite'
    DB_URL = '/data/database.sqlite3'


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    PROTOCOL = "https"
    HOST = '0.0.0.0'
    ENDPOINT_SERVER = "URLACCESSERVER"
    PORT = 8443
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    """Las de root no se usan"""
    DB_ROOT_USER = ''
    DB_ROOT_PASSWORD = ''


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    PORT = 8080
    HOST = 'localhost'
    ENDPOINT_SERVER = "localhost"
    DB_USER = 'devuser'
    DB_PASSWORD = 'devuserpassword'
    DB_ROOT_USER = ''
    DB_ROOT_PASSWORD = ''


class CIConfig(Config):
    """Continuous integration configuration."""

    ENV = 'test'
    TESTING = True
    DEBUG = True
    HOST = '0.0.0.0'
    ENDPOINT_SERVER = "localhost"
    PORT = 9090
    DB_USER = 'devuser'
    DB_PASSWORD = 'devuserpassword'
    DB_ROOT_USER = ''
    DB_ROOT_PASSWORD = ''
