import pygame as pg
from settings import G,mv,dt,friction,strt_rad,rate,WIDTH,HEIGHT
from math import sqrt,pi

def mul(ls,cf):
    return [cf*x for x in ls]

class Object(pg.sprite.Sprite):
    def __init__(self,pos,radius=strt_rad,locked=True,vel=[0,0]):
        super().__init__()
        self.center=list(pos)
        self.vel=vel
        if (radius**2)*pi<=WIDTH*HEIGHT:
            self.mass=4*pi*mv*(radius**3)/3
            self.radius=radius
        else:
            print("screen filled")
            exit(1)
        self.locked=locked
    def smash(self,group,obj):
        self.mass+=obj.mass
        group.add(Object(self.center,radius=(3*self.mass/(4*pi*mv))**(1/3),locked=False,vel=self.vel))
        obj.kill()
        self.kill()
    def update(self,group,screen):
        dv=mul(self.vel,friction*dt/self.mass)
        #add proper collision
        for obj in group:
            distance=sqrt((obj.center[0]-self.center[0])**2 + (obj.center[1]-self.center[1])**2)
            if self==obj:
                continue
            acc=(G*obj.mass)/distance**2
            cos=(obj.center[0]-self.center[0])/distance
            sin=(obj.center[1]-self.center[1])/distance
            dv=[dv[0]+acc*cos*dt,dv[1]+acc*sin*dt]
        if not self.locked:
            self.vel=[self.vel[0]+dv[0],self.vel[1]+dv[1]]
            self.vel=mul(self.vel,dt)
            self.center=[self.vel[0]+self.center[0],self.vel[1]+self.center[1]]
        pg.draw.circle(surface=screen,color='#ffffff',center=(self.center[0],self.center[1]),radius=self.radius)
    def stimulate(self,pos):
        distance=sqrt((pos[0]-self.center[0])**2 + (pos[1]-self.center[1])**2)
        if distance<=self.radius:
            self.vel=mul(self.vel,2)
            self.locked=True
            return True
        return False
    def increase(self):
        self.radius+=rate
        self.mass=4*pi*mv*(self.radius**3)/3