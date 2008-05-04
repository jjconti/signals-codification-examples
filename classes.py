# -*- coding: utf-8 -*-
import string
import sys
import math

import pygame
from pygame.locals import *

from config import *

class BandaBase(pygame.sprite.Sprite):
    
    def __init__(self, binary):
        pygame.sprite.Sprite.__init__(self)
        self.title = u"Banda Base"
        self.binary = binary
        self.size = 200
        self.step = 50
        self.ytopmargin = 60
        self.ybottommargin = 20
        self.amp = self.size - self.ytopmargin - self.ybottommargin
        self.bottom =  self.size - self.ybottommargin
        self.image = pygame.Surface((WINDOW[0], self.size))
        self.rect = self.image.get_rect().move(0,200)

    def update(self):
        self.image.fill(COLOR2)
        font = pygame.font.Font(None, 40)
        name = font.render(self.title, True, BLACK)
        self.image.blit(name, (10,10))
        x = self.step
        y = self.bottom
        self._update(x, y)

    def _update(self, x, y):
        for bit in self.binary.binary:
            if bit == '0':
                if y == self.ytopmargin:
                    pygame.draw.line(self.image, BLACK, (x,y), (x, self.bottom), 2)
                    y = self.bottom
                pygame.draw.line(self.image, BLACK, (x,y), (x + self.step, y), 2)
            else:   # bit == '1'
                if y != self.ytopmargin:
                    pygame.draw.line(self.image, BLACK, (x,y), (x, self.ytopmargin), 2)
                    y = self.ytopmargin
                pygame.draw.line(self.image, BLACK, (x,y), (x + self.step, y), 2)
            x += self.step

class CodificacionManchester(BandaBase):
    
    def __init__(self, binary):
        '''
        Los valores 1 o 0 se identifican por el flanco creciento o decreciente
        de la señal y no por el valor muestreado del pulso.
        '''
        super(CodificacionManchester, self).__init__(binary)
        self.title = u"Codificación Manchester"

    def _update(self, x, y):
        for bit in self.binary.binary:
            if bit == '0':
                if y != self.ytopmargin:
                    #si está abajo, primero subir a señal
                    pygame.draw.line(self.image, BLACK, (x,y), (x, self.ytopmargin), 2)
                    y = self.ytopmargin
                pygame.draw.line(self.image, BLACK, (x,y), (x + self.step / 2, y), 2)
                x += self.step / 2
                pygame.draw.line(self.image, BLACK, (x,y), (x, self.bottom), 2)
                y = self.bottom
                pygame.draw.line(self.image, BLACK, (x,y), (x + self.step / 2, y), 2)
                x += self.step / 2
            else:   # bit == '1'
                if y == self.ytopmargin:
                    #si está arriba, primero bajar la señal
                    pygame.draw.line(self.image, BLACK, (x,y), (x, self.bottom), 2)
                    y = self.bottom
                pygame.draw.line(self.image, BLACK, (x,y), (x + self.step / 2, y), 2)
                x += self.step / 2
                pygame.draw.line(self.image, BLACK, (x,y), (x, self.ytopmargin), 2)
                y = self.ytopmargin
                pygame.draw.line(self.image, BLACK, (x,y), (x + self.step / 2, y), 2)
                x += self.step / 2

class CodificacionAMI(BandaBase):
    
    def __init__(self, binary):
        '''
        AMI o Alternate Mark Inversion es una codificacion del tipo bipolar por que
        genera un valor +V o -V alternado a los valores binarios 1. También es llamada
        Bipolar NRZ (no retorno a cero). 
        '''
        super(CodificacionAMI, self).__init__(binary)
        self.title = u"Codificación AMI"
        self.ycero = (self.ytopmargin + self.bottom) / 2 

    def _update(self, x, y):
        uno = 1
        for bit in self.binary.binary:
            if bit == '0':
                if y in (self.ytopmargin, self.bottom):
                    #volver a cero
                    pygame.draw.line(self.image, BLACK, (x,y), (x, self.ycero), 2)
                    y = self.ycero
                pygame.draw.line(self.image, BLACK, (x,y), (x + self.step, y), 2)
            else:   # bit == '1'
                if uno == 1:
                    #subir
                    pygame.draw.line(self.image, BLACK, (x,y), (x, self.ytopmargin), 2)
                    y = self.ytopmargin
                else:   #-1
                    #bajar
                    pygame.draw.line(self.image, BLACK, (x,y), (x, self.bottom), 2)
                    y = self.bottom
                #pulso
                pygame.draw.line(self.image, BLACK, (x,y), (x + self.step, y), 2)
                uno *= -1   #alternar
            x += self.step

