
import sys
from PySide6 import QtWidgets,QtGui
import socket
import threading
import multiprocessing
import time
import os
import random
from AllModels import *

from AllModels.Game import startGame



        

class MyWidget(QtWidgets.QGraphicsView):
    
    def __init__(self):
        super().__init__()
        self.resize(1160, 800)
        self.setFixedSize(1160, 800)# initinal page size
        self.setWindowIcon(QtGui.QIcon('photo/hall/yuki.ico'))
        self.setWindowTitle('The Day of Sagittarius 3')

        self.IpRoom={}# used to store ip which be found ip:time
        self.ServerSwitch=[True]# broadcast and main room loop control
        self.ClientSwitch=[True]# broadcast control
        self.mainClientSwitch=[True]# main room loop control
        self.Server=0# initinal the Server thread
        self.Client=0# initinal the Client thread
        self.ServerMainRoom=0 # initinal the MainRoom thread
        self.ClientConnect=None# initinal socket object used for change team
        self.ServerIP=None# used for change team

        self.autoUpdateServerThread=0
        self.autoUpdateClientThread=0

        self.TeamTop={}# ip : {"client":conn,"time":time.time()}
        self.TeamTopItems={}# index : item
        self.TeamBottom={}
        self.TeamBottomItems={}
        self.hallButton={"START":self.toMatchRoom,"TUTORIAS":self.toTutorial}# initinal  the event of ech key
        self.tutorDictPage1=readDefineFile()
        
        self.backGround=QtGui.QPixmap("photo/hall/back.jpg")#background
        self.backGround=self.backGround.scaled(self.width(),self.height())
        self.setBackgroundBrush(self.backGround)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.scene().addPixmap(self.backGround)

        self.backButton = QtWidgets.QPushButton("BACK")
        self.backButton.setObjectName("backButton")
        self.backButton.setGeometry(140, 710, 100, 50)
        self.backButton.clicked.connect(self.toHall)
        self.backButton.hide()
        self.scene().addWidget(self.backButton)
        # initinal all components
        self.InitinalHall()
        self.InitinalTutorial()
        self.InitinalMatchRoom()
        self.InitinalCreateRoom()
        self.InitinalMainRoom()
        self.InitinalSearchRoom()
    
        self.startClient()
    
        
    """Initinal page"""
    def InitinalHall(self):
        getList=self.setup_button()
        getTitle=self.setup_scene((130,80))
        self.CurrentCompoents=[getList,getTitle]
        self.Hall=self.CurrentCompoents

    def InitinalTutorial(self):
        getTitle=self.setup_scene((30,30),300,100)
        getTitle.hide()
        getList=self.setup_tutorPageList1()
        getList.hide()
        getKeyTitle=self.getKeyTitle()
        getKeyTitle.hide()
        getLabel=self.tutorLabel()
        getLabel.hide()
        self.tutorImage={'+':[self.initinalImage("photo/hall/enlarge.png",(350,200),(750,550))],# initinal all the tutor image
                        '-':[self.initinalImage("photo/hall/compress.png",(350,200),(750,550))],
                        '0~9':[self.initinalImage("photo/hall/click0-9.png",(350,250),(750,350))],
                        "'!'~')'":[self.initinalImage("photo/hall/click!-).png",(350,250),(750,350))],
                        'S':[self.initinalImage("photo/hall/spreat.png",(400,250),(650,450))],
                        'D':[self.initinalImage("photo/hall/Deploy.png",(400,250),(650,500))],
                        'L':[self.initinalImage("photo/hall/Laser.png",(400,250),(650,500))],
                        'T':[self.initinalImage("photo/hall/Torpid.png",(400,250),(650,500))],
                        'C':[self.initinalImage("photo/hall/collect.png",(400,250),(700,450))],}
        self.currentTutor=[]
        self.Tutorual=[getTitle,getList,getLabel,getKeyTitle,self.backButton]

    def InitinalMatchRoom(self):
        self.RoomButton = QtWidgets.QPushButton("Create Room")
        self.RoomButton.setObjectName("backButton")
        self.RoomButton.setGeometry(740, 710, 100, 50)
        self.RoomButton.clicked.connect(self.toCreateRoom)
        self.RoomButton.hide()

        SearchButton = QtWidgets.QPushButton("Search Room")
        SearchButton.setObjectName("backButton")
        SearchButton.setGeometry(600, 710, 100, 50)
        SearchButton.clicked.connect(self.toSearchRoom)
        SearchButton.hide()

        self.UpdateButton = QtWidgets.QPushButton("Update")
        self.UpdateButton.setObjectName("backButton")
        self.UpdateButton.setGeometry(740, 100, 100, 50)
        self.UpdateButton.clicked.connect(self.upDateIp)
        self.UpdateButton.hide()  

        self.scene().addWidget(self.UpdateButton)
        self.scene().addWidget(self.RoomButton)
        self.scene().addWidget(SearchButton)

        getIpButton,self.IpListWidget=self.setup_IpButton()

        getTitle=self.setup_scene((30,30),300,100)
        getTitle.hide()

        self.MatchRoom=[self.RoomButton,getIpButton,self.backButton,getTitle,self.UpdateButton,SearchButton]

    def InitinalCreateRoom(self):

        self.editBox=QtWidgets.QLineEdit()
        self.editBox.setGeometry(340, 300, 400, 100)
        self.editBox.setPlaceholderText("Input server ip address")
        
        self.editBox.setObjectName("CreateEdit")
        self.editBox.hide()

        enter = QtWidgets.QPushButton("Create")
        enter.setObjectName("backButton")
        enter.setGeometry(450, 470, 180, 50)
        enter.clicked.connect(self.startServer)
        enter.hide()  

        BackMatch = QtWidgets.QPushButton("Back")
        BackMatch.setObjectName("backButton")
        BackMatch.setGeometry(240, 600, 100, 50)
        BackMatch.clicked.connect(self.toMatchRoom)
        BackMatch.hide()  

        self.scene().addWidget(self.editBox)
        self.scene().addWidget(enter)
        self.scene().addWidget(BackMatch)

        getTitle=self.setup_scene((30,30),300,100)
        getTitle.hide()
        self.CreateRoom=[enter,self.editBox,getTitle,BackMatch]

    def InitinalSearchRoom(self):
        self.searchBox=QtWidgets.QLineEdit()
        self.searchBox.setGeometry(340, 300, 400, 100)
        self.searchBox.setPlaceholderText("Input server ip address")
        
        self.searchBox.setObjectName("CreateEdit")
        self.searchBox.hide()

        enter = QtWidgets.QPushButton("Search")
        enter.setObjectName("backButton")
        enter.setGeometry(450, 470, 180, 50)
        enter.clicked.connect(self.searchTheServer)
        enter.hide()  

        BackMatch = QtWidgets.QPushButton("Back")
        BackMatch.setObjectName("backButton")
        BackMatch.setGeometry(240, 600, 100, 50)
        BackMatch.clicked.connect(self.toMatchRoom)
        BackMatch.hide()  

        self.scene().addWidget(self.searchBox)
        self.scene().addWidget(enter)
        self.scene().addWidget(BackMatch)

        getTitle=self.setup_scene((30,30),300,100)
        getTitle.hide()
        self.SearchRoom=[enter,self.searchBox,getTitle,BackMatch]

    def InitinalMainRoom(self):
        iconTop=self.initinalTeamBox(self.TeamTopItems,200)
        iconBottom=self.initinalTeamBox(self.TeamBottomItems,500)

        BackMatch = QtWidgets.QPushButton("Back")
        BackMatch.setObjectName("backButton")
        BackMatch.setGeometry(140, 650, 100, 50)
        BackMatch.clicked.connect(self.toMatchRoom)
        BackMatch.hide()  

        self.startGameButton = QtWidgets.QPushButton("Start")
        self.startGameButton.setObjectName("backButton")
        self.startGameButton.setGeometry(540, 380, 100, 50)
        self.startGameButton.clicked.connect(self.startGame)
        self.startGameButton.hide()  

        changeTeam = QtWidgets.QPushButton("Change Team")
        changeTeam.setObjectName("backButton")
        changeTeam.setGeometry(840, 380, 100, 50)
        changeTeam.clicked.connect(self.ChangeTeam)
        changeTeam.hide()  

        self.scene().addWidget(BackMatch)
        self.scene().addWidget(self.startGameButton)
        self.scene().addWidget(changeTeam)

        getTitle=self.setup_scene((30,30),300,100)
        getTitle.hide()
        self.MainRoom=[iconTop,getTitle,iconBottom,BackMatch,self.startGameButton,changeTeam]

    def initinalTeamBox(self,dic,y):# initinal the main room of team
        boxTop=QtWidgets.QListWidget()
        boxTop.setGeometry(140, y, 900, 100)
        boxTop.setFlow(QtWidgets.QListView.LeftToRight)
        boxTop.setObjectName("TeamButton")
        for each in range(6):
            item=QtWidgets.QListWidgetItem(f"Empty_{each}")
            item.setTextAlignment(QtGui.Qt.AlignCenter)
            
            dic[each]=item
            boxTop.addItem(item)
        boxTop.setCurrentRow(2)
        icon=self.scene().addWidget(boxTop)
        icon.hide()
        return icon

    def searchTheServer(self):
        try:
            self.mainClientSwitch[0]=True
            mainClient(self.mainClientSwitch,self.searchBox.text(),self)
            self.startGameButton.hide()
        except:
            self.mainClientSwitch[0]=False
            self.toMatchRoom()

    def setup_scene(self,pos,length=0,hight=0):# initinal the TDOS title
        image=QtGui.QPixmap("photo/hall/title.png")
        if length!=0 and hight!=0:
            image=image.scaled(length,hight,QtGui.Qt.IgnoreAspectRatio)
        icon: QtWidgets.QGraphicsPixmapItem = self.scene().addPixmap(image)
        icon.setZValue(1)
        icon.setPos(*pos)
        return icon

    def initinalImage(self,path,position,size):
        image=QtGui.QPixmap(path)
        image=image.scaled(*size)
        icon: QtWidgets.QGraphicsPixmapItem = self.scene().addPixmap(image)
        icon.setZValue(1)
        icon.setPos(*position)
        icon.hide()
        return icon

    def setup_tutorPageList1(self):
        box=QtWidgets.QListWidget()
        box.setGeometry(140, 200, 100, 500)
        box.setObjectName("TutorButton")
        for each in self.tutorDictPage1:
            item=QtWidgets.QListWidgetItem(each)
            item.setTextAlignment(QtGui.Qt.AlignCenter)
            box.addItem(item)
        box.itemClicked.connect(self.ChangeKey)
        box.setCurrentRow(2)
        icon=self.scene().addWidget(box)
        return icon

    def ChangeKey(self,item):# key event used in tutoral
        for each in self.currentTutor:
            each.hide()
        getLabel=self.Tutorual[2]
        getLabel.setText(self.tutorDictPage1[item.text()])
        self.currentTutor=self.tutorImage[item.text()]
        for each in self.currentTutor:
            each.show()

    def CurrentMethod(self):# this will change to client method and server method
        return

    def ChangeTeam(self):# call CurrentMethod()
        self.CurrentMethod()
        print("ChangeTeam")


    def MainRoomBack(self):#when from main room to match room call this function
        if self.mainClientSwitch[0]:
            self.ClientConnect.sendall("out".encode())
        self.toMatchRoom()

    
    
        
    def setup_button(self):
        box=QtWidgets.QListWidget()
        box.setGeometry(470, 450, 200, 200)
        box.setObjectName("evilButton")
        for each in self.hallButton:
            item=QtWidgets.QListWidgetItem(each)
            item.setTextAlignment(QtGui.Qt.AlignCenter)
            box.addItem(item)
        box.itemClicked.connect(self.itemCheck)
        box.setCurrentRow(2)
        icon=self.scene().addWidget(box)
        return icon

    def tutorLabel(self):# tutoral message
        label=QtWidgets.QLabel(self)
        label.setObjectName("TutorLabel")
        label.setGeometry(340, 100, 800, 650)
        label.setText("Click any button to view the information")

        label.setWordWrap(True)
        label.setAlignment(QtGui.Qt.AlignHCenter | QtGui.Qt.AlignLeft)
        self.scene().addWidget(label)
        return label

    def setup_IpButton(self):# used to show and click the button
        box=QtWidgets.QListWidget()
        box.setGeometry(170, 150, 700, 500)
        box.setObjectName("IpButton")
        for each in self.IpRoom:
            item=QtWidgets.QListWidgetItem(each)
            item.setTextAlignment(QtGui.Qt.AlignCenter)
            box.addItem(item)
        box.itemClicked.connect(self.IpChoose)
        box.setCurrentRow(2)
        icon=self.scene().addWidget(box)
        icon.hide()
        return icon,box
    
    def IpChoose(self,item):#when select ip function will call
        if time.time()-self.IpRoom[item.text()]<=2:
            self.mainClientSwitch[0]=True
            mainClient(self.mainClientSwitch,item.text(),self)
            self.startGameButton.hide()
            
        else:
            self.upDateIp()

    def getKeyTitle(self,text="KEY PRESSED"):
        label=QtWidgets.QLabel(self)
        label.setObjectName("TutorKey")
        label.setGeometry(100, 150, 200, 50)
        label.setText(text)
        self.scene().addWidget(label)
        return label

    def startServer(self):# start the main Server and broadcast
        #self.ClientSwitch[0]=False
        self.ServerSwitch[0]=True
        if self.Server==0 or not(self.Server.is_alive()):
            self.Server=threading.Thread(target=startRoomServer,args=(self.ServerSwitch,self,),daemon = True)
            self.Server.start()
        self.toMainRoom()
    
    def startClient(self):# start to receive broadcast
        self.ServerSwitch[0]=False
        if self.Client==0 or not(self.Client.is_alive()):
            self.Client=threading.Thread(target=startRoomClient,args=(self.ClientSwitch,self.IpRoom,),daemon = True)
            self.Client.start()

    def upDateIp(self):# used to delete to add ip button by detect the broadcast receive
        print(self.IpRoom)
        for each in dict(self.IpRoom):
            getTime=time.time()
            if getTime-self.IpRoom[each]>=2:
                del self.IpRoom[each]
                
        for delete in range(self.IpListWidget.count()):
            self.IpListWidget.takeItem(0)
        
        for add in self.IpRoom:
            item=QtWidgets.QListWidgetItem(add)
            item.setTextAlignment(QtGui.Qt.AlignCenter)
            self.IpListWidget.addItem(item)
        print(self.IpRoom,"end")

    def itemCheck(self,item):# hall button event
        self.hallButton[item.text()]()
    
    def HideCurrent(self):# hide the current page
        for each in self.CurrentCompoents:
            each.hide()
        for image in self.tutorImage:
            for each in self.tutorImage[image]:
                each.hide()

    def ShowCurrent(self):#show the current page
        for each in self.CurrentCompoents:
            each.show()

    """to other page"""
    def toHall(self):
        self.HideCurrent()
        self.ServerSwitch[0]=False
        self.mainClientSwitch[0]=False
        self.CurrentCompoents=self.Hall
        self.ShowCurrent()

    def toTutorial(self):
        self.HideCurrent()
        self.CurrentCompoents=self.Tutorual
        self.ShowCurrent()

    def toMatchRoom(self):
        
        for each in dict(self.IpRoom):# delete all element in this dict
            del self.IpRoom[each]
        self.upDateIp()
        
        self.HideCurrent()
        self.ServerSwitch[0]=False
        self.mainClientSwitch[0]=False
        self.CurrentCompoents=self.MatchRoom
        self.ShowCurrent()

        boardcastRoom(self.TeamTop,"out")
        boardcastRoom(self.TeamBottom,"out")
    
    def toCreateRoom(self):
        self.HideCurrent()
        self.CurrentCompoents=self.CreateRoom
        self.ShowCurrent()
    
    def toMainRoom(self):
        self.HideCurrent()
        self.CurrentCompoents=self.MainRoom
        self.ShowCurrent()
    
    def toSearchRoom(self):
        self.HideCurrent()
        self.CurrentCompoents=self.SearchRoom
        self.ShowCurrent()

    def UpdateRoomMember(self):# update room sit name
        for Top,each in enumerate(self.TeamTop):
            self.TeamTopItems[Top].setText(each)
        for T in range(len(self.TeamTop),5):
            self.TeamTopItems[T].setText(f"Empty_{T}")

        for Bottom,each in enumerate(self.TeamBottom):
            self.TeamBottomItems[Bottom].setText(each)
        for B in range(len(self.TeamBottom),5):
            self.TeamBottomItems[B].setText(f"Empty_{B}")

    def changeTeamClient(self):# change team in client pattern
        self.ClientConnect.sendall("change".encode())

    def changeTeamServer(self):# change team in Server pattern
        if self.ServerIP in self.TeamTop:
            if len(self.TeamBottom)<5:
                self.TeamBottom[self.ServerIP]=self.TeamTop[self.ServerIP]
                del self.TeamTop[self.ServerIP]
        else :
            if len(self.TeamTop)<5:
                self.TeamTop[self.ServerIP]=self.TeamBottom[self.ServerIP]
                del self.TeamBottom[self.ServerIP]
    def startGame(self):
        if not(len(self.TeamTop) and len(self.TeamBottom)):
            return
        prepareColor=colorCreate(self)
        for top in self.TeamTop:
            getInfo=gameGroupEncode(self,top,prepareColor)
            if self.TeamTop[top]==1:
                myInfo=getInfo
            else:
                self.TeamTop[top]['client'].sendall((f"S{getInfo}").encode())
            print(getInfo)
        for bottom in self.TeamBottom:
            getInfo=gameGroupEncode(self,bottom,prepareColor)
            if self.TeamBottom[bottom]==1:
                myInfo=getInfo
            else:
                self.TeamBottom[bottom]['client'].sendall((f"S{getInfo}").encode())
        getDecode=gameGroupDecode(myInfo)
        print(getDecode)
        self.ResultDict=getDecode
        self.hide()

        process=multiprocessing.Process(target=startGame,args=(self.ResultDict,))
        process.start()
        
        checkProcess=threading.Thread(target=self.checkGameIsOver,args=(process,))
        checkProcess.start()
        self.toMatchRoom()
        
    def checkGameIsOver(self,process:multiprocessing.Process):
        while process.is_alive():
            time.sleep(0.5)
        self.show()
        


    
        



