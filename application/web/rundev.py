from application.web.app import create_app
from application.web.settings import DevConfig

app = create_app(DevConfig)