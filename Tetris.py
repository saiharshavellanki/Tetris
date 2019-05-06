import pygame
import time
import random
import sys
from pygame.locals import *
pygame.init()

class Declaration:
    global Display_Width
    Display_Width=1000
    global Display_Height
    Display_Height=800
    global White
    White=(255,255,255)
    global Black
    Black=(0,0,0)
    global Green
    Green=(0,155,0)

    pygame.display.set_caption('Tetris')

    global Font
    Font=pygame.font.SysFont(None,30)
    global SmallFont
    SmallFont=pygame.font.SysFont(None,20)


    global Board_Width
    Board_Width=30
    global Board_Height
    Board_Height=32 
    global Display
    Display=pygame.display.set_mode((Display_Width,Display_Height))


    S_Shape =       [[
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    [
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

    Z_Shape =       [[
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    [
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

    I_Shape =         [[
                         '..O..',
                         '..O..',
                         '..O..',
                         '..O..'],
                        [
                         '.....',
                         'OOOO.',
                         '.....',
                         '.....']]

    O_Shape=           [[
                         '.....',
                         '.OO..',
                         '.OO..',
                         '.....']]

    L_Shape =           [[
                         '...O.',
                         '.OOO.',
                         '.....',
                         '.....'],
                        [
                         '..O..',
                         '..O..',
                         '..OO.',
                         '.....'],
                        [
                         '.....',
                         '.OOO.',
                         '.O...',
                         '.....'],
                        [
                         '.OO..',
                         '..O..',
                         '..O..',
                         '.....']]

    global Pieces
    Pieces = {'S': S_Shape,
              'Z': Z_Shape,
            'L': L_Shape,
             'I': I_Shape,
            'O': O_Shape
            }

    global Block_Size
    Block_Size=20

    global TopXPos
    TopXPos = (Display_Width-Block_Size*Board_Width)/2
    global TopYPos
    TopYPos = Display_Height-Block_Size*Board_Width-160

    global Clock
    Clock = pygame.time.Clock()
    global Fps
    Fps=8

class Board(Declaration):
	
    def DrawBoard(self,Board):
        pygame.draw.rect(Display, Green, (TopXPos-3,TopYPos-7, Board_Width*Block_Size+8,Board_Height*Block_Size+8), 5)
        pygame.draw.rect(Display, Black,(TopXPos,TopYPos,Board_Width*Block_Size,Board_Height*Block_Size))
        
        for x in range(Board_Width):
            for y in range(Board_Height):
               self.DrawBox(x, y, Board[x][y],None,None,1)

    def CheckRowEmpty(self,Board,y):
        for x in range(Board_Width):
            if Board[x][y]=='.':
                count+=1
        if count==Board_Width:
            return True
        else:
            return False

    def CheckIsValid(self,Board,Piece,X_Shift,Y_Shift):
    	for x in range(4):
    	    for y in range(4): 
                CheckInside=y+Piece['y']+Y_Shift
                if CheckInside<0 :
                    continue
                if Pieces[Piece['shape']][Piece['rotation']][y][x] == '.':
    	           continue
    	        X= x + Piece['x'] + X_Shift
                Y=y + Piece['y'] + Y_Shift
                if X<0 or X>=Board_Width or Y>=Board_Height :
                    return False
                if Board[X][Y] != '.':
                    return False
    	return True

    def CheckRowFull(self,Board,y):
        count=0
        for x in range(Board_Width):
            if Board[x][y] != '.':
                count+=1
        if count==Board_Width:
            return True
        else:
            return False

    def FillPiecePos(self,Board, Piece):
    	for x in range(4):
    	    for y in range(4):
    	        if Pieces[Piece['shape']][Piece['rotation']][y][x] != '.':
    	            Board[x + Piece['x']][y + Piece['y']]='0'
    	return 


    def RemoveLines(self,Board):
        count = 0
        y = Board_Height-1
        while y >= 0:
            val=self.CheckRowFull(Board,y)
            if val:
                for y in range(Board_Height):
                    for x in range(Board_Width):
                        Board[x][y] = Board[x][y-1]
                for x in range(Board_Width):
                    Board[x][0] = '.'
                count += 1
            else:
                y=y-1
        return count

    

class Block(Declaration):

    def DrawBox(self,Box_X_Pos, Box_Y_Pos,color,x,y,Status):
        if color=='.':
            return
        if Status==1:
            x= TopXPos + (Box_X_Pos) * Block_Size
            y= TopYPos + (Box_Y_Pos) * Block_Size

        pygame.draw.rect(Display, White, (x + 1, y + 1, Block_Size - 1, Block_Size - 1))
        pygame.draw.rect(Display, White, (x + 1, y + 1, Block_Size- 4, Block_Size - 4))

    def Rotate(self,Board,FallingPiece):
        FallingPiece['rotation'] = (FallingPiece['rotation'] + 1) % len(Pieces[FallingPiece['shape']])
        if not self.CheckIsValid(Board,FallingPiece,0,0):
            self.BackRotate(Board,FallingPiece)
        return

    def BackRotate(self,Board,FallingPiece):

        FallingPiece['rotation'] = (FallingPiece['rotation'] - 1) % len(Pieces[FallingPiece['shape']])
        return

    def MoveLeft(self,FallingPiece):
        FallingPiece['x']=FallingPiece['x']-1
        return

    def MoveRight(self,FallingPiece):
        FallingPiece['x']=FallingPiece['x']+1
        return


    def DrawPiece(self,Piece):
        DrawPiece = Pieces[Piece['shape']][Piece['rotation']]
        Pixelx, Pixely =  (TopXPos+ (Piece['x'] * Block_Size)), (TopYPos+ (Piece['y']* Block_Size))
        for x in range(4):
            for y in range(4):
                if DrawPiece[y][x]!='.':
                    self.DrawBox(None,None,White,Pixelx +(x * Block_Size), Pixely + (y * Block_Size),0)

    
class Gamplay(Block,Board,Declaration):

    def SelectPiece(self):
 	Shape = random.choice(list(Pieces.keys()))
 	Piece = {'shape': Shape,
                'rotation': random.randint(0, len(Pieces[Shape]) - 1),
                'x' : 13,
                'y' : -1,
                }
        return Piece
    
    def text_objects(self,text,color):
        textSurface=Font.render(text,True,color)
        return textSurface,textSurface.get_rect()

    def message_to_screen(self,check,msg,color):
        textSurf,textRect=self.text_objects(msg,color)
        if check==1:
            textRect.center=(100,100)
        elif check==2:
            textRect.center=(100,140)

        Display.blit(textSurf,textRect)

    def DisplayScore_Level(self,Score,Level):
        pygame.draw.rect(Display,Black,[42,80,120,70])
        pygame.draw.rect(Display,Black,[100,140,70,70])
        self.message_to_screen(1,'Score : '+str(Score),White)
        self.message_to_screen(2,'Level : '+str(Level),White)


    def UpdateScore(self,Score,value):
        Score+=int(value)
        return Score

    def CheckForKeyUp(self,event,MoveLeft,MoveRight):
        if event.type==KEYUP and event.key==K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type==KEYUP:
            if event.key==K_d :
                MoveRight=False
            elif event.key==K_a:
                MoveLeft=False
        return MoveLeft,MoveRight

    def CheckForKeyDown(self,Board,FallingPiece,event,MoveLeft,MoveRight):
        if event.type==KEYDOWN :
            if event.key==K_d and self.CheckIsValid(Board, FallingPiece,1,0):
             	FallingPiece['x']=FallingPiece['x']+1
             	MoveRight=True
             	MoveLeft=False

            elif event.key==K_a and self.CheckIsValid(Board,FallingPiece,-1,0):
                FallingPiece['x']=FallingPiece['x']-1
                MoveLeft=True
                MoveRight=False

            elif event.key==K_w:
             	self.Rotate(Board,FallingPiece)

            elif event.key==K_SPACE:
             	MoveRight=False
             	MoveLeft=False

                for i in range(1, 20):
                    if not self.CheckIsValid(Board, FallingPiece,0,i):
                        break
                    FallingPiece['y'] = FallingPiece['y']+i-1
        return MoveLeft,MoveRight

    def StartGame(self):
        global Fps
     	Board=[['.' for x in range(Board_Height)]for y in range(Board_Width)]    	

    	MoveRight = False
    	MoveLeft = False
       
    	Score = 0
        Level=1
        GameRun=True
        FallingPiece = self.SelectPiece()
     	while GameRun:
            if FallingPiece== None :
                FallingPiece=self.SelectPiece()
                if not self.CheckIsValid(Board,FallingPiece,0,0):
                    GameRun=False
                    return

            for event in pygame.event.get(QUIT):
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                MoveLeft,MoveRight = self.CheckForKeyUp(event,MoveLeft,MoveRight)

                MoveLeft,MoveRight = self.CheckForKeyDown(Board,FallingPiece,event,MoveLeft,MoveRight)

            	if MoveRight and self.CheckIsValid(Board,FallingPiece,1,0):
                    self.MoveRight(FallingPiece)

            	elif MoveLeft and self.CheckIsValid(Board,FallingPiece,-1,0):
            	    self.MoveLeft(FallingPiece)

            if  self.CheckIsValid(Board, FallingPiece,0,1):
                FallingPiece['y']=FallingPiece['y']+1
            else:
                self.FillPiecePos(Board, FallingPiece)
                no_of_rows_del=self.RemoveLines(Board)
                self.Updatescore=(Score,no_of_rows_del)
                if no_of_rows_del > 0:
                    Score=self.UpdateScore(Score,100*no_of_rows_del)
                else:
                    Score=self.UpdateScore(Score,10)
                Level=int(Score/100)+1
                Fps=Fps+0.5*(Level-1)
                FallingPiece = None
            
            self.DrawBoard(Board)
            self.DisplayScore_Level(Score, Level)
            if FallingPiece != None:
                self.DrawPiece(FallingPiece)
            pygame.display.update()
            Clock.tick(Fps)

ob=Gamplay()
ob.StartGame()