"""functions"""
def readQssFile():# read qss(css) file
    with open("QTStyle/SeparateTable.qss",'r') as file:
        get=file.read()
    return get

def readDefineFile():# read the tutorial message
    dic={}
    with open("QTStyle/tutorKeyDefine.txt",'r') as file:
        get=file.read()
    for each in get.split("\n"):
        key,content=each.split("#")
        dic[key]=content
    return dic

def pingIp(ip,dic=0):# ping the ip
    hostname = ip
    response = os.system("ping -c 1  -t 1 " + hostname)
    os.system("clear")
    if response == 0:
        getBool=True
    else:
        getBool=False
    if dic==0:
        return getBool
    else:
        dic[ip]=getBool

def ListEncode(listTop:dict,listBottom:dict)->str:# ip_ip|ip_ip
    getStr="_".join(listTop)+'|'+"_".join(listBottom)
    return getStr

def gameGroupEncode(self:MyWidget,clientIP:str,eachColors:dict):
    """
    level1:'|'
        level2:'?'
            level3:'@'
    Myself
        (ip)
        (color)
    Server
        (ip)
    Myteams
        each people
            (ip)
            (color)
    Oppoteams
        each people
            (ip)
            (color)
    """
    Server=""
    Myself=f"{clientIP}?{eachColors[clientIP]}"
    MyTeams=[]
    OppoTeams=[]
    if clientIP in self.TeamTop:
        myTeam,oppoTeam=self.TeamTop,self.TeamBottom
    else: 
        myTeam,oppoTeam=self.TeamBottom,self.TeamTop
    
    for mate in myTeam:
        if myTeam[mate]==1:
            Server=mate
        if mate!=clientIP:
            MyTeams.append(f"{mate}@{eachColors[mate]}")

    for oppo in oppoTeam:
        if oppoTeam[oppo]==1:
            Server=oppo
        if oppo!=clientIP:
            OppoTeams.append(f"{oppo}@{eachColors[oppo]}")

    myselfStr,oppoStr="?".join(MyTeams),"?".join(OppoTeams)
    return f"{Myself}|{Server}|{myselfStr}|{oppoStr}"

