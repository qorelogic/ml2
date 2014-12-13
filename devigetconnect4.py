# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as n
import pandas as p

def debug(name, var=None, debugLevel=9):
    if debugLevel <= 1:
        if var != None:
            print name+': '+str(var)
        else:
            print name
        
class connectfour:
    def __init__(self):
        print '__init__'
        # initialize who starts the game to a random player, either 1 or player 2
        self.whosTurn = (n.random.randint(0,1000) % 2)+1 # 1 or 2
        self.turn = 0
        self.players = range(1,3) # two players
        self.whoWon = 0
        
        # start the grid
        self.grid = n.array(n.zeros(6*7)).reshape(6,7)
        self.grid = p.DataFrame(self.grid)
        
        self.gridP1 = None
        self.gridP2 = None
        
        self.printGrid('init grid')        
        self.status()
        
    def resetBoard(self):
        print 'resetBoard()'
        self.__init__()
        
    def nextTurn(self):
        debug('nextTurn()')
        # increment the turn counter
        self.turn += 1
        
        # set the next player
        if self.whosTurn == self.players[0]:
            self.whosTurn = self.players[1]
        else:
            self.whosTurn = self.players[0]
        
    def play(self, column):
        if self.whoWon != 0:
            self.sendAlert('game won by player '+str(self.whoWon))
        else:
            try:
                # find the columns first unfilled row..
                indx = n.max(n.nonzero(self.grid.ix[:,column] == 0))
                # ..and fill it with the players id
                self.grid.ix[indx,column] = self.whosTurn
                self.nextTurn()
            except: # an exception is thrown if the column is filled
                self.sendAlert('Column '+str(column)+' is already filled, please select another column.')
                
            # player 1's filled slots
            self.gridP1 = n.array(self.grid.ix[:,:] == 1, dtype=int)
            # player 2's filled slots
            self.gridP2 = n.array(self.grid.ix[:,:] == 2, dtype=int)
            
            connectX = 4
            if self.sense(n.array(self.gridP1), 1, connectX):
                self.whoWon = 1
                
            if self.sense(n.array(self.gridP2), 1, connectX):
                self.whoWon = 2
            
            self.printGrid('play - column:'+str(column))
            self.status()
            
    def playRandom(self):
        self.play((n.random.randint(0,1000) % 6)+1)        
        
    def tautology(self, a):
        if len(n.array(n.nonzero(a == 0))[0]) == 0:
            return True
        else:
            return False
    
    def sense(self, r, number, howManyInARow):
        debug('sense()')
        #print self.grid
        r = (r == number)
        r = n.array(r, dtype=int)
        #print r
        #print
                
        rT = r.transpose()
        #print rT
        #print
            
        def senseMat(r, howManyInARow):
            for i in range(0,len(r)):
                #print r[i]
                for j in range(0,len(r[i])):
                    s = r[i][j:j+howManyInARow]
                    if len(s) == howManyInARow:
                        debug(str(howManyInARow)+' in a row '+ str(s) + ' ' + str(self.tautology(s)))
                        if self.tautology(s):
                            return True
                        
            #print
            
        def senseMatDiag(r, howManyInARow):
            for i in range(-(n.size(r,0) - 1), n.size(r, 1)):
                a =  n.diag(r,i)
                #print a
                #print len(a)
                for j in range(0,len(a)):
                    s = a[j:j+howManyInARow]
                    if len(s) == howManyInARow:
                        debug(str(howManyInARow)+' in a row '+ str(s) + ' ' + str(self.tautology(s)))
                        if self.tautology(s):
                            return True
            #print            
        
        # horizontals
        debug('sense horz')
        if senseMat(r, howManyInARow):
            return True
        # verticlas
        debug('sense verts')
        if senseMat(rT, howManyInARow):
            return True
        
        # diagonals
        debug('sense diags')
        if senseMatDiag(r, howManyInARow):
            return True
            
        debug('sense diags transpose')
        if senseMatDiag(r.transpose(), howManyInARow):
            return True
        
        # if none above return true, then return false
        return False
    
    def sendAlert(sel, msg):
        print msg
     
    def printGrid(self, label):
        print label
        print self.grid
        
        #debug(self.gridP1)
        
        #debug(self.gridP2)
        
    def status(self):
        print '------ status ------'
        debug('turn', self.turn,1)
        debug('players', self.players,1)
        debug('whosTurn', self.whosTurn,1)
        debug('whoWon', self.whoWon,1)
        print '------ end status ------'
        print


"""
c4 = connectfour()
c4.play(4)
c4.play(3)
c4.play(5)
c4.playRandom()
c4.play(3)
c4.resetBoard()
"""
        
"""
c4 = connectfour()
c4.play(2)

# <codecell>

c4.play((n.random.randint(0,1000) % 6)+1)
#c4.__init__()

# <codecell>

c4.play(n.random.randint(0,1000) % 6)

# <codecell>

#players = n.array([1,2])
[1,2]

# <codecell>

a = [3,2,3,4,5,3,7,8,9,10,11,12]
r = p.DataFrame(n.array(a).reshape(3,4))
print r
#r = n.array(r == 3, dtype=int)            
c4.sense(r, 3, 2)

# <codecell>

print r
print -(n.size(r,0) - 1)
print n.size(r,1)

print
for i in range(-(n.size(r,0) - 1), n.size(r, 1)):
    a =  n.diag(r,i)
    print a
    print c4.tautology(a)
"""
