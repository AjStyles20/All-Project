"""ASGI entry point for the P001 platform (MySQL product layer + web UI).

Run from the project folder, with the P001_DB_* variables set (see database/mysql/README.md):

    uvicorn app.main:app --host 127.0.0.1 --port 8001

then open http://127.0.0.1:8001/ in a browser.
"""
from app.api.mysql_platform_api import create_mysql_platform_app

app = create_mysql_platform_app()
