import asyncio
from types import TracebackType

import aio_pika
from aio_pika.abc import AbstractExchange
from aiormq import DeliveryError
from pamqp.commands import Basic
from pydantic import BaseSettings, Field

from app.shared.event_bus.connectors.abc import FailedSending, IBusConnector, IEventSender, ISenderConnection
from app.shared.event_bus.connectors.message import Message
from app.shared.event_bus.outbox import Outbox


class RabbitMQSettings(BaseSettings):
    host: str = Field(env="RABBIT_HOST")
    port: int = Field(env="RABBIT_PORT")
    login: str = Field(env="RABBIT_LOGIN")
    password: str = Field(env="RABBIT_PASSWORD")
    exchange: str = Field(env="RABBIT_EXCHANGE")


class RabbitMQConnector(IBusConnector):
    def __init__(self, settings: RabbitMQSettings) -> None:
        self._settings = settings

    def sender(self) -> ISenderConnection:
        return _RabbitMQSenderConnection(settings=self._settings)


class RabbitMQSender(IEventSender):
    def __init__(self, exchange: AbstractExchange) -> None:
        self._exchange = exchange

    async def send(self, outbox: Outbox) -> None:
        message = Message(
            id=outbox.id,
            data=outbox.data,
            created_at=outbox.created_at,
        )

        try:
            confirmation = await self._exchange.publish(
                message=aio_pika.Message(body=message.to_bytes(), content_type="application/json"),
                routing_key=outbox.event,
                timeout=5,
            )
        except DeliveryError as error:
            raise FailedSending(message=f"Сообщение не дошло до брокера по причине: {error}") from error

        except asyncio.TimeoutError as error:
            raise FailedSending(message="Превышен таймаут отправки") from error

        else:
            if not isinstance(confirmation, Basic.Ack):
                raise FailedSending(message="Сообщение не было принято брокером")


class _RabbitMQSenderConnection(ISenderConnection):
    def __init__(self, settings: RabbitMQSettings) -> None:
        self._settings = settings

    async def __aenter__(self) -> IEventSender:
        self._connection = await aio_pika.connect_robust(
            host=self._settings.host,
            port=self._settings.port,
            login=self._settings.login,
            password=self._settings.password,
        )
        channel = await self._connection.channel(publisher_confirms=True)
        exchange = await channel.get_exchange(name=self._settings.exchange, ensure=False)

        return RabbitMQSender(exchange=exchange)

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        await self._connection.close()
