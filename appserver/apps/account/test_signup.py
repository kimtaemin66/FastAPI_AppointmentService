from sqlalchemy.ext.asyncio import AsyncSession
from appserver.apps.account.endpoints import signup
from appserver.apps.account.models import User


async def test_모든_입력_항목을_유효한_값으로_입력하면_계정이_생성된다(db_session: AsyncSession):
    payload={
        "username": "test",
        "email": "test@example.com",
        "display_name": "test",
        "password": "test테스트1234",
    }
    
    result = await signup(payload, db_session)
    
    assert isinstance(result, User)
    assert result.username == payload["username"]
    assert result.email == payload["email"]
    assert result.display_name == payload["display_name"]
    assert result.is_host is False