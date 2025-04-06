import sys, random
from PySide6.QtWidgets import QLabel, QPushButton, QToolButton, QFrame, QApplication, QMainWindow, QLineEdit
from PySide6.QtCore import Qt
from PySide6 import QtCore
from PySide6.QtGui import QFont, QFontDatabase, QScreen
import os

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bowling Sim - Baig")
        self.setGeometry(100, 100, 1200, 600)
        self.setCentralWidget(PlayerInputPage(self))

class PlayerInputPage(QFrame):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setStyleSheet('background-color:#150549;')
        self.playerNames = []
        self.count =0
        self.loadcomponents()

    def loadcomponents(self):
        secondFont = os.path.abspath("assets/second.ttf")
        self.protest = QFontDatabase.addApplicationFont(secondFont)
        self.families2 = QFontDatabase.applicationFontFamilies(self.protest)
        thirdFont = os.path.abspath("assets/third.ttf")
        self.sixtyfour = QFontDatabase.addApplicationFont(thirdFont)
        self.families3 = QFontDatabase.applicationFontFamilies(self.sixtyfour)

        self.alleyName = QLabel('Bowling Sim - Baig', self)
        self.alleyName.setGeometry(450, 30, 500, 100)
        self.alleyName.setStyleSheet('font-size: 30px;color:#ff4d00;')
        self.alleyName.setFont(QFont(self.families2[0], 30))

        self.bowler_edit = QLineEdit(self)
        self.bowler_edit.setPlaceholderText("Enter Bowler name")
        self.bowler_edit.setGeometry(100, 140, 300, 45)
        self.bowler_edit.setStyleSheet('font-size:13px;color:#ff4d00;border-radius:10px;background-color:white;')

        self.loadPlayers = QPushButton('Enter Players !', self)
        self.loadPlayers.setGeometry(100, 200, 300, 45)
        self.loadPlayers.setStyleSheet(
            """
            color: #00ecff;
            background-color: #ff22df;
            """
        )
        self.loadPlayers.clicked.connect(self.addPlayers)

        self.bowler_label = QLabel('', self)
        self.bowler_label.setGeometry(450, 140, 200, 200)
        self.bowler_label.setStyleSheet(
            """
            color: #00ecff;
            background-color: #ff22df;
            font-size:16px;
            border-radius:10px;
            """
        )
        self.bowler_label.hide()

        self.error_code = QLabel("Sorry, the Name is too long", self)
        self.error_code.setGeometry(100,320,300,45)
        self.error_code.setStyleSheet(
            """
            color: #00ecff;
            background-color: #ff22df;
            border-radius:10px;
            """
        )
        self.error_code.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_code.hide()

        self.toPage = QPushButton("Let's Play", self)
        self.toPage.setGeometry(100, 260, 300, 45)
        self.toPage.setStyleSheet(
            """
            color: #00ecff;
            background-color: #ff22df;
            border-radius:10px;
            """
        )
        self.toPage.clicked.connect(self.pageSwitch)

    def pageSwitch(self):
        self.window.setCentralWidget(BowlingGame(window, self.playerNames, self.bowler_label.text()))

    def addPlayers(self):
        player_name = self.bowler_edit.text().upper()

        if len(player_name) > 10:
            self.error_code.setText("Sorry, the name is too long")
            self.error_code.show()  # Show the error message label
            self.bowler_edit.clear()
        elif len(self.playerNames) > 9:
            self.error_code.setText("Too many players")
            self.error_code.show()  # Show the error message label
            self.bowler_edit.clear()
        else:
            self.error_code.hide()
            player = Player(player_name)
            self.playerNames.append(player)
            self.bowler_label.setText("\n".join([f"{i + 1}. {player.name}" for i, player in enumerate(self.playerNames)]))
            self.bowler_label.show()
            self.bowler_edit.clear()
