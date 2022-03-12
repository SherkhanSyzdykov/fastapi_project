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
async def get_body(key: str, duplicates: bool):
    pass


@app.delete('/api/remove/{key}')
async def delete_body(key: str):
    pass


@app.put('/api/update')
async def update_body():
    pass


@app.get('/api/statistic')
async def get_statistic():
    pass
