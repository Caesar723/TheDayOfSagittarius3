
import math
import numpy as np
from multiprocessing import Process,Value
import time
from AllModels.functions import *
from AllModels.QTable import *
import random



PATH='src/photo/game/'
class MAP:
    factor = 1
    MAXRANGE, MINRANGE = 3, 1
    OriRadius = 400

    timeParam=50#test (self.test+4)%27


    @property
    def radius(self) -> int:  # return the real radius
        return int(self.OriRadius * self.factor)

    def __init__(self, screen) -> None:
        self.map = makeMap()
        self.position = [800, 800]# the position of map
        self.screen = screen
        self.Flights=[]#flights' position
        self.scout=[]#scouts' position
        self.torpid=[]#torpids' position
        self.imageInitialise()

    def imageInitialise(self): # Initialise image
        print("ok")
        self.menu=pygame.transform.scale(pygame.image.load(f"{PATH}Background.png"),(120,30))
        print("ok")
        self.font=pygame.font.SysFont('Helvetica', 15)
        self.Mfont=pygame.font.SysFont('Helvetica', 20)
        self.menuPosition={"ATTACK":(815,430),"SCOUT":(815,550),"DIVISION":(815,660)}
        self.Status={"SHIPS LEFT":(825,50),"SPEED":(825,80),"DEFENSIVE POWER":(825,110),"OFFENSIVE POWER":(955,80)}
        self.SingleTitlePosition={"STATUS":(815,20),"Teammate":(815,170)}

        self.menuTitle={}
        self.StatusTitle={}
        self.SingleTitle={}

        for title in self.menuPosition:
            self.menuTitle[title]=self.font.render(title, True, (234,233,155))
        for status in self.Status:
            self.StatusTitle[status]=self.font.render(status, True, (209,212,219))
        for single in self.SingleTitlePosition:
            self.SingleTitle[single]=self.Mfont.render(single, True, (234,233,155))

    def showCurrentArea(self) -> None:  # show the small box in right down side

        x, y = int(195 * (self.position[0] - self.radius) / 5000), int(
            390 * (self.position[1] - self.radius) / 10000
        )
        drawBox(
            955 + x,
            410 + y,
            int((self.radius * 2 / 5000) * 195),
            int((self.radius * 2 / 10000) * 390),
            self.screen,
            (255, 255, 255),
            1,
            1,
        )
        drawFlightsPosition(self.screen,self.Flights)

    def showMenu(self)->None: # show image
        for title in self.menuPosition:
            self.screen.blit(self.menu,self.menuPosition[title])
            self.screen.blit(self.menuTitle[title],(self.menuPosition[title][0]+50,self.menuPosition[title][1]+10))
        for status in self.Status:
            self.screen.blit(self.StatusTitle[status],self.Status[status])
        for single in self.SingleTitlePosition:
            self.screen.blit(self.SingleTitle[single],self.SingleTitlePosition[single])
    #@timeRecord
    def showArea(self) -> np.array:  # return the practical map

        

        if self.position[0] < self.radius:
            self.position[0] = self.radius
        if self.position[0] > 5000 - self.radius:
            self.position[0] = 5000 - self.radius
        if self.position[1] < self.radius:
            self.position[1] = self.radius
        if self.position[1] > 10000 - self.radius:
            self.position[1] = 10000 - self.radius
        
        getScreenPosition=np.array(self.position,dtype=np.int32)
        
        self.timeParam=(self.timeParam+4)%24
        

        getAllObject=self.getMyTeamsObjects()#np.array(self.Flights+self.scout,dtype=np.int32)


        

        getMap = drawVisibleArea(
            self.map, getAllObject,getScreenPosition, 200,self.radius
        )
        

        getMap=drawMyScout(
            getMap,np.array(self.scout,dtype=np.int32),self.rgbBody,getScreenPosition,self.radius
        )

        getMap=drawMytorpid(
            getMap,np.array(self.torpid,dtype=np.int32),self.rgbBody
        )
        
        getMap=drawOtherFlight(
            getMap,getAllObject,self.playerDictOppo,self.playerDictMate,self.timeParam,getScreenPosition,self.radius
        )

        getMap=drawLaser(
            getMap,self.player,self.timeParam
        )
        

        getMap= drawMyFlights(
            getMap,np.array(self.Flights,dtype=np.int32),self.rgbSide,self.rgbBody,getScreenPosition,self.radius
        )

        
        
        get = getMap[
            (self.position[1] - self.radius) : (self.position[1] + self.radius),
            (self.position[0] - self.radius) : (self.position[0] + self.radius),
        ]
        
        return get

    def areaLarger(self):
        self.factor += 0.1 if self.factor < self.MAXRANGE else 0

    def areaSmaller(self):
        self.factor -= 0.1 if self.factor > self.MINRANGE else 0

    #@timeRecord
    def getMyTeamsObjects(self):# which include  my teams' and my flights and scouts
        AllObj=list(self.Flights+self.scout)
        for mate in self.playerDictMate:
            for flight in self.playerDictMate[mate].flights:
                if flight[4]:
                    AllObj.append(flight[:4])
            for scout in self.playerDictMate[mate].scouts:
                if scout[4]:
                    AllObj.append(scout[:4])
        
        return np.array(AllObj,dtype=np.int32)
    
    def getMyTeamsTorpid(self):# which include  my teams' and my torpid
        AllObj=list(self.torpid)
        for mate in self.playerDictMate:
            for torpid in self.playerDictMate[mate].torpid:
                if torpid[4]:
                    AllObj.append(torpid[:4])
        return np.array(AllObj,dtype=np.int32)