class CodificacionHDB3(BandaBase):
    
    def __init__(self, binary):
        '''
        Binario de alta densidad de 3 ceros permitidos.
        '''
        super(CodificacionManchester, self).__init__(binary)
        self.title = u"Codificación HDB3"

    def _update(self, x, y):
        pass

class ModulacionFrecuencia(pygame.sprite.Sprite):
    
    def __init__(self, binary):
        pygame.sprite.Sprite.__init__(self)
        self.binary = binary
        self.size = 200
        self.step = 50
        self.ytopmargin = 50
        self.ybottommargin = 20
        self.amp = self.size - self.ytopmargin - self.ybottommargin
        self.bottom =  self.size - self.ybottommargin
        self.image = pygame.Surface((WINDOW[0], self.size))
        self.rect = self.image.get_rect().move(0,200 + self.size)

    def update(self):
        self.image.fill(COLOR1)
        font = pygame.font.Font(None, 40)
        name = font.render(u"Modulación en frecuencia", True, BLACK)
        self.image.blit(name, (10,10))
        x = self.step
        y = self.bottom
        #for bit in self.binary.binary:
            #if bit == '0':
                #self._draw_sin(1, x)
                #x += self.step
            #else:   # bit == '1'
                #self._draw_sin(1, x)
                #x += self.step

    def _draw_sin(self, freq, x1):
        definicion = 1
        x2 = x1 + self.step
        _sin = self._gen_sin(x1, x2)
        for i,j in zip(range(x1, x2), range(x1 + 1, x2 + 1)):
            y1 = self.amp - _sin(i) + self.ytopmargin
            y2  = self.amp - _sin(j) + self.ytopmargin
            pygame.draw.line(self.image, BLACK, (i,y1), (j,y2), 2)

    def _gen_sin(self, x1, x2):
        return lambda i: math.sin((i - x1) / float((x2 - x1)) * math.pi) * self.amp

class ModulacionCuadratura(pygame.sprite.Sprite):
    
    def __init__(self, binary):
        pygame.sprite.Sprite.__init__(self)
        self.binary = binary
        self.size = 150
        self.image = pygame.Surface((WINDOW[0], self.size))
        self.image.fill(COLOR1)
        font = pygame.font.Font(None, 40)
        name = font.render(u"Modulación en cuadratura", True, BLACK)
        self.image.blit(name, (0,0))
        self.rect = self.image.get_rect().move(0,200 + self.size)

    def update(self):
        pass

class TestCod(pygame.sprite.Sprite):
    
    def __init__(self, binary):
        pygame.sprite.Sprite.__init__(self)
        self.binary = binary
        self.size = 55
        self.ideal = self.get_ideal(self.binary.binary)
        self.image = pygame.Surface((self.size, self.size))

    def update(self):
        font = pygame.font.Font(None, self.size)
        self.ideal = self.get_ideal(self.binary.binary)
        self.image = font.render("Ideal: %s" % self.ideal, True, BLACK)
        self.rect = self.image.get_rect().move(200,200)
        
    def get_ideal(self, binary):
        def t(i):
            if i == '1':
                return '-'
            else:
                return '_'
        return "".join([t(x) for x in binary])

class Binary(pygame.sprite.Sprite):
    
    def __init__(self, ascii):
        pygame.sprite.Sprite.__init__(self)
        self.ascii = ascii
        self.size = 55
        self.binary = self.get_binary(self.ascii.ascii)
        self.image = pygame.Surface((self.size, self.size))

    def update(self):
        font = pygame.font.Font(None, self.size)
        self.binary = self.get_binary(self.ascii.ascii)
        self.image = font.render("Binario: %s" % self.binary, True, BLACK)
        self.rect = self.image.get_rect().move(200,75)
        
    def get_binary(self, n):
        r = ""
        while n != 1:
            r = str(n % 2) + r
            n /= 2

        return "1" + r
        
