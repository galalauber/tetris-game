#Neopixel
#https://docs.micropython.org/en/latest/library/neopixel.html
#https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
#Exemplo do uso de canvas: https://wokwi.com/projects/330751728413573715
#Outro exemplo: https://github.com/wokwi/wokwi-features/issues/237
#Exemplos da bilbioteca: https://wokwi.com/arduino/libraries/Adafruit_NeoPixel
#Tetris online: https://tetris.com/play-tetris

import time
import machine, neopixel

from machine import Pin

# create an input pin on pin #2, with a pull up resistor
botaoEsq = Pin(34, Pin.IN, Pin.PULL_UP) #Pull-up interno não funcionou
botaoDir = Pin(21, Pin.IN, Pin.PULL_UP)
botaoRot = Pin(25, Pin.IN, Pin.PULL_UP)

#This configures a NeoPixel strip on GPIO4 with 16 pixels. 
#You can adjust the “4” (pin number) and the “16” (number of pixel) 
#to suit your set up.
np = neopixel.NeoPixel(machine.Pin(4), 16)
linhas = 14     #O objeto canvas só funciona com linhas pares
colunas = 10    #O objeto canvas só funciona com linhas pares
posicao = (0,0)
#Neopixel
#https://docs.micropython.org/en/latest/library/neopixel.html
#https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
#Exemplo do uso de canvas: https://wokwi.com/projects/330751728413573715
#Outro exemplo: https://github.com/wokwi/wokwi-features/issues/237
#Exemplos da bilbioteca: https://wokwi.com/arduino/libraries/Adafruit_NeoPixel
#Tetris online: https://tetris.com/play-tetris

import time
import machine, neopixel

from machine import Pin

# create an input pin on pin #2, with a pull up resistor
botaoEsq = Pin(34, Pin.IN, Pin.PULL_UP) #Pull-up interno não funcionou
botaoDir = Pin(21, Pin.IN, Pin.PULL_UP)
botaoRot = Pin(25, Pin.IN, Pin.PULL_UP)

#This configures a NeoPixel strip on GPIO4 with 16 pixels. 
#You can adjust the “4” (pin number) and the “16” (number of pixel) 
#to suit your set up.
np = neopixel.NeoPixel(machine.Pin(4), 16)

#Matriz canvas
linhas = 14     #O objeto canvas no Wokwi só funciona com linhas pares
colunas = 10    #O objeto canvas no Wokwi só funciona com linhas pares
posicao = (0,0)
npm = neopixel.NeoPixel(machine.Pin(4), linhas*colunas)

def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

def teste_linhas_colunas(c, l):
    total = l*c
    # Sequência
    # Apaga todos
    #for i in range(l):
    #    for j in range(c):
    #        npm[i*c+j] = (0, 0, 0)
    npm.fill((0,0,0))
    npm.write()
    time.sleep_ms(250)
    # Acende um por vez
    for i in range(l):
        for j in range(c):
            npm[i*c+j] = (255, 255, 255)
            npm.write()
            time.sleep_ms(25)

def limpa_matriz(cor):
    npm.fill(cor)
    npm.write()
    posicao = (0, 0)

#Desloca de um ponto a outro
def desloca(origem, destino, cor_fundo, cor_pixel, tempo):
    ox = origem[0]
    oy = origem[1]
    dx = destino[0]
    dy = destino[1]
    deltax = dx-ox
    deltay = dy-oy
    
    if deltax < 0:
        mdeltax = -deltax
    else:
        mdeltax = deltax
    
    if  deltay < 0:
        mdeltay = -deltay
    else:
        mdeltay = deltay

    if mdeltax > mdeltay:
        if ox < dx:
            while ox <= dx:
                pixel = ox + oy*colunas
                npm.__setitem__(pixel, cor_fundo)
                npm.write()
                npm.__setitem__(pixel, cor_pixel)
                npm.write()
                time.sleep_ms(tempo)
                ox = ox + 1
                if oy < dy:
                    oy = oy+1
                elif oy > dy:
                    oy = oy-1
            ox = ox - 1
        else:
            while ox >= dx:
                pixel = ox + oy*colunas
                npm.__setitem__(pixel, cor_fundo)
                npm.write()
                npm.__setitem__(pixel, cor_pixel)
                npm.write()
                time.sleep_ms(tempo)
                ox = ox - 1
                if oy < dy:
                    oy = oy+1
                elif oy > dy:
                    oy = oy-1
            ox = ox + 1
    else:
        if oy < dy:
            while oy <= dy:
                pixel = ox + oy*colunas
                npm.__setitem__(pixel, cor_fundo)
                npm.write()
                npm.__setitem__(pixel, cor_pixel)
                npm.write()
                time.sleep_ms(tempo)
                oy = oy + 1
                if ox < dx:
                    ox = ox+1
                elif ox > dx:
                    ox = ox-1
            oy = oy - 1
        else:
            while oy >= dy:
                pixel = ox + oy*colunas
                npm.__setitem__(pixel, cor_fundo)
                npm.write()
                npm.__setitem__(pixel, cor_pixel)
                npm.write()
                time.sleep_ms(tempo)
                oy = oy - 1
                if ox < dx:
                    ox = ox+1
                elif ox > dx:
                    ox = ox-1
            oy = oy + 1
    
    posicao = (ox, oy)
    print(posicao)
    return posicao

#Desloca partindo do ponto atual
def desloca2(offset, cor_fundo, cor_pixel, tempo):
    destino = (0,0)
    destinox = posicao[0]+offset[0]
    destinoy = posicao[1]+offset[1]
    destino = (destinox, destinoy)
    # print(destino)
    return desloca(posicao, destino, cor_fundo, cor_pixel, tempo)

while True:
    demo(np)
    #Teste 1 - Preenche linhas e colunas com delay
    '''
    teste_linhas_colunas(colunas, linhas)
    #'''
    #Teste 2 - Limpeza da matriz
    '''
    limpa_matriz((255, 255, 255))
    time.sleep_ms(1000)
    limpa_matriz((000, 255, 000))
    time.sleep_ms(1000)
    limpa_matriz((000, 000, 255))
    time.sleep_ms(1000)
    #'''
    #Teste 3 - Desloca um pixel dentre os pontos de origem e destino por tempo
    '''
    desloca((9,12), (1,15), (255,255,255), (255,0,0), 100)
    #'''
    #Teste 4 - Define um pixel de desloca (sem classe)
    '''
    posicao = (2,10)
    desloca2((3, 0), (255,255,255), (255,0,0), 100)
    #'''