def teamDecode(string:str)->dict:# decode each team(Myteams,Oppoteams)
    result={}
    if string:
        for mate in string.split("?"):
            colorDict={}
            ip,colors=mate.split("@")
            colorDict["ColorBody"],colorDict["ColorSide"]=[color.split('.') for color in colors.split('_')]
            result[ip]=colorDict
    return result

def gameGroupDecode(encoded:str)->dict:
    """
    Myself:{IP:...,ColorBody:[],ColorSide:[]},
    Server:{IP:...}
    Myteams,Oppoteams:{
        (ip):{ColorBody:[],ColorSide:[]},
        (ip):{ColorBody:[],ColorSide:[]},
    }
    """
    result={}
    
    fourTypes=encoded.split("|")
    myIP,myColor=fourTypes[0].split('?')
    mySelf={'IP':myIP}
    mySelf["ColorBody"],mySelf["ColorSide"]=[color.split('.') for color in myColor.split('_')]
    
    server={"IP":fourTypes[1]}
    teamMates=teamDecode(fourTypes[2])
    teamOppos=teamDecode(fourTypes[3])

    result={
        'Myself':mySelf,
        'Server':server,
        'Myteams':teamMates,
        'Oppoteams':teamOppos
    }

    return result

    
def colorCreate(self:MyWidget):
    # body_side
    AllColor=[[['128', '165', '242'],['56', '86', '244']],#blue
    [['231', '50', '35'],['127', '38', '53']],#red
    [['76','153','98'],['57','124','70']],#green
    [['200','177','207'],['178','155','188']],#purple
    [['231','105','190'],['196','74','150']],#pink
    [['245','195','75'],['146','96','40']],#yellow
    [['192','192','192'],['128','138','135']],#gray
    [['138','43','226'],['106','90','205']],# purple blue
    [['0','255','255'],['0','139','139']]#cyan
    ]
    colors=["_".join(".".join(color) for color in each) for each in AllColor]
    
    IPColor={}

    for top in self.TeamTop:
        index=random.randint(0,len(colors)-1)
        IPColor[top]=colors[index]
        colors.pop(index)
    for bottom in self.TeamBottom:
        index=random.randint(0,len(colors)-1)
        IPColor[bottom]=colors[index]
        colors.pop(index)
    return IPColor