class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.frames = [] # 0 - 9
        self.display = None
        self.next_player = 0
        # self.total_score = 0
        self.current_frame = 0
        self.next_throw = 0
        self.strike = False
        self.spare = False
        self.total_score = 0
        self.tenthFrame = False
        self.third_throw = None

    def set_player_display(self, display):
        self.display = display

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.name

    def set_next_player(self, position):
        self.next_player = position

    def bowling(self, y):
        self.x = 230 + 74 * self.current_frame
        self.y = 165
        
        if self.current_frame < 9:
    
            self.player_frame = self.frames[self.current_frame]
            self.previous_frame = self.frames[self.current_frame-1]
            
            if self.player_frame.throws == [] and self.current_frame<10:
                self.throw_one = 10
                self.throw_one = random.randint(0,10)
                self.player_frame.throws.append(self.throw_one)

                if self.throw_one == 10:
                    self.player_frame.is_strike = True
                    self.player_frame.throwsLabel1.setGeometry(self.x, self.y + self.player_frame.tracker * 80, 74, 40)
                    self.player_frame.throwsLabel1.setText(f'X')
                    self.player_frame.throwsLabel2.hide()
                elif self.throw_one == 0:
                    self.player_frame.throwsLabel1.setText(f'-')
                else:
                    self.player_frame.throwsLabel1.setText(f'{self.throw_one}')
                    
            elif len(self.player_frame.throws) == 1 and self.current_frame<9:
                self.throw_two = random.randint(0, 10 - self.throw_one)
                self.total_score += self.throw_one + self.throw_two
                self.frame_score = self.throw_one + self.throw_two

                self.player_frame.throws.append(self.throw_two)
                self.player_frame.throwsLabel2.setText(f'{self.throw_two}')
                
                self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                self.player_frame.nameScore.setText('')
                self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                self.current_frame += 1

                if self.throw_one + self.throw_two == 10 and self.throw_one != 10 and self.current_frame<9:
                    self.player_frame.is_spare = True
                    self.player_frame.throwsLabel1.setText(f'{self.throw_one}')
                    self.player_frame.throwsLabel2.setText(f'/')
                    self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                    self.player_frame.nameScore.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.player_frame.score.setText(f'')
                if self.throw_one == 10:
                    self.player_frame.throwsLabel1.setText(f'X')
                if self.throw_two == 0:
                    self.player_frame.throwsLabel2.setText(f'-')
                if self.throw_one == 0:
                    self.player_frame.throwsLabel1.setText(f'-')
                if self.throw_one +self.throw_two == 10 and self.throw_one !=10:
                    self.player_frame.throwsLabel2.setText(f'/')
                
                if self.current_frame > 0 and self.previous_frame.is_spare == True:
                    self.total_score -=self.throw_two
                    self.previous_frame.score.setText(f'{self.total_score}')
                    self.total_score += self.frame_score
                    self.player_frame.score.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                    self.player_frame.nameScore.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    return self.next_player
                elif self.current_frame > 0 and self.previous_frame.is_strike == True and len(self.player_frame.throws) >1 :
                    # self.total_score += self.frame_score
                    self.previous_frame.score.setText(f'{self.total_score}')
                    self.total_score += self.frame_score

                    self.player_frame.score.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                    self.player_frame.nameScore.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    

                    if self.frames[self.current_frame-3].is_strike == True and self.frames[self.current_frame-2].is_strike == True:
                        print(self.total_score)
                        self.thing = 10-self.throw_one
                        self.total_score-=self.frame_score
                        self.total_score+=self.throw_one
                        self.total_score-=20
                        self.total_score+=self.thing
                        self.frames[self.current_frame-3].score.setText(f'{self.total_score}') 
                        print(self.total_score)
                
                        if self.player_frame.is_spare:
                            self.total_score+=self.frame_score+self.throw_one+self.throw_two
                            
                        else:
                            self.thing = 10-self.throw_one
                            print(self.thing, 'thing')
                            print(self.throw_one, 'throw one')
                            self.total_score+=self.frame_score+self.frame_score
                            self.total_score-=self.throw_two
                            self.total_score+=self.thing
                            print('hola')
                        print(self.current_frame)
                        self.frames[self.current_frame-2].score.setText(f'{self.total_score}')
                        self.total_score+=self.frame_score
                        self.frames[self.current_frame-1].score.setText(f'{self.total_score}')
                        print(self.current_frame)

                        self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                        self.player_frame.nameScore.setText(f'{self.total_score}')
                        self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)       
                    
                else:
                    self.player_frame.score.setStyleSheet('background-color:transparent; border: 1px solid white;color:white;')
                    self.player_frame.score.setText(f'{self.total_score}')
                    self.player_frame.score.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)   
                    self.player_frame.nameScore.setText(f'{self.total_score}')             
                    self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                    self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    return self.next_player
            return self.next_player

