import asyncio
import aiohttp
from aiohttp import web
import aioredis
import json

connect_client = {}
count = 0

async def receive_message_from_client(ws, user_id, redis) :
  async for msg in ws :
    if msg.type == aiohttp.WSMsgType.text :
      await redis.publish("chat", msg.data)
  connect_client.pop(user_id)
  await redis.publish("chat", json.dumps({"sender": user_id, "message": "closed"})) #사용자가 종료했을 때
  print(user_id,"closed")
  print(connect_client)
  await ws.close()

async def send_message_to_client(ws, user_id, pubsub) :
  while True :
    try :
      message = await pubsub.get_message(ignore_subscribe_messages=True)
      if message is not None :
        print(message)
        message_data = json.loads(message["data"].decode())
        send_user_id, receive_message = message_data["sender"], message_data["message"]
        if receive_message == "closed" : #종료 메세지일 때
          if user_id == send_user_id :
            break
          else :
            await ws.send_str(json.dumps({"sender": "Server", "message": "User"+f"{send_user_id} leave chat room.", "group_count": len(connect_client)}))
        elif receive_message == "Join" : #사용자 참가 메세지일 때
          if user_id != send_user_id :
            await ws.send_str(json.dumps({"sender": "Server", "message": "User"+f"{send_user_id} have joined chat room.", "group_count": len(connect_client)}))
          else :
            await ws.send_str(json.dumps({"sender": "Server", "message": "You have joined new Chat Room.", "group_count": len(connect_client)}))
        else : #유저가 메세지를 보냈을 때
          await ws.send_str(json.dumps({"sender": send_user_id, "message": receive_message}))
    except asyncio.TimeoutError :
      pass

async def websocket_handler(request) :
  ws = web.WebSocketResponse()
  await ws.prepare(request)
  redis = await aioredis.from_url("redis://localhost") #redis 연결
  pubsub = redis.pubsub()
  await pubsub.subscribe("chat") #구독
  global count
  count += 1
  user_id = str(count)
  connect_client[user_id] = ws
  await ws.send_str(user_id)
  await redis.publish("chat", json.dumps({"sender": user_id, "message": "Join"})) #구독자에게 참가한 유저 아이디와 참여했다는 메세지 publish
  print("Connect", user_id)
  print(connect_client)
  receive_message = asyncio.create_task(receive_message_from_client(ws, user_id, redis))
  send_message = asyncio.create_task(send_message_to_client(ws, user_id, pubsub))
  await asyncio.gather(receive_message, send_message)
  return ws
  
def main() :
  app = web.Application()
  app.add_routes([web.get("/ws", websocket_handler)])
  web.run_app(app)
  print("\nServer를 종료합니다.")

main()