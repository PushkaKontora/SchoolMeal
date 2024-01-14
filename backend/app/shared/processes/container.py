from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton


class SchedulerContainer(DeclarativeContainer):
    scheduler = Singleton(AsyncIOScheduler)