class Flyer:
    speed=10
    def __init__(self,position:list,map:MAP,player)->None:
        self.Information=position+[0,0]
        self.player=player
        self.map=map
        self.id=str(next(IpGenerator))
        player.attackCache[self.id]=0
    @property
    def y(self)->int:
        return self.Information[0]
    @y.setter
    def y(self,value)->None:
        self.Information[0]=value
    @property
    def x(self)->int:
        return self.Information[1]
    @x.setter
    def x(self,value)->None:
        self.Information[1]=value
    def checkCycle(self):
        pass
    def beAttacked(self):
        pass

class Flight(Flyer):# first angle next move then attack. finish: stay
    state=0# 0: stay  (1:rotate) 2:move 
    attack=0 # whether attack
    
    power=40
    defense=30
    rotateDirection=1# 1 clockwise   0 anticlockwise
    def __init__(self,position:list,size:int,map:MAP,player,blood=15000,angle=90) -> None:
        super().__init__(position,map,player)
        self.blood=blood
        self.Information=position+[size, angle]# y,x,size,angle
        map.Flights.append(self.Information)
        self.targetDistance=0
        self.targetAngle=0
        self.TargetIp=""
        self.TargetId=-1

        self.SpreadSwitch=Value("i",0)# connect with QTablex
        self.TargetPosition=np.array([0,0])
        self.getAttackValue=self.LaserAttack()
    
    @property
    def angle(self):
        return self.Information[3]
    @property
    def power(self):
        return int(0.000467*self.blood+33)
    @property
    def defense(self):
        return int(0.002*self.blood)

    @angle.setter
    def angle(self,value):
        self.Information[3]=(value-1)%360 +1
    

    def checkCycle(self):# command it to this position
        self.checkBlood()
        getPower=self.player.attackCache[self.id]
        if getPower!=0:
            #self.player.LeftShips-=getPower
            self.blood-=(getPower-self.defense)
            self.player.attackCache[self.id]-=getPower
        if self.SpreadSwitch.value!=0:
            
            if self.SpreadSwitch.value<self.blood and self.player.CurrentShips<=19:
                
                self.spread()
            self.SpreadSwitch.value=0
            
        if self.state:
            if abs(self.angle-self.targetAngle)>4:
                
                self.angle+=3 if (self.rotateDirection) else -3
            elif self.state==2 :
                rad=np.pi*self.targetAngle/180
                self.y-=self.speed*math.sin(rad)
                self.x+=self.speed*math.cos(rad)
                self.targetDistance-=self.speed
                if self.targetDistance>-15 and self.targetDistance<9: 
                    self.state=0 
        else:
            if self.attack!=0:
                if ((self.TargetPosition[1]-self.Information[1])**2 + (self.TargetPosition[0]-self.Information[0])**2)**0.5>200 or self.TargetPosition[4]==0:
                    self.attack=0
        self.checkAttack()
        
                    
    def spread(self):
        newFlight=Flight(self.Information[:2],40,self.map,self.player,self.SpreadSwitch.value,self.angle)
        self.player.flights.append(newFlight)
        self.player.CurrentShips+=1
        self.blood-=self.SpreadSwitch.value

    def checkAttack(self):# used to reduce opponenet's blood
        if self.state==0 and self.attack==1 and self.TargetPosition[4]!=0:
            getPower=next(self.getAttackValue)
            
            if getPower:
                if self.player.attackDict[self.TargetIp]=='':
                    self.player.attackDict[self.TargetIp]=f"@{self.TargetId}_{getPower}"
                else:
                    self.player.attackDict[self.TargetIp]+=f"|{self.TargetId}_{getPower}"


    def LaserAttack(self):# use time period to reduce blood
        getTime=time.time()
        while True:
            getTime2=time.time()
            if time.time()-getTime>=0.5:
                getTime=getTime2
                yield self.power
            else:
                yield 0
    def checkBlood(self):
        if self.blood<=0:
            self.player.flights.remove(self)
            self.map.Flights.pop(findSameId(self.map.Flights,self.Information))
            self.player.CurrentShips-=1
            print(self.player.flights)
            print(self.map.Flights)
        self.Information[2]=int(self.blood*0.00333+20)
        
