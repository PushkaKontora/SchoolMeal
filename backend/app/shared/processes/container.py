from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider, Singleton


class SchedulerContainer(DeclarativeContainer):
    scheduler: Provider[BaseScheduler] = Singleton(AsyncIOScheduler)
