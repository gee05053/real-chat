import aiohttp
import asyncio
import aioconsole
import json

async def send_message_to_server(ws, user_id) :
  while True :
    message = await aioconsole.ainput()
    check_blank = message.replace(" ", "")
    if message == "q" :
      break
    elif message == "" or check_blank == "" :
      continue
    else :
      await ws.send_str(json.dumps({"sender":user_id, "message": message}))
  print("Client를 종료합니다.")
  await ws.close()

async def receive_message_from_server(ws, user_id) :
  async for msg in ws :
    if msg.type == aiohttp.WSMsgType.text :
      message_data = json.loads(msg.data)
      if message_data["sender"] == "Server" :
        print(message_data["message"], "현재 채팅방은 " + str(message_data["group_count"]) + "명 있습니다.")
      else :
        if user_id != message_data["sender"] :
          print(message_data["message"])
    elif msg.type == aiohttp.WSMsgType.closed :
      break

async def main() :
  async with aiohttp.ClientSession("http://localhost:8080") as session :
    async with session.ws_connect("/ws") as ws : #웹소켓 연결
      user_id = await ws.receive() #user_id를 서버에서 받기
      print(user_id)
      print("Connect Server!!")
      print("My name is:", "User"+user_id.data)
      print("종료하실려면 q를 입력하세요.")
      send_message = send_message_to_server(ws, user_id.data)
      receive_message = receive_message_from_server(ws, user_id.data)
      await asyncio.gather(send_message, receive_message)

try :
  asyncio.run(main())
except KeyboardInterrupt :
  print("\nClient를 종료합니다.") 