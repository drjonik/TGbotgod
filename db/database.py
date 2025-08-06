import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    text = Column(String)
    date_time = Column(DateTime)
    repeat = Column(String, nullable=True)
    done = Column(Integer, default=0)

engine = None
SessionLocal = None

async def init_db(db_url: str):
    global engine, SessionLocal
    engine = create_async_engine(db_url, echo=False)
    SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_task(user_id: int, task_in):
    async with SessionLocal() as session:
        task = Task(user_id=user_id, text=task_in.text, date_time=task_in.date_time, repeat=task_in.repeat)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

async def get_pending_tasks():
    async with SessionLocal() as session:
        result = await session.execute(
            Task.__table__.select().where(Task.done == 0)
        )
        return result.scalars().all()

async def get_task(task_id: int):
    async with SessionLocal() as session:
        return await session.get(Task, task_id)

async def remove_task(user_id: int, text: str):
    async with SessionLocal() as session:
        result = await session.execute(
            Task.__table__.delete().where(Task.user_id==user_id, Task.text.ilike(f"%{text}%"))
        )
        await session.commit()
        return result.rowcount > 0
