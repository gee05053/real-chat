# RealTime WebChat
해당 Repo는 하나의 채팅방에서 여러 사용자들이 실시간 채팅을 할 수 있는 프로젝트이다.

# Server
서버는 server.py에 구현되어 있다.

사용 기술
* aioredis
* aiohttp
* asyncio

# Web
구현 예정

# Installation
1. git clone

```
$ git clone https://github.com/gee05053/realtime-webChat.git
```

2. docker compose
```
$ docker compose docker-compose.yml up --build
```
3. run client.py on serveral terminal
```
$ python3 client.py
```