# split between tenth frame and all other frames
        if self.current_frame >= 9 and self.current_frame <=10:
            self.player_frame = self.player_frame.frames[9]
            self.previous_frame = self.player_frame.frames[8]
            
            if self.player_frame.throws == []:
                self.throw_one = random.randint(0, 10)
                # self.throw_one = 10
                print(self.throw_one)
                self.player_frame.throws.append(self.throw_one)
            
                if self.throw_one == 10:
                    self.player_frame.is_strike = True
                    self.player_frame.throwsLabel1.setText(f'X')
                    self.total_score += 10
                    self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                    self.player_frame.nameScore.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    return self.next_player
                
                if  self.throw_one == 0:
                    self.player_frame.throwsLabel1.setText(f'-')
                    self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                    self.player_frame.nameScore.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    return self.next_player
                
                if self.throw_one != 10 and self.throw_one != 0:
                    self.total_score += self.throw_one
                    self.player_frame.throwsLabel1.setText(f'{self.throw_one}')
                    self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                    self.player_frame.nameScore.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    return self.next_player
            
            elif self.current_frame >= 9 and len(self.player_frame.throws) == 1 and self.current_frame<=10:
                if self.throw_one == 10:
                    self.throw_two = random.randint(0, 10)
                else:
                    self.throw_two = random.randint(0,10-self.throw_one)
                # self.throw_two =10
                self.player_frame.throws.append(self.throw_two)
                self.total_score += self.throw_two
                self.frames[9].middle.setText(f'{self.throw_two}')
                print(self.throw_one)
                
                if self.throw_two == 10 and self.throw_one == 10:
                    self.frames[9].middle.setText(f'X')
                    
                
                if self.throw_two == 0:
                    self.player_frame.middle.setText(f'-')
                if self.throw_one+self.throw_two == 10 and self.throw_one != 10:
                    self.player_frame.middle.setText(f'/')
                if self.throw_two == 10 and self.throw_one+self.throw_two != 10:
                    self.player_frame.middle.setText(f'X')
                
                self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                self.player_frame.nameScore.setText(f'{self.total_score}')
                self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if self.current_frame >=9 and self.previous_frame.is_strike == True and len(self.player_frame.throws) >=1 :
                    # self.total_score+=self.frame_score
                    
                    self.previous_frame.score.setText(f'{self.total_score}')

                    self.total_score += self.frame_score

                    self.player_frame.score.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                    self.player_frame.nameScore.setText(f'{self.total_score}')
                    self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    if  self.frames[self.current_frame-2].is_strike == True:
                        self.total_score-=30
                      
                        self.total_score+=10
                        self.total_score-=self.throw_two
                        self.frames[self.current_frame-2].score.setText(f'{self.total_score}') 
                        print(self.total_score, 'tenth')
                
                        self.total_score+=self.throw_one+self.frame_score+self.throw_two
                        self.frames[self.current_frame-1].score.setText(f'{self.total_score}')
                        self.total_score+=self.frame_score+self.throw_one
                        self.total_score-=(10-self.throw_two)
                        self.frames[self.current_frame].score.setText(f'{self.total_score}')
                        print(self.current_frame)

                        self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                        self.player_frame.nameScore.setText(f'{self.total_score}')
                        self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  
                        self.current_frame+=1
                        return self.next_player
                    if self.current_frame >=9 and self.previous_frame.is_spare == True :
                        print('YIPEE') # Dont run
                        self.total_score += self.throw_one
                        self.previous_frame.score.setText(f'{self.total_score}')
                        self.total_score += self.frame_score
                        self.player_frame.score.setText(f'{self.total_score}')
                        self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                        self.player_frame.nameScore.setText(f'{self.total_score}')
                        self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        self.current_frame+=1

                        return self.next_player
                


            if (self.throw_one == 10 or self.throw_two == 10) and self.current_frame >=9:# if first throw or second throw is a strike
                print('hello')
                
                if self.throw_two == 10:
                    self.third_throw = random.randint(0,10)
                else:
                    self.third_throw = random.randint(0,10-self.throw_two)                
                print(self.third_throw)
                # self.third_throw = 10
                self.player_frame.throws.append(self.third_throw)
                self.total_score+=self.third_throw
                self.player_frame.throwsLabel2.setText(f'{self.third_throw}')
                self.player_frame.score.setText(f'{self.total_score}')
                self.player_frame.nameScore.setText(f'{self.total_score}')
                if self.third_throw == 10:
                    self.player_frame.throwsLabel2.setText(f'X')
                if self.third_throw == 0:
                    self.player_frame.throwsLabel2.setText(f'-')
                if self.third_throw+self.throw_two == 10 and self.throw_two !=10:
                    self.player_frame.throwsLabel2.setText(f'/')
                if self.frames[self.current_frame-1].is_spare == True:
                    print('monkey')
                    self.total_score-=self.frame_score
                    self.total_score+=self.throw_one
                    self.previous_frame.score.setText(f'{self.total_score}')
                    self.total_score+=self.frame_score
                    self.frames[self.current_frame-1].score.setText(f'{self.total_score}')


                
                if self.frames[self.current_frame-2].is_strike == True and self.frames[self.current_frame-1].is_strike == True:
                    self.total_score-=30
                    self.frames[self.current_frame-2].score.setText(f'{self.total_score}')
                if self.frames[self.current_frame-1].is_strike == True:
                    self.total_score-=30
                    self.total_score+=self.throw_one
                    if self.third_throw == 10:
                        self.total_score+=0
                    else:
                        self.total_score-=self.third_throw
                    print(self.throw_one+self.throw_two, 'self')
                    self.frames[self.current_frame-1].score.setText(f'{self.total_score}')
                    self.total_score+=self.third_throw+self.frame_score
                    self.total_score+=self.throw_one+self.throw_two+self.third_throw
                    print(self.total_score, 'total_score')
                    # self.total_score+=self.frame_score
                    self.frames[self.current_frame-1].score.setText(f'{self.total_score}')
                
                print(self.frame_score, 'strike third throw')
                self.current_frame+=1
                self.current_frame = 11

                return self.next_player
            if self.throw_one +self.throw_two ==10 and self.throw_one != 10 : # accounts for if first two throws are spare
                print('hi')
                if self.throw_two == 10:
                    self.third_throw = random.randint(0,10)
                else:
                    self.third_throw = random.randint(0,10-self.throw_two)
                # self.third_throw = 10
                
                self.player_frame.throws.append(self.third_throw)
                self.total_score+=self.third_throw
                self.player_frame.throwsLabel2.setText(f'{self.third_throw}')
                self.player_frame.score.setText(f'{self.total_score}')
                self.player_frame.nameScore.setText(f'{self.total_score}')
                if self.third_throw == 10:
                    self.player_frame.throwsLabel2.setText(f'X')
                    

                if self.third_throw == 0:
                    self.player_frame.throwsLabel2.setText(f'-')
                if self.third_throw+self.throw_two == 10 and self.throw_two !=10:
                    self.player_frame.throwsLabel2.setText(f'X')
                if self.frames[self.current_frame-1].is_spare == True:
                    print('sier')
                    self.total_score+=self.throw_one
                    self.previous_frame.score.setText(f'{self.total_score}')
                    self.total_score+=self.frame_score
                    self.previous_frame.setText(f'{self.total_score}')
                elif self.frames[self.current_frame-2].is_strike == True:
                    print(self.total_score)
                    # self.total_score-=self.frame_score
                    self.total_score-=self.third_throw-self.frame_score
                    self.total_score+=self.throw_two
                    print(self.throw_one+self.throw_two, 'self')
                    self.frames[self.current_frame-2].score.setText(f'{self.total_score}')
                    self.total_score+=self.frame_score+self.third_throw+self.third_throw
                    
                    print(self.total_score, 'total_score')
                    self.frames[self.current_frame].score.setText(f'{self.total_score}')
                # elif self.frames[self.current_frame-1].is_spare == True:
                #     print(self.total_score)
                #     self.total_score-=self.frame_score
                #     self.total_score-=self.third_throw-self.throw_two
                #     self.frames[self.current_frame-1].score.setText(f'{self.total_score}')
                #     self.total_score+=self.frame_score+self.third_throw+self.third_throw
                #     self.frames[self.current_frame].score.setText(f'{self.total_score}')
                    
              
                print(self.frame_score, 'spare third throw')

                self.current_frame+=1
                self.current_frame = 11
           
                return self.next_player
            # if self.current_frame >=9 and self.previous_frame.is_spare == True and self.third_throw == None and self.current_frame<=9:
            #     print('YIPEE') # Dont run
            #     self.total_score += self.throw_one
            #     self.previous_frame.score.setText(f'{self.total_score}')
            #     self.total_score += self.player_frame.throws[1] + self.player_frame.throws[0]
            #     self.player_frame.score.setText(f'{self.total_score}')
            #     self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
            #     self.player_frame.nameScore.setText(f'{self.total_score}')
            #     self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            #     self.current_frame+=1

            #     return self.next_player
           
            
            else:
                self.player_frame.score.setStyleSheet('background-color:transparent; border: 1px solid white;color:white;')
                self.player_frame.score.setText(f'{self.total_score}')
                self.player_frame.score.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)   
                self.player_frame.nameScore.setText(f'{self.total_score}')             
                self.player_frame.nameScore.setStyleSheet('background-color:#150549; border: 1px solid white;color:white;')
                self.player_frame.nameScore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.current_frame+=1

                return self.next_player
            

            
                    
      
                    
        return self.next_player


            