def StrDecode(string:str,self):# decode string to top and down dict (used in client)
    self.TeamTop,self.TeamBottom={},{}
    top,bottom=string.split("|")
    for eachTop in top.split("_"):
        if eachTop:
            self.TeamTop[eachTop]=1
    for eachBottom in bottom.split("_"):
        if eachBottom:
            self.TeamBottom[eachBottom]=1

def Server_update(self:MyWidget,CliIp):# update the time
    if CliIp in self.TeamTop:
        self.TeamTop[CliIp]['time']=time.time()
    elif CliIp in self.TeamBottom:
        self.TeamBottom[CliIp]['time']=time.time()

def Server_change(self:MyWidget,CliIp):
    if CliIp in self.TeamTop:
        if len(self.TeamBottom)<5:
            self.TeamBottom[CliIp]=self.TeamTop[CliIp]
            del self.TeamTop[CliIp]
    else :
        if len(self.TeamTop)<5:
            self.TeamTop[CliIp]=self.TeamBottom[CliIp]
            del self.TeamBottom[CliIp]

def Server_out(self:MyWidget,CliIp):
    if CliIp in self.TeamTop:
        currentTeam=self.TeamTop 
    elif CliIp in self.TeamBottom:
        currentTeam=self.TeamBottom
    else:
        return 
    currentTeam[CliIp]['client'].close()
    del currentTeam[CliIp]


