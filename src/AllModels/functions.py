import pygame
import math
import ctypes
import numpy.ctypeslib as cnl
import numpy as np
import time
import threading

"""
[y,x]
"""

def initinaliseGenerator(fun):
    get=fun()
    return get

def timeRecord(fun):
    def func(*args):
        t = time.time()
        get = fun(*args)
        print(time.time() - t)
        return get

    return func

def loadDll():# try to load dll in possible path
    address=("libhug.so","Dll1.dll","Dll1.dll")#possible path
    for addr in address:
        try:
            lib=ctypes.CDLL(addr)
            return lib
        except:
            pass

def initialise():  # initialise c++ functions
    lib = loadDll()
    lib.drawMapLine.argtypes = [
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        )
    ]
    lib.addVisibleArea.argtypes = [
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int
        
    ]
    lib.drawFlights.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        ctypes.c_int,cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
    ]
    lib.getThreePoint.argtypes=[
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        cnl.ndpointer(dtype=np.double, ndim=2, flags="C_CONTIGUOUS")
    ]
    lib.DrawOpponentFlights.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
    ]
    lib.drawLaser.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
    ]
    lib.CheckWhetherAttack.argtypes=[
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        
        ctypes.c_double,ctypes.c_double,
    ]
    lib.CheckWhetherAttack.restype=ctypes.c_int
    lib.CheckWhetherAttackTorpid.argtypes=[
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        
        ctypes.c_double,ctypes.c_double,
    ]
    lib.CheckWhetherAttackTorpid.restype=ctypes.c_int
    lib.InRange.argtypes=[
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        ctypes.c_double,ctypes.c_double,
        ctypes.c_int,
        ctypes.c_int,
    ]
    lib.InRange.restype=ctypes.c_bool
    lib.Assgn.argtypes=[
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        ctypes.c_int,
    ]
    lib.drawMyScout.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,

    ]
    lib.ReDraw.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        
    ]
    lib.DrawTorpid.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS")
    ]
    lib.AssgnFlyer.argtypes=[
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        ctypes.c_int,
    ]
    lib.DrawOpponentScout.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        ctypes.c_int,
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int
    ]
    lib.DrawOpponentTorpid.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int
    ]
    lib.DrawMateFlights.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int,
    ]
    lib.DrawMateScout.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        ctypes.c_int,
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int
    ]
    lib.DrawMateTorpid.argtypes=[
        cnl.ndpointer(
            dtype=np.int32, ndim=2, shape=(10000, 5000 * 3), flags="C_CONTIGUOUS"
        ),
        cnl.ndpointer(dtype=np.int32, ndim=2, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        cnl.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS"),
        ctypes.c_int
    ]
    return lib


c = initialise()


def drawBox(
    x: int,
    y: int,
    length: int,
    width: int,
    screen,
    color=(255, 255, 255),
    radius=10,
    thick=3,
) -> None:
    diameter = [radius * 2] * 2
    pygame.draw.line(
        screen, color, [x + radius, y], [x + length - radius, y], thick
    )  # up
    pygame.draw.arc(
        screen, color, (x, y, *diameter), math.radians(90), math.radians(180), thick
    )

    pygame.draw.line(
        screen, color, [x, y + radius], [x, y + width - radius], thick
    )  # left
    pygame.draw.arc(
        screen,
        color,
        (x, y + width - radius * 2, *diameter),
        math.radians(180),
        math.radians(270),
        thick,
    )

    pygame.draw.line(
        screen, color, [x + length, y + radius], [x + length, y + width - radius], thick
    )  # right
    pygame.draw.arc(
        screen,
        color,
        (x + length - radius * 2, y, *diameter),
        math.radians(0),
        math.radians(90),
        thick,
    )

    pygame.draw.line(
        screen, color, [x + radius, y + width], [x + length - radius, y + width], thick
    )  # down
    pygame.draw.arc(
        screen,
        color,
        (x + length - radius * 2, y + width - radius * 2, *diameter),
        math.radians(270),
        math.radians(360),
        thick,
    )


def makeMap():  # initialise Map
    spaceMap = (
        np.zeros((10000, 5000, 3), dtype=np.int32)
        + np.array([14, 15, 28], dtype=np.int32)
    ).reshape(10000, 5000 * 3)
    c.drawMapLine(spaceMap)
    return spaceMap.reshape(10000, 5000, 3)

#@timeRecord
def separateRemake(start,end,map, allMyObject, radius):
    for i in range(start,end):
        c.ReDraw(map,allMyObject[i],radius)
def remakeMap(map,allMyObject):
    ma = map.reshape(10000, 5000 * 3)
    length=len(allMyObject)
    
    thread=[]
    get=np.linspace(0,length,5 if length>5 else 2,dtype=int)
    val=0
    for i in get[1:]:
        th=threading.Thread(target=separateRemake,args=(val,i,ma,allMyObject,220))
        val=i
        th.start()
        thread.append(th)

    for ii in thread:
        ii.join()
    return ma

def ReMakeTorpid(map,Torpid):# make the Torpids' area become origin
    for i in Torpid:
        c.ReDraw(map,i,25)

def drawFrames(screen) -> None: #draw the outer frame
    drawBox(*[0, 0], 800, 800, screen)
    drawBox(*[805, 0], 350, 150, screen)
    drawBox(*[805, 155], 350, 250, screen)
    drawBox(*[805, 410], 150, 390, screen)
    drawBox(*[955, 410], 195, 390, screen)


#@timeRecord
def separateThread(start,end,map, filghts, radius,radiusOfScreen,ScreenPosition):# try to reduce the occupation of cpu
    for i in range(start,end):
        c.addVisibleArea(map, filghts, ScreenPosition,i,radius,radiusOfScreen)

#@timeRecord
def drawVisibleArea(map, filghts, ScreenPosition,radius=70, radiusOfScreen=400):  # draw circles
    ma = map.reshape(10000, 5000 * 3)
    length=len(filghts)
    thread=[]
    
    get=np.linspace(0,length,5 if length>5 else 2,dtype=int)
    val=0
    for i in get[1:]:
        th=threading.Thread(target=separateThread,args=(val,i,ma, filghts,radius,radiusOfScreen,ScreenPosition))
        val=i
        th.start()
        thread.append(th)

    for ii in thread:
        ii.join()

    return ma

def drawScoutVisible(map, scouts, radius=70):
    length=len(scouts)
    thread=[]
    get=np.linspace(0,length,10 if length>10 else 2,dtype=int)
    for i in get[1:]:
        th=threading.Thread(target=c.addVisibleScout,args=(map, scouts, i, radius))
        
        th.start()
        thread.append(th)

    for ii in thread:
        ii.join()

    return map
#@timeRecord
def drawMyFlights(map,flights,sideColor,bodyColor,ScreenPosition,ScreenRadius):
    #ma = map.reshape(10000, 5000 * 3)
    length=len(flights)
    #thread=[]
    for i in range(length):
        c.drawFlights(map,flights,i,sideColor,bodyColor,ScreenPosition,ScreenRadius)
    
    
    return map.reshape(10000, 5000, 3)

#@timeRecord
def drawOtherFlight(map,flights,playerDictOppo,playerDictMate,timePara,ScreenPosition,ScreenRadius):
    #thread=[]
    
    for ipOppo in playerDictOppo:
        
        playerDictOppo[ipOppo].showFlights(flights,map,timePara,ScreenPosition,ScreenRadius)
    for ipMate in playerDictMate:
        playerDictMate[ipMate].showFlights(map,timePara,ScreenPosition,ScreenRadius)
    
    return map

def drawMyScout(map,scouts,bodyColor,ScreenPosition,ScreenRadius):
    length=len(scouts)
    if length!=0:
        c.drawMyScout(map,scouts,length,bodyColor,3,ScreenPosition,ScreenRadius)
    return map
    
def drawMytorpid(map,torpids,bodyColor):
    
    for torpid in torpids:
        c.DrawTorpid(map,torpid,bodyColor)
    return map


def drawLaser(map,player,timepara):#test
    for flight in player.flights:
        if flight.attack!=0 and flight.state==0:
            
            c.drawLaser(map,np.array(flight.Information,dtype=np.int32),flight.TargetPosition,timepara)

    return map

def playMusic():#background music
    pygame.mixer.music.load(
        "music/4.mp3"
    )
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)  # play background music

