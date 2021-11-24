# Client for Chat Wars API for Python3

Currently, based on [`pika`](https://pypi.org/project/pika/) and [`aio-pika`](https://pypi.org/project/aio-pika/).

## Version `1!2021.11.24b0`

`{implementation version}!{date when it works}{sub releases}`

## Installing

Build on your machine:

`pip install git+https://github.com/LandgrafHomyak/cwapi-python@v1!2021.11.24b0`

or

`pip install https://github.com/LandgrafHomyak/cwapi-python/archive/refs/tags/v1!2021.11.24b0.tar.gz`

or go to [release page](https://github.com/LandgrafHomyak/cwapi-python/releases/tag/v1!2021.11.24b0) and download wheel package directly.

## Using

Synchronous client:

```python3
from cwapi import ChatWarsApiClient, Server
from cwapi.requests import *
from cwapi.types import Operation
from cwapi.responses import ForbiddenError

# Allowed servers:
Server.CW3
Server.International  # castles enum not initialized yet, will raise ValueError if response contains it's value

with ChatWarsApiClient(Server.CW3, "your instance name", PASSWORD) as c:
    print(
        c.ask(
            GetInfoRequest()
        ).balance
    )

    try:
        profile = c.ask(
            RequestProfileRequest(token="1234567890abcdef")
        )

        print(str(profile.castle) + profile.userName)
        print(
            (str(profile.castle) if profile.guild.emoji is None else profile.guild.emoji) + str(profile.guild)
        )
    except ForbiddenError:
        req = c.ask(
            AuthAdditionalOperationRequest(token="1234567890abcdef", operation=Operation.GetUserProfile)
        )
        c.ask(
            GrantAdditionalOperationRequest(token="1234567890abcdef", requestId=req.requestId, authCode=input("auth code: "))
        )
```

Asyncio client:

```python3
from cwapi import AsyncChatWarsApiClient, Server

...


async def main():
    async with AsyncChatWarsApiClient(Server.CW3, "your instance name", PASSWORD) as c:
        ...

```

Alternative connection variant (works with boh clients):

```python3
c = ...
c.connect()

...

c.disconnect()
```

Info about message types and classes read in [API reference](https://chatwars.github.io/chatwars-api-docs/) and `*.pyi` files in the package.

Some features like `.dump()` method on responses are not implemented