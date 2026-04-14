import pygame as pg
from settings import G,mv,dt,friction,strt_rad,rate,WIDTH,HEIGHT,system
from math import sqrt,pi

def mul(ls,cf):
    return [cf*x for x in ls]

class Object(pg.sprite.Sprite):
    def __init__(self,pos,radius=strt_rad,locked=True,vel=[0,0]):
        super().__init__()
        self.vel=vel
        if (radius**2)*pi<=WIDTH*HEIGHT:
            self.mass=4*pi*mv*(radius**3)/3
            self.radius=radius
        else:
            print("screen filled")
            exit(1)
        self.locked=locked
        self.rect=pg.Rect(*pos,2*self.radius,2*self.radius)
    def smash(self,obj):
        self.vel=(mul(self.vel,self.mass)+mul(obj.vel,obj.mass))
        self.mass+=obj.mass
        self.vel=mul(self.vel,1/self.mass)
        system.add(Object(self.rect.center,radius=(3*self.mass/(4*pi*mv))**(1/3),locked=False,vel=self.vel))
        obj.kill()
        self.kill()
    def update(self,screen):
        dv=mul(self.vel,friction*dt/self.mass)
        for obj in pg.sprite.spritecollide(self,system,False):
            if obj==self:
                continue
            self.smash(obj)
        for obj in system:
            distance=sqrt((obj.rect.centerx-self.rect.centerx)**2 + (obj.rect.centery-self.rect.centery)**2)
            if self==obj:
                continue
            acc=(G*obj.mass)/distance**2
            cos=(obj.rect.centerx-self.rect.centerx)/distance
            sin=(obj.rect.centery-self.rect.centery)/distance
            dv=[dv[0]+acc*cos*dt,dv[1]+acc*sin*dt]
        if not self.locked:
            self.vel=[self.vel[0]+dv[0],self.vel[1]+dv[1]]
            self.vel=mul(self.vel,dt)
            self.rect.centerx+=self.vel[0]
            self.rect.centery+=self.vel[1]
        pg.draw.circle(surface=screen,color='#ffffff',center=(self.rect.centerx,self.rect.centery),radius=self.radius)
    def stimulate(self,pos):
        distance=sqrt((pos[0]-self.rect.centerx)**2 + (pos[1]-self.rect.centery)**2)
        if distance<=self.radius:
            self.vel=mul(self.vel,2)
            self.locked=True
            return True
        return False
    def increase(self):
        self.radius+=rate
        self.mass=4*pi*mv*(self.radius**3)/3