def stopMusic():
    pygame.mixer.music.stop()

def drawFlightsPosition(screen,flights:list):#in small map
    for flight in flights:
        points=np.zeros((3,2),dtype=np.double)
        c.getThreePoint(np.array(flight,dtype=np.int32),10,points)
        pygame.draw.polygon(screen,(255,255,255),points.astype("int32"))

def drawMatesPosition(screen,MatesDict):#in small map
    for ip in MatesDict:
        for flight in MatesDict[ip].flights:
            if flight[4]:
                points=np.zeros((3,2),dtype=np.double)
                c.getThreePoint(np.array(flight,dtype=np.int32),10,points)
                pygame.draw.polygon(screen,MatesDict[ip].rgbBody,points.astype("int32"))


def CycleChecks(player,map):
    getMap=remakeMap(map.map,map.getMyTeamsObjects())
    ReMakeTorpid(getMap,map.getMyTeamsTorpid())
    for flight in player.flights:
        flight.checkCycle()
    for scout in player.scouts:
        scout.checkCycle()
    for torp in player.torpid:
        torp.checkCycle()

def CycleUpdate(dicOppo,dicMate,dicInfo):
    
    for ipOppo in dicOppo:
        dicOppo[ipOppo].updatePosition(dicInfo[ipOppo])
    for ipMate in dicMate:
        dicMate[ipMate].updatePosition(dicInfo[ipMate])

def findSameId(list,object):
    for i in range(len(list)):
        if list[i] is object:
            return i

@initinaliseGenerator   
def IpGenerator():
    number=0
    while True:
        yield number
        number+=1

def showFlightsLabel(player,playerDictOppo,playerDictMate,screen):
    player.showFlightsLabel(screen)
    for eachOppo in playerDictOppo:
        playerDictOppo[eachOppo].showFlightsLabel(screen)
    for eachMate in playerDictMate:
        playerDictMate[eachMate].showFlightsLabel(screen)

def displayTeammate(screen,MatesDict,render):# teammates' label
    interval=50
    for index,ip in enumerate(MatesDict):
        pygame.draw.polygon(screen,MatesDict[ip].rgbBody,((835, 205+index*interval),(835, 225+index*interval),(855, 215+index*interval)) )
        screen.blit(render(f"{MatesDict[ip].blood()}  /  15000",True,(219,224,229)),(980,205+index*interval))