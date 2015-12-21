#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)
from math import (sin, cos, pi)
from datetime import datetime

# Fix fuer Python 2.x/3.x
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    import tkMessageBox as msgbox
except ImportError:
    import tkinter.messagebox as msgbox



def conv_pol_to_kart_coords(radius, angle, angle_offset, offsetx, offsety):
    """  This function converts polar coords to karthesian coords """              
    angle = angle_offset + angle
    x = offsetx + radius*round(cos(2*pi/360*angle),3) # X mit 3 Dezimalstellen
    y = offsety - radius*round(sin(2*pi/360*angle),3) # Y mit 3 Dezimalstellen
    return x, y

def circle_outline(canvas,x,y,r,outline,width):
    """  This are Circle_Outlines where the Movers move on top
    Creates an canvas oval"""
    item = canvas.create_oval(x-r,y-r,x+r,y+r, outline=outline, width=width, tags='circle_outline')
    canvas.lower(item)
    return item

def marking_circle_outline(canvas,radius_1,angle_1,radius_2,angle_2,
                           angle_offset,offsetx,offsety,fill,width):
    x1, y1 = conv_pol_to_kart_coords(radius=radius_1,angle=angle_1,
                                     angle_offset=angle_offset, offsetx=offsetx ,offsety=offsety)
    x2, y2 = conv_pol_to_kart_coords(radius=radius_2,angle=angle_2,
                                     angle_offset=angle_offset, offsetx=offsetx ,offsety=offsety)
    item = canvas.create_line(x1, y1, x2, y2, fill=fill, width=width, tags="marking_circle_outline")
    canvas.lower(item)
    return item

def create_canvas_elements(n,distance,canvas,width,height,color_markings,color_movers1,color_movers2,dist_between_elements,dist_between_movers,angle_offset):
        """ The following items are drawn on the canvas:
        Marking_Circle_Outlines &  Circle_Outlines ==> Movers ==> Pulsar  """
        marking_items = []
        movers = []
        tempdict = {}               # empty dict for creating Marking_Circle_Outlines values
        for i in range(1,n+1):      # Outer Loop for Circle_Outlines and Movers number = 1,2,3,4,5
            marking_items.append(circle_outline(canvas,width/2,height/2,40+distance*i,
                                                outline=color_markings,width=2))
            movers.append(Mover(canvas, radius1=dist_between_elements+(distance*i+dist_between_elements),
                                      radius2=distance*(1+i), start=0, extent=(360/2**i),angle_offset=angle_offset, offsetx=width/2, offsety=height/2, 
                                      color1=color_movers1, color2=color_movers2,width=2))

            for j in range(0 ,100*360, int(100*360/2**i)):      # inner loop for Marking_Circle_Outlines | Intervall = 100*360/2**i
                new_angle = j/100                               # j/100 to get the real angle back. int(100*360/2**i) is only used to get an integer value
                if new_angle not in tempdict:                   # Check if not already exist
                    #print('i =',i,'new_angle =',new_angle)
                    tempdict[new_angle] = i                     # create a new entry
                    item = marking_circle_outline(canvas=canvas, radius_1=dist_between_elements+distance*i,
                                                  angle_1=new_angle, radius_2=dist_between_elements+(distance*(1+n)),
                                                  angle_2=new_angle, angle_offset=angle_offset, offsetx=width/2,
                                                  offsety=height/2, fill=color_markings, width=2) # Intervall = 100*360/2**i   
                    marking_items.append(item)                   
       
        # Pulsar
        pulsar = (Pulsar(canvas,width/2,height/2,dist_between_movers,offsetx=width/2,
                             offsety=height/2,color1=color_movers1,color2=color_movers2,width=2))
        
        return marking_items, movers, pulsar