def ServerReceive(RUN,conn,self,clientIp):# process data received from client
    """
    update: to check whether client appear
    change: to change the team
    out : out the room
    """
    dicServer={"update":Server_update,"change":Server_change,"out":Server_out}
    
    while RUN[0]:
        try:
            receive=conn.recv(1024).decode()
            dicServer[receive](self,clientIp)
            print(receive)
        except:
            print("error 76")
            break
        
def boardcastRoom(team,text):# send text to all player
    for Ip in dict(team):
        if team[Ip]!=1:
            try:
                team[Ip]['client'].sendall(text.encode())
            except:
                print(Ip,"error 86 send",text)
            

def checkTimeout(team):# check whether client send update
    getTime=time.time()
    for Ip in dict(team):
        if team[Ip]!=1 and getTime-team[Ip]['time']>=2:
            try:
                print(getTime-team[Ip]['time'],"timeput")
                team[Ip]['client'].sendall("out".encode())
            except:
                print(f"fail too send to{Ip}")
            team[Ip]['client'].close()
            del team[Ip]
            

def autoUpdateServer(RUN,self:MyWidget):#check whether people appear and uodate room
    while RUN[0]:
        
        try:
            checkTimeout(self.TeamTop)
            checkTimeout(self.TeamBottom)
            
            boardcastRoom(self.TeamTop,f"!{ListEncode(self.TeamTop,self.TeamBottom)}")
            boardcastRoom(self.TeamBottom,f"!{ListEncode(self.TeamTop,self.TeamBottom)}")
        except:
            print("error 489")
        self.UpdateRoomMember()
        time.sleep(0.8)

