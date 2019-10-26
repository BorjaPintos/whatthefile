from app import create_app
from settings import ProdConfig

app = create_app(ProdConfig)