class scout(Flyer):
    state=0
    def __init__(self, position: list,map:MAP, player):
        super().__init__(position,map, player)
        self.targetDistance=0
        self.targetAngle=0
        #self.map.scout.append(self.Information)
    def checkCycle(self):
        if self.state==2 :
            rad=np.pi*self.targetAngle/180
            self.y-=self.speed*math.sin(rad)
            self.x+=self.speed*math.cos(rad)
            self.targetDistance-=self.speed
            if self.targetDistance>-15 and self.targetDistance<9: 
                self.state=0 

class torpid(Flyer):
    power=500
    blood=100

    MASS=30#30
    SIZE=10
    DrivingForce=0
    TargetForce=10
    InitinalSpeed=30

    MaxSpeed=15
    MaxForce=300

    KpV=KpP=3.5
    KdV=KdP=100.3
    KiV=KiP=0.00005
    def __init__(self, position: list, map: MAP,taregtPositon, player,direction) -> None:
        super().__init__(position, map, player)
        self.Information=position+[10, direction]
        self.targetPosition=taregtPositon
        self.TargetIp=''
        self.TargetId=-1
        self.direction=0
        
        self.verticalVelocity=-math.sin(math.pi*direction/180)*self.InitinalSpeed
        self.parallelVelocity=math.cos(math.pi*direction/180)*self.InitinalSpeed
        self.First=True
        self.currentVer=self.currentPal=0
        self.countDiffV=0
        self.countDiffP=0
        map.torpid.append(self.Information)
        self.player.torpid.append(self)


    @property
    def angle(self):
        return self.Information[3]

    @angle.setter
    def angle(self,value):
        self.Information[3]=(value-1)%360 +1

    def checkWhetherAttack(self):
        distance=((self.Information[0]-self.targetPosition[0])**2+(self.Information[1]-self.targetPosition[1])**2)**0.5
        if distance<20:
            self.player.torpid.remove(self)
            self.map.torpid.pop(findSameId(self.map.torpid,self.Information))
            if self.player.attackDict[self.TargetIp]=='':
                self.player.attackDict[self.TargetIp]=f"@{self.TargetId}_{self.power}"
            else:
                self.player.attackDict[self.TargetIp]+=f"|{self.TargetId}_{self.power}"

    def checkCycle(self):
        getPower=self.player.attackCache[self.id]
        if getPower!=0:
            
            self.blood-=getPower
            self.player.attackCache[self.id]-=getPower
            
        diffVar=(self.targetPosition[0]-self.Information[0])/100
        diffPara=(self.targetPosition[1]-self.Information[1])/100

        self.countDiffV+=diffVar
        self.countDiffP+=diffPara

        dfVer=diffVar*self.KpV+(diffVar-self.currentVer)*self.KdV+self.countDiffV*self.KiV
        dfPara=diffPara*self.KpP+(diffPara-self.currentPal)*self.KdP+self.countDiffP*self.KiP

        
        self.currentVer=diffVar
        self.currentPal=diffPara

        if abs(dfVer)>self.MaxForce:
            dfVer=self.MaxForce*dfVer/abs(dfVer)
        if abs(dfPara)>self.MaxForce:
            dfPara=self.MaxForce*dfPara/abs(dfPara)
        
        
        
            
        acceleVer=(dfVer)/self.MASS
        accelePara=(dfPara)/self.MASS

        self.verticalVelocity+=acceleVer
        self.parallelVelocity+=accelePara

        if abs(self.verticalVelocity)>self.MaxSpeed:
            self.verticalVelocity=self.MaxSpeed*self.verticalVelocity/abs(self.verticalVelocity)
        if abs(self.parallelVelocity)>self.MaxSpeed:
            self.parallelVelocity=self.MaxSpeed*self.parallelVelocity/abs(self.parallelVelocity)

        angle=abs(360*math.atan( self.verticalVelocity/self.parallelVelocity)/(2*math.pi))
        if self.verticalVelocity>=0 and self.parallelVelocity<=0:
            angle=180+angle
        elif self.verticalVelocity>=0 and self.parallelVelocity>=0:
            angle=360-angle
        elif self.verticalVelocity<=0 and self.parallelVelocity<=0:
            angle=180-angle
        
        angle=angle%360
        self.angle=angle
        
        self.Information[1]+=self.parallelVelocity
        self.Information[0]+=self.verticalVelocity

        self.checkBlood()
        self.checkWhetherAttack()
        
    def checkBlood(self):
        if self.blood<=0:
            self.player.torpid.remove(self)
            self.map.torpid.pop(findSameId(self.map.torpid,self.Information))

    


