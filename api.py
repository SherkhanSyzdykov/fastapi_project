from fastapi import Request
from service import UrlService, RequestService
import domain
from middleware import app


@app.post('/api/add')
async def create_body(request: Request) -> domain.Request:
    body = await request.json()
    service = RequestService(session=request.state.session)
    return await service.create(url='api/add', body=body)


@app.get('/api/get')
async def get_body(request: Request, key: str) -> domain.Request:
    service = RequestService(session=request.state.session)
    return await service.get(key=key)


@app.delete('/api/remove/{key}')
async def delete_body(request: Request, key: str) -> None:
    service = RequestService(session=request.state.session)
    await service.remove(key=key)


@app.put('/api/update/{key}')
async def update_body(request: Request, key: str) -> domain.Request:
    body = await request.json()
    service = RequestService(session=request.state.session)
    return await service.edit(key=key, body=body)


@app.get('/api/statistic')
async def get_statistic(request: Request) -> int:
    service = RequestService(session=request.state.session)
    return await service.get_statistic()

