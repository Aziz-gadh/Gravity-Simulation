import pygame as pg
from object import Object
from settings import WIDTH,HEIGHT,FPS,max_rad,system,scroll
pg.init()
clock=pg.time.Clock()
screen=pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('GRAVITY simulation')
running=True
object=None
holding=False
bg=pg.Surface(screen.get_size())
view=pg.Rect(0,0,WIDTH,HEIGHT)
while running:
    screen.blit(bg,(0,0),area=view)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            system.empty()
            running=False
        elif event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE:
            system.empty()
        elif event.type==pg.MOUSEBUTTONDOWN:
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
        elif event.type==pg.KEYDOWN and event.key==pg.K_RIGHT:
            view.x+=scroll
        elif event.type==pg.KEYDOWN and event.key==pg.K_LEFT:
            view.x-=scroll
        elif event.type==pg.KEYDOWN and event.key==pg.K_DOWN:
            view.y+=scroll
        elif event.type==pg.KEYDOWN and event.key==pg.K_UP:
            view.y-=scroll
    if holding and object and object.radius<=max_rad:
        object.increase()
    system.update(screen)
    pg.display.update()
    clock.tick(FPS)
pg.quit()