from typing import Type
from sqlalchemy import insert, select, delete, update, func
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

    async def delete(
        self,
        id: int
    ):
        delete_stmt = delete(self._model).where(self._model.id == id)
        await self.session.execute(delete_stmt)

    async def update(
        self,
        id: int,
        body: str
    ) -> domain.Request:
        update_stmt = update(self._model).where(
            self._model.id == id
        ).values(body=body).returning(self._model)
        select_stmt = select(self._model).from_statement(update_stmt)

        record = await self.session.scalar(select_stmt)
        return adapters.request_record_to_request_domain(record=record)

    async def select_count(self) -> int:
        select_stmt = select(func.count(self._model.id))
        count = await self.session.scalar(select_stmt)
        if count is None:
            return 0
        return count

    async def select_duplicates_count(self) -> int:
        """
        SQL STATEMENT:
        SELECT sum(anon_1.group_counts) AS sum_1
        FROM (SELECT request.body AS body, count(request.body) AS group_counts
        FROM request GROUP BY request.body
        HAVING count(request.body) > :count_1) AS anon_1
        :return:
        """
        subquery_alias = select(
            self._model.body,
            func.count(self._model.body).label('group_counts')
        ).group_by(self._model.body).having(
            func.count(self._model.body) > 1
        ).subquery().alias()
        select_stmt = select(func.sum(subquery_alias.c.group_counts)).select_from(subquery_alias)

        duplicates_count = await self.session.scalar(select_stmt)
        if duplicates_count is None:
            return 0
        return duplicates_count
