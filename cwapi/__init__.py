from asyncio import Lock as aioLock
from enum import Enum, auto
from queue import Queue
from threading import Lock as thrLock, Thread, Condition

import aio_pika
from pika import URLParameters, BlockingConnection
from aio_pika import connect_robust

from .requests import request


class Server(Enum):
    __slots__ = "__port", "__host", "__protocol"

    def __new__(cls, protocol, host, port):
        self = object.__new__(cls)
        self.__protocol = protocol
        self.__host = host
        self.__port = port
        return self

    @property
    def protocol(self):
        return self.__protocol

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    def build_address(self, instance_name, password):
        if type(instance_name) is not str:
            raise TypeError("instance name must be str")
        if type(password) is not str:
            raise TypeError("password must be str")

        return f"{self.__protocol}://{instance_name}:{password}@{self.__host}:{self.__port}/"

    Classic = (None, None, None)
    International = ("amqps", "api.chatwars.me", 5673)
    CW3 = ("amqps", "api.chtwrs.com", 5673)


class _sync_async_descriptor:
    __slots__ = "__sync", "__async"

    def __get__(self, instance, owner):
        if issubclass(owner, AsyncChatWarsApiClient):
            return self.__async.__get__(instance, owner)
        else:
            return self.__sync.__get__(instance, owner)

    def _sync(self, f):
        try:
            self.__sync
            raise TypeError("Override not allowed")
        except AttributeError:
            self.__sync = f
            return self

    def _async(self, f):
        try:
            self.__async
            raise TypeError("Override not allowed")
        except AttributeError:
            self.__async = f
            return self


class _consumer:
    __slots__ = "__connection_link", "__input_queue_name", "__connection", "__channel", "last", "__thread", "condvar", "__stoped", "__stop_mutex"

    def __new__(cls, connection_link, input_queue_name):
        self = super().__new__(cls)
        self.__connection_link = connection_link
        self.__input_queue_name = input_queue_name
        self.__connection = None
        self.__channel = None
        self.last = None
        self.condvar = Condition()
        self.__stoped = False
        self.__stop_mutex = thrLock()
        self.__thread = Thread(target=self, daemon=True)
        self.__thread.start()
        return self

    def __callback(self, channel, method_frame, header_frame, body):
        with self.condvar:
            self.last = body
            channel.ack()
            self.condvar.notify_all()

    def __call__(self):
        with self.__stop_mutex:
            self.__connection = BlockingConnection(URLParameters(self.__connection_link))
            self.__channel = self.__connection.channel()
            self.__channel.basic_consume(queue=self.__input_queue_name, on_message_callback=self.__callback, exclusive=True)
        if not self.__stoped:
            self.__channel.start_consuming()

    def __del__(self):
        if self.__channel is not None:
            self.stop()
            self.__channel.close()
            self.__channel = None
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def stop(self):
        self.__stoped = True
        with self.__stop_mutex:
            self.__channel.stop_consuming()


class ChatWarsApiClient:
    __slots__ = "__connection_link", "__instance_name", "__password", "__server", "__connection", "__channel", "__output_exchange_name", "__input_queue_name", "__routing_key", "__output_exchange", "__input_queue", "__mutex", "__consumer", "__aio_loop"

    @property
    def instance_name(self):
        return self.__instance_name

    @property
    def connection_link(self):
        return self.__connection_link

    @property
    def server(self):
        return self.__server

    @property
    def output_exchange_name(self):
        return self.__output_exchange_name

    @property
    def input_queue_name(self):
        return self.__input_queue_name

    @property
    def routing_key(self):
        return self.__routing_key

    loop = _sync_async_descriptor()

    @loop._async
    @property
    def loop(self):
        return self.__aio_loop

    def __new__(cls, server, instance_name, password, *, __loop=None):
        if type(server) is not Server:
            raise TypeError(f"server must instance of {Server.__qualname__ !r} enum")
        if type(instance_name) is not str:
            raise TypeError("instance name must be str")
        if type(password) is not str:
            raise TypeError("password must be str")

        self = super().__new__(cls)
        self.__server = server
        self.__instance_name = instance_name
        self.__password = password
        self.__aio_loop = __loop

        self.__connection_link = server.build_address(instance_name, password)
        self.__output_exchange_name = f"{instance_name}_ex"
        self.__input_queue_name = f"{instance_name}_i"
        self.__routing_key = f"{instance_name}_o"

        self.__connection = None
        self.__channel = None
        self.__output_exchange = None
        self.__input_queue = None
        self.__consumer = None

        if issubclass(cls, AsyncChatWarsApiClient):
            self.__mutex = aioLock()
        else:
            self.__mutex = thrLock()

        return self

    def is_connected(self):
        return self.__connection is not None

    connect = _sync_async_descriptor()

    @connect._sync
    def connect(self):
        self.__connection = BlockingConnection(URLParameters(self.__connection_link))
        self.__channel = self.__connection.channel()
        self.__output_exchange = self.__channel.exchange_declare(self.__output_exchange_name, passive=True)

        self.__consumer = _consumer(self.__connection_link, self.__input_queue_name)

    @connect._async
    async def connect(self):
        self.__connection = await aio_pika.connect_robust(self.__connection_link)
        self.__channel = self.__connection.channel()
        self.__output_exchange = await self.__channel.get_exchange(self.__output_exchange_name)
        self.__input_queue = await self.__channel.get_queue(self.__input_queue_name)

    disconnect = _sync_async_descriptor()

    @disconnect._sync
    def disconnect(self):
        if not self.is_connected():
            raise ConnectionError("client not connected")
        self.__consumer.stop()
        self.__consumer.__del__()
        self.__channel.close()
        self.__connection.close()

    @disconnect._async
    async def disconnect(self):
        if not self.is_connected():
            raise ConnectionError("client not connected")
        await self.__channel.close()
        await self.__connection.close()

    send = _sync_async_descriptor()

    @send._sync
    def send(self, req, /):
        if not isinstance(req, request):
            raise TypeError("unsupported type of request")

        if not self.is_connected():
            raise ConnectionError("client not connected")

        with self.__mutex, self.__consumer.condvar:
            self.__channel.basic_publish(exchange=self.__output_queue_name, routing_key=self.__routing_key, body=req.dump())
            self.__consumer.wait()
            return self.__consumer.last

    @send._async
    async def send(self, req, /):
        if not isinstance(req, request):
            raise TypeError("unsupported type of request")

        if not self.is_connected():
            raise ConnectionError("client not connected")

        self.__channel.basic_publish(exchange=self.__output_queue_name, routing_key=self.__routing_key, body=req.dump())

    __enter__ = _sync_async_descriptor()

    @__enter__._sync
    def __enter__(self):
        self.connect()
        return self

    __exit__ = _sync_async_descriptor()

    @__exit__._sync
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False


class AsyncChatWarsApiClient(ChatWarsApiClient):
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
