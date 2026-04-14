import pygame as pg
from object import Object
from settings import WIDTH,HEIGHT,FPS,rate,strt_rad,max_rad,ms
pg.init()
clock=pg.time.Clock()
screen=pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('GRAVITY simulation')
running=True
system=pg.sprite.Group()
object=None
while running:
    screen.fill('#000000')
    holding=False
    score=sum(list(map(lambda x:x.mass,system)))
    for event in pg.event.get():
        if event.type == pg.QUIT or score>=WIDTH*HEIGHT*ms:
            system.empty()
            running=False
        elif event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE:
            system.empty()
        elif event.type==pg.MOUSEBUTTONDOWN:
            time=0
            for obj in system:
                object=obj if obj.stimulate(pg.mouse.get_pos()) else None
            if not object:
                object=Object(pg.mouse.get_pos(),min(time*rate+strt_rad,max_rad))
                system.add(object)
            holding=True
        elif event.type==pg.MOUSEBUTTONUP:
            holding=False
            object.locked=False
            object.vel=[0,0]
            object=None
            time=0
    dt=1000/FPS
    if holding:
        time+=dt
    system.update(system,screen)
    pg.display.update()
    clock.tick(FPS)
print(round(score,3))
pg.quit()