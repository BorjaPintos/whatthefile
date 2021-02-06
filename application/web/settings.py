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
    SERVERNAME = 'whatthefile-server'


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    PROTOCOL = "http"
    HOST = '0.0.0.0'
    ENDPOINT_SERVER = "URLACCESSERVER"
    PORT = 8443

class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    PORT = 8080
    HOST = 'localhost'
    ENDPOINT_SERVER = "localhost"