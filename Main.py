import pygame, sys
from pygame.locals import *
from random import randint

width = 640
height = 480

class Nave(pygame.sprite.Sprite):
    
    vivo = True
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("nave.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = height - height/10
        self.speed = 0.3
        
    def mover(self,t,keys):
        if self.vivo:
            if self.rect.left >= 0:
                if keys[K_a]:
                    self.rect.centerx -= self.speed*t
            if self.rect.right <= width:
                if keys[K_d]:
                    self.rect.centerx += self.speed*t
                      
    def muerte(self):
        self.vivo = False
        self.image = pygame.image.load("explosion.png")
               
class Alien_amarillo(pygame.sprite.Sprite):
    
    vivo = True
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien_amarillo.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0.2
        self.speedy = 1
                        
    def update(self,t):
        if self.vivo:
            self.rect.centerx += self.speedx*t
            if self.rect.left <= 0:
                self.speedx *= -1.1
                self.rect.centerx += self.speedx*t
                self.rect.centery += self.speedy*t
                
            if self.rect.right >= width:
                self.speedx *= -1.1
                self.rect.centerx += self.speedx*t
                self.rect.centery += self.speedy*t
        else:
            self.rect.centery += self.speedy*t*0.1
    
    def muerte(self):
        self.vivo = False
        self.image = pygame.image.load("alien2_amarillo.png")

class Bala(pygame.sprite.Sprite):
    
    en_espera = True
    def __init__(self, x, y, i):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bala2.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 0.5*i

    def update(self,t):
        if not self.en_espera:
            self.rect.centery -= self.speed*t
    
    def desaparicion(self, nave):
        self.en_espera = True
        self.image = pygame.image.load("bala2.png")
        self.rect.centery = nave.rect.centery
        self.rect.centerx = nave.rect.centerx
            
    def disparo(self, nave):
        self.image = pygame.image.load("bala.png")
        self.rect= self.image.get_rect()
        self.rect.centery = nave.rect.centery
        self.rect.centerx = nave.rect.centerx
        self.en_espera = False
    
    def disparo_alien(self, alien):
        self.image = pygame.image.load("bala.png")
        self.rect= self.image.get_rect()
        self.rect.centery = alien.rect.centery
        self.rect.centerx = alien.rect.centerx
        self.en_espera = False
        
class Alien_verde(pygame.sprite.Sprite):#Solo intentara matar
    
    vivo = True
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien_verde.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0.5
        self.speedy = 0
    
    def update(self,t):
        if self.vivo:
            self.rect.centerx += self.speedx*t
            if self.rect.left <= 0:
                self.speedx *= -1
                self.rect.centerx += self.speedx*t
                self.rect.centery += self.speedy*t
                
            if self.rect.right >= width:
                self.speedx *= -1
                self.rect.centerx += self.speedx*t
                self.rect.centery += self.speedy*t
        else:
            self.rect.centery += 0.1*t
    def muerte(self):
        self.vivo = False
        self.image = pygame.image.load("alien2_verde.png")

class Asteroide(pygame.sprite.Sprite):
    
    def __init__(self):
        self.image = pygame.image.load("asteroide.png")
        self.speed = randint(1,20)/2
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(1,width)
        self.rect.centery = 0
        
    def update(self,t):
        self.rect.centery += self.speed*t*0.1
    
    def reiniciar(self):
        if self.rect.centery >= height:
            self.rect.centery = 0
            self.rect.centerx = randint(1, width)

        
def text(texto, posx, posy, color, t):
    font = pygame.font.Font('DroidSans.ttf', t)
    output = pygame.font.Font.render(font, texto, 1, color)
    output_rect = output.get_rect()
    output_rect.centerx = posx
    output_rect.centery = posy
    return output, output_rect


def main():
    
    juego = True
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space Invaders")
    screen.fill([0,0,0])
    clock = pygame.time.Clock()
    bala_jug = Bala(nave.rect.centerx, nave.rect.centery,1)
    bala_alien_amarillo = Bala(alien_amarillo.rect.centerx, alien_amarillo.rect.centery,-1)
    bala_alien_verde = Bala(alien_verde.rect.centerx, alien_verde.rect.centery, -1)
    fondo = pygame.image.load("fondo.png")
    asteroides = []
    balas = [bala_jug, bala_alien_amarillo, bala_alien_verde]
    fin = True
        
    for i in range(10):
        asteroides.append(Asteroide())
            
    while juego:
        
        t = clock.tick(30)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)

        nave.mover(t, keys)
           
        if keys[K_p] and bala_jug.en_espera:
            bala_jug.disparo(nave)
        if alien_verde.vivo and bala_alien_verde.en_espera:
            bala_alien_verde.disparo_alien(alien_verde)
        if randint(1,100) == 1 and alien_amarillo.vivo:
            bala_alien_amarillo.disparo_alien(alien_amarillo)
            
        for bala in balas:
            bala.update(t)
        
        for alien in aliens:
            if pygame.sprite.collide_rect(alien, bala_jug):
                alien.muerte()
                bala_jug.desaparicion(nave)        
        if pygame.sprite.collide_rect(nave,bala_alien_amarillo) or pygame.sprite.collide_rect(nave,bala_alien_verde):
            nave.muerte()
            juego = False
        for asteroide in asteroides:
            if pygame.sprite.collide_rect(nave, asteroide):
                nave.muerte()
                juego = False    
        if alien_amarillo.rect.bottom >= 9*height/10 and alien_amarillo.vivo:
            juego = False
        
        
        if bala_jug.rect.centery <= 0 and not bala_jug.en_espera:    
            bala_jug.desaparicion(nave)
        if bala_alien_amarillo.rect.centery >= height and not bala_alien_amarillo.en_espera:
            bala_alien_amarillo.desaparicion(alien_verde)
        if bala_alien_verde.rect.centery >= height and not bala_alien_verde.en_espera:
            bala_alien_verde.desaparicion(alien_verde)
                    
        for alien in aliens:
            alien.update(t)
            
        if not alien_verde.vivo and not alien_amarillo.vivo:
            juego = False
            
        screen.blit(fondo, (0,0))
        for asteroide in asteroides:
            asteroide.update(t)
            asteroide.reiniciar()
            screen.blit(asteroide.image, asteroide.rect)
        for bala in balas:
            screen.blit(bala.image, bala.rect)
        screen.blit(nave.image, nave.rect)
        for alien in aliens:
            screen.blit(alien.image, alien.rect)
        pygame.display.flip()


    while fin:
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        if keys[K_SPACE]:
            fin = False            
        gameover, gameover_rect = text("GAME OVER", width/2, height/2, [255,255,255], 30)
        press_space, press_space_rect = text("Press space to try again", width/2, height*6/10, [255,255,255], 30)
        screen.blit(gameover, gameover_rect)
        screen.blit(press_space, press_space_rect)
        pygame.display.flip()
                
                
if __name__ == '__main__':
    pygame.init()
    start = False
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Demo")
    while True:
        nave = Nave()
        alien_amarillo = Alien_amarillo(randint(30, width-30),height/4)
        alien_verde = Alien_verde(randint(30, width-30), height/5)
        aliens = [alien_amarillo, alien_verde]
        screen.fill([0,0,0])
        keys = pygame.key.get_pressed()
        if keys[K_RETURN]:
            start = True
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        press_start, press_start_rect = text("Press start", width/2, height*6/10, [255,255,255], 30)
        titulo, titulo_rect = text("Demo", width/2, height/2, [255,255,255], 40)
        instrucciones1, instrucciones1_rect = text("Esquiva los asteroides y balas, mientras matas al alien", width/2, height/5, [255,255,255], 20)
        instrucciones2, instrucciones2_rect = text("'P' para disparar, 'A' y 'D' para moverse", width/2, height/4, [255,255,255], 20)
        screen.blit(titulo, titulo_rect)
        screen.blit(press_start, press_start_rect)
        screen.blit(instrucciones1, instrucciones1_rect)
        screen.blit(instrucciones2, instrucciones2_rect)
        pygame.display.flip() 
        if start:
            main()
            start = False