from typing import Type
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import async_scoped_session
import adapters
import domain
import exceptions
import models


class BaseProvider:
    session: async_scoped_session

    def __init__(self, session: async_scoped_session):
        self.session = session


class UrlProvider(BaseProvider):
    _model: Type[models.Url] = models.Url

    async def insert(
        self,
        url: str
    ) -> domain.Url:
        insert_stmt = insert(self._model).values(url=url).returning(self._model)
        select_stmt = select(self._model).from_statement(insert_stmt)
        record = await self.session.scalar(select_stmt)
        return adapters.url_record_to_url_domain(record)

    async def select_one(
        self,
        id: int = ...,
        url: str = ...
    ) -> domain.Url:

        select_stmt = select(self._model)
        if id is not ...:
            select_stmt = select_stmt.where(self._model.id == id)
        if url is not ...:
            select_stmt = select_stmt.where(self._model.url == url)

        record = await self.session.scalar(select_stmt)
        if not record:
            raise exceptions.UrlDoesNotExist

        return adapters.url_record_to_url_domain(record=record)


class RequestProvider(BaseProvider):
    _model: Type[models.Request] = models.Request

    async def insert(
        self,
        body: str,
        url_id: int
    ) -> domain.Request:
        insert_stmt = insert(self._model).values(
            body=body,
            url_id=url_id
        ).returning(self._model)
        select_stmt = select(self._model).from_statement(insert_stmt)
        record = await self.session.scalar(select_stmt)
        return adapters.request_record_to_request_domain(record=record)

    async def select_one(
        self,
        id: int = ...,
        body: str = ...,
        url_id: int = ...
    ) -> domain.Request:
        select_stmt = select(self._model)
        if id is not ...:
            select_stmt = select_stmt.where(self._model.id == id)
        if body is not ...:
            select_stmt = select_stmt.where(self._model.body == body)
        if url_id is not ...:
            select_stmt = select_stmt.where(self._model.url_id == url_id)

        record = await self.session.scalar(select_stmt)
        if not record:
            raise exceptions.RequestDoesNotExist

        return adapters.request_record_to_request_domain(record=record)

    async def select_multi(
        self,
        body: str = ...,
        url_id: int = ...
    ) -> domain.Requests:
        select_stmt = select(self._model)
        if body is not ...:
            select_stmt = select_stmt.where(self._model.body == body)
        if url_id is not ...:
            select_stmt = select_stmt.where(self._model.url_id == url_id)

        records = await self.session.scalars(select_stmt)
        return adapters.request_records_to_requests_domain(records=records)
