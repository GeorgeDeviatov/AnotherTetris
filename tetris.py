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
        questions = [["Width_pixels",1200,'1200'],
                     ["Height_pixels",800,'800'],['Width_cells',10,'10'],['Height_cells',20,'20'],["FPS",30,'30'],["Step time",160,'160'],['Aceleration',1,'1'],
                     ["Pack",0,'0']]
        
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
            self.write('Press Enter to play',(255,0,0),(20,400),50)
            self.write('Press p to go to pack menu',(255,0,0),(20,500),50)
            self.write('Press g to read guide',(255,0,0),(20,600),50)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    name = pg.key.name(event.key)
                    if name == 'return':
                        end = True
                        break
                    elif name == 'backspace':
                        if clicked:
                            questions[que][2] = questions[que][2][0:len(questions[que][2])-1]
                    elif name == 'p':
                        self.fig_menu()
                    elif name == 'g':
                        self.guide()
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
        self.environment.init_field(questions[2][2],questions[3][2])
        self.fps = questions[4][2]
        self.environment.step_time = questions[5][2]
        self.environment.acel = questions[6][2]
        self.environment.pack = questions[7][2]
        self.width_gm = int((self.width_sc / 3 ) * 2)
        self.height_gm = int((self.height_sc / 3) * 2)
        self.size_x = self.width_gm/self.environment.x
        self.size_y = self.height_gm/self.environment.y
        self.screen = pg.display.set_mode((self.width_sc,self.height_sc))
        self.environment.figures = self.environment.packs[self.environment.pack]
        self.draw()
    
    

    
    def draw_grid(self):
        for x in range(self.environment.x+1):
            pg.draw.line(self.screen,(255,255,255),(self.size_x*x,0),(self.size_x*x,self.height_gm))
        for y in range(self.environment.y+1):
            pg.draw.line(self.screen,(255,255,255),(0,self.size_y*y),(self.width_gm,self.size_y*y))
    
    
    def check_coord(self,to_check_1,to_check_2):
        return to_check_1[0] > to_check_2[0][0] and to_check_1[1] > to_check_2[0][1] and to_check_1[0] < to_check_2[2][0] and to_check_1[1] < to_check_2[2][1]
    
    
    
    

    def load_fig(self):
        f = open('figures.txt','w')#standard, not standart
        f.seek(0)
        f.write('Standard {} \n'.format(str(self.environment.stand_figs)))
        for figure in self.environment.all_figures:
            name = "N" + figure.name + '\n'
            f.write(name)
            max_y = figure.places[0][0][1]
            max_x = 0
            
            pos = 0
            
            for ps in figure.places:
                m = max(ps,key = lambda x:x[1])
                if max_y < m[1]:
                    max_y = m[1]
            for y in range(max_y+1):
                line = ''
                for pos in range(len(figure.places)):
                    max_x = max(figure.places[pos])[0]
                    for x in range(max_x+1):
                        if [x,y] in figure.places[pos]:
                            line += '1'
                        else:
                            line += '0'
                    line += 'x'
                line = line[0:len(line)-1]
                line += '\n'
                f.write(line)
        f.close()
                    
    
    def reload_image(self,now):
        image = pg.image.load('GuidePage{}.png'.format(str(now)))
        image = pg.transform.scale(image,(1200,800))
        rect = image.get_rect()
        return image,rect
    
    def guide(self):
        width,height = 1200,800
        self.screen = pg.display.set_mode((width,height))
        clock = pg.time.Clock()
        now = 0
        maximum = 2
        br = False#brrrrrrrrr
        
        try:
            image,rect = self.reload_image(now)
            
            
            while True:
                self.screen.blit(image,rect)
                
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                    elif event.type == pg.KEYDOWN:
                        name = pg.key.name(event.key)
                        if name == 'd' or name == 'right':
                            if now < maximum -1:
                                now+=1
                                image,rect = self.reload_image(now)
                                rect = image.get_rect()
                        elif name == 'a' or name == 'left':
                            if now > 0:
                                now -= 1
                                image,rect = self.reload_image(now)
                        elif name == 'return':
                            br = True
                            break
                
                if br:
                    break
                pg.display.flip()
                self.screen.fill((0,0,0))
                clock.tick(30)
                pg.display.set_caption('Guide')
        
        except:
            while True:
                self.write('For guide you have to download some images',(255,0,0),(20,20),50)
                self.write('But if you dont need in guide you can dont do it', (255,0,0), (20,400),50)
                self.write('Press Enter to return',(255,0,0),(0,500),40)
                
                br = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                    elif event.type == pg.KEYDOWN:
                        name = pg.key.name(event.key)
                        if name == 'return':
                            br = True
                            break
                    
                if br:break 
                pg.display.flip()
                self.screen.fill((0,0,0))
                clock.tick(30)
                pg.display.set_caption('Guide(no images)')  



                      
                
    def make_fig_menu(self,make_new_fig,cur_fig=0):        
            
        width,height = 1200,800
        self.screen = pg.display.set_mode((width,height))
        
        field_beg_y = 120
        side_b = 100
        dist = 10
        
        cur_pos = 0
        add_but = [[dist,dist],[side_b+dist,dist],[side_b+dist,side_b+dist],[dist,side_b+dist]]
        del_but = [[side_b*3+dist*4,dist],[side_b*4+dist*4,dist],[side_b*4+dist*4,side_b+dist],
                      [side_b*3+dist*4,side_b+dist]]
        
        lef_but = [[side_b*2+dist*2,dist],[side_b*2+dist*2,side_b+dist],[side_b+dist*2,side_b/2+dist]]
        rig_but = [[side_b*2+dist*3,dist],[side_b*3+dist*3,side_b/2+dist],[side_b*2+dist*3,side_b+dist]]
        
        lef_but_sq = [[side_b+dist*2,dist],[side_b*2+dist*2,dist],[side_b*2+dist*2,side_b+dist],
                      [side_b+dist*2,side_b+dist]]
        rig_but_sq = [[side_b*2+dist*3,dist],[side_b*3+dist*3,dist],[side_b*3+dist*3,side_b+dist],
                      [side_b*2+dist*3,side_b+dist]]
        
        beg_x = 0
        beg_y = 0
        
        side = width//10
        
        x = 10
        y = 5
        
        field = []
        places = []
        if make_new_fig:
            places = [[]]
        else:
            for old_place in self.environment.all_figures[cur_fig].places:
                places.append(old_place)
        
        
        
        for yy in range(1,y+2):
            for xx in range(x):
                field.append([[side*xx,side*yy],[side*(xx+1),side*yy],[side*(xx+1),side*(yy+1)],
                              [side*xx,side*(yy+1)]])
        
        
        while True:
            pg.draw.polygon(self.screen,(255,0,0),add_but)
            pg.draw.polygon(self.screen,(0,255,0),lef_but)
            pg.draw.polygon(self.screen,(0,255,0),rig_but)
            pg.draw.polygon(self.screen,(100,150,100),del_but)
            
            for clicked in places[cur_pos]:
                pg.draw.polygon(self.screen, (0,255,0), field[clicked[1]*x+clicked[0]])
            
            for xx in range(x):
                pg.draw.line(self.screen,(255,255,255),(xx*side,field_beg_y),(xx*side,height))
                self.write(str(xx+beg_x), (100,100,100), (xx*side,field_beg_y), 40)
            
            
            self.write(str(beg_y),(100,100,100),(0,field_beg_y+50),40)
            for yy in range(2,y+2):
                pg.draw.line(self.screen,(255,255,255),(0,yy*side),(width,yy*side))
                self.write(str(yy+beg_y-1), (100,100,100), (0,yy*side), 40)
            
            pg.draw.line(self.screen,(255,0,0),(0,field_beg_y),(1200,field_beg_y))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    name = pg.key.name(event.key)
                    if name == 'return':
                        if make_new_fig:
                            new_fig = Figure(self.prov_name,places)
                            self.environment.all_figures.append(new_fig)
                        else:
                            self.environment.all_figures[cur_fig].places = places
                        self.load_fig()
                        self.fig_menu()
                        
                    
                    elif name == 'right':
                        beg_x += 1
                    elif name == 'left':
                        if beg_x > 0:
                            beg_x-=1
                    elif name == 'down':
                        beg_y+=1
                    elif name == 'up':
                        if beg_y>0:
                            beg_y -= 1
                elif event.type == pg.MOUSEBUTTONDOWN:
                    num_x = 0
                    num_y = 0
                    if self.check_coord(event.pos,add_but):
                        places.append([])
                        cur_pos = len(places)-1
                    elif self.check_coord(event.pos,lef_but_sq):
                        if cur_pos > 0:
                            cur_pos-=1
                    elif self.check_coord(event.pos,rig_but_sq):
                        if cur_pos < len(places)-1:
                            cur_pos+=1
                    elif self.check_coord(event.pos,del_but):
                        if len(places) > 1:
                            places.pop(cur_pos)
                            if cur_pos >= len(places):
                                cur_pos-=1
                    else:
                        for pol in field:
                            if self.check_coord(event.pos,pol):
                                place = [num_x+beg_x,num_y+beg_y]
                                if place in places[cur_pos]:
                                    places[cur_pos].remove(place)
                                else:
                                    places[cur_pos].append(place)
                                break
                            if num_x >= x-1:
                                num_y += 1
                                num_x = 0
                            else:
                                num_x += 1
                        
                        
            
            pg.display.flip()
            self.clock.tick(30)
            pg.display.set_caption('Make a figure')
            self.screen.fill((0,0,0))
        
        
    
    
    
    def name_menu(self):
        width,height = 1200,800
        self.screen = pg.display.set_mode((width,height))
        name = ''
        while True:
            if len(name) > 0:
                sz = width/len(name)
                if height < sz:
                    sz = height
                
                self.write(name, (255,0,0), (20,20), int(sz))
            
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    sym = pg.key.name(event.key)
                    if sym == 'return':
                        if len(name) == 0:
                            name = 'A'
                        self.prov_name = name
                        self.make_fig_menu(True)
                    elif sym == 'backspace':
                        name = name[0:len(name)-1]
                    else:
                        name += sym
            
            
            pg.display.flip()
            self.clock.tick(30)
            pg.display.set_caption('Choose name of new figure')
            self.screen.fill((0,0,0))
    
    
    
    
    
    
    def fig_menu(self):#Making and changing packs menu
        def transfer(field):
            to_return = []
            for element in range(len(field)):
                if field[element]:
                    to_return.append(self.environment.all_figures[element])
            return to_return
        
        def reload(cur_pack):
            field = []
            for num_f in range(len(self.environment.all_figures)):
                if self.environment.all_figures[num_f] in self.environment.packs[cur_pack]:
                    field.append(True)
                else:
                    field.append(False)
            return field
        
        def load():#Load changed packs to packs.txt
            file = open('packs.txt','w')
            file.seek(0)
            n = 0
            to_wr = ''
            for pack in self.environment.packs:
                to_wr = str(n)
                to_wr += ' '
                for figure in pack:
                    to_wr += figure.name
                    to_wr += ' '
                to_wr += '\n'
                file.write(to_wr)
                n+=1
            file.close()
            
            
        a = 0
        width = 1200
        height = 800
        side = (width - width//5)//17
        dist = width//60
        
        add_fig_but = [[width-side-dist,dist],[width-dist,dist],[width-dist,side+dist],
                       [width-side-dist,side+dist]]#Adding new figure button
        
        #Coords in buttons are going in this order:
        #[x,y] -> [x+1,y] -> [x+1,y+1] - > [x,y+1]
        #Also another one visualization:
        #0   1
        #3   2
        
        add_but = [[side+dist,dist],[side*2+dist,dist],[side*2+dist,side+dist],[side+dist,side+dist]]
        #Adding new pack button
        del_but = [[side+dist,side+dist*2],[side*2+dist,side+dist*2],[side*2+dist,side*2+dist*2],
                   [side+dist,side*2+dist*2]]
        #Deleting pack button
        
        tr_lf = [[side*12+dist*12,side//2+dist],[side*13+dist*12,dist],[side*13+dist*12,side+dist]]
        #Drawing of decreasing of number of packs on a panel  / \
        #                                                    |
        tr_lf_sq = [[side*12+dist*12,dist],[side*13+dist*12,dist],[side*13+dist*12,side+dist],
                    [side*12+dist*12,side+dist]]
        #Reacting on clicking on button decreasing of number of packs on a panel / \
        #                                                                      |
        # tr_lf is a list of points of triangle to draw.
        #But tr_lf_sq is a list of coords between who you must click
        # tr_lf - texture, tr_lf_sq - hitbox
        #Same situation with tr_rg and tr_rg_sq
        #But they are need to increase number of packs on a panel
        # 0 1 2 3 ...
        # 1 2 3 4 ... increased
        # 0 1 2 3 ... decreased
        
        
        
        
        tr_rg = [[side*14+dist*14,dist],[side*14+dist*14,side+dist],[side*15+dist*14,side//2+dist]]
        tr_rg_sq = [[side*14+dist*14,dist],[side*14+dist*14,dist],[side*15+dist*14,side+dist],
                    [side*15+dist*14,side+dist]]
        
        
        
        # tr_lf_f, tr_lf_sq_f, tr_rg_f, tr_rg_sq_f same situation with last four buttons
        #But theese buttons need for figures
        tr_lf_f = [[side*12+dist*12,side//2+dist*2+side],[side*13+dist*12,dist*2+side],[side*13+dist*12,side*2+dist*2]]
        tr_lf_sq_f = [[side*12+dist*12,side+dist*2],[side*13+dist*12,side+dist*2],[side*13+dist*12,side*2+dist*2],
                    [side*12+dist*12,side*2+dist*2]]
        tr_rg_f = [[side*14+dist*14,dist*2+side],[side*14+dist*14,side*2+dist*2],[side*15+dist*14,side//2+side+dist*2]]
        tr_rg_sq_f = [[side*14+dist*14,dist*2+side],[side*14+dist*14,dist*2+side],[side*15+dist*14,side*2+dist*2],
                    [side*15+dist*14,side*2+dist*2]]
        
        
        pac = []# Buttons what mean packs
        fps = 30 #fps
        x = 2
        
        
        
        beg_p = 0 #Number of first pack in panel of packs
        # 3 4 5 6 ... - beg_p = 3
        # 0 1 2 3 ... - beg_p = 0
        

        
        
        for xx in range(x,12):#Add buttons in pac
            pac.append([[side*x+dist*x,20],[side*(x+1)+dist*x,20],[side*(x+1)+dist*x,side+20],
                        [side*x+dist*x,side+20]])
            x+=1
        
        
        x = 0
        y = 2
        beg_f = 0 #Number of first figure in field of figures
        fig = [] #Buttons what mean figures
        side_f = side*2
        for f in self.environment.all_figures:
            fig.append([[side_f*x+dist*x,side_f*y+dist*y],[side_f*(x+1)+dist*x,side_f*y+dist*y],
                       [side_f*(x+1)+dist*x,side_f*(y+1)+dist*y],[side_f*x+dist*x,side_f*(y+1)+dist*y]])
            if side_f * (x+2) + dist * (x+2) > width:
                if side_f * (y+2) + dist * (y+2) > height:
                    break
                else:
                    y += 1
                    x = 0
            else:
                x+=1
            
        
        cur_pack = 2 #Selected pack
        cur_fig = 0  #Selected figure
        
        field = reload(cur_pack) #Field of figures where figures represented as boolean
        #variables: True if figure in selected pack and False if figure not in selected pack
        

        
        while True:
            #Draw buttons what dont mean directly pack or figure | \/
            pg.draw.polygon(self.screen,(255,0,0),add_but)
            self.write('Add',(100,100,100),(add_but[0][0],add_but[0][1]),20)# (add_but[0][0],add_but[0][1]) - left upper point of button
            self.write('new',(100,100,100),(add_but[0][0],add_but[0][1]+16),20)#+12 - below on 12 pixels
            self.write('pack',(100,100,100),(add_but[0][0],add_but[0][1]+32),20)
            pg.draw.polygon(self.screen,(255,150,120),del_but)
            self.write('Delete',(100,100,100),(del_but[0][0],del_but[0][1]),18)
            self.write('selected',(100,100,100),(del_but[0][0],del_but[0][1]+16),15)
            self.write('pack',(100,100,100),(del_but[0][0],del_but[0][1]+32),18)
            
            pg.draw.polygon(self.screen,(0,255,0),tr_lf)#I DONT draw tr_lf_sq and same polygons
            pg.draw.polygon(self.screen,(0,255,0),tr_rg)
            
            pg.draw.polygon(self.screen,(0,255,0),tr_lf_f)
            pg.draw.polygon(self.screen,(0,255,0),tr_rg_f)
            
            pg.draw.polygon(self.screen,(255,0,0),add_fig_but)
            self.write('Add',(100,100,100),(add_fig_but[0][0],add_fig_but[0][1]),20)
            self.write('new',(100,100,100),(add_fig_but[0][0],add_fig_but[0][1]+20),20)
            self.write('figure',(100,100,100),(add_fig_but[0][0],add_fig_but[0][1]+40),20)
            
            num = 0 #Count variable
            for to_dr in pac:#Drawing of packs (buttons what mean packs)
                if num >= len(self.environment.packs):break
                pg.draw.polygon(self.screen,(0,0,255),to_dr)
                self.write(str(num+beg_p), (100,100,100), ((num+2)*side+dist*(num+2),side//4+dist), side//len(str(num)))
                num+=1
            
            num = beg_f#Count variable again
            for to_dr_f in fig:#Drawing of figures (buttons what mean figures)
                color = (0,0,255)
                if field[num]: #self.environment.all_figures[num] in self.environment.packs[cur_pack] - old realization without field list:
                    color = (0,0,0)            
                                
                
                pg.draw.polygon(self.screen,color,to_dr_f)
                name = self.environment.all_figures[num].name
                sz = side_f//len(name)*2
                if side_f < sz:sz = side_f
                
                
                self.write(name,(0,200,50),(to_dr_f[0][0],to_dr_f[0][1]),sz)
                
                if num == cur_fig:#If this figure is selected figure will be underlined
                    pg.draw.line(self.screen, (255,0,0), (to_dr_f[0][0],to_dr_f[0][1]),
                                 (to_dr_f[1][0],to_dr_f[1][1]), 1)
                    pg.draw.line(self.screen,(255,0,0),(to_dr_f[1][0],to_dr_f[1][1]),
                                 (to_dr_f[2][0],to_dr_f[2][1]))
                    
                    pg.draw.line(self.screen,(255,0,0),(to_dr_f[2][0],to_dr_f[2][1]),
                                 (to_dr_f[3][0],to_dr_f[3][1]),1)
                    
                    pg.draw.line(self.screen,(255,0,0),(to_dr_f[3][0],to_dr_f[3][1]),
                                 (to_dr_f[0][0],to_dr_f[0][1]))
                    
                num+=1
                
            for event in pg.event.get():
                if event.type == pg.QUIT:#classical pygame exiting a programm
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if pg.key.name(event.key) == 's':#IF clicked 'c' on keyboard and
                    #if len of current pack bigger than 0
                    #then go to setting menu
                        repack = transfer(field)
                        if len(repack) == 0:
                            break
                        else:
                            self.environment.packs[cur_pack] = repack
                        if len(self.environment.packs[cur_pack]) != 0:
                            load()
                            self.set_draw()
                    elif pg.key.name(event.key) == 'a':#If clicked button 'a'
                    #and if current pack not standard pack
                    #then add/delete figure to/from selected pack
                        if cur_pack != 0:
                            field[cur_fig] = not(field[cur_fig])
                    elif pg.key.name(event.key) == 'backspace':#If clicked button 'backspace'
                    #and if current(selected) figure is not standard(first seven) then
                    #delete current(selected) figure
                        if cur_fig >= self.environment.stand_figs:
                            self.environment.all_figures.pop(cur_fig)
                            self.load_fig()
                            
                            fig = fig[0:len(fig)-1]
                    elif pg.key.name(event.key) == 'c':#If clicked button 'c' 
                    #and selected figure is not standard then change this figure
                    #change - change blocks and poses of this figure
                        if cur_fig >= self.environment.stand_figs:
                            self.make_fig_menu(False,cur_fig)
                        
                        
                        
                        
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.check_coord(event.pos,tr_lf_sq):#if clicked this button
                    # (how works checking of clicking on button I try explain in check_coord )
                    # and if shift(number of first pack) - beg_p of(in) panel of packs more than 0
                    # then decrease this parametr
                        if beg_p > 0:
                            beg_p-=1
                    elif self.check_coord(event.pos, tr_rg_sq):#If clicked this button
                    # and if shift(number of first pack) - beg_p of(in) panel of packs less than 
                    # (len of list of packs) - 1
                    # then increase this parametr
                        if beg_p+len(pac) < len(self.environment.packs)-1:
                            beg_p+=1
                    elif self.check_coord(event.pos, tr_lf_sq_f):#Same things but with panel of figures
                        if beg_f>0:
                            beg_f-=1
                    
                    elif self.check_coord(event.pos,tr_rg_sq_f):
                        if beg_f + len(fig) < len(self.environment.all_figures):
                            beg_f+=1
                    elif self.check_coord(event.pos,add_but):#If clicked this button
                    #then add new empty pack
                        self.environment.packs.append([])
                    
                    elif self.check_coord(event.pos,del_but):#If clicked this button
                    #and if current(selected) pack is not standard(first)
                    #then delete selected pack
                        if cur_pack != 0:
                            
                            self.environment.packs.pop(cur_pack)
                            if cur_pack >= len(self.environment.packs):
                                cur_pack-=1
                            field = reload(cur_pack)
                    
                    elif self.check_coord(event.pos,add_fig_but):#IF clicked this button
                    #then begin making of new figure
                        self.name_menu()
                    
                        
                    now = 0
                    for c in pac:#Checking if ckicked any pack from panel of packs
                    # and if clicked then set number of selected pack
                    # on number of clicked pack
                    # and change field on field of clicked pack
                    # what is field i explained upper, around 459th line
                        if now >= len(self.environment.packs):break
                        if self.check_coord(event.pos, c):
                            repack = transfer(field)
                            if len(repack) == 0:
                                break
                            else:
                                self.environment.packs[cur_pack] = repack
                            cur_pack = beg_p+now
                            field = reload(cur_pack)
                            break
                        now+=1
                    
                    now = 0
                    for s in fig:#Same thing with figures but without field.
                        if self.check_coord(event.pos, s):
                            cur_fig = now+beg_f
                            break
                        now+=1
                            
                            
            #Standart pygame things
            pg.display.flip()
            self.clock.tick(fps)
            pg.display.set_caption("Maker of packs")
            self.screen.fill((0,0,0))
    
    
    
    
    
    def draw_field(self):#Just drawing game field
        for line in range(self.environment.x):
            for column in range(len(self.environment.field[line])):
                if self.environment.field[line][column]:
                    
                    color = self.environment.color_field[line][column]
                    pg.draw.polygon(self.screen,color,((line*self.size_x,column*self.size_y)
                    ,((line+1)*self.size_x,column*self.size_y),
                    ((line+1)*self.size_x,(column+1)*self.size_y),
                    (line*self.size_x,(column+1)*self.size_y)))
                elif [line,column] in self.environment.new_fig.coords:
                    color = self.environment.new_fig.color

                    pg.draw.polygon(self.screen,color,((line*self.size_x,column*self.size_y)
                    ,((line+1)*self.size_x,column*self.size_y),
                    ((line+1)*self.size_x,(column+1)*self.size_y),
                    (line*self.size_x,(column+1)*self.size_y)))
    
    '''
    old and bad realization
    def write_end(self,text,color,base_y):
        #pg.draw.line(self.screen,(255,255,255),(600,0),(600,800))
        sz = self.width_sc // len(text)
        f = pg.font.SysFont('corbel',sz)
        font = f.render(text,True,color)
        self.screen.blit(font,(self.width_sc/2 - sz*len(text)/6,base_y))'''
    
    def write(self,text,color,pos,size):
        f = pg.font.SysFont('c059', size)
        font = f.render(text, True, color)
        self.screen.blit(font,pos)
        
        

    def draw(self):
        #There are two menu: directly game and basic
        #If in game press e you will go to basic menu
        #And if you press Enter in basic menu you will go to game menu
        #Also you can go to settings from basic menu
        prov_time = 0
        begin_time = 0
        while True:
            for event in pg.event.get():#Game management
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    name = pg.key.name(event.key)
                    if name == 'return':
                        if self.environment.end_game:
                            self.environment.end_game = False
                            self.environment.spawn()
                    elif name == 'right':
                        self.environment.move('right')
                    elif name == 'left':
                        self.environment.move('left')
                    elif name == 'down':
                        self.environment.move('down')
                    elif name == 'o':
                        self.environment.rotate('left')
                    elif name == 'p':
                        self.environment.rotate('right')
                    elif name == 's':
                        if self.environment.end_game:
                            self.set_draw()
                    elif name == 'e':
                        if not(self.environment.end_game):
                            self.environment.end_game = True
                            self.environment.score = 0
                            self.environment.clean_all()
                    
                        
            if self.environment.end_game:#Basic menu
                #It should be a separate menu, but this realization
                #too possible
                
                chapter = self.height_sc//3
                
                
                tx_1 = "Another Tetris"
                sz = self.width_sc // len(tx_1)
                if chapter < sz:
                    sz = chapter
                
                self.write(tx_1,(255,0,0),(self.width_sc/2 - sz*len(tx_1)/3,20),sz)
                
                sz = self.width_sc // len(tx_1)
                if chapter < sz:
                    sz = chapter
                tx_2 = "To play press Enter"
                self.write(tx_2,(100,0,100),(self.width_sc/2 - sz*len(tx_1)/3,chapter*2),sz)
                    
                    
            else:
                prov_time = pg.time.get_ticks() - begin_time
                if prov_time >= self.environment.step_time:#Figure goes down only if 
                    # passed some time recorded in environment.step_time
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


class Figure:#class figure
    #Programm make object of this class with inf about positions and name
    #positions - what does figure consist of in certain pose what you can change(rotate)
    def __init__(self,name,places):
        self.places = places
        self.place = 0
        self.name = name



#Thats useless now |
#                 \ /
#                  .
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




#Thats useless now .
#                 / \
#                  |



class Environment:
    def __init__(self,packs,all_figures,stand_figs):
        self.stand_figs = stand_figs
        self.spawned = False
        self.packs = packs
        self.pack = 0
        self.all_figures = all_figures
        self.figures = self.packs[self.pack]
        #self.spawn()
        self.end_game = True
        self.score = 0
        
    
    def init_field(self,x,y):
        self.x = x
        self.y = y
        self.field = [[False for y in range(self.y)] for x in range(self.x)]
        self.color_field = [[(0,0,0) for y in range(self.y)] for x in range(self.x)]
    
    def clean_all(self):
        self.field = [[False for y in range(self.y)] for x in range(self.x)]
    
    
    def spawn(self):
        new_fig_cl = random.choice(self.figures)

        new_fig = new_fig_cl

        
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
    
    def plus(self,a_,b_):#Plus two vectors
        a = copy.deepcopy(a_)
        b = copy.deepcopy(b_)
        for cor in range(len(a)):
            for el in range(len(b)):
                if el < len(a[cor]):
                    
                    a[cor][el] += b[el]
        return a
    
    def fall_lines(self,line):#If one line fully filled and destroyed lines upper must fall
        for to_fall in range(line-1,0,-1):
            for el in range(self.x):
                self.field[el][to_fall+1] = self.field[el][to_fall]
        
    
    def check_lines(self):#Checking lines if soe from them fully filled
        for line in range(self.y):
            tot = True
            for column_1 in range(self.x):
                if self.field[column_1][line] == False:#If at least one block isnt fulled - all line dont countes
                    tot = False
                    break
            if tot:
                self.score += 100
                for column_2 in range(self.x):
                    self.field[column_2][line] = False
                self.fall_lines(line)
                
            
    def update(self):#Update environment
        if self.spawned:
            plused_coords = self.plus(self.new_fig.coords , [0,1])
            if self.check(plused_coords):#If figure can go down it go down
                self.new_fig.coords = plused_coords
                self.new_fig.pos[1] += 1
            else:
                
                for coord in self.new_fig.coords:#Else figure set down and will spawn new figure
                    self.field[coord[0]][coord[1]] = True
                    self.color_field[coord[0]][coord[1]] = self.new_fig.color
                    self.spawned = False
        else:
            self.check_lines()
            self.spawn()
            self.step_time -= self.acel#After stopping figure step_time decreases
            
    
    def move(self,direction):#Check can figure move in certain direction and if can it moves
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

    
    def rotate(self,direction):#Same thing with rotation 
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
        
    

def load_figs():#load figures from figures.txt
    f = open('figures.txt','r')
    
    stand_figs = int(f.readline().split(" ")[1])
    lines = f.readlines()
    
    l = []
    new_l = []
    y = 0
    x = 0
    
    for line in lines:
        if line[0] == 'N':
            l.append(new_l)
            new_l = []
            coords = [[]]
            name = line[1:len(line)]#clean N
            if name[len(line)-2:len(line)]=='\n':#clean \n
                name = name[0:len(line)-2]
            new_l.append(name)
            new_l.append(coords)
            y = 0
        else:
            coor = 0
            x = 0
            for symbol in line:
                if symbol == "x":
                    coor += 1
                    if coor >= len(coords):
                        coords.append([])#If symbol is x then we have a new positon
                    x = 0
                    #continue
                elif symbol == "0" or symbol == "1":
                    if symbol == "1":
                        coords[coor].append([x,y])#If symbol is 1 yhen this block belongs to this position
                    x+=1
            y+=1
    l.pop(0)
    l.append(new_l)
    return l, stand_figs


def load_packs():#load packs from packs.txt
    f = open('packs.txt','r')
    
    packs = []
    lines = f.readlines()
    
    
    for line in lines:
        
        els = line.split(' ')
        elements = els[1:len(els)]
        
        el = elements[len(elements)-1]
        if el[len(el)-1:len(el)+1] == '\n':
            elements[len(elements)-1] = el[0:len(el)-1]
        packs.append(elements)
        
    
    return packs
    
    
    
        
        
if __name__ == '__main__':
    l,stand_figs = load_figs()
    figures = []

    
    for fig in l:
        figures.append(Figure(fig[0],fig[1]))
    '''
    print(11111111111111111)
    print(figures)
    print(1111111111111111)'''
    '''
    packs.append(figures[0:stand_figs])
    packs.append(figures)'''
    pacs = load_packs()
    packs = []
    for pp in pacs:#Forming packs (in original figures presented as their names but in pack they must be presented as Objects)
        new_p = []
        for p in pp:
            for f in figures:
                if f.name == p:
                    new_p.append(f)
        packs.append(new_p)
    
    
    

    #figures = [Cube,Stick,L_Fig,Z_Fig,Triangle]
    


    environment = Environment(packs,figures,stand_figs)
    app = App(environment)
    app.set_draw()
    #app.draw()