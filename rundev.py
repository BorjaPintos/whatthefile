from app import create_app
from settings import DevConfig

app = create_app(DevConfig)