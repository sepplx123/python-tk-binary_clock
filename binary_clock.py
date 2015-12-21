    #!/usr/bin/python
    # -*- coding: utf-8 -*-
     
    from __future__ import (absolute_import, division,print_function, unicode_literals)
    from math import (sin, cos, pi)
    import Tkinter as tk
    from datetime import datetime
     
     
    class Uhrzeit():
        '''  Creates the actual time and the necessary values for other functions. '''
        def __init__(self):
            self.dt = datetime.now()
            self.hours = 0
            self.minutes = 0
            self.seconds = 0
            self.micros = 0
            self.time_s = 0
            self.time_format = 0
            #print("{0:02d}:{1:02d}:{2:02d}:{3:03d}".format(self.hours,self.minutes,self.seconds,self.micros))
     
        def anzeigen(self):
            '''  Returns the actual time in a proper format hh:mm:ss:micros '''
            self.dt = datetime.now()
            self.hours = self.dt.hour
            self.minutes = self.dt.minute
            self.seconds = self.dt.second
            self.micros = int(self.dt.microsecond/1000)
            #print("{0:02d}:{1:02d}:{2:02d}:{3:03d}".format(self.hours,self.minutes,self.seconds,self.micros))
            return ("{0:02d}:{1:02d}:{2:02d}:{3:03d}".format(self.hours,self.minutes,self.seconds,self.micros))
     
        def hms_anzeigen(self):
            '''  Returns the actual time in a proper format hh:mm:ss '''
            self.dt = datetime.now()
            self.hours = self.dt.hour
            self.minutes = self.dt.minute
            self.seconds = self.dt.second
            #return time.strftime("%H:%M:%S")
            return ("{0:02d}:{1:02d}:{2:02d}".format(self.hours,self.minutes,self.seconds))
     
        def values(self):
            '''  Returns the values of the actual time '''
            self.dt = datetime.now()
            self.hours = self.dt.hour
            self.minutes = self.dt.minute
            self.seconds = self.dt.second
            self.micros = int(self.dt.microsecond/1000)
            return self.hours,self.minutes,self.seconds,self.micros
       
        def get_micros(self):
            '''  Calculates the microseconds of the actual time '''
            self.dt = datetime.now()
            self.micros = int(self.dt.microsecond/1000)      
            return self.micros
     
        def time_in_s(self):
            '''  Transforms the actual time in seconds '''
            self.hours,self.minutes,self.seconds,self.micros = self.values()
            self.time_s = (self.hours*3600) + (self.minutes*60) + self.seconds
            return self.time_s
       
        def time_from_s(self,time_in_s):
            '''  Transforms the given time in seconds back to the format hh:mm:ss '''
            self.time_s = time_in_s
            hours, rest = divmod(self.time_s, 3600)
            minutes, seconds = divmod(rest, 60)
            return ("{0:02d}:{1:02d}:{2:02d}".format(hours,minutes,seconds))
           
       
    class GUI():
        '''  Creates and draws all ui elements  in the window. '''
        def __init__(self, master):
            self.master = master
            self.width = 800
            self.height = 800      
            self.uhr = Uhrzeit()
            self.cycle_time = 1                 # time in ms for one program cycle
     
            self.color_bg =         '#ffffff'
            self.color_movers =     '#00bfff'   #'#4169e1' #
            self.color_m_Circle_Outlines =   '#87cefa'   #'#6495ed' #
            marking_angle = []
            marking_items = []
            self.counter = 0
            self.micros = 0
            self.hms_last_cycle = 0
            self.movers = []
            self.hiders = []
            self.simulation_counter = 0
           
            self.start_stop = tk.BooleanVar()
            self.start_stop.set(False)
            self.start_stop.trace("w", self.callback)
     
            self.strv_zeitangabe = tk.StringVar()
           
            self.strv_uhrzeit = tk.StringVar()
            self.strv_uhrzeit.trace("w", self.callback) # calls the function for animate the general movement wihtout any time correspandance
           
            self.sim_uhrzeit = tk.StringVar()
            self.sim_uhrzeit.set('00:00:00')
           
            self.time_anim_status = tk.BooleanVar()
            self.time_anim_status.set(False)
     
            # Frames            
            self.fr1 = tk.Frame(self.master, width=100, height=50, background='grey')
            self.fr2 = tk.Frame(self.master, width=100, height=50, background='grey')
            self.fr3 = tk.Frame(self.master, width=100, height=20, background='grey')
            self.fr1.pack(expand=1,fill='both')
            self.fr2.pack(expand=1,fill='both', anchor='center')
            self.fr3.pack(expand=1,fill='both')
     
            # Buttons
            self.bStart = tk.Button(self.fr2,width=0, height=1, bg='red',bd=5, text = "Simulation Start", command = self.startbutton )
            self.bStart.grid(row=2,column=0,padx=10, pady=10, sticky='nw')
            self.bReset = tk.Button(self.fr2,width=0, height=1, bg='red',bd=5, text = "Simulation Reset", command = self.reset)
            self.bReset.grid(row=2,column=1,padx=10, pady=10, sticky='nw')
            self.bQuit = tk.Button(self.fr1,padx=0, pady=5,width=10, height=1,bd=5, bg='red', text = "Quit", command = self.exit_program)
            self.bQuit.pack(side='right', padx=10, anchor='center')
           
            self.bAnimTime = tk.Button(self.fr2,width=30,padx=0, pady=5, height=1,bd=5, bg='blue', text = "Time Animation Start", command = self.time_animation_start_stop)      
            self.bAnimTime.grid(row=0,column=0,columnspan=2,padx=10, pady=5, sticky='nw')
     
     
            # Scales
            self.speed_label = tk.Label(self.fr2, bg='red', highlightthickness=1, height=2, text='Speed Adjustment')
            self.speed_label.grid(row=3,column=0,ipadx=0,pady=0,sticky='ne')
            self.speed_slider = tk.Scale(self.fr2, bg='red',length=300, troughcolor='black', highlightbackground='blue', highlightthickness=0, from_=1, to=100, orient='vertical')
            self.speed_slider.set(10)
            self.speed_slider.grid(row=3,column=1,ipadx=0,pady=0,sticky='n')
           
            # Canvas        
            self.canvas = tk.Canvas(self.fr2, width = self.width, height = self.height, highlightthickness=0, background=self.color_bg)
            self.canvas.grid(row=0,column=2,rowspan=10)
     
            # Labels
            self.label_uhrzeit = tk.Label(self.fr1, textvariable=self.strv_zeitangabe,bg='grey',fg='red',width=50, height=1,font=("Arial", 20))
            self.label_uhrzeit.pack(side='left',padx=0,ipadx=0, anchor='center')
           
            self.label_Simulation = tk.Label(self.fr2, text='Simulated time',bg='white',fg='red',width=20, height=2,font=("Arial", 15))
            self.label_Simulation.grid(row=1,column=0,columnspan=2, ipadx=0,ipady=10,sticky='n')      
            self.label_sim_uhrzeit = tk.Label(self.fr2, textvariable=self.sim_uhrzeit,bg='white',fg='red',width=20, height=0,font=("Arial", 15))
            self.label_sim_uhrzeit.grid(row=1,column=0,columnspan=2,ipadx=0,ipady=10,pady=0,sticky='s')
           
     
            # Text Items
           
     
            # Layout Design:   Circle_Outlines ==> Movers ==> Hiders ==> Pulsar
            marking_angle = [360-360,360/2]
            for item in marking_angle:
                marking_items.append(Marking_Circle_Outlines(self.canvas,370,item,70,item,fill=self.color_m_Circle_Outlines,width=2)) # 0, 180°
            marking_angle = [360/4,360-360/4]      
            for item in marking_angle:
                marking_items.append(Marking_Circle_Outlines(self.canvas,370,item,70+60,item,fill=self.color_m_Circle_Outlines,width=2)) # 90, 270°
            marking_angle = [360/8*1,360/8*3,360/8*5,360/8*7]      
            for item in marking_angle:
                marking_items.append(Marking_Circle_Outlines(self.canvas,370,item,70+60*2,item,fill=self.color_m_Circle_Outlines,width=2)) #
            marking_angle = [360/16*1,360/16*3,360/16*5,360/16*7,360/16*9,360/16*11,360/16*13,360/16*15]      
            for item in marking_angle:
                marking_items.append(Marking_Circle_Outlines(self.canvas,370,item,70+60*3,item,fill=self.color_m_Circle_Outlines,width=2)) #
            marking_angle = [360/32*1,360/32*3,360/32*5,360/32*7,360/32*9,360/32*11,360/32*13,360/32*15,360/32*17,360/32*19,360/32*21,
                             360/32*23,360/32*25,360/32*27,360/32*29,360/32*31]      
            for item in marking_angle:
                marking_items.append(Marking_Circle_Outlines(self.canvas,370,item,70+60*4,item,fill=self.color_m_Circle_Outlines,width=2)) #
           
            self.line1 = Circle_Outlines(self.canvas,400,400,340,outline=self.color_m_Circle_Outlines,width=2)                        # Linien
            self.mover1 = Movers(self.canvas, x=400, y=400, r=360, start=90, extent=(360/32), outline=self.color_movers, fill=self.color_movers ,width=1)
            self.hider1 = Movers(self.canvas, x=400, y=400, r=320, start=90, extent=(360/32)+2, outline=self.color_bg, fill=self.color_bg ,width=3)
     
            self.line2 = Circle_Outlines(self.canvas,400,400,280,outline=self.color_m_Circle_Outlines,width=2)
            self.mover2 = Movers(self.canvas, x=400, y=400, r=300, start=90, extent=(360/16), outline=self.color_movers, fill=self.color_movers,width=1)
            self.hider2 = Movers(self.canvas, x=400, y=400, r=260, start=90, extent=(360/16)+2, outline=self.color_bg, fill=self.color_bg ,width=3)
                         
            self.line3 = Circle_Outlines(self.canvas,400,400,220,outline=self.color_m_Circle_Outlines,width=2)
            self.mover3 = Movers(self.canvas, x=400, y=400, r=240, start=90, extent=(360/8), outline=self.color_movers, fill=self.color_movers ,width=1)
            self.hider3 = Movers(self.canvas, x=400, y=400, r=200, start=90, extent=(360/8)+2, outline=self.color_bg, fill=self.color_bg ,width=3)
           
            self.line4 = Circle_Outlines(self.canvas,400,400,160,outline=self.color_m_Circle_Outlines,width=2)
            self.mover4 = Movers(self.canvas, x=400, y=400, r=180, start=90, extent=(360/4), outline=self.color_movers, fill=self.color_movers ,width=1)
            self.hider4 = Movers(self.canvas, x=400, y=400, r=140, start=90, extent=(360/4)+2, outline=self.color_bg, fill=self.color_bg, width=3)
                                 
            self.line5 = Circle_Outlines(self.canvas,400,400,100,outline=self.color_m_Circle_Outlines,width=2)
            self.mover5 = Movers(self.canvas, x=400, y=400, r=120, start=90, extent=(360/2), outline=self.color_movers, fill=self.color_movers ,width=1)
            self.hider5 = Movers(self.canvas, x=400, y=400, r=80, start=90, extent=(360/2)+2, outline=self.color_bg, fill=self.color_bg ,width=3)
     
            self.pulsar = Pulsar(self.canvas,400,400,60,outline=self.color_movers,fill=self.color_movers,width=1)        # Pulsar
            #self.canvas.lift(self.movers[item])
            #self.canvas.lift(self.circles[item])
     
            self.movers = [self.mover1,self.mover2,self.mover3,self.mover4,self.mover5]
            self.hiders = [self.hider1,self.hider2,self.hider3,self.hider4,self.hider5]
           
            #print(self.uhr.anzeigen(), 'class init GUI done')
            self.update_time()              # Starts the mainloop
            ###### Init finished #####
     
     
        def callback(self, *event):
            ''' callback functions when the variables for the time and the start button is changed.
           Its used to control the speed of the animation. '''
            self.speed = self.speed_slider.get()
     
            if 0 < self.speed and self.speed <= 10:
                self.speed = self.speed / 2
            elif 10 < self.speed and self.speed <= 20:
                self.speed = self.speed / 5
            elif 20 < self.speed and self.speed <= 30:
                self.speed = self.speed / 2.5
            elif 30 < self.speed and self.speed <= 40:
                self.speed = self.speed / 2
            elif 40 < self.speed and self.speed <= 50:
                self.speed = self.speed / 1.5
               
            self.counter += self.speed
     
            if self.start_stop.get():                   # animates the genereal movement without any time correspondance
                if  self.counter >= 100:
                    self.counter = 0
                    self.animation_mover()
                    #print(self.uhr.anzeigen())
                   
            if self.time_anim_status.get():             # animates the pulsar only when the "actual time" simulation is chosen
                self.animation_pulsar()
     
        def update_time(self):
            ''' Updates the actual time and represents the mainloop. This function is called as dast as possible. '''
            self.strv_uhrzeit.set(self.uhr.anzeigen())                          # Loop for animation
            self.strv_zeitangabe.set('actual time:'+self.uhr.hms_anzeigen())                   # Show the actual time on top of the window
     
            if self.hms_last_cycle <> self.strv_zeitangabe.get():               # check if 1 second has passed
                self.time_animation()                                           # Call this function only when values changes (every 1s)
            self.hms_last_cycle = self.strv_zeitangabe.get()                    # copy the actual value to the last cycle variable
                                                                                                     
            self.master.after(self.cycle_time, self.update_time)                # Mainloop
     
        def exit_program(self,*event):
            ''' Close the window and exit the program '''
            self.master.destroy()
     
        def startbutton(self):
            ''' Starts or stops the animation '''
            if not self.start_stop.get():
                if self.time_anim_status.get():                     # when the time simulation is running, stop it first
                    self.time_animation_start_stop()
                self.start_stop.set(True)
                self.bStart.config(text='Simulation Stop',bg='green')
                self.pulsar.reset()
            else:
                self.start_stop.set(False)
                self.bStart.config(text='Simulation Start',bg='red')            
     
        def time_animation_start_stop(self):
            ''' Starts or stops the animation according to the actual time '''      
            if not self.time_anim_status.get():
                if self.start_stop.get():                            # when the simulation is running, stop it first
                    self.startbutton()
                self.time_anim_status.set(True)
                self.bAnimTime.config(text='Time Animation Stop',bg='green')
                self.time_animation()
            else:
                self.time_anim_status.set(False)
                self.bAnimTime.config(text='Time Animation Start',bg='blue')
     
        def time_animation(self,*event):
            ''' time animation function. This function is called every 1s. '''        
            self.time_in_s = self.uhr.time_in_s()
           
            if self.time_anim_status.get():                                     # animates the actual time when the button Time Animation Start was pressed
                for item in range(len(self.movers)):                
                    self.hiders[item].show_time(self.time_in_s,int(item+1))
                    self.movers[item].show_time(self.time_in_s,int(item+1))
           
        def animation_mover(self):
            '''
           Mover Rotation Increments see http://www.bartelmus.org/binar-uhr/#more-136
           '''      
            for item in range(len(self.movers)):
                self.hiders[item].rotate(int(item+1))
                self.movers[item].rotate(int(item+1))
     
            self.sim_uhrzeit.set(self.uhr.time_from_s(self.simulation_counter)) # shows a simulated time
            self.simulation_counter =  self.simulation_counter+1                # updates the counter for the virtual seconds
     
        def animation_pulsar(self):
            ''' The animation of the pulsar in the middle of the window. This item represents the microseconds of ath actual second. '''
            self.micros = self.uhr.get_micros()
            self.pulsar.puls(self.micros)        
     
        def reset(self):
            '''Resets all moving items to its start position and stops all actions '''
            if self.start_stop.get():
                self.startbutton()
               
            if self.time_anim_status.get():
                self.time_animation_start_stop()    
     
            for element in self.hiders:
                element.reset()
            for element in self.movers:
                element.reset()        
            self.pulsar.reset()
            self.simulation_counter = 0
            self.sim_uhrzeit.set(self.uhr.time_from_s(self.simulation_counter))
           
    class Marking_Circle_Outlines():
        '''  This are Marking Circle_Outlines on the canvas.
       This is only to have a better overview about the position of the Movers. '''    
        def __init__(self, canvas, *args, **kwargs):
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lift(self.id)
     
        def create(self,canvas,radius_1,angle_1,radius_2,angle_2,fill,width):
            '''  This function creates an canvas line.
           The first step is to convert the given polar coords to karthesian coords and create the start and end point of the line.
           The 2nd step is to create the item'''
            self.canvas = canvas
            self.x1, self.y1 = self.conv_pol_to_kart_coords(radius_1,angle_1)
            self.x2, self.y2 = self.conv_pol_to_kart_coords(radius_2,angle_2)    
            item = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill, width=width, tags="marking_line")
            return item
     
        def conv_pol_to_kart_coords(self,radius,angle,offsetx=400,offsety=400):   # Funktion konvertiert Polar-Koords in Karthesische-Koords
            '''  This function converts polar coords to karthesian coords '''
            self.direction = 1
            self.angle_offset = 90
            self.angle = self.angle_offset - angle
            coord_x = offsetx+radius*round(cos(2*pi/360*self.direction*self.angle),3)    #berechnete Soll-Position am Kreis in X mit 3 Dezimalstellen
            coord_y = offsety+radius*round(sin(2*pi/360*self.direction*(-self.angle)),3) #berechnete Soll-Position am Kreis in Y mit 3 Dezimalstellen
            return coord_x, coord_y
     
     
    class Circle_Outlines():
        '''  This are Circle_Outlines where the Movers move on top '''
        def __init__(self, canvas, *args, **kwargs):
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lift(self.id)
     
        def create(self,canvas,x,y,r,outline,width):
            '''  creates an canvas oval '''
            self.canvas = canvas
            item = canvas.create_oval(x-r,y-r,x+r,y+r,outline=outline,width=width, tags='outline')
            return item
     
    class Movers():
        '''  This are moving objects to show the actual time '''
        def __init__(self, canvas, *args, **kwargs):
            self.ValueDict = {1:1, 2:16, 3:128, 4:512, 5:1024}
           
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lower(self.id)
            self.angleOffset = -90
            self.direction= -1
            self.angle = 0
     
     
        def create(self,canvas,x,y,r,start,extent,outline,fill,width):
            '''  creates an canvas arc '''
            self.canvas = canvas
            item = canvas.create_arc(x-r,y-r,x+r,y+r,start=start,extent=extent,outline=outline,fill=fill,width=width, tags='mover')
            return item
         
        def rotate(self,ident):
            '''
           rotates the object with the given increment    The Incredements each mover should move per one cycle
           mover1_inc = 360/86400*1          
           mover2_inc = 360/86400*16
           mover3_inc = 360/86400*128
           mover4_inc = 360/86400*512
           mover5_inc = 360/86400*1024
           '''
            #x1, y1, x2, y2 = self.canvas.bbox(self.id)
            self.ident = ident
            self.value = self.ValueDict[self.ident]
            self.increment = 360 / 86400 * self.value
             
            self.canvas.itemconfig(self.id, start=self.direction*(self.angle+self.angleOffset))       # Changes the start angle
     
            if self.angle >= 360.0:
                self.angle -= 360.0
            self.angle += self.increment
     
        def show_time(self,time_in_s,ident):
            '''
           shows its value according to the given time.        Mover position corresponding to the actual time
           self.mover1_value = 360/86400*1*self.time_in_s        
           self.mover2_value = 360/86400*16*self.time_in_s
           self.mover3_value = 360/86400*128*self.time_in_s
           self.mover4_value = 360/86400*512*self.time_in_s
           self.mover5_value = 360/86400*1024*self.time_in_s
           formula: calc_position = self.direction * (self.angleOffset + (360 / 86400 * self.moverX_value * self.time_in_s))
           '''
            self.time_in_s = time_in_s
            self.ident = ident
            self.value = self.ValueDict[self.ident]
            calc_position = self.direction * (self.angleOffset + (360 / 86400 * self.value * self.time_in_s)) # calculates the position according to the actual time
            self.canvas.itemconfig(self.id, start=calc_position)        # Changes the start angle according to the given value
            #print (self.time_in_s, self.ident, self.value, calc_position)
                   
        def reset(self):
            '''  reset to start position '''
            self.angle = 0
            self.canvas.itemconfig(self.id, start=self.direction*(self.angle+self.angleOffset))
     
           
    class Pulsar():
        '''  This is the Pulsar shown in the middle of the window. It represents the micro seconds according to its size.
       1000 micros represent the biggest size and 0 the minimum with an radius of 0. '''
        def __init__(self, canvas, *args, **kwargs):
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lift(self.id)
     
        def create(self,canvas,x,y,r,outline,fill,width):
            '''  creates an canvas oval '''
            self.canvas = canvas
            item = canvas.create_oval(x-r,y-r,x+r,y+r,outline=outline, fill=fill ,width=width,tags='pulsar')
            return item
           
        def puls(self,micros):
            '''  adjusts the sizes of the object according to the given value '''
            self.micros = micros
            micros_len_pointer = self.micros/1000 * 60
            self.canvas.coords(self.id, 400 - micros_len_pointer, 400 - micros_len_pointer, 400 + micros_len_pointer, 400 + micros_len_pointer)
     
        def reset(self):
            '''  reset to start position '''
            micros_len_pointer = 60
            self.canvas.coords(self.id, 400 - micros_len_pointer, 400 - micros_len_pointer, 400 + micros_len_pointer, 400 + micros_len_pointer)    
     
     
    def main():
        '''  main program '''
        root = tk.Tk()
        ui = GUI(root)
        root.mainloop()
     
     
    if __name__ == '__main__':
        main()
