    #!/usr/bin/python
    # -*- coding: utf-8 -*-
     
    from __future__ import (absolute_import, division,print_function, unicode_literals)
     
    import time
    from math import *
    import Tkinter as tk
    from datetime import datetime
     
     
    class Uhrzeit():
        def __init__(self):
            #print(self.anzeigen(), 'class init Uhrzeit done')
            pass
     
        def anzeigen(self):
            self.dt = datetime.now()
            self.hours = self.dt.hour
            self.minutes = self.dt.minute
            self.seconds = self.dt.second
            self.micros = int(self.dt.microsecond/1000)
            #self.format = str(self.hours)+':'+str(self.minutes)+':'+str(self.seconds)+':'+str(self.micros)
            #print("{0:02d}:{1:02d}:{2:02d}:{3:03d}".format(self.hours,self.minutes,self.seconds,self.micros))
            return ("{0:02d}:{1:02d}:{2:02d}:{3:03d}".format(self.hours,self.minutes,self.seconds,self.micros))
     
        def values(self):
            self.dt = datetime.now()
            self.hours = self.dt.hour
            self.minutes = self.dt.minute
            self.seconds = self.dt.second
            self.micros = int(self.dt.microsecond/1000)
            return self.hours,self.minutes,self.seconds,self.micros
     
        def hms_anzeigen(self):
            self.dt = datetime.now()
            self.hours = self.dt.hour
            self.minutes = self.dt.minute
            self.seconds = self.dt.second
            #return time.strftime("%H:%M:%S")
            return ("{0:02d}:{1:02d}:{2:02d}".format(self.hours,self.minutes,self.seconds))
       
        def get_micros(self):
            self.dt = datetime.now()
            self.micros = int(self.dt.microsecond/1000)      
            return self.micros
       
    class GUI():
        def __init__(self, master):
            self.master = master
            self.width = 800
            self.height = 800      
            self.uhr = Uhrzeit()
            self.cycle_time = 1    # time in ms for one program cycle
     
            self.color_bg = '#ffffff'
            self.color_movers =  '#00bfff' #'#4169e1' #
            self.color_markings = '#87cefa' #'#6495ed'
            marking_angle = []
            marking_items = []
            self.counter = 0
           
            self.start_stop = tk.BooleanVar()
            self.start_stop.set(False)
            self.start_stop.trace("w", self.callback)
     
            self.strv_zeitangabe = tk.StringVar()            
            self.strv_uhrzeit = tk.StringVar()
            self.strv_uhrzeit.trace("w", self.callback)
                     
            # Frames            
            self.fr1 = tk.Frame(self.master, width=100, height=50, background='white')
            self.fr2 = tk.Frame(self.master, width=100, height=50, background='grey')
            self.fr3 = tk.Frame(self.master, width=100, height=20, background='white')
            self.fr1.pack(expand=1,fill='both')
            self.fr2.pack(expand=1,fill='both', anchor='center')
            self.fr3.pack(expand=1,fill='both')
     
            # Buttons
            self.bStart = tk.Button(self.fr1,width=10, height=1, bg='red', text = "Start", command = self.startbutton )
            self.bStart.pack(side='left', padx=10, anchor='center')
            self.bReset = tk.Button(self.fr1,width=10, height=1, bg='red', text = "Reset", command = self.reset)
            self.bReset.pack(side='left', padx=10, anchor='center')
            self.bQuit = tk.Button(self.fr1,width=10, height=1, bg='red', text = "Quit", command = self.exitprogramm)
            self.bQuit.pack(side='right', padx=10, anchor='center')
     
            # Scales
            self.speed_label = tk.Label(self.fr2, bg='red', highlightthickness=1, height=2, text='Speed Adjustment')
            self.speed_label.pack(side='left', padx=0,anchor='n')
            self.speed_slider = tk.Scale(self.fr2, bg='red',length=300, troughcolor='black', highlightbackground='blue', highlightthickness=0, from_=1, to=100, orient='vertical')
            self.speed_slider.pack(side='left', padx=0,pady=0, anchor='n')
            self.speed_slider.set(10)
           
            # Canvas        
            self.canvas = tk.Canvas(self.fr2, width = self.width, height = self.height, highlightthickness=0, background=self.color_bg)
            self.canvas.pack(expand=1, anchor='center')
     
            # Labels
            self.label_uhrzeit = tk.Label(self.fr1, textvariable=self.strv_zeitangabe,bg='grey',fg='red',width=50, height=1)
            self.label_uhrzeit.config(font=("Arial", 20))
            self.label_uhrzeit.pack(side='left',anchor='center')
     
            # Text Items
           
     
            # Layout Design:   Lines ==> Movers ==> Kreise ==> Pulsar
            marking_angle = [360-360,360/2]
            for item in marking_angle:
                marking_items.append(Markings(self.canvas,370,item,70,item,fill=self.color_markings,width=2)) # 0, 180°
            marking_angle = [360/4,360-360/4]      
            for item in marking_angle:
                marking_items.append(Markings(self.canvas,370,item,70+60,item,fill=self.color_markings,width=2)) # 90, 270°
            marking_angle = [360/8*1,360/8*3,360/8*5,360/8*7]      
            for item in marking_angle:
                marking_items.append(Markings(self.canvas,370,item,70+60*2,item,fill=self.color_markings,width=2)) #
            marking_angle = [360/16*1,360/16*3,360/16*5,360/16*7,360/16*9,360/16*11,360/16*13,360/16*15]      
            for item in marking_angle:
                marking_items.append(Markings(self.canvas,370,item,70+60*3,item,fill=self.color_markings,width=2)) #
            marking_angle = [360/32*1,360/32*3,360/32*5,360/32*7,360/32*9,360/32*11,360/32*13,360/32*15,360/32*17,360/32*19,360/32*21,
                             360/32*23,360/32*25,360/32*27,360/32*29,360/32*31]      
            for item in marking_angle:
                marking_items.append(Markings(self.canvas,370,item,70+60*4,item,fill=self.color_markings,width=2)) #
           
            self.line1 = Lines(self.canvas,400,400,340,outline=self.color_markings,width=2)                        # Linien
            self.mover1 = Movers(self.canvas, x=400, y=400, r=360, start=90, extent=(360/32), outline=self.color_movers, fill=self.color_movers ,width=1)
            self.mover11 = Kreise(self.canvas, x=400, y=400, r=320, start=90, extent=(360/32)+2, outline=self.color_bg, fill=self.color_bg ,width=2)
     
            self.line2 = Lines(self.canvas,400,400,280,outline=self.color_markings,width=2)
            self.mover2 = Movers(self.canvas, x=400, y=400, r=300, start=90, extent=(360/16), outline=self.color_movers, fill=self.color_movers,width=1)
            self.mover22 = Kreise(self.canvas, x=400, y=400, r=260, start=90, extent=(360/16)+2, outline=self.color_bg, fill=self.color_bg ,width=2)
                         
            self.line3 = Lines(self.canvas,400,400,220,outline=self.color_markings,width=2)
            self.mover3 = Movers(self.canvas, x=400, y=400, r=240, start=90, extent=(360/8), outline=self.color_movers, fill=self.color_movers ,width=1)
            self.mover33 = Kreise(self.canvas, x=400, y=400, r=200, start=90, extent=(360/8)+2, outline=self.color_bg, fill=self.color_bg ,width=2)
           
            self.line4 = Lines(self.canvas,400,400,160,outline=self.color_markings,width=2)
            self.mover4 = Movers(self.canvas, x=400, y=400, r=180, start=90, extent=(360/4), outline=self.color_movers, fill=self.color_movers ,width=1)
            self.mover44 = Kreise(self.canvas, x=400, y=400, r=140, start=90, extent=(360/4)+2, outline=self.color_bg, fill=self.color_bg, width=2)
                                 
            self.line5 = Lines(self.canvas,400,400,100,outline=self.color_markings,width=2)
            self.mover5 = Movers(self.canvas, x=400, y=400, r=120, start=90, extent=(360/2), outline=self.color_movers, fill=self.color_movers ,width=1)
            self.mover55 = Kreise(self.canvas, x=400, y=400, r=80, start=90, extent=(360/2)+2, outline=self.color_bg, fill=self.color_bg ,width=2)
     
            self.pulsar = Pulsar(self.canvas,400,400,60,outline=self.color_movers,fill=self.color_movers,width=1)        # Pulsar
            #self.canvas.lift(self.movers[item])
            #self.canvas.lift(self.circles[item])
           
            #print(self.uhr.anzeigen(), 'class init GUI done')
            self.update_time()              # Mainloop
            ###### Init finished #####
     
     
        def callback(self, *event):
            self.speed = self.speed_slider.get()
            if 0 < self.speed and self.speed <= 10:
                self.speed = self.speed / 10
            elif 10 < self.speed and self.speed <= 20:
                self.speed = self.speed / 5
            elif 20 < self.speed and self.speed <= 30:
                self.speed = self.speed / 2.5
            elif 30 < self.speed and self.speed <= 40:
                self.speed = self.speed / 2
            elif 40 < self.speed and self.speed <= 50:
                self.speed = self.speed / 1.5
               
            self.counter += self.speed
     
            if self.start_stop.get():    
                if  self.counter >= 100:
                    self.counter = 0
                    self.animation_mover()
                self.animation_pulsar()
     
        def update_time(self):
            self.strv_uhrzeit.set(self.uhr.anzeigen())                          # Loop for animation
            self.strv_zeitangabe.set(self.uhr.hms_anzeigen())                   # Show the actual time on top of the window
                                                                                # schedule timer to call myself after a defined time in ms
            self.master.after(self.cycle_time, self.update_time)                # Mainloop
     
        def exitprogramm(self,*event):
            self.master.destroy()
     
        def startbutton(self):
            if not self.start_stop.get():
                self.start_stop.set(True)
                self.bStart.config(text='Stop',bg='green')
            else:
                self.start_stop.set(False)
                self.bStart.config(text='Start',bg='red')            
     
        def animation_mover(self):
            '''
           Mover Rotation Increments per 1 Second:
           
           reference:      http://www.bartelmus.org/binar-uhr/#more-136
     
           In dieser Implementierung existieren 5 Zeiger.
           Die Zahlensysteme für die Zeiger sind dabei: (2, 4, 8, 16, 32).
     
           Die Größen der Zeiger (in Bezug zu einen Gesamtkreis) sind von innen nach aussen: (1/2, 1/4, 1/8, 1/16, 1/32).
           Der innerste Kreis dient nur als Stilelement und hat keine Funktion.
     
           Die Bedingung für eine vollständige Umdrehung eines Zeigers ist die Umdrehung des
           nächstinneren Zeigers um genau den Umkehrwert seiner Größe im Bezug auf einen Kreis.
     
           Z.B.: der dritte Zeiger vollzieht genau dann eine vollständige Umdrehung,
           wenn der zweite Zeiger 4 Umdrehungen vollzogen hat.
     
           Wenn 24 Stunden vergangen sind, sind alle Teilkreise bis auf den kleinsten um den Umkehrwert ihrer Größe gewandert.
           Der kleinste (äußerste) Kreis hat dann eine Umdrehung erreicht.
     
           24h entspricht 24*60*60s = 86400s
           -----------------------------------------------------------------------------
             2 * 1/2    2   8   64  1024    * 360° =>> 1024*360°/86400s ==> 4,2666 °/s
             4 * 1/4    1   4   32  512 * 360° =>>  512*360°/86400s ==> 2,1333 °/s
             8 * 1/8        1   8   128 * 360° =>>  128*360°/86400s ==> 0,5333 °/s
            16 * 1/16           1   16  * 360° =>>   16*360°/86400s ==>
            32 * 1/32               1   * 360° =>>    1*360°/86400s ==>
           '''
            self.mover1_inc = 360/86400*1           # The Incredements each mover should move per one cycle
            self.mover2_inc = 360/86400*16
            self.mover3_inc = 360/86400*128
            self.mover4_inc = 360/86400*512
            self.mover5_inc = 360/86400*1024
           
            self.mover5.rotate(self.mover5_inc)     # The Movers
            self.mover4.rotate(self.mover4_inc)
            self.mover3.rotate(self.mover3_inc)
            self.mover2.rotate(self.mover2_inc)
            self.mover1.rotate(self.mover1_inc)
           
            self.mover55.rotate(self.mover5_inc)    # The cover circles to hide the arcs
            self.mover44.rotate(self.mover4_inc)
            self.mover33.rotate(self.mover3_inc)
            self.mover22.rotate(self.mover2_inc)
            self.mover11.rotate(self.mover1_inc)
     
        def animation_pulsar(self):
            self.pulsar.puls()        
     
        def reset(self):
            if self.start_stop.get():
                self.start_stop.set(False)
                self.bStart.config(text='Start',bg='red')
           
            self.mover5.reset()
            self.mover4.reset()
            self.mover3.reset()
            self.mover2.reset()
            self.mover1.reset()
            self.pulsar.reset()
     
            self.mover55.reset()
            self.mover44.reset()
            self.mover33.reset()
            self.mover22.reset()
            self.mover11.reset()
           
     
    class Markings():
        def __init__(self, canvas, *args, **kwargs):
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lift(self.id)
     
        def create(self,canvas,radius_1,angle_1,radius_2,angle_2,fill,width):
            self.canvas = canvas
            self.x1, self.y1 = self.conv_pol_to_xy_coords(radius_1,angle_1)
            self.x2, self.y2 = self.conv_pol_to_xy_coords(radius_2,angle_2)    
            item = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill, width=width, tags="marking_line")
            return item
     
        def conv_pol_to_xy_coords(self,radius,angle,offsetx=400,offsety=400):   # Funktion konvertiert Polar-Koords in XY-Koords
            self.direction = 1
            self.angle_offset = 90
            self.angle = self.angle_offset - angle
            coord_x = offsetx+radius*round(cos(radians(self.direction*self.angle)),3)      #berechnete Soll-Position am Kreis in X mit 3 Dezimalstellen
            coord_y = offsety+radius*round(sin(radians(self.direction*(-self.angle))),3)     #berechnete Soll-Position am Kreis in Y mit 3 Dezimalstellen
            return coord_x, coord_y
     
     
    class Lines():
        def __init__(self, canvas, *args, **kwargs):
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lift(self.id)
     
        def create(self,canvas,x,y,r,outline,width):
            self.canvas = canvas
            item = canvas.create_oval(x-r,y-r,x+r,y+r,outline=outline,width=width, tags='outline')
            return item
     
    class Kreise():
        def __init__(self, canvas, *args, **kwargs):
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lower(self.id)
            self.angleOffset = -90 + 1
            self.direction= -1
            self.angle = 0
            self.radius = 200
            self.line_length = 0
     
        def create(self,canvas,x,y,r,start,extent,outline,fill,width):
            self.canvas = canvas
            item = canvas.create_arc(x-r,y-r,x+r,y+r,start=start,extent=extent,outline=outline,fill=fill,width=width, tags='circle')
            return item
         
        def rotate(self,increment):
            #x1, y1, x2, y2 = self.canvas.bbox(self.id)
            self.increment = increment
             
            self.canvas.itemconfig(self.id, start=self.direction*(self.angle+self.angleOffset))       # Changes the start angle
     
            if self.angle >= 360.0:
                self.angle -= 360.0
             
            self.angle += self.increment
                   
     
        def output_angle(self):
            return self.angle
     
        def reset(self):
            self.angle = 0
            self.canvas.itemconfig(self.id, start=self.direction*(self.angle+self.angleOffset))
     
     
    class Movers():
        def __init__(self, canvas, *args, **kwargs):
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lower(self.id)
            self.angleOffset = -90
            self.direction= -1
            self.angle = 0
     
     
        def create(self,canvas,x,y,r,start,extent,outline,fill,width):
            self.canvas = canvas
            item = canvas.create_arc(x-r,y-r,x+r,y+r,start=start,extent=extent,outline=outline,fill=fill,width=width, tags='mover')
            return item
         
        def rotate(self,increment):
            #x1, y1, x2, y2 = self.canvas.bbox(self.id)
            self.increment = increment
             
            self.canvas.itemconfig(self.id, start=self.direction*(self.angle+self.angleOffset))       # Changes the start angle
     
            if self.angle >= 360.0:
                self.angle -= 360.0
            self.angle += self.increment
                   
        def reset(self):
            self.angle = 0
            self.canvas.itemconfig(self.id, start=self.direction*(self.angle+self.angleOffset))
     
           
    class Pulsar():
        def __init__(self, canvas, *args, **kwargs):
            self.uhr = Uhrzeit()
           
            self.canvas = canvas
            self.id = self.create(self.canvas, *args, **kwargs)        
            #self.canvas.lift(self.id)
     
        def create(self,canvas,x,y,r,outline,fill,width):
            self.canvas = canvas
            item = canvas.create_oval(x-r,y-r,x+r,y+r,outline=outline, fill=fill ,width=width,tags='pulsar')
            return item
           
        def puls(self):
            self.micros = self.uhr.get_micros()
            micros_len_pointer = self.micros/1000 * 60
            self.canvas.coords(self.id, 400 - micros_len_pointer, 400 - micros_len_pointer, 400 + micros_len_pointer, 400 + micros_len_pointer)
     
     
        def reset(self):
            micros_len_pointer = 60
            self.canvas.coords(self.id, 400 - micros_len_pointer, 400 - micros_len_pointer, 400 + micros_len_pointer, 400 + micros_len_pointer)    
     
     
    def main():
        root = tk.Tk()
        ui = GUI(root)
        root.mainloop()
     
     
    if __name__ == '__main__':
        main()
