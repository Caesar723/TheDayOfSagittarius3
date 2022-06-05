import asyncio
import socket
import time

def IP()->str: #return IP address
    try:
        soc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        soc.connect(('8.8.8.8',20))
        ip=soc.getsockname()[0]
    finally:
        soc.close()
    print(ip)
    return ip

async def receive(reader:asyncio.StreamReader):#position information_index,blood reduced]
    data = await reader.readuntil(b"!")
    return data.decode()

async def send(writer:asyncio.StreamWriter,ipClient):# ip _ position information_index,blood reduced
    #print(info)
    for ip in dict(info):
        #print(info,ip)
        if ip!=ipClient:
            
            writer.write((f"{ip}_{info[ip]}!").encode())
            await writer.drain()
            
    if attack[ipClient]!='':
        #print(attack[ipClient])
        writer.write((attack[ipClient]+"!").encode())
        await writer.drain()
        attack[ipClient]=''

async def autoSend(writer,addr):
    while True:
        await send(writer,addr)
        await asyncio.sleep(0.03)

async def handle_echo(reader:asyncio.StreamReader, writer:asyncio.StreamWriter):
    addr = writer.get_extra_info('peername')[0]
    autoSendFuture=asyncio.create_task(autoSend(writer,addr))
    try:
        while True:
            
            message=await receive(reader)
            if message[0]=='@':
                AttackMessage,ip=message[1:-1].split('&')
                if MyIP==ip:
                    attackList=AttackMessage.split('|')
                    for each in attackList:
                        id,power=each.split('_')
                        power=int(power)
                        cache[id]+=power
                else:
                    if attack[ip]=='':
                        attack[ip]='@'+AttackMessage
                    else:
                        attack[ip]+='|'+AttackMessage
                
            else:
                #try:
                info[addr]=message[:-1]
                
            
    except asyncio.exceptions.IncompleteReadError:
        
        writer.close()
    except  ConnectionResetError:
        writer.close()
    info[addr]="1_800|800|70|90|0|0|0|0|0|0_0__0_!"


async def main():
    server = await asyncio.start_server(
        handle_echo,MyIP, 8888)
    print("Start server")
    #print(server.sockets)

    async with server:
        await server.serve_forever()




def startSocket(dic,dicAttack,attackCache,IP):
    global info,attack,cache,MyIP
    info=dic
    attack=dicAttack
    cache=attackCache
    MyIP=IP
    
    
    
    asyncio.run(main())


    