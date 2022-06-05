import pygame
from AllModels.objectCreate import *
from AllModels.functions import *
from AllModels.socketProcessServer import startSocket, IP
from AllModels.socketProcessClient import startSocketClient
from multiprocessing import Process, Manager



def initinalDict(map,playerDictOppo,playerDictMate,GameInformation):
    
    for oppoPlayers in GameInformation['Oppoteams']:# create oppo player object
        oppo = Opponent(
            map,
            np.array(GameInformation['Oppoteams'][oppoPlayers]['ColorSide'], dtype=np.int32),
            np.array(GameInformation['Oppoteams'][oppoPlayers]['ColorBody'], dtype=np.int32),
        )
        playerDictOppo[oppoPlayers]= oppo
        
    for matePlayers in GameInformation['Myteams']:# create teammate object
        mate=Teammate(
            map,
            np.array(GameInformation['Myteams'][matePlayers]['ColorSide'], dtype=np.int32),
            np.array(GameInformation['Myteams'][matePlayers]['ColorBody'], dtype=np.int32),
        )
        playerDictMate[matePlayers]=mate

def initinalManage(dictAttack,dictInfo,GameInformation):
    for attackOppo in GameInformation['Oppoteams']:# initinalise all manage
        dictAttack[attackOppo]=''
        dictInfo[attackOppo] = ""
    for arrackSelf in GameInformation['Myteams']:
        dictAttack[arrackSelf]=''
        dictInfo[arrackSelf] = ""
    selfIp = GameInformation['Myself']['IP']
    
    dictAttack[selfIp]=''
    dictInfo[selfIp] = ""

    return selfIp# return my Ip

def startGame(GameInformation):
    
    playerDictOppo,playerDictMate={},{}

    manage=Manager()
    attackCache=manage.dict()
    dictInfo = manage.dict()
    dictAttack=manage.dict()


    selfIp=initinalManage(dictAttack,dictInfo,GameInformation)

    if GameInformation['Server']['IP']==selfIp:
        multi = Process(target=startSocket, args=(dictInfo,dictAttack,attackCache,selfIp,))
        print('servef')
    else:
        multi = Process(target=startSocketClient, args=(dictInfo,dictAttack,attackCache,selfIp,GameInformation['Server']['IP'],))
    multi.start()

    pygame.init()# start game
    pygame.display.set_icon(pygame.image.load('photo/game/yuki.png'))
    pygame.display.set_caption('The Day of Sagittarius 3')
    
    screen = pygame.display.set_mode((1160, 800))

    map = MAP(screen)# create map object

    player = MySelf(
        map,
        np.array(GameInformation['Myself']['ColorSide'], dtype=np.int32),
        np.array(GameInformation['Myself']['ColorBody'], dtype=np.int32),
        dictAttack,
        attackCache,
        (GameInformation['Server']['IP'] in GameInformation['Myteams']) or (GameInformation['Server']['IP']==GameInformation['Myself']['IP'])
    )# create my player
    map.player = player
    
    
    
    initinalDict(map,playerDictOppo,playerDictMate,GameInformation)
    map.playerDictOppo = playerDictOppo
    map.playerDictMate = playerDictMate
    
    

    eventProcessor = EventProcessor(map, player, screen, playerDictOppo,playerDictMate)

    dictInfo[selfIp] = str(player)
    

    getCurrentTime = time.time()

    
    playMusic()
    while eventProcessor.RUN:

        if time.time() - getCurrentTime > 0.05:
            
            getCurrentTime = time.time()
            CycleChecks(player, map)  # check each flights's status and process
            CycleUpdate(playerDictOppo,playerDictMate, dictInfo)

            screen.fill((27, 36, 69))  # fill the screen
            gameSurface = pygame.pixelcopy.make_surface(map.showArea().transpose(1, 0, 2))
            
            pictureResize = pygame.transform.scale(gameSurface, (800,800))
            
            screen.blit(pictureResize, (0, 0))  # select the block of map to display
            drawFrames(screen)
            map.showCurrentArea()
            map.showMenu()
            player.refreshAllObject(screen)
            player.showStatus(screen)
            drawMatesPosition(screen,playerDictMate)
            displayTeammate(screen,playerDictMate,map.Mfont.render)

            showFlightsLabel(player,playerDictOppo,playerDictMate,screen)
            #player.showFlightsLabel(screen)
            

            dictInfo[selfIp] = str(player)

            # print(map.Flights)
            for eve in pygame.event.get():  # event check

                eventProcessor.pygameEventDetect(eve, multi)

            if eventProcessor.SCREENLOCATESWITCH:
                pos = pygame.mouse.get_pos()
                
                pos = [
                    int(5000 * (pos[0] - 955) / 195),
                    int(10000 * (pos[1] - 410) / 390),
                ]
                map.position = pos
            eventProcessor.checkCurrntSituation(multi)
            pygame.display.flip()
            
    stopMusic()
    pygame.quit()
    
    multi.close()
    print("over")
    


if __name__ == "__main__":
    startGame({'Myself': {'IP': '192.168.2.20', 'ColorBody': ['76', '153', '98'], 'ColorSide': ['57', '124', '70']}, 'Server': {'IP': '192.168.2.20'}, 'Myteams': {'192.168.2.132': {'ColorBody': ['45', '195', '75'], 'ColorSide': ['146', '96', '40']}}, 'Oppoteams': {'192.168.2.175': {'ColorBody': ['245', '195', '75'], 'ColorSide': ['146', '96', '40']}}})
