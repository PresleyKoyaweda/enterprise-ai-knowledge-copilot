import asyncio

from app.db.session import engine
from app.db.models import Base


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    print("Tables créées avec succès.")


if __name__ == "__main__":
    asyncio.run(init_db())