import asyncio
import socket
#from concurrent.futures import ProcessPoolExecutor


def IP()->str: #return IP address
    try:
        soc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        soc.connect(('8.8.8.8',20))
        ip=soc.getsockname()[0]
    finally:
        soc.close()
    return ip

async def receive(reader:asyncio.StreamReader):

    data = await reader.readuntil(b"!")
    data=data.decode()
    if data[0]=='@':
        attackList=data[1:-1].split('|')
        for each in attackList:
            id,power=each.split('_')
            power=int(power)
            cache[id]+=power


    else:
        id,message=data.split('_',1)
        info[id]=message[:-1]
        #print(info,data)
        
async def connectServerRW(ServerIP):# repeat connect until success
    tryConn,tryCount=True,0
    while tryConn:
        try:
            reader, writer = await asyncio.open_connection(
                ServerIP, 8888)
            tryConn=False
        except:
            tryCount+=1
            if tryCount>=10:
                raise ConnectionRefusedError
            await asyncio.sleep(3)
    return reader, writer

async def autoReceive(reader):
    while True:
        await receive(reader)

async def tcp_echo_client(ip,ServerIP):
    reader, writer = await connectServerRW(ServerIP)

    getRradFuture=asyncio.create_task(autoReceive(reader))
    while True:
        
        if info[ip]!="":
            writer.write(f"{info[ip]}!".encode())
            await writer.drain()
            info[ip]=""

        
        for AttackIP in dict(attack):
            if attack[AttackIP]!='':
                writer.write((attack[AttackIP]+'&'+AttackIP+"!").encode())# (attack value )& ip
                await writer.drain()
                attack[AttackIP]=''
        await asyncio.sleep(0.03)


        
def startSocketClient(dic,dicAttack,attackCache,MyIP,ServerIP):
    global info,attack,cache
    info=dic
    attack=dicAttack
    cache=attackCache
    asyncio.run(tcp_echo_client(MyIP,ServerIP))

