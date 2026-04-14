import pygame as pg
from object import Object
from settings import WIDTH,HEIGHT,FPS,max_rad
pg.init()
clock=pg.time.Clock()
screen=pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('GRAVITY simulation')
running=True
system=pg.sprite.Group()
object=None
holding=False
while running:
    screen.fill('#000000')
    for event in pg.event.get():
        if event.type == pg.QUIT:
            system.empty()
            running=False
        elif event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE:
            system.empty()
        elif event.type==pg.MOUSEBUTTONDOWN:
            time=0
            for obj in system:
                object=obj if obj.stimulate(pg.mouse.get_pos()) else None
            if not object:
                object=Object(pg.mouse.get_pos())
                system.add(object)
            holding=True
        elif event.type==pg.MOUSEBUTTONUP:
            holding=False
            object.locked=False
            object.vel=[0,0]
            object=None
            time=0
    if holding and object and object.radius<=max_rad:
        object.increase()
    system.update(system,screen)
    pg.display.update()
    clock.tick(FPS)
pg.quit()