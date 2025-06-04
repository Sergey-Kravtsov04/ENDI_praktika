from sqlalchemy.ext.asyncio  import create_async_engine, async_sessionmaker

from setting import settings

engine = create_async_engine(settings.DATABASE_URL, pool_size=100,max_overflow=0, pool_pre_ping=True)

AsyncSession = async_sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def get_session():
    session = AsyncSession()
    try:
        yield session
    finally:
        await session.close()