def color_mix(canvas,limit,color1,color2,i):
    """ Mixes 2 colors in the defined limit"""
    (r1,g1,b1) = canvas.winfo_rgb(color1)
    (r2,g2,b2) = canvas.winfo_rgb(color2)
    r_ratio = float(r2-r1) / limit
    g_ratio = float(g2-g1) / limit
    b_ratio = float(b2-b1) / limit
    nr = int(r1 + (r_ratio * i))
    ng = int(g1 + (g_ratio * i))
    nb = int(b1 + (b_ratio * i))
    color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
    return color


class GUI(object):
    """  Creates and draws all ui elements  in the window. """
    def __init__(self, master):
        self.master = master
        self.width = 800
        self.height = 800
        self.no_movers = 5
        self.dist_between_movers = 60
        self.dist_between_elements = 10
        self.angle_offset = 90
        
        self.cycle_time = 1                         # time in ms for one program cycle
        self.act_time = datetime.now().time()
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.micros = 0

        self.color_bg =       '#ffffff'
        self.color_movers1 =  '#00bfff'
        self.color_movers2 =  'blue'
        self.color_markings = '#87cefa'
        self.counter = 0
        self.micros = 0
        self.time_last_cycle = 0
        self.simulation_counter = 0
        
        self.marking_items = []                     # Items to divide the circle outlines in intervalls
        self.movers = []                            # Items to show the time that move on the canvas
        self.pulsar = None                            # The item in the middle that shows the microseconds of the actual second

        self.start_stop = tk.BooleanVar()           # Start/Stop the simulation
        self.start_stop.set(False)
        self.strv_zeitangabe = tk.StringVar()       # actual time shown above
        self.strv_zeitangabe.set('00:00:00')
        self.sim_uhrzeit = tk.StringVar()           # displayed time for simulation
        self.sim_uhrzeit.set('00:00:00')
        self.time_anim_status = tk.BooleanVar()     # Start/Stop realtime animation
        self.time_anim_status.set(False)

        # Frames
        self.fr1 = tk.Frame(self.master, width=100, height=50, background='grey')
        self.fr2 = tk.Frame(self.master, width=100, height=50, background='grey')
        self.fr3 = tk.Frame(self.master, width=100, height=20, background='grey')
        self.fr1.pack(expand=1,fill='both')
        self.fr2.pack(expand=1,fill='both', anchor='center')
        self.fr3.pack(expand=1,fill='both')

        # Buttons
        self.bStart = tk.Button(self.fr2,width=0, height=1, bg='red',bd=5,
                                text = "Simulation Start", command = self.startbutton )
        self.bStart.grid(row=2,column=0,padx=10, pady=10, sticky='nw')
        self.bReset = tk.Button(self.fr2,width=0, height=1, bg='red',bd=5,
                                text = "Simulation Reset", command = self.reset)
        self.bReset.grid(row=2,column=1,padx=10, pady=10, sticky='nw')
        self.bQuit = tk.Button(self.fr1,padx=0, pady=5,width=10, height=1,bd=5, bg='red',
                               text = "Quit", command = self.myquit) #self.exit_program
        self.bQuit.pack(side='right', padx=10, anchor='center')
        self.bAnimTime = tk.Button(self.fr2,width=30,padx=0, pady=5, height=1,bd=5, bg='blue',
                                   text = "Real Time Animation Start", command = self.realtime_animation_start_stop)
        self.bAnimTime.grid(row=0,column=0,columnspan=2,padx=10, pady=5, sticky='nw')

        # Scales
        self.speed_label = tk.Label(self.fr2, bg='red', highlightthickness=1, height=2, text='Speed Adjustment')
        self.speed_label.grid(row=3,column=0,ipadx=0,pady=0,sticky='ne')
        self.speed_slider = tk.Scale(self.fr2, bg='red',length=300, troughcolor='black',
                                     highlightbackground='blue', highlightthickness=0,
                                     from_=1, to=100, orient='vertical')
        self.speed_slider.set(10)
        self.speed_slider.grid(row=3,column=1,ipadx=0,pady=0,sticky='n')

        # Canvas
        self.canvas = tk.Canvas(self.fr2, width = self.width, height = self.height,
                                highlightthickness=0, background=self.color_bg)
        self.canvas.grid(row=0,column=2,rowspan=10)

        # Labels
        self.label_uhrzeit = tk.Label(self.fr1, textvariable=self.strv_zeitangabe,
                                      bg='grey',fg='red',width=50, height=1,font=("Arial", 20))
        self.label_uhrzeit.pack(side='left',padx=0,ipadx=0, anchor='center')

        self.label_Simulation = tk.Label(self.fr2, text='Simulated time',bg='white',fg='red',
                                         width=20, height=2,font=("Arial", 15))
        self.label_Simulation.grid(row=1,column=0,columnspan=2, ipadx=0,ipady=10,sticky='n')
        self.label_sim_uhrzeit = tk.Label(self.fr2, textvariable=self.sim_uhrzeit,bg='white',fg='red',
                                          width=20, height=0,font=("Arial", 15))
        self.label_sim_uhrzeit.grid(row=1,column=0,columnspan=2,ipadx=0,ipady=10,pady=0,sticky='s')

        # Menubar; aendert sich im laufenden Programm auch nicht mehr
        # "Datei"-Menue
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="##***#####****",
                                  command=None)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Programm beenden",
                                  command=self.exit_program)
        self.menubar.add_cascade(label="Datei", menu=self.filemenu)

        # "Hilfe"-Menue
        self.infomenu = tk.Menu(self.menubar, tearoff=0)
        self.infomenu.add_command(label="About", command=self.showInfo)
        self.menubar.add_cascade(label="Info", menu=self.infomenu)
        self.master.config(menu=self.menubar)


        # Text Items
        

        # Canvas Elements:   Marking_Circle_Outlines &  Circle_Outlines ==> Movers ==> Pulsar
        self.marking_items, self.movers, self.pulsar = create_canvas_elements(
                                                                            n=self.no_movers,distance=self.dist_between_movers,canvas=self.canvas,width=self.width,height=self.height,
                                                                            color_markings=self.color_markings,color_movers1=self.color_movers1,color_movers2=self.color_movers2,
                                                                            dist_between_elements=self.dist_between_elements,dist_between_movers=self.dist_between_movers,
                                                                            angle_offset=self.angle_offset
                                                                            )
        #print(self.uhr.anzeigen(), 'class init GUI done')
        self.main_loop()          # Starts the mainloop
        ###### Init finished #####

    def main_loop(self):
        """ Updates the actual time and represents the mainloop.
        This function is called as fast as possible. """

        #Step1: get the actual time
        self.act_time = self.get_act_time()

        #Step2: Forward the variables to update the actual time shown on top of the window
        self.strv_zeitangabe.set(
                                 'actual time: {0:02d}:{1:02d}:{2:02d}'.format
                                 (self.act_time.hour,self.act_time.minute,self.act_time.second)
                                 )

        #Step3: Call the simulation function
        self.time_simulation()

        #Step4: Check if 1s has passed to call the function for the real time animation
        if not self.time_last_cycle == self.act_time.second:# check if 1 second has passed
            self.realtime_animation()                       # Call this function only when values changes (every 1s)
        self.time_last_cycle = self.act_time.second         # copy the actual value to the last cycle variable


        #Step5: start the loop again
        self.master.after(self.cycle_time, self.main_loop)    # mainloop

    def startbutton(self):
        """ Starts or stops the animation """
        if not self.start_stop.get():
            if self.time_anim_status.get():                     # when the time simulation is running, stop it first
                self.realtime_animation_start_stop()
            self.start_stop.set(True)
            self.bStart.config(text='Simulation Stop',bg='green')
            self.pulsar.reset()
        else:
            self.start_stop.set(False)
            self.bStart.config(text='Simulation Start',bg='red')

    def realtime_animation_start_stop(self):
        """ Starts or stops the animation according to the actual time """
        if not self.time_anim_status.get():
            if self.start_stop.get():                            # when the simulation is running, stop it first
                self.startbutton()
            self.time_anim_status.set(True)
            self.bAnimTime.config(text='Real Time Animation Stop',bg='green')
            self.realtime_animation()
        else:
            self.time_anim_status.set(False)
            self.bAnimTime.config(text='Real Time Animation Start',bg='blue')

    def time_simulation(self, *event):
        """ time_simulation functions when the variables for the time or the start button are changed.
        Its used to control the speed of the animation. """
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

        if self.start_stop.get():       # animates the general movement without any time correspondence
            if  self.counter >= 100:
                self.counter = 0
                self.animation_mover()

        if self.time_anim_status.get(): # animates the pulsar only when the "real time" simulation is chosen
            self.animation_pulsar()


    def realtime_animation(self,*event):
        """ time animation function. This function is called every 1s.
        animates the actual time when the button Time Animation Start was pressed"""
        if self.time_anim_status.get():
            for item in range(len(self.movers)):
                self.movers[item].show_time(self.time_in_s(self.act_time),int(item+1))

    def animation_mover(self):
        """ Mover Rotation Increments without time reference
        http://www.bartelmus.org/binar-uhr/#more-136 """
        for item in range(len(self.movers)):
            self.movers[item].rotate(ident=int(item+1))

        self.sim_uhrzeit.set(self.time_from_s(self.simulation_counter)) # shows a simulated time
        self.simulation_counter += 1  # updates the counter for the virtual seconds

    def animation_pulsar(self):
        """ The animation of the pulsar in the middle of the window.
        This item represents the microseconds of the actual second. """
        self.pulsar.puls(self.act_time.microsecond)
        
    def reset(self):
        """Resets all moving items to its start position and stops all actions """
        #Step1: stop all active simulations first
        if self.start_stop.get():
            self.startbutton()
        if self.time_anim_status.get():
            self.realtime_animation_start_stop()

        #Step2: reset the movers
        for item in self.movers:
            item.reset()

        #Step3: reset the pulsar and the simulation time
        self.pulsar.reset()
        self.simulation_counter = 0
        self.sim_uhrzeit.set(self.time_from_s(self.simulation_counter))

    def get_act_time(self):
        """  Returns the values of the actual time """
        return datetime.now().time()

    def time_in_s(self,given_time):
        """  Transforms the actual time in seconds """
        self.time_s = (given_time.hour*3600) + (given_time.minute*60) + given_time.second
        return self.time_s

    def time_from_s(self,time_in_s):
        """  Transforms the given time in seconds back to the format hh:mm:ss """
        self.time_s = time_in_s
        hours, rest = divmod(self.time_s, 3600)
        minutes, seconds = divmod(rest, 60)
        return ("{0:02d}:{1:02d}:{2:02d}".format(hours,minutes,seconds))

    def exit_program(self,*event):
        """ Close the window and exit the program """
        self.master.destroy()

    def myquit(self):
        """ Messagebox Ask ok to cancel """
        if  msgbox.askokcancel("Quit","Do you really want to quit?"):
            self.exit_program()

    def showInfo(self):
        """ Shows an Info box """
        msgbox.showinfo(
            "Info",
            "Erstellt von sepplx123 \n\n"
            "Orginial idea from: \n"
            "http://www.bartelmus.org/binar-uhr/#more-136"
            )


