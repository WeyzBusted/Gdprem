from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from utils.database import get_session
from utils.schemas import Sessions


async def add_session(
        user_id: int,
        phone: str,
        password: str
):
    user = Sessions(
        user_id=user_id,
        phone=phone,
        password=password
    )
    async with get_session() as session:
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def select_user(user_id: int):
    async with get_session() as session:
        user = await session.execute(select(Sessions).where(Sessions.user_id == user_id))
        return user.scalar()


async def select_session(session_id: int):
    async with get_session() as session:
        user = await session.execute(select(Sessions).where(Sessions.id == session_id))
        return user.scalar()


async def select_sessions():
    async with get_session() as session:
        user = await session.execute(select(Sessions))
        return user.scalars().all()


async def delete_session(session_id: int):
    async with get_session() as session:
        await session.execute(
            delete(Sessions).where(Sessions.id == session_id)
        )
        await session.commit()