class Frame(QFrame):
    def __init__(self, display, y, frames, x, tracker,num,players):
        super().__init__(display)
        self.throws = []
        self.frames = frames
        self.is_strike = False
        self.is_spare = False
        self.frame_score = 0
        self.tracker = tracker
        self.players = players
        self.num = num
        self.throwNumb = 0
        self.total_score = 0 
        

            
        self.x = x
        self.y = y+40
        # self.y +=40
        self.setGeometry(self.x, self.y-40, 75, 80)
        secondFont = os.path.abspath("assets/second.ttf")
        self.protest = QFontDatabase.addApplicationFont(secondFont)
        self.families2 = QFontDatabase.applicationFontFamilies(self.protest)
        # self.setGeometry(self.x, self.y-40, 960, 80)
        self.setStyleSheet("background-color: transparent;border: 1px solid white;")
        self.nameScore = QLabel(display)
        self.nameScore.setGeometry(970, self.y-40, 220, 80)
        self.nameScore.setStyleSheet("background-color:transparent;color:white;")
        self.nameScore.setFont(QFont(self.families2[0], 20))
        self.score = QLabel(display)
        self.score.setGeometry(self.x, self.y,75, 40)
        self.score.setStyleSheet("background-color:transparent;border:1px solid white;color:white;")
        self.score.setFont(QFont(self.families2[0], 13))
        self.score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    
            
        self.throwsLabel1 = QLabel( display)
        self.throwsLabel1.setGeometry(self.x,self.y-40, 37.5, 40 )
        self.throwsLabel1.setStyleSheet("background-color:transparent;border:1px solid white;color:white;")
        self.throwsLabel1.setFont(QFont(self.families2[0], 13))
        self.throwsLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.throwsLabel2 = QLabel( display)
        self.throwsLabel2.setGeometry(self.x+37.5,self.y-40, 37.5, 40)
        self.throwsLabel2.setStyleSheet("background-color:transparent;border:1px solid white;color:white;")
        self.throwsLabel2.setFont(QFont(self.families2[0], 13))
        self.throwsLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle = QLabel(display)
        self.middle.setGeometry(895+25,self.y-40,25,40)
        self.middle.setStyleSheet("background-color:transparent;border:1px solid white;color:white;")
        self.middle.setFont(QFont(self.families2[0], 13))
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle.hide()
        self.x+=74
        
        if len(self.throws) == 0:
            self.throwsLabel1.setText('')
            self.throwsLabel2.setText('')
            self.score.setText('')
        if self.num ==9:
            self.throwsLabel1.setGeometry(895, self.y-40, 25, 40)
            self.throwsLabel2.setGeometry(895+50, self.y-40, 25, 40)
            self.middle.show()

   

        
        


        

