import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.users import User


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, async_session: AsyncSession) -> None:
    async_session.add(
        User(
            username="test",
            first_name="test",
            last_name="test",
            bio="test",
        )
    )
    response = await client.get(f"{settings.app.API_V1_STR}/users")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["username"] == "test"
