import asyncio
import base64
from typing import Any, Dict
from sqlalchemy.ext.asyncio import async_scoped_session
from provider import UrlProvider, RequestProvider
import domain
import exceptions


class BaseService:
    def __init__(self, session: async_scoped_session):
        pass


class UrlService(BaseService):
    _provider: UrlProvider

    def __init__(self, session: async_scoped_session):
        super().__init__(session=session)
        self._provider = UrlProvider(session=session)

    async def create(
        self,
        url: str
    ) -> domain.Url:
        return await self._provider.insert(url=url)

    async def get(
        self,
        id: int = ...,
        url: str = ...
    ) -> domain.Url:
        return await self._provider.select_one(
            id=id,
            url=url
        )

    async def get_or_create(
        self,
        url: str
    ) -> domain.Url:
        try:
            return await self.get(url=url)
        except exceptions.UrlDoesNotExist:
            return await self.create(url=url)


class RequestService(BaseService):
    _provider: RequestProvider
    _url_service: UrlService

    def __init__(self, session: async_scoped_session):
        super().__init__(session=session)
        self._provider = RequestProvider(session=session)
        self._url_service = UrlService(session=session)

    def _encode_body(
        self,
        body: Dict[str, Any]
    ) -> str:
        keys_and_values = ''
        for key, value in body.items():
            keys_and_values += f'{key}+{value}'
            keys_and_values += ' '
        keys_and_values = keys_and_values.rstrip()

        encoded_keys_and_values: str = base64.b64encode(
            keys_and_values.encode('utf-8')
        ).decode('utf-8')

        return encoded_keys_and_values

    async def create(
        self,
        url: str,
        body: Dict[str, Any]
    ) -> domain.Request:
        domain_url: domain.Url = await self._url_service.get_or_create(url=url)

        encoded_body = self._encode_body(body=body)

        return await self._provider.insert(
            body=encoded_body,
            url_id=domain_url.id
        )

    async def get(
        self,
        key: str
    ) -> domain.Request:
        return await self._provider.select_one(body=key)

    async def list(
        self,
        key: str
    ) -> domain.Requests:
        return await self._provider.select_multi(body=key)

    async def remove(
        self,
        key: str
    ):
        """
        Дубликаты тоже надо удалять???
        :param key:
        :return:
        """
        request: domain.Request = await self.get(key=key)
        await self._provider.delete(id=request.id)

    async def edit(
        self,
        key: str,
        body: Dict[str, Any]
    ) -> domain.Request:
        """
        Что делать с дупликатами?
        :param key:
        :param body:
        :return:
        """
        request: domain.Request = await self.get(key=key)
        encoded_body = self._encode_body(body=body)

        return await self._provider.update(id=request.id, body=encoded_body)

    async def get_statistic(self) -> int:
        all_count, duplicates_count = await asyncio.gather(
            self._provider.select_count(),
            self._provider.select_duplicates_count()
        )

        return (duplicates_count * 100) / all_count
