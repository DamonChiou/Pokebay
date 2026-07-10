# SQLAlchemy has:
# -create_async_engine: builds the object that manages DB connection
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


# import the DATABASE_URL from Settings instead of hardcoding
from pokebay.config import settings

# building the async engine, reads our database url and builds the engine
engine: AsyncEngine = create_async_engine(
    settings.database_url,

    # echo = True will print all SQL statements to teminal
    echo=True,

    # Instead of opening and closing new pool connections each time, 
    # Requests borrow a connection from the pool

    pool_size=5,
    max_overflow=10,
)


# Sessions track ORM objects that have been changed, engine manages connections
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    # prevents commits from expiring previous python objects
    expire_on_commit=False
)

# Dependency injection 
# FastAPI uses dependencies, which are async generator functions
# that yield a resource, lets the route handler use it, then cleans it up


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # async with is shorthand for a try/finally block, which means
    # the computer tries to give a session to route
    # after session is yielded, computer closes the session

    async with AsyncSessionLocal() as session:
        
        yield session