def autoUpdateClient(RUN,client,self:MyWidget):# to talk to server that the client is alive
    while RUN[0]:
        try:
            client.sendall("update".encode())
            self.UpdateRoomMember()
        except:
            print("error 97")
            
            break
        
        time.sleep(0.8)
    
    self.toMatchRoom()
    client.close()

def mainServer(RUN,ip,self:MyWidget):# used to response the client (out , start , ! position ) 
    
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, 1145))
    server.listen(10)
    print(ip)
    
    while RUN[0]:
        conn,addr=server.accept()
        print("acc")
        # if len(self.TeamTop)>=5 and len(self.TeamBottom)>=5:
        #     conn.sendall("out".encode())
        # else:
        if len(self.TeamTop)<=4:
            self.TeamTop[addr[0]]={"client":conn,"time":time.time()}
        else:
            self.TeamBottom[addr[0]]={"client":conn,"time":time.time()}

        conn.sendall(ListEncode(self.TeamTop,self.TeamBottom).encode())
        receive=threading.Thread(target=ServerReceive,args=(RUN,conn,self,addr[0],))
        
        receive.start()
            

def mainClient(RUN,ip,self:MyWidget):# initinal client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("connect",ip)
    client.connect((ip, 1145))
    #print('success')
    self.CurrentMethod=self.changeTeamClient

    getPlayer=client.recv(1024).decode()# !:accept and send player ,out : refuse
    print(getPlayer)
    if getPlayer!="out":
        StrDecode(getPlayer,self)
        self.ClientConnect=client
        self.toMainRoom()
        thr=threading.Thread(target=ClientReceive,args=(RUN,client,self))
        thr.start()
        autoUpdate=threading.Thread(target=autoUpdateClient,args=(RUN,client,self))
        autoUpdate.start()

