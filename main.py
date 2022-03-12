import uvicorn
from api import app
import settings


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT
    )
