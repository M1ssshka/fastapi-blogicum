import pytest
from httpx import AsyncClient

from application.core.exceptions.domain_exceptions import ForbiddenActionException


async def assert_get_all_empty(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
):
    override_use_case(dep_func, lambda *a, **kw: [])
    response = await async_client.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def assert_get_all_with_data(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
    make_func,
):
    override_use_case(dep_func, lambda *a, **kw: [make_func()])
    response = await async_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1


async def assert_get_by_id_success(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
    make_func,
):
    override_use_case(dep_func, lambda *a, **kw: make_func())
    response = await async_client.get(url)
    assert response.status_code == 200


async def assert_get_by_id_not_found(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
    not_found_exception,
):
    async def mock(*a, **kw):
        raise not_found_exception(id=999)

    override_use_case(dep_func, mock)
    response = await async_client.get(url)
    assert response.status_code == 404


async def assert_create_success(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
    payload: dict,
    make_func,
):
    override_use_case(dep_func, lambda *a, **kw: make_func())
    response = await async_client.post(url, json=payload)
    assert response.status_code == 201


async def assert_create_unauthorized(
    async_client: AsyncClient, url: str, payload: dict
):
    response = await async_client.post(url, json=payload)
    assert response.status_code == 401


async def assert_update_success(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
    payload: dict,
    make_func,
):
    async def mock(*a, **kw):
        return make_func()

    override_use_case(dep_func, mock)
    response = await async_client.put(url, json=payload)
    assert response.status_code == 200


async def assert_update_not_found(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
    payload: dict,
    not_found_exception,
):
    async def mock(*a, **kw):
        raise not_found_exception(id=999)

    override_use_case(dep_func, mock)
    response = await async_client.put(url, json=payload)
    assert response.status_code == 404


async def assert_update_forbidden(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
    payload: dict,
):
    async def mock(*a, **kw):
        raise ForbiddenActionException()

    override_use_case(dep_func, mock)
    response = await async_client.put(url, json=payload)
    assert response.status_code == 403


async def assert_delete_success(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
):
    override_use_case(dep_func, lambda *a, **kw: None)
    response = await async_client.delete(url)
    assert response.status_code == 200


async def assert_delete_forbidden(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
):
    async def mock(*a, **kw):
        raise ForbiddenActionException()

    override_use_case(dep_func, mock)
    response = await async_client.delete(url)
    assert response.status_code == 403


async def assert_delete_not_found(
    async_client: AsyncClient,
    override_use_case,
    dep_func,
    url: str,
    not_found_exception,
):
    async def mock(*a, **kw):
        raise not_found_exception(id=999)

    override_use_case(dep_func, mock)
    response = await async_client.delete(url)
    assert response.status_code == 404