def Client_out(self:MyWidget):
    self.toMatchRoom()


def ClientReceive(RUN,client,self:MyWidget):
    """
    out : out the Room
    S (information): start the game
    !(position): all people's ip in different teams
    """
    dicClient={"out":Client_out}
    
    while RUN[0]:
        try:
            get=client.recv(1024).decode()
            print(get)
            if get[0]=='!':
                StrDecode(get[1:],self)
            elif get[0]=='S':
                self.ResultDict=gameGroupDecode(get[1:])
                self.hide()
                process=multiprocessing.Process(target=startGame,args=(self.ResultDict,))
                process.start()
                
                checkProcess=threading.Thread(target=self.checkGameIsOver,args=(process,))
                checkProcess.start()

                self.toMatchRoom()
                print("close")
                break
            else:
                dicClient[get](self)
        except:
            print("error 160")
            break

def startRoomServer(RUN,self:MyWidget):# broadcast Server
    

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    getIp=self.editBox.text()

    if len(getIp.split("."))!=4 or not(pingIp(getIp)):# check ip is valid
        getIp = socket.gethostbyname(socket.gethostname())

    
    IP=getIp[:getIp.rindex('.')]+'.255'

    if self.ServerMainRoom==0 or not(self.ServerMainRoom.is_alive()):
        self.ServerMainRoom=threading.Thread(target=mainServer,args=(RUN,getIp,self,))
        self.ServerMainRoom.start()
    
    if self.autoUpdateServerThread==0 or not(self.autoUpdateServerThread.is_alive()):
        self.autoUpdateServerThread=threading.Thread(target=autoUpdateServer,args=(RUN,self,))
        self.autoUpdateServerThread.start()

    self.TeamTop,self.TeamBottom={getIp:1},{}# initinal variable
    self.UpdateRoomMember()
    self.ServerIP=getIp
    self.CurrentMethod=self.changeTeamServer

    while RUN[0]:
        sock.sendto('ServerIP'.encode(), (IP, 723))
        time.sleep(0.6)
        

def startRoomClient(RUN,cache:dict):# receive broadcast Client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 723))
    selfIp=socket.gethostbyname(socket.gethostname())
    while RUN[0]:
        data, addr = sock.recvfrom(1024)
        if data.decode() == 'ServerIP' and addr[0]!=selfIp:
            cache[addr[0]]=time.time()
        #time.sleep(0.6)
        
if __name__ == '__main__':
    app =QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(readQssFile())
    demo =MyWidget()
    

    demo.show()
    app.exec()
    #print("over")
    
    demo.ServerSwitch[0]=False
    demo.ClientSwitch[0]=False
    demo.mainClientSwitch[0]=False

    
    sys.exit()
    