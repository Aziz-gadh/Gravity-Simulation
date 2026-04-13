import pygame as pg
from settings import G,ms
from math import sqrt,pi

def mul(ls,cf):
    return [cf*x for x in ls]

class Object(pg.sprite.Sprite):
    def __init__(self,pos,radius):
        super().__init__()
        self.center=list(pos)
        self.vel=[0,0]
        self.mass=pi*ms*(radius**2)
        self.radius=radius
        self.locked=True
    def smash(self,obj):
        if obj==self:
            return
        mv1=mul(self.vel,self.mass)
        mv2=mul(obj.vel,obj.mass)
        mm=[mv1[0]+mv2[0],mv1[1]+mv2[1]]
        self.mass+=obj.mass
        self.vel=mul(mm,1/self.mass)
        self.radius=sqrt(self.mass/(ms*pi))
        obj.kill()
    def update(self,group,screen):
        for obj in group:
            distance=sqrt((obj.center[0]-self.center[0])**2 + (obj.center[1]-self.center[1])**2)
            if distance==0:
                self.smash(obj)
                continue
            acc=(G*obj.mass)/distance**2
            cos=(obj.center[0]-self.center[0])/distance
            sin=(obj.center[1]-self.center[1])/distance
            dv=[acc*cos,acc*sin]
            if not self.locked:
                self.vel=[self.vel[0]+dv[0],self.vel[1]+dv[1]]
                self.center=[self.vel[0]+self.center[0],self.vel[1]+self.center[1]]
        pg.draw.circle(surface=screen,color='#ffffff',center=(self.center[0],self.center[1]),radius=self.radius)
    def stimulate(self,pos):
        distance=sqrt((pos[0]-self.center[0])**2 + (pos[1]-self.center[1])**2)
        if distance<=self.radius:
            self.vel=mul(self.vel,2)
            self.locked=True
            return True
        return False