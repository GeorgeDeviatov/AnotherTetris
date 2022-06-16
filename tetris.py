###########TetrisRound2###########
import random
import pygame as pg
import copy
pg.init()


class App:
    def __init__(self,environment):
        self.clock = pg.time.Clock()
        self.environment = environment


    
    def set_draw(self):# Very bad realization/
        #Not so bad as I thought but anyway
        self.screen = pg.display.set_mode((1200,800))
        clock = pg.time.Clock()
        clicked = False
        end = False
        que = 0
        questions = [["Width",1200,'1200'],
                     ["Height",800,'800'],["FPS",30,'30'],["Step time",160,'160'],['Aceleration',1,'1']]
        
        x,y = 20,20
        for apply in questions:
            apply.append(((x+120,y),(x+120,y+20),(x+170,y+20),(x+170,y)))
            apply.append([[x+120,y],[x+170,y+20]])
            if x + 200 < 1000:
                x += 400
            else:
                y += 100
                x = 20
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if pg.key.name(event.key) == 'return':
                        end = True
                        break
                    if pg.key.name(event.key) == 'backspace':
                        if clicked:
                            questions[que][2] = questions[que][2][0:len(questions[que][2])-1]
                    else:
                        if clicked:
                            questions[que][2] += pg.key.name(event.key)
                        
                elif event.type == pg.MOUSEBUTTONDOWN:
                    que = 0
                    for q in questions:
                        clicked = False
                        if ( event.pos[0] > q[4][0][0] and event.pos[1] > q[4][0][1] ) and (event.pos[0] < q[4][1][0] and event.pos[1] < q[4][1][1]):
                            clicked = True
                            break
                        
                        que+=1
            
            if end:
                break
                    
            
            y = 20
            x = 20
            for apply in questions:
                self.write(apply[0],(255,0,0),(x,y),170//len(apply[0]))
                pg.draw.polygon(self.screen,(255,255,255),apply[3])
                self.write(apply[2],(0,255,0),(x+200,y),100//(len(apply[2])+1))
                
                if x + 200 < 1000:
                    x += 400
                else:
                    y += 100
                    x = 20
            
            pg.display.flip()
            self.screen.fill((0,0,0))
            clock.tick(30)
            pg.display.set_caption("Settings")
        
        for q in questions:
            try:
                q[2] = int(q[2])
            except:
                q[2] = q[1]
        
        self.width_sc = questions[0][2]
        self.height_sc = questions[1][2]
        self.fps = questions[2][2]
        self.environment.step_time = questions[3][2]
        self.environment.acel = questions[4][2]
        self.width_gm = int((self.width_sc / 3 ) * 2)
        self.height_gm = int((self.height_sc / 3) * 2)
        self.size_x = self.width_gm/self.environment.x
        self.size_y = self.height_gm/self.environment.y
        self.screen = pg.display.set_mode((self.width_sc,self.height_sc))
    
    

    
    def draw_grid(self):
        for x in range(self.environment.x+1):
            pg.draw.line(self.screen,(255,255,255),(self.size_x*x,0),(self.size_x*x,self.height_gm))
        for y in range(self.environment.y+1):
            pg.draw.line(self.screen,(255,255,255),(0,self.size_y*y),(self.width_gm,self.size_y*y))
    
    def draw_field(self):
        for line in range(self.environment.x):
            for column in range(len(self.environment.field[line])):
                if self.environment.field[line][column]:
                    
                    color = self.environment.color_field[line][column]
                elif [line,column] in self.environment.new_fig.coords:
                    color = self.environment.new_fig.color
                else:
                    color = (0,0,0)
                pg.draw.polygon(self.screen,color,((line*self.size_x,column*self.size_y)
                ,((line+1)*self.size_x,column*self.size_y),
                ((line+1)*self.size_x,(column+1)*self.size_y),
                (line*self.size_x,(column+1)*self.size_y)))
    
    def write_end(self,text,color,base_y):
        #pg.draw.line(self.screen,(255,255,255),(600,0),(600,800))
        sz = self.width_sc // len(text)
        f = pg.font.SysFont('corbel',sz)
        font = f.render(text,True,color)
        self.screen.blit(font,(self.width_sc/2 - sz*len(text)/6,base_y))
    
    def write(self,text,color,pos,size):
        f = pg.font.SysFont('c059', size)
        font = f.render(text, True, color)
        self.screen.blit(font,pos)
        
        

    def draw(self):
        prov_time = 0
        begin_time = 0
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if pg.key.name(event.key) == 'return':
                        if self.environment.end_game:
                            self.environment.end_game = False
                            self.environment.spawn()
                    elif pg.key.name(event.key) == 'right':
                        self.environment.move('right')
                    elif pg.key.name(event.key) == 'left':
                        self.environment.move('left')
                    elif pg.key.name(event.key) == 'down':
                        self.environment.move('down')
                    elif pg.key.name(event.key) == 'o':
                        self.environment.rotate('left')
                    elif pg.key.name(event.key) == 'p':
                        self.environment.rotate('right')
                    elif pg.key.name(event.key) == 's':
                        if self.environment.end_game:
                            self.set_draw()
                    elif pg.key.name(event.key) == 'e':
                        if not(self.environment.end_game):
                            self.environment.end_game = True
                            self.environment.score = 0
                            self.environment.clean_all()
                        
            if self.environment.end_game:
                    tx_1 = "Another Tetris"
                    self.write_end(tx_1,(255,0,0),20)
                    
                    tx_2 = "To play press Enter"
                    self.write_end(tx_2,(100,0,100),200)
                    
                    
            else:
                prov_time = pg.time.get_ticks() - begin_time
                if prov_time >= self.environment.step_time:
                    self.environment.update()
                    begin_time = pg.time.get_ticks()
                self.draw_field()
                self.draw_grid()
                
                
                sz_w = (self.width_sc - self.width_gm) / len(str(self.environment.score))
                sz_h = self.height_sc
                if sz_h < sz_w:
                    sz_w = sz_h
                self.write(str(self.environment.score), (0,255,0), (self.width_gm+20,20), int(sz_w))
                
                
                
            
            
            
            
            pg.display.flip()
            self.clock.tick(self.fps)
            pg.display.set_caption("FPS:"+str(int(self.clock.get_fps())))
            self.screen.fill((0,0,0))


class Figure:
    def __init__(self,places):
        self.places = places

class Cube(Figure):
    def __init__(self):
        self.places = [[[0,0],[1,0],[1,1],[0,1]],[[0,0],[1,0],[1,1],[0,1]],[[0,0],[1,0],[1,1],[0,1]],
                       [[0,0],[1,0],[1,1],[0,1]]]
        
        self.place = 0

class Stick(Figure):
    def __init__(self):
        self.places = [[[0,0],[1,0],[2,0],[3,0]],[[1,0],[1,1],[1,2],[1,3]],[[0,0],[1,0],[2,0],[3,0]],
                      [[1,0],[1,1],[1,2],[1,3]]]
        
        self.place = 0

class L_Fig(Figure):
    def __init__(self):
        self.places = [[[0,0],[0,1],[0,2],[1,2]],[[0,1],[0,2],[1,1],[2,1]],[[-1,0],[0,0],[0,1],[0,2]],
                      [[0,2],[1,2],[2,2],[2,1]]]
        
        self.place = 0

class Z_Fig(Figure):
    def __init__(self):
        self.places = [[[0,0],[0,1],[1,1],[1,2]],[[0,1],[1,1],[1,0],[2,0]],[[0,0],[0,1],[1,1],[1,2]],
                      [[0,1],[1,1],[1,0],[2,0]]]
        
        self.place = 0

class Triangle(Figure):
    def __init__(self):
        self.places = [[[0,1],[1,1],[1,0],[2,1]],[[1,0],[1,1],[1,2],[2,1]],[[0,1],[1,1],[2,1],[1,2]],
                       [[1,0],[1,1],[0,1],[1,2]]]
        
        self.place = 0

class Environment:
    def __init__(self,x,y,figures):
        self.x = x
        self.y = y
        self.field = [[False for y in range(self.y)] for x in range(self.x)]
        self.spawned = False
        self.figures = figures
        self.spawn()
        self.end_game = True
        self.score = 0
        self.color_field = [[(0,0,0) for y in range(self.y)] for x in range(self.x)]
    
    def clean_all(self):
        self.field = [[False for y in range(self.y)] for x in range(self.x)]
    
    
    def spawn(self):
        new_fig_cl = random.choice(self.figures)
        
        new_fig = new_fig_cl()
        
        self.new_fig = new_fig
        self.new_fig.color = (random.randint(50,255),random.randint(50,255),random.randint(50,255))
        
        self.new_fig.coords = self.plus( self.new_fig.places[0] , [4,0])
        self.new_fig.pos = [4,0]
        
        if not(self.check(self.new_fig.coords)):
            self.end_game = True
            self.score = 0
            self.clean_all()
        
        self.spawned = True
    
    
    def check(self,coords):
        for coord in coords:
            if coord[0] < self.x  and coord[1] < self.y and coord[0] >= 0 and coord[1] >= 0:
                if self.field[coord[0]][coord[1]]:
                    return False
            else:
                return False
        return True
    
    def plus(self,a_,b_):
        a = copy.deepcopy(a_)
        b = copy.deepcopy(b_)
        for cor in range(len(a)):
            for el in range(len(b)):
                if el < len(a[cor]):
                    
                    a[cor][el] += b[el]
        return a
    
    def fall_lines(self,line):
        for to_fall in range(line-1,0,-1):
            for el in range(self.x):
                self.field[el][to_fall+1] = self.field[el][to_fall]
        
    
    def check_lines(self):
        for line in range(self.y):
            tot = True
            for column_1 in range(self.x):
                if self.field[column_1][line] == False:
                    tot = False
                    break
            if tot:
                self.score += 100
                for column_2 in range(self.x):
                    self.field[column_2][line] = False
                self.fall_lines(line)
                
            
    def update(self):
        if self.spawned:
            plused_coords = self.plus(self.new_fig.coords , [0,1])
            if self.check(plused_coords):
                self.new_fig.coords = plused_coords
                self.new_fig.pos[1] += 1
            else:
                
                for coord in self.new_fig.coords:
                    self.field[coord[0]][coord[1]] = True
                    self.color_field[coord[0]][coord[1]] = self.new_fig.color
                    self.spawned = False
        else:
            self.check_lines()
            self.spawn()
            self.step_time -= self.acel
            
    
    def move(self,direction):
        where = 0
        if direction == 'right':
            where = [1,0]
            xory = 0
        elif direction == 'left':
            where = [-1,0]
            xory = 0
        elif direction == 'down':
            where = [0,1]
            xory = 1
        
        moved_coords = self.plus(self.new_fig.coords, where)
        if self.check(moved_coords):
            self.new_fig.coords = moved_coords
            self.new_fig.pos[xory] += where[xory]

    
    def rotate(self,direction):
        where = 0
        if direction == 'left':
            where = -1
        elif direction == 'right':
            where = 1
        
        if self.new_fig.place + where < 0:
            pl = len(self.new_fig.places) - 1
        elif self.new_fig.place + where >= len(self.new_fig.places):
            pl = 0
        else:
            pl = self.new_fig.place + where
        
        new_coords = self.plus(self.new_fig.places[pl],self.new_fig.pos)
        if self.check(new_coords):
            self.new_fig.coords = new_coords
            self.new_fig.place = pl
        
        
        
        
        
if __name__ == '__main__':

    figures = [Cube,Stick,L_Fig,Z_Fig,Triangle]
    
    
    environment = Environment(10,20,figures)
    app = App(environment)
    app.set_draw()
    app.draw()