from application.web.app import create_app
from application.web.settings import ProdConfig

app = create_app(ProdConfig)