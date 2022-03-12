from asyncio import current_task
from typing import Callable
from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import async_scoped_session
from api import app
from database import async_session_factory


@app.middleware('http')
async def sqlalchemy_session_handler(request: Request, call_next: Callable):
    scoped_session = async_scoped_session(async_session_factory, scopefunc=current_task)
    session = scoped_session()
    request.sqlalchemy_session = session
    try:
        response = await call_next(request)
        await session.commit()
        await session.close()
        return response
    except BaseException as e:
        await session.rollback()
        await session.close()
        print()
        print(request.url)
        print(e)
        print()
