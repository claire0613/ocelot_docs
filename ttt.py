import asyncio
import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("Connected to the server.")
    # 模擬登錄，發送teacher_login事件
    await sio.emit('teacher_login', {'user_id': '123', 'org_id': 'abc'})

@sio.event
async def disconnect():
    print("Disconnected from the server.")

@sio.event
async def teacher_logout(data):
    print("Received teacher_logout event:", data)
    # 處理teacher_logout事件...

    # 發送確認回應
    return 'Logout acknowledged'

async def start():
    await sio.connect('http://localhost:5000')  # 確保這裡的地址和端口匹配你的服務器
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(start())