class Mover():
    """  This are moving objects to show the actual time """
    def __init__(self, canvas, radius1, radius2, start, extent, angle_offset, offsetx ,offsety, color1, color2, width):
        self.movers = []
        self.ValueDict = {5:2**0, 4:2**4, 3:2**7, 2:2**9, 1:2**10}
        self.canvas = canvas

        self.angle = 0
        self.angle_offset = angle_offset
        self.offsetx = offsetx
        self.offsety = offsety
        self.r1 = radius1
        self.r2 = radius2        
        self.start = start
        self.extent = extent
        self.mov_val = 0
        
        self.range_ = 1000
        limit = 1000

        for i in range(self.range_):
            step = i*self.extent/self.range_
            color = color_mix(canvas=self.canvas,limit=limit,color1=color1,color2=color2,i=i)  
            x1, y1 = conv_pol_to_kart_coords(self.r1,step, self.angle_offset, self.offsetx , self.offsety)
            x2, y2 = conv_pol_to_kart_coords(self.r2,step, self.angle_offset, self.offsetx , self.offsety) 
            item = canvas.create_line(x1,y1,x2,y2,fill=color,width=width,tags="mover")
            self.movers.append(item)     
            #self.canvas.lower(item)
 
    def rotate(self,ident):
        """ The amount for the rotation will be calculated according the given ident """
        direction = -1
        self.ident = ident
        self.value = self.ValueDict[self.ident]
        self.increment = 360 / 86400 * self.value
        self.move(self.mov_val, direction)
        
        if self.mov_val >= 360.0:
            self.mov_val -= 360.0
        self.mov_val += self.increment

    def show_time(self,time_in_s,ident):
        """
        Mover position corresponding to the actual time
        self.mover1_value = 360/86400*1*self.time_in_s
        self.mover2_value = 360/86400*16*self.time_in_s
        self.mover3_value = 360/86400*128*self.time_in_s
        self.mover4_value = 360/86400*512*self.time_in_s
        self.mover5_value = 360/86400*1024*self.time_in_s
        calc_position = (360 / 86400 * self.moverX_value * self.time_in_s))
        """
        direction=-1        
        self.time_in_s = time_in_s
        self.ident = ident
        self.value = self.ValueDict[self.ident]
        calc_position =  360 / 86400 * self.value * self.time_in_s      
        n = int(calc_position) // 360
        calc_position -= n*360
        self.move(calc_position,direction)
        
    def move(self,value,direction):
        """ Moves the item according to the given value """
        self.value = value
        for item in range(len(self.movers)):
            step = item*self.extent/self.range_ + direction*self.value
            x1, y1 = conv_pol_to_kart_coords(self.r1,step,self.angle_offset, self.offsetx , self.offsety)
            x2, y2 = conv_pol_to_kart_coords(self.r2,step,self.angle_offset, self.offsetx , self.offsety)
            self.canvas.coords(self.movers[item],x1,y1,x2,y2)

    def reset(self):
        """  reset to start position with angle 0 """
        self.mov_val = 0
        direction = 1
        self.move(self.mov_val, direction)

