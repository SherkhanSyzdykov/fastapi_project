import base64
from typing import Iterable
import models
import domain


def url_record_to_url_domain(
        record: models.Url
) -> domain.Url:
    return domain.Url.from_orm(record)


def url_records_to_urls_domain(
        records: Iterable[models.Url]
) -> domain.Urls:
    urls = domain.Urls()
    for record in records:
        urls.items.append(url_record_to_url_domain(record=record))
    return urls


def request_record_to_request_domain(
        record: models.Request
) -> domain.Request:
    body: str = record.body
    decoded_body = base64.b64decode(body).decode('utf-8')
    keys_and_values = decoded_body.split(' ')

    dict_body = {}
    for key_and_value in keys_and_values:
        divide_symbol_index = key_and_value.index('+')
        key = key_and_value[:divide_symbol_index]
        value = key_and_value[divide_symbol_index+1:]
        dict_body[key] = value

    return domain.Request(id=record.id, body=dict_body, key=body)


def request_records_to_requests_domain(
        records: Iterable[models.Request]
) -> domain.Requests:
    requests = domain.Requests()
    for record in records:
        requests.items.append(request_record_to_request_domain(record=record))
    return requests
