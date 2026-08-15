from sqlalchemy import select

from src.database.db import SessionLocal
from src.database.models import UserSettings


def get_settings(user_id: int):
    session = SessionLocal()

    statement = select(UserSettings).where(
        UserSettings.user_id == user_id
    )

    result = session.execute(statement)

    settings = result.scalar_one_or_none()

    if settings is None:
        settings = UserSettings(user_id=user_id)
        session.add(settings)
        session.commit()
        session.refresh(settings)

    session.close()

    return settings


def set_notifications(user_id: int, enabled: bool):
    session = SessionLocal()

    statement = select(UserSettings).where(
        UserSettings.user_id == user_id
    )

    result = session.execute(statement)

    settings = result.scalar_one_or_none()

    if settings is None:
        settings = UserSettings(
            user_id=user_id,
            notifications_enabled=enabled,
        )
        session.add(settings)
    else:
        settings.notifications_enabled = enabled

    session.commit()
    session.close()