class Player:
    MAXSHIP=20
    def __init__(self,map:MAP,rgbSide,rgbBody):
        
        self.rgbSide=rgbSide
        self.rgbBody=rgbBody
        self.map=map
        self.flights=[] # store the player's all ships
        self.scouts=[]
        self.torpid=[]
        #self.LeftShips=15000# the left ships
        
        
### players subclass

class MySelf(Player):
    
    def __init__(self,map,rgbSide,rgbBody,attackDict,attackCache,initinalPositionSwitch):#initinalPosition(# 1 in top position,0 in bottom position)
        super().__init__(map, rgbSide, rgbBody)
        
        self.attackDict=attackDict
        self.attackCache=attackCache
        getInitinalPosition=self.initinalisePosition(initinalPositionSwitch)
        map.position=getInitinalPosition[::-1]
        self.CurrentFlight=Flight(getInitinalPosition,70,map,self)
        self.flights.append(self.CurrentFlight) # store the player's all ships
        self.map.rgbSide=rgbSide # the color of ship
        self.map.rgbBody=rgbBody
        self.CurrentIndex=0 # the index of current ship
        self.LeftScout=10# number of Scout
        self.LeftTorpid=20# number of Torpid
        self.CurrentShips=1# number of ship

        
        self.imageInitialise(map)
        self.Allimages["LASER"].State=1
    def initinalisePosition(self,Bool:int):# 1 in top position,0 in bottom position
        if Bool:
            return [random.randint(100,2000),random.randint(100,4900)]
        else:
            return [random.randint(8000,9900),random.randint(100,4900)]

    def imageInitialise(self,map): # Initialise dynamic image
        self.Allimages={}

        self.itemNonClick=pygame.transform.scale(pygame.image.load(f"{PATH}item.png"),(93,30))# initialize image
        self.itemClick=pygame.transform.scale(pygame.image.load(f"{PATH}Selected.png"),(93,30))
        self.itemPosition={"LASER":(820,460),"TORPID":(820,500),"DEPLOY":(820,580),"COLLECT":(820,620)}
        for name in self.itemPosition:
            self.Allimages[name]=Image(map.font.render(name, True, (248,224,243)),
                self.itemPosition[name],(5,13),self.itemNonClick,self.itemClick)

        self.buttonClick=pygame.transform.scale(pygame.image.load(f"{PATH}Click.png"),(20,20))
        self.buttonNonClick=pygame.transform.scale(pygame.image.load(f"{PATH}NonClick.png"),(20,20))
        
        for ships in range(20):
            self.Allimages[str(ships)]=Image(map.font.render(str(ships), True, (248,224,243)),
                    (820 + (ships%5)*23,695+(ships//5)*25),(6-(ships//10)*3,4),self.buttonNonClick,self.buttonClick)
        self.Allimages["0"].State=1
        
    def refreshAllObject(self,screen):
        for image in self.itemPosition:
            self.Allimages[image].refresh(screen)
        for ships in range(self.CurrentShips):
            self.Allimages[str(ships)].refresh(screen)

    def showStatus(self,screen):
        
        screen.blit(self.map.Mfont.render(str(self.LeftScout), True, (219,224,229)),(915,590))
        screen.blit(self.map.Mfont.render(str(self.LeftTorpid), True, (219,224,229)),(915,512))
        screen.blit(self.map.Mfont.render(str(self.CurrentFlight.speed), True, (219,224,229)),(890,77))
        screen.blit(self.map.Mfont.render(str(self.CurrentFlight.power), True, (219,224,229)),(1110,77))
        screen.blit(self.map.Mfont.render(f"{self.LeftShips}  /  15000", True, (219,224,229)),(940,47))
        screen.blit(self.map.Mfont.render(str(self.CurrentFlight.defense), True, (219,224,229)),(990,108))

    def changeFlight(self,Id):
        index=int(Id)
        if index<self.CurrentShips:
            self.Allimages[str(self.CurrentIndex)].State=0
            self.Allimages[Id].State=1
            
            self.CurrentFlight=self.flights[index]
            self.CurrentIndex=index
            
    def showFlightsLabel(self,screen):
        for index,flight in enumerate(self.flights):
            
            if flight.x>self.map.position[0]-self.map.radius and \
                flight.x<self.map.position[0]+self.map.radius and \
                flight.y<self.map.position[1]+self.map.radius and \
                flight.y>self.map.position[1]-self.map.radius:

                screen.blit(self.map.font.render(f"({index}){flight.blood}", True,
                 (219,224,229)),
                 (400*(flight.x-self.map.position[0]+self.map.radius-23)/self.map.radius,400*(flight.y-self.map.position[1]+self.map.radius+30)/self.map.radius))

    def changeAttackToLaser(self):
        self.Allimages["LASER"].State=1
        self.Allimages["TORPID"].State=0
    def changeAttackToTorpid(self):
        self.Allimages["LASER"].State=0
        self.Allimages["TORPID"].State=1

    def collectScout(self):
        #print(self.map.scout,self.scouts)
        if len(self.scouts)>0:
            getScout=self.scouts.pop(0)
            self.map.scout.pop(findSameId(self.map.scout,getScout.Information))
            ma = self.map.map.reshape(10000, 5000 * 3)
            c.ReDraw(ma,np.array(getScout.Information,dtype=np.int32),220)
            self.LeftScout+=1
        #print(self.map.scout,self.scouts)

    @property
    def LeftShips(self):# the left ships
        totalShip=0
        for flight in self.flights:
            totalShip+=flight.blood

        return totalShip

    def __repr__(self):# y,x,size,angle,blood,state,attack,attack position,id
        
        flightsInfo="/".join( ("|".join('%s'%int(i) for i in flight.Information))+\
            '|'+str(flight.blood)+'|'+str(flight.state)+'|'+str(flight.attack)+'|'+\
                "|".join(flight.TargetPosition[:2].astype(str))+"|"+flight.id for flight in self.flights )
        
        scoutInfo="/".join("|".join("%s"%int(infos) for infos in sco.Information)+"|1|"+sco.id for sco in self.scouts)

        torpidInfo="/".join("|".join("%s"%int(infot) for infot in tor.Information)+'|'+str(tor.blood)+"|"+tor.id for tor in self.torpid)
        allInfo=f"{self.CurrentShips}_{flightsInfo}_{10-self.LeftScout}_{scoutInfo}_{len(self.torpid)}_{torpidInfo}"
        #print(allInfo)
        return allInfo

class otherPlayers(Player):
    def __init__(self, map, rgbSide, rgbBody):
        super().__init__(map, rgbSide, rgbBody)
        self.flights=np.zeros((20,10),dtype=np.int32)# allFllights 
        self.flights[0]=np.array([400,300,70,90,1,0,0,0,0,0])# y,x,size,angle,whether have this ship,state,attack,attack position,id
        self.scouts=np.zeros((10,6),dtype=np.int32)# y,x,size,angle,whether have this scout,id
        self.torpid=np.zeros((20,6),dtype=np.int32)
    def updatePosition(self,string):
        if string!="":
            
            string=string
            
            length,shipsInfo,scolength,scoInfo,trilength,triInfo=string.split("_")

            scolength,trilength,length=int(scolength),int(trilength),int(length)

            if length!=0:
                ships=np.array([ship.split("|") for ship in shipsInfo.split("/")],dtype=np.int32)
            else:
                ships=np.zeros((1,10),dtype=np.int32)
            if scolength!=0:
                scouts=np.array([sco.split("|") for sco in scoInfo.split("/")],dtype=np.int32)
            else:
                scouts=np.zeros((1,6),dtype=np.int32)
            if trilength!=0:
                tripods=np.array([tri.split("|") for tri in triInfo.split("/")],dtype=np.int32)
            else:
                tripods=np.zeros((1,6),dtype=np.int32)

            c.Assgn(ships,self.flights,length)
            c.AssgnFlyer(scouts,self.scouts,scolength,10)
            c.AssgnFlyer(tripods,self.torpid,trilength,20)
            
    def blood(self):
        totalBlood=0
        for fli in self.flights:
            totalBlood+=fli[4]
        return totalBlood
    
class Teammate(otherPlayers):
    def __init__(self, map, rgbSide, rgbBody):
        super().__init__(map, rgbSide, rgbBody)
        self.flights[0]=np.array([500,300,70,90,1,0,0,0,0,0])
    
    def showFlights(self,map,timePara,ScreenPosition,ScreenRadius):
        
        c.DrawMateFlights(map,
            self.flights,
            self.rgbSide,self.rgbBody,timePara,
            ScreenPosition,ScreenRadius)
        c.DrawMateScout(map,3,
            self.scouts,
            self.rgbBody,
            ScreenPosition,ScreenRadius)
        c.DrawMateTorpid(map,
            self.torpid,
            self.rgbBody,
            ScreenPosition,ScreenRadius)
    def showFlightsLabel(self,screen):
        for index,each in enumerate(self.flights):
            if each[4]!=0 and each[1]>self.map.position[0]-self.map.radius and \
                each[1]<self.map.position[0]+self.map.radius and \
                each[0]<self.map.position[1]+self.map.radius and \
                each[0]>self.map.position[1]-self.map.radius:
                screen.blit(self.map.font.render(f"({index}){each[4]}", True,
                        (219,224,229)),
                        (400*(each[1]-self.map.position[0]+self.map.radius-23)/self.map.radius,400*(each[0]-self.map.position[1]+self.map.radius+30)/self.map.radius))

class Opponent(otherPlayers):
    

    def showFlights(self,myFlights,map,timePara,ScreenPosition,ScreenRadius):
        length=len(myFlights)
        if length:
            c.DrawOpponentFlights(map,myFlights,
                length,
                self.flights,
                self.rgbSide,self.rgbBody,timePara,
                ScreenPosition,ScreenRadius)
            c.DrawOpponentScout(
                map,myFlights,
                length,3,
                self.scouts,
                self.rgbBody,
                ScreenPosition,ScreenRadius
            )
            c.DrawOpponentTorpid(
                map,myFlights,
                length,
                self.torpid,
                self.rgbBody,
                ScreenPosition,ScreenRadius
            )
    def showFlightsLabel(self,screen):
        getAllObj=self.map.getMyTeamsObjects()
        length=len(getAllObj)
        if length:
            for index,each in enumerate(self.flights):
                
                if each[4]!=0 and c.InRange(getAllObj,each[0],each[1],length,200):
                    screen.blit(self.map.font.render(f"({index}){each[4]}", True,
                            (219,224,229)),
                            (400*(each[1]-self.map.position[0]+self.map.radius-23)/self.map.radius,400*(each[0]-self.map.position[1]+self.map.radius+30)/self.map.radius))

    
        
###
    

class EventProcessor:
    SCREENLOCATESWITCH = False
    RUN=True
    SCOUTPattern=False
    SENDOVERSWITCH=True
    KEYCONVERT={'!':"11",'@':'12',"#":'13',"$":'14',"%":'15',"^":'16','&':'17','*':'18','(':'19',')':'10'}
    def __init__(self,map:MAP,player:MySelf,screen,playerDictOppo,playerDictMate):
        #playMusic()
        self.keysDict = {'+': map.areaLarger, '-': map.areaSmaller,"S":self.spread,"D":self.ChangeScoutPattern,"L":player.changeAttackToLaser,"T":player.changeAttackToTorpid,"C":player.collectScout}
        self.screen=screen
        self.player=player
        self.map=map
        self.process=Process(target=startQT,args=(self.player.CurrentFlight.SpreadSwitch,))
        self.playerDictOppo=playerDictOppo
        self.playerDictMate=playerDictMate
        self.OverMessageFont=pygame.font.SysFont('Helvetica', 90)


    def pygameEventDetect(self,eve,multi):
        
        if eve.type == pygame.QUIT:
                
                self.RUN=False
                multi.terminate()
                
        elif eve.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > 955 and pos[0] < 1160 and pos[1] > 410 and pos[1] < 800:
                self.SCREENLOCATESWITCH = True
            elif pos[0] > 10 and pos[0] < 790 and pos[1] > 10 and pos[1] < 790:
                if self.SCOUTPattern:
                    self.SendScout(pos)
                else:
                    self.ProcessInMap(pos)


        elif eve.type == pygame.MOUSEBUTTONUP:
            self.SCREENLOCATESWITCH = False
            
        elif eve.type == pygame.TEXTINPUT:
            if eve.text in self.keysDict:
                self.keysDict[eve.text]()
            else:
                if '0'<=eve.text and eve.text<='9':
                    self.player.changeFlight(eve.text)
                elif eve.text in self.KEYCONVERT:
                    self.player.changeFlight(self.KEYCONVERT[eve.text])
                
    def SendScout(self,pos):# place scout in map
        if self.player.LeftScout>=1:
            x,y=self.map.radius*(pos[0]-400)/400 +self.map.position[0],self.map.radius*(pos[1]-400)/400 +self.map.position[1]
            newScout=scout(self.player.CurrentFlight.Information[:2],self.map,self.player)
            newScout.state=2
            newScout.targetAngle,newScout.targetDistance=self.calculatePositionAngle(x,y)
            
            self.player.scouts.append(newScout)
            self.map.scout.append(newScout.Information)
            
            self.player.LeftScout-=1

    def ProcessInMap(self,pos):
        
        index=-1

        x,y=self.map.radius*(pos[0]-400)/400 +self.map.position[0],self.map.radius*(pos[1]-400)/400 +self.map.position[1]
        
            
        
        ###check the goal whether is to attack ship
        getAllObj=self.map.getMyTeamsObjects()
        if c.InRange(getAllObj,y,x,len(getAllObj),200):
            
            for name in self.playerDictOppo:
                getRelateIndex=c.CheckWhetherAttack(self.playerDictOppo[name].flights,
                    x,y)
                getRelateIndexTorpid=c.CheckWhetherAttackTorpid(self.playerDictOppo[name].torpid,
                    x,y)
                
                if getRelateIndex!=-1:
                    getList=self.playerDictOppo[name].flights
                    index=getRelateIndex
                elif getRelateIndexTorpid!=-1:
                    getList=self.playerDictOppo[name].torpid
                    index=getRelateIndexTorpid
                
                if index!=-1  :

                    if self.player.Allimages["LASER"].State==1:# laser pattern

                        self.player.CurrentFlight.targetAngle,self.player.CurrentFlight.targetDistance=self.calculatePositionAngle(x,y)# find target distane and find angle
                
                        if (self.player.CurrentFlight.angle-self.player.CurrentFlight.targetAngle)>0:#check the rotate direction
                            self.player.CurrentFlight.rotateDirection=1 if abs(self.player.CurrentFlight.angle-self.player.CurrentFlight.targetAngle)>180 else 0
                        else:
                            self.player.CurrentFlight.rotateDirection=0 if abs(self.player.CurrentFlight.angle-self.player.CurrentFlight.targetAngle)>180 else 1


                        Distance=\
                        ((self.player.CurrentFlight.y-getList[index][0])**2+\
                        (self.player.CurrentFlight.x-getList[index][1])**2)**0.5
                        

                        if Distance>200:
                            self.player.CurrentFlight.targetDistance=Distance-190
                            
                            
                        else:
                            self.player.CurrentFlight.targetDistance=0

                        self.player.CurrentFlight.state=2
                        self.player.CurrentFlight.TargetPosition=getList[index]
                        self.player.CurrentFlight.attack=1
                        self.player.CurrentFlight.TargetIp=name
                        self.player.CurrentFlight.TargetId=getList[index][-1]
                        #print(self.playerDict[name].flights[getRelateIndex])
                        return 
                    elif self.player.Allimages["TORPID"].State==1:# torpid pattern
                        if  self.player.LeftTorpid>0:
                            self.player.LeftTorpid-=1
                            getTorpid=torpid(self.player.CurrentFlight.Information[:2],self.map,getList[index],self.player,self.player.CurrentFlight.angle)
                            getTorpid.TargetIp=name
                            getTorpid.TargetId=getList[index][-1]
                        return 
                    
                    
                    
        
        self.player.CurrentFlight.targetAngle,self.player.CurrentFlight.targetDistance=self.calculatePositionAngle(x,y)# find target distane and find angle
                
        if (self.player.CurrentFlight.angle-self.player.CurrentFlight.targetAngle)>0:#check the rotate direction
            self.player.CurrentFlight.rotateDirection=1 if abs(self.player.CurrentFlight.angle-self.player.CurrentFlight.targetAngle)>180 else 0
        else:
            self.player.CurrentFlight.rotateDirection=0 if abs(self.player.CurrentFlight.angle-self.player.CurrentFlight.targetAngle)>180 else 1

        self.player.CurrentFlight.state=2
        self.player.CurrentFlight.attack=0

    def spread(self):
        if not(self.process.is_alive()):
            self.process=Process(target=startQT,args=(self.player.CurrentFlight.SpreadSwitch,))
            self.process.start()
        
    def calculatePositionAngle(self,x,y):
        
        
        ang=-180*math.atan((self.player.CurrentFlight.y-y)/(self.player.CurrentFlight.x-x+0.001))/np.pi
        if self.player.CurrentFlight.x-x>0:
            if self.player.CurrentFlight.y-y>0:
                ang+=180
            else:
                ang-=180
        ang=(ang+360) if ang<0 else ang

        return (ang,((self.player.CurrentFlight.y-y)**2+(self.player.CurrentFlight.x-x)**2)**0.5)
        
    def ChangeScoutPattern(self):
        self.SCOUTPattern=not(self.SCOUTPattern)
        self.player.Allimages['DEPLOY'].State=int(self.SCOUTPattern)
        
    def checkCurrntSituation(self,multi):
        MyTeamSwitch=OppoTeamSwitch=False
        for Teammate in self.playerDictMate:
            MyTeamSwitch=MyTeamSwitch or self.playerDictMate[Teammate].blood()>0
        MyTeamSwitch=MyTeamSwitch or self.player.LeftShips>0

        for Teamoppo in self.playerDictOppo:
            OppoTeamSwitch=OppoTeamSwitch or self.playerDictOppo[Teamoppo].blood()>0
        
        #print(MyTeamSwitch,OppoTeamSwitch)
        if not(MyTeamSwitch):
            self.showGameOverMessage("YOU LOSE")
            if self.SENDOVERSWITCH:
                threading.Thread(target=self.timeSetCloseGame,args=(3,multi,)).start()
                self.SENDOVERSWITCH=False

        if not(OppoTeamSwitch):
            self.showGameOverMessage("YOU WIN")
            if self.SENDOVERSWITCH: 
                threading.Thread(target=self.timeSetCloseGame,args=(3,multi,)).start()
                self.SENDOVERSWITCH=False

    def showGameOverMessage(self,message:str):
        self.screen.blit(self.OverMessageFont.render(message, True, (250,10,10)),(440,337))
    
    def timeSetCloseGame(self,set:int,multi):
        time.sleep(set)
        self.RUN=False
        multi.terminate()

class Image:

    def __init__(self,Name,position:tuple,difference:tuple,surfaceNonClick,surfaceClick):
        self.State=0 #0 :none click 1: click
        self.Name=Name
        self.surface={0:surfaceNonClick,1:surfaceClick}
        self.position=position
        self.NamePosition=(position[0]+difference[0],position[1]+difference[1])
        self.diff=difference
    def refresh(self,screen):
        screen.blit(self.surface[self.State],self.position)
        screen.blit(self.Name,self.NamePosition)


        