class Ascii(pygame.sprite.Sprite):
    
    def __init__(self, letter):
        pygame.sprite.Sprite.__init__(self)
        self.letter = letter
        self.size = 55
        self.ascii = ord(self.letter.letter)
        self.image = pygame.Surface((self.size, self.size))

    def update(self):
        font = pygame.font.Font(None, self.size)
        self.ascii = ord(self.letter.letter)
        self.image = font.render("ASCII: %d" % self.ascii, True, BLACK)
        self.rect = self.image.get_rect().move(200,20)

class Letter(pygame.sprite.Sprite):

    def __init__(self, letter="A"):
        pygame.sprite.Sprite.__init__(self)
        self.letter = letter
        self.size = 100
        self.image = pygame.Surface((self.size, self.size))

    def update(self):
        font = pygame.font.Font(None, self.size)
        self.image = font.render(self.letter, True, BLACK)
        self.rect = self.image.get_rect().inflate(15,15).move(15,15)
        
    def next(self):
        '''
        >>> l = Letter("A")
        >>> l.next()
        >>> l.letter == "B"
        True
        >>> l = Letter("Z")
        >>> l.next()
        >>> l.letter == "a"
        True
        >>> l = Letter("z")
        >>> l.next()
        >>> l.letter == "A"
        True
        '''
        next = ord(self.letter) + 1
        if next == ord("z") + 1:
            self.letter = "A"
        elif next == ord("Z") + 1:
            self.letter = "a"
        else:
            self.letter = chr(next)

    def prev(self):
        '''
        >>> l = Letter("A")
        >>> l.prev()
        >>> l.letter == "z"
        True
        >>> l = Letter("Z")
        >>> l.prev()
        >>> l.letter == "Y"
        True
        >>> l = Letter("z")
        >>> l.prev()
        >>> l.letter == "y"
        True
        '''
        prev = ord(self.letter) - 1
        if prev == ord("a") - 1:
            self.letter = "Z"
        elif prev == ord("A") - 1:
            self.letter = "z"
        else:
            self.letter = chr(prev)

    def set(self, letter):
        '''
        >>> l = Letter("A")
        >>> l.set("j")
        >>> l.letter == "j"
        True
        >>> l = Letter("A")
        >>> l.set("Ñ")
        >>> l.letter == "Ñ"
        False
        '''
        if letter in string.letters:
            self.letter = letter
 
class Label(pygame.sprite.Sprite):

    def __init__(self, text="", xy=(0,0), size=25, color=BLACK):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.size = size
        self.x, self.y = xy    #topleft
        self.color = BLACK
        self.image = pygame.Surface((self.size, self.size))

    def update(self):
        font = pygame.font.Font(None, self.size)
        self.image = font.render(self.text, True, self.color)
        self.rect = self.image.get_rect().inflate(10,10).move(self.x, self.y)

CODIFICACIONES = (BandaBase, CodificacionManchester, CodificacionAMI)
MODULACIONES = ()

class App(object):

    def __init__(self, screen):
        self.screen = screen
        self.letter = Letter()
        self.ascii = Ascii(self.letter)
        self.binary = Binary(self.ascii)
        self.codificacion = CODIFICACIONES[2](self.binary)
        self.modulacion = ModulacionFrecuencia(self.binary)
        self.widgets = pygame.sprite.OrderedUpdates()
        self.widgets.add(self.letter, self.ascii, self.binary, self.codificacion, self.modulacion)
        labels = [Label(u"(para transmisión digital)", (530, 380)), Label(u"(para transmisión analógica)", (530, 580))]
        self.widgets.add(labels)
        self.exit = False
        self.clock = pygame.time.Clock()

    def loop(self):
       pygame.display.flip()
       while not self.exit:

            self.clock.tick(100)
            
            self.screen.fill(WHITE)
            
            for event in pygame.event.get():
                self.control(event)
            
            self.update()
            self.draw()
            
            pygame.display.flip()
            
    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            self.keypress(event)
        elif event.type == MOUSEBUTTONDOWN:
            self.mouseclick(event) 
        
    def update(self):
        self.widgets.update()
        
    def mouseclick(self, event):
        if self.letter.rect.collidepoint(event.pos):
            self.letter.next()
            
    def keypress(self, event):
        if event.unicode:
            self.letter.set(event.unicode)
        
    def draw(self):
        self.widgets.draw(self.screen)
        
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