class Pulsar():
    """
    This is the Pulsar shown in the middle of the window.
    It represents the micro seconds according to its size.
    1000 micros represent the biggest size and 0 the minimum with an radius of 0.
    """
    def __init__(self,canvas,x,y,r,offsetx,offsety,color1,color2,width):
        self.pulsar = []
        self.micros = 0
        self.init_radius = r
        self.canvas = canvas
        range_ = r
        limit = r
  
        for i in range(1,range_ + 1):
            step = range_ - i
            color = color_mix(canvas=self.canvas,limit=limit,color1=color1,color2=color2,i=i)
            
            item = self.pulsar.append(self.canvas.create_oval(offsetx-step,offsety-step,offsetx+step,offsety+step,outline=color,
                                                                   fill='' ,width=width, tags=('pulsar','puls_'+str(step))))
            #self.canvas.lift(item)

    def puls(self,micros):
        """ adjusts the sizes of the object according to the given value """
        self.micros = int(micros / 1000)
        self.micros_len_pointer = int(round(self.micros / 1000 * self.init_radius))
        
        for i in range(len(self.pulsar)):
            if i <  self.micros_len_pointer:
                self.canvas.itemconfigure('puls_'+str(i),state='normal')
            else:
                self.canvas.itemconfigure('puls_'+str(i),state='hidden')

    def reset(self):
        """  reset to the init position """
        self.micros_len_pointer = self.init_radius
        self.canvas.itemconfigure('pulsar',state='normal')

def main():
    """  main program """
    root = tk.Tk()
    ui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
