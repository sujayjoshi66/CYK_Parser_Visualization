############################################################################
NON_TERMINALS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TERMINALS = 'abcdefghijklmnopqrstuvwxyz'
############################################################################
import pygame 
import random 
import time
import tkinter as tk
from tkinter import messagebox
pygame.font.init()
char_font = pygame.font.SysFont("comicsans", 20)
main_font = pygame.font.SysFont("comicsans", 80)
conclusion_font = pygame.font.SysFont("comicsans", 40)
 
# Total window 
win = pygame.display.set_mode((900, 700))

#Color Initialization
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)

# Title
pygame.display.set_caption("CYK PARSING VISUALISER")
win.fill(WHITE)


##############################################################################################################################################
##############################################################################################################################################
class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.cleaned_grammar=[]
        
    def clean(self):    
        for rule in self.grammar:
            rule = list(rule)
            if rule[0] in TERMINALS:
                print('Invalid')
                return False

            i=0
            while i<len(rule):
                if rule[i]=='-' and rule[i+1]=='>':
                    rule[i] = rule[i]+rule[i+1]
                    rule.pop(i+1)
                    i+=1
                elif rule[i] in TERMINALS and i<(len(rule)-1):
                    if rule[i+1]!='|' and rule[i-1]!='|':
                        print('Invalid Grammar')
                        return False
                    i+=1
                elif rule[i] in NON_TERMINALS and i<(len(rule)-1):
                    if rule[i+1] in NON_TERMINALS:
                        rule[i] = rule[i]+rule[i+1]
                        rule.pop(i+1)
                        i+=1
                    i+=1
                else:
                    i+=1  
            self.cleaned_grammar.append(rule)

    def find_non_terminals(self, input_str, i, j, blocks):
        #computing thenon-terminal values in the 0'th row directly 
        s=blocks[i][j]
        s.draw(70, 60, GREEN)
        if i==0:
            terminal = input_str[j]
            for rule in self.cleaned_grammar:
                if terminal in rule:
                    s.derivatives.append(rule[0])      
            return s.derivatives
        elif i>0:
            s.derivatives.clear()
            return self.find_non_terminals_util(i,j,blocks)
        
    #helper function to calculate the values in the lower rows by taking into consideration the values from upper row blocks   
    def find_non_terminals_util(self, i, j, blocks):
        s=blocks[i][j]
        start=0
        j_new = j
        i_new = i
        #print(i,j)
        while start<i:
            obj1 = blocks[start][j]
            obj2 = blocks[i_new-1][j_new+1]
           #print((str(i), str(j), '         length of obj1 ' ,str(len(obj1.derivatives)), '  length of obj2: ', str(len(obj2.derivatives))))
            for x in range(0, len(obj1.derivatives)):
                for y in range(0, len(obj2.derivatives)):
                    non_terminal_pair = obj1.derivatives[x] + obj2.derivatives[y]
                    self.parse(non_terminal_pair,s)
                    y+=1
                x+=1
            j_new+=1
            i_new-=1
            start+=1
        return s.derivatives    

    def parse(self, non_terminal_pair,s):
        for rule in self.cleaned_grammar:
            if non_terminal_pair in rule:
                creator = rule[0]
                s.derivatives.append(creator)
            continue
        return s.derivatives

    #function to check if the first_non terminal is present in the last block
    #returns true if present else returns false
    def is_derivable(self, creators):
        if self.grammar[0][0] in creators:
            return True
        return False
        
        
              
    def print_cleaned_grammar(self):
        for n in self.cleaned_grammar:
            print(n)            
##############################################################################################################################################
##############################################################################################################################################
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.derivatives=[]   #creating a list associated to every block object

    #method to draw a block at desired co-ordinates and color    
    def draw(self, l, b, color):
        empty_rect = pygame.Rect(self.x, self.y, l, b)
        pygame.draw.rect(win, color, empty_rect, 3)
        pygame.display.update()

    #write the values to the pygame window in their respective blocks 
    def fill_table(self, creators, count):
        x = self.x
        y = self.y
        if not len(creators):
            character = char_font.render('NONE', 1, BLACK)
            win.blit(character, (x+10,y+20))
            return
        else:
            x+=5
            y+=5
            for non_terminal in creators:
                character = char_font.render((non_terminal), 1, BLACK)
                if count<=3:
                    win.blit(character, (x,y))
                    count+=1
                elif count>3:
                    x=self.x+5
                    y=self.y+20
                    win.blit(character, (x,y))
                    count=1
                pygame.display.update()
                x+=15    
        return

#used to removes duplicatenon terminals from the array
def create_unique(arr):
    creators = set()
    for non_terminal in arr:
        creators.add(non_terminal)
    return creators


#for placing characters horizontally above the lookup table
def place_characters(input_str, x, y):
    input_str = list(input_str)
    for char in input_str:
        character = char_font.render(f"{char}",1,BLACK)
        win.blit(character, (x,y))
        pygame.display.update()
        #pygame.time.delay(100)
        x+=70
    place_vertical_characters(input_str, 125, 120)

#for placing characters vertically next to the lookup table    
def place_vertical_characters(input_str, x, y):
    input_str = list(input_str)
    for char in input_str:
        character = char_font.render(f"{char}",1,BLACK)
        win.blit(character, (x,y))
        pygame.display.update()
        #pygame.time.delay(100)
        y+=60

#########################################################
##MAIN FUNCTION
#########################################################
input_str = 'aabbbf'
i=j=0
col_count=0
n=m=len(input_str)
x=150
y=100
run=True
blocks=[[[] for j in range(n)] for i in range(m)]
grammar = ['S->AB',
           'A->BB|a|h',
           'B->AS|b|a',
           'H->FG|a',
          ]
p=Parser(grammar)
p.clean()
#p.print_cleaned_grammar()
title = main_font.render("CYK PARSER VISUALIZATION", 1,(0,0,255))
win.blit(title, (40,10))
place_characters(input_str, 175,75)
while run:
    while i<m:
        col_count=i
        while col_count<n:
            b=Block(x,y)
            b.draw(70,60, BLACK)
            blocks[i][j]=b
            #print('value inserted at '+str(i)+', '+str(j))
            creators = p.find_non_terminals(list(input_str), i, j, blocks) 
            blocks[i][j].derivatives=creators
            unique_creators = create_unique(creators)
            b.fill_table(unique_creators, count=0)
            pygame.time.delay(200)
            b.draw(70, 60, BLACK)
            pygame.time.delay(50)
            x+=70
            j+=1
            col_count+=1
        j=0    
        y+=60
        x=150
        i+=1        
    run=False
    
if p.is_derivable(creators):  #implies string is derivable if value returned is true
    conclusion = conclusion_font.render(('String is derivable from the given grammar') ,1, GREEN)
else:
    conclusion = conclusion_font.render(('String is not derivable from the given grammar') ,1, RED)
win.blit(conclusion, (x+90,((m+1)*60)))
pygame.display.update()
pygame.time.delay(5000)
pygame.quit()