class PlayerDisplay(QFrame):
    def __init__(self, window, player, y):
        super().__init__(window)
        self.window = window
        self.player = player
      
        thirdFont = os.path.abspath("assets/third.ttf")
        self.sixtyfour = QFontDatabase.addApplicationFont(thirdFont)
        self.families3 = QFontDatabase.applicationFontFamilies(self.sixtyfour)

        self.setGeometry(10, y, 1180, 80)
        self.setStyleSheet('border: 1px solid white;color:white;')
        self.nameBox = QLabel(f'{player.name}', window)
        self.nameBox.setStyleSheet("font-size: 12px; color: white; background-color: transparent;border: 1px solid white;")
        self.nameBox.setGeometry(10, y, 220, 80)
        self.nameBox.setFont(QFont(self.families3[0], 12))





class BowlingGame(QFrame):
    def __init__(self, window, playerNames, bowler_labelText):
        super().__init__()
        self.window = window
        self.players = playerNames
        self.bowler_label = bowler_labelText
        self.x = 225
        self.y = 125
        self.count = 1
        self.current_player = 0
        self.game_over = False
        bowling_body = QFrame(self)
        bowling_body.setGeometry(0, 0, 1200, 1200)
        self.setStyleSheet('background-color:#150549;')
        firstFont = os.path.abspath("assets/Orbitron-Black.ttf")
        self.orbit = QFontDatabase.addApplicationFont(firstFont)
        self.families = QFontDatabase.applicationFontFamilies(self.orbit)
        thirdFont = os.path.abspath("assets/third.ttf")
        self.sixtyfour = QFontDatabase.addApplicationFont(thirdFont)
        self.families3 = QFontDatabase.applicationFontFamilies(self.sixtyfour)

        secondFont = os.path.abspath("assets/second.ttf")
        self.protest = QFontDatabase.addApplicationFont(secondFont)
        self.families2 = QFontDatabase.applicationFontFamilies(self.protest)

        self.alleyName = QLabel('Bowling Sim - Baig', self)
        self.alleyName.setGeometry(450, 30, 500, 100)
        self.alleyName.setStyleSheet('''font-size: 30px;color:#ff4d00;''')
        self.alleyName.setFont(QFont(self.families2[0], 30))
        self.alleyName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for x in range(10):
            self.frames1 = QLabel(str(self.count), self)
            self.frames1.setGeometry(self.x, self.y,75,40 )
            self.frames1.setStyleSheet("font-size:12px;color:white;background-color:#ff4d00;background-color:transparent;border:1px solid white;")
            self.frames1.setFont(QFont(self.families3[0],12))
            self.frames1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.count +=1
            self.x+=75

        self.nameLabel = QLabel('', self)
        self.nameLabel.setGeometry(10, 125, 220, 40)
        self.nameLabel.setStyleSheet("border:1px solid white;")
        self.nameScore = QLabel('',  self)
        self.nameScore.setGeometry(970, 125, 220, 40)
        self.nameScore.setStyleSheet("border:1px solid white;")

        for x in range(len(playerNames)):
            player = playerNames[x]
            self.x = 10
            # self.y = 165 + y_off_set*x
            self.y = 80*x+165
            player.set_player_display(PlayerDisplay(self, player, self.y))
            # Frame(self, self.y, player.frames)

            if x == len(self.players) - 1:
                x = -1
            player.set_next_player(x + 1)
            playerNames[self.current_player].display.setStyleSheet('background-color:red;border-color:1px solid white;')
       
        firstBall = QPushButton('Bowl', self)
        firstBall.setGeometry(self.x, self.y + 90, 1180, 30)
        firstBall.setStyleSheet('font-size:12px;color:white; background-color:#ff4d00;')
        firstBall.setFont(QFont(self.families3[0], 12))
        firstBall.clicked.connect(self.bowl)
        self.y = 165
        tracker = 0
        num = 0
        for player in self.players:
            self.x = 230
            
            for x in range(10):
                    
                player.frames.append(Frame(self, self.y, player.frames, self.x, tracker, num, self.players))
                num+=1
                self.x+=74
                if num ==10:
                    num = 0

                    
                    
               
            tracker+=1
            self.y+=80
        
    def bowl(self):
        # Bowl for the current player
        self.scores = []
        next_player_index = self.players[self.current_player].bowling(self.y)
 # Reset background color for all PlayerDisplay widgets
        for player in self.players:
            player.display.setStyleSheet('border: 1px solid white;')
            # Highlight the PlayerDisplay widget for the next player
            self.players[next_player_index].display.setStyleSheet('background-color:red; border:1px solid white;')
            # Update the current player index
            self.current_player = next_player_index
            # Frame(self.window, self.y, player.frames)
        if len(self.players)>1:
            self.players[self.current_player - 1].display.setStyleSheet('background-color:transparent;border:1px solid white;')
        for player in self.players:
            if player.current_frame >=10:
                self.scores.append(player.total_score)
                
        if len(self.scores) == len(self.players):
            top_score = max(self.scores)
           
            for player in self.players:
                if top_score == player.total_score:
                    player.display.setStyleSheet('background-color:#93b7d5;border:1px solid white;')
                if top_score != player.total_score:
                    player.display.setStyleSheet('border: 1px solid white;')
            # self.game_over = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    geo = window.frameGeometry()
    geo.moveCenter(center)
    window.move(geo.topLeft())
    window.show()
    sys.exit(app.exec())