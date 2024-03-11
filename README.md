<h1>RealTime WebChat</h1>
해당 Repo는 하나의 채팅방에서 여러 사용자들이 실시간 채팅을 할 수 있는 프로젝트이다.

<h2>Server</h2>
서버는 server.py에 구현되어 있다.
비동기 처리를 위해서 aiohttp, aioredis, asyncio를 사용

<h2>Web</h2>
구현 예정

<h2>Installation</h2>
1. git clone

```
$ git clone https://github.com/gee05053/realtime-webChat.git
```

2. docker compose
```
$ docker compose docker-compose.yml up --build
```
3. 
```
$ python3 client.py
```
