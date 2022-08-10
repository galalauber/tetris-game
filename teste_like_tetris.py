#Neopixel
#https://docs.micropython.org/en/latest/library/neopixel.html
#https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
#Exemplo do uso de canvas: https://wokwi.com/projects/330751728413573715
#Outro exemplo: https://github.com/wokwi/wokwi-features/issues/237
#Exemplos da bilbioteca: https://wokwi.com/arduino/libraries/Adafruit_NeoPixel
#Tetris online: https://tetris.com/play-tetris

import time
import machine, neopixel
import sys

from machine import Pin

# create an input pin on pin #2, with a pull up resistor
botaoEsq = Pin(34, Pin.IN, Pin.PULL_UP) #Pull-up interno não funcionou
botaoDir = Pin(21, Pin.IN, Pin.PULL_UP)
botaoRot = Pin(25, Pin.IN, Pin.PULL_UP)

linhas = 15     #O objeto canvas só funciona com linhas pares
colunas = 10    #O objeto canvas só funciona com linhas pares
posicao = (0,0)

class like_tetris(neopixel.NeoPixel):
    def __init__(self, pino, col, lin, tipo_mat="t_linha"):
        self.colunas = col
        self.linhas = lin
        self.pixels = col*lin
        self.tipo_matriz = tipo_mat
        self.posicao = (0,0)
        neopixel.NeoPixel.__init__(self, pino, self.pixels)
    
    #Retorna o número do pixel de um ponto
    #Isso depende da forma construtiva da matriz
    def num_pixel(self, xy):
        if self.tipo_matriz == "t_linha":
            return xy[0] + xy[1]*self.colunas
        
        elif self.tipo_matriz == "t_linha_zig_zag":
            #Se é linha par (avança da esq. p/ dir.)
            if xy[1]%2 == 0:
                return xy[0] + xy[1]*self.colunas
            #Se é linha ímpar (avança da dir. p/ esq.)
            else:
                return colunas-1-xy[0] + xy[1]*self.colunas
        
        elif self.tipo_matriz == "t_coluna":
            return xy[0]*self.linhas + xy[1]
        
        elif self.tipo_matriz == "t_coluna_zig_zag":
            #Se é coluna par (avança da cima p/ baixo)
            if xy[0]%2 == 0:
                return xy[0]*self.linhas + xy[1]
            #Se é coluna ímpar (avança da vaixo p/ cima)
            else:
                return xy[0]*self.linhas + self.linhas-1-xy[1]
        
        else: #Tipo t_linha é o padrão
            return xy[0] + xy[1]*self.colunas
        #'''
    #Limpa a matriz todo com a cor escolhida
    def limpa_matriz(self, cor):
        neopixel.NeoPixel.fill(self, cor)
        neopixel.NeoPixel.write(self)
        self.posicao = (0, 0)
    
    #Desenha uma linha a parir de um ponto de origem até um ponto de destino
    def linha_od(self, origem, destino, cor_pixel, tempo):
        self.ox = origem[0]
        self.oy = origem[1]
        self.dx = destino[0]
        self.dy = destino[1]
        self.deltax = self.dx-self.ox
        self.deltay = self.dy-self.oy
        
        if self.deltax < 0:
            self.mdeltax = -self.deltax
        else:
            self.mdeltax = self.deltax
        
        if  self.deltay < 0:
            self.mdeltay = -self.deltay
        else:
            self.mdeltay = self.deltay

        if self.mdeltax > self.mdeltay:
            if self.ox < self.dx:
                while self.ox <= self.dx:
                    self.pixel = self.ox + self.oy*self.colunas
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
                    neopixel.NeoPixel.write(self)
                    time.sleep_ms(tempo)
                    self.ox = self.ox + 1
                    if self.oy < self.dy:
                        self.oy = self.oy+1
                    elif self.oy > self.dy:
                        self.oy = self.oy-1
                self.ox = self.ox - 1
            else:
                while self.ox >= self.dx:
                    self.pixel = self.ox + self.oy*self.colunas
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
                    neopixel.NeoPixel.write(self)
                    time.sleep_ms(tempo)
                    self.ox = self.ox - 1
                    if self.oy < self.dy:
                        self.oy = self.oy+1
                    elif self.oy > self.dy:
                        self.oy = self.oy-1
                self.ox = self.ox + 1
        else:
            if self.oy < self.dy:
                while self.oy <= self.dy:
                    self.pixel = self.ox + self.oy*colunas
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
                    neopixel.NeoPixel.write(self)
                    time.sleep_ms(tempo)
                    self.oy = self.oy + 1
                    if self.ox < self.dx:
                        self.ox = self.ox+1
                    elif self.ox > self.dx:
                        self.ox = self.ox-1
                self.oy = self.oy - 1
            else:
                while self.oy >= self.dy:
                    self.pixel = self.ox + self.oy*self.colunas
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
                    neopixel.NeoPixel.write(self)
                    time.sleep_ms(tempo)
                    self.oy = self.oy - 1
                    if self.ox < self.dx:
                        self.ox = self.ox+1
                    elif self.ox > self.dx:
                        self.ox = self.ox-1
                self.oy = self.oy + 1
        
        self.posicao = (self.ox, self.oy)
        print(self.posicao)
        return self.posicao

    #Desenha uma linha a parir do último ponto desenhado até de deslocamento desejado
    def linha_delta(self, offset, cor_pixel, tempo):
        self.destino = (0,0)
        self.destinox = self.posicao[0]+offset[0]
        self.destinoy = self.posicao[1]+offset[1]
        self.destino = (self.destinox, self.destinoy)
        # print(destino)
        return self.linha_od(self.posicao, self.destino, cor_pixel, tempo)

    #Desloca um pixel do ponto de origem ao ponto de destino respeitando o tempo
    #entre cada movimento
    def desloca_od(self, origem, destino, cor_fundo, cor_pixel, tempo):
        self.ox = origem[0]
        self.oy = origem[1]
        self.dx = destino[0]
        self.dy = destino[1]

        #Calcula o delta de deslocamento em x e y
        self.deltax = self.dx-self.ox
        self.deltay = self.dy-self.oy
        
        if self.deltax < 0:
            self.mdeltax = -self.deltax
        else:
            self.mdeltax = self.deltax
        
        if  self.deltay < 0:
            self.mdeltay = -self.deltay
        else:
            self.mdeltay = self.deltay
        
        #Desenha o pixel na origem
        self.pixel = self.ox + self.oy*self.colunas
        neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
        neopixel.NeoPixel.write(self)
        time.sleep_ms(tempo)

        #Se o delocamento em x é maior que em y
        if self.mdeltax > self.mdeltay:
            #Se o ponto de origem em x é menor que o destino
            if self.ox < self.dx:
                #Enquanto não chegar no destino
                while self.ox < self.dx:
                    #Apaga o pixel anterior
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_fundo)
                    neopixel.NeoPixel.write(self)
                    #Desloca o ponto em x e y                                        
                    self.ox = self.ox + 1
                    if self.oy < self.dy:
                        self.oy = self.oy + 1
                    elif self.oy > self.dy:
                        self.oy = self.oy - 1
                    #Calcula o número do pixel
                    self.pixel = self.ox + self.oy*self.colunas
                    #Desenha o pixel na nova posição
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
                    neopixel.NeoPixel.write(self)
                    time.sleep_ms(tempo)

            else:
                #Enquanto não chegar no destino
                while self.ox > self.dx:
                    #Apaga o pixel anterior 
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_fundo)
                    neopixel.NeoPixel.write(self)
                    #Desloca o ponto em x e y 
                    self.ox = self.ox - 1
                    if self.oy < self.dy:
                        self.oy = self.oy+1
                    elif self.oy > self.dy:
                        self.oy = self.oy-1
                    #Calcula o número do pixel
                    self.pixel = self.ox + self.oy*self.colunas
                    #Desenha o pixel na nova posição
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
                    neopixel.NeoPixel.write(self)
                    time.sleep_ms(tempo)
        #Se o delocamento em y é maior que em x
        else:
            
            if self.oy < self.dy:
                
                while self.oy < self.dy:
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_fundo)
                    neopixel.NeoPixel.write(self)

                    self.oy = self.oy + 1
                    if self.ox < self.dx:
                        self.ox = self.ox+1
                    elif self.ox > self.dx:
                        self.ox = self.ox-1
                    
                    self.pixel = self.ox + self.oy*self.colunas

                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
                    neopixel.NeoPixel.write(self)
                    time.sleep_ms(tempo)

            else:
                while self.oy > self.dy:
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_fundo)
                    neopixel.NeoPixel.write(self)
                    
                    self.oy = self.oy - 1
                    if self.ox < self.dx:
                        self.ox = self.ox+1
                    elif self.ox > self.dx:
                        self.ox = self.ox-1

                    self.pixel = self.ox + self.oy*self.colunas
                    
                    neopixel.NeoPixel.__setitem__(self, self.pixel, cor_pixel)
                    neopixel.NeoPixel.write(self)
                    time.sleep_ms(tempo)
        #Atualiza a última posição desenhada
        self.posicao = (self.ox, self.oy)

        print(self.posicao)
        #Retorna a posição do último pixel desenhado
        return self.posicao

    #Desloca um pixel a parir do último ponto desenhado até de deslocamento desejado
    def desloca_delta(self, offset, cor_fundo, cor_pixel, tempo):
        self.destino = [0,0]
        self.destinox = self.posicao[0]+offset[0]
        self.destinoy = self.posicao[1]+offset[1]
        self.destino = [self.destinox, self.destinoy]
        # print(destino)
        return self.desloca_od(self.posicao, self.destino, cor_fundo, cor_pixel, tempo)

    #Cria um bloco de tetris a partir de um ponto de origem, tipo e cor desejada
    #Não desenha o bloco
    def cria_bloco(self, origem, tipo, cor):
        self.ox = origem[0]
        self.oy = origem[1]
                     #P1     P2     P3     P4     Cor      Tipo Ponto Fixo
        self.bloco = [[0,0], [0,0], [0,0], [0,0], (0,0,0), 0,   0]
        if tipo == 0:     #Traço
            self.bloco = [[0+self.ox,0+self.oy], [1+self.ox,0+self.oy], 
                          [2+self.ox,0+self.oy], [3+self.ox,0+self.oy],
                          cor, 0, 1]
        elif tipo == 1:   #Z
            self.bloco = [[0+self.ox,0+self.oy], [1+self.ox,0+self.oy], 
                          [1+self.ox,1+self.oy], [2+self.ox,1+self.oy],
                          cor, 1, 1]
        elif tipo == 2:   #S
            self.bloco = [[1+self.ox,0+self.oy], [2+self.ox,0+self.oy], 
                          [0+self.ox,1+self.oy], [1+self.ox,1+self.oy],
                          cor, 2, 0]
        elif tipo == 3:   #Quadrado
            self.bloco = [[0+self.ox,0+self.oy], [1+self.ox,0+self.oy], 
                          [0+self.ox,1+self.oy], [1+self.ox,1+self.oy],
                          cor, 3, -1]
        elif tipo == 4:   #T
            self.bloco = [[0+self.ox,0+self.oy], [1+self.ox,0+self.oy], 
                          [2+self.ox,0+self.oy], [1+self.ox,1+self.oy],
                          cor, 4, 1]
        elif tipo == 5:   #L
            self.bloco = [[0+self.ox,0+self.oy], [0+self.ox,1+self.oy], 
                          [0+self.ox,2+self.oy], [1+self.ox,2+self.oy],
                          cor, 5, 1]
        elif tipo == 6:   #J
            self.bloco = [[1+self.ox,0+self.oy], [1+self.ox,1+self.oy], 
                          [0+self.ox,2+self.oy], [1+self.ox,2+self.oy],
                          cor, 6, 1]
        #Retorna uma lista que representa o bloco
        return self.bloco

    #Desenha um bloco
    def desenha_bloco(self, bloco):
        #Verifica se está fora dos limites da matriz
        if self.num_pixel(bloco[0]) >= self.pixels \
        or self.num_pixel(bloco[1]) >= self.pixels \
        or self.num_pixel(bloco[2]) >= self.pixels \
        or self.num_pixel(bloco[3]) >= self.pixels:
            return False
                                            #posição pixel            cor
        neopixel.NeoPixel.__setitem__(self, self.num_pixel(bloco[0]), bloco[4])
        neopixel.NeoPixel.__setitem__(self, self.num_pixel(bloco[1]), bloco[4])
        neopixel.NeoPixel.__setitem__(self, self.num_pixel(bloco[2]), bloco[4])
        neopixel.NeoPixel.__setitem__(self, self.num_pixel(bloco[3]), bloco[4])
        neopixel.NeoPixel.write(self)
        
        return True
    
    #Apaga um bloco
    def apaga_bloco(self, bloco, cor_fundo):
        #self.novo_bloco = bloco #Não pode ser usado, funciona como ponteiro
        self.novo_bloco = [[0,0], [0,0], [0,0], [0,0], (0,0,0), 0, 0]
        self.novo_bloco[0] = bloco[0]
        self.novo_bloco[1] = bloco[1]
        self.novo_bloco[2] = bloco[2]
        self.novo_bloco[3] = bloco[3]
        self.novo_bloco[4] = cor_fundo
        self.novo_bloco[5] = bloco[5]
        self.novo_bloco[6] = bloco[6]
        self.desenha_bloco(self.novo_bloco)

    #Desloca um bloco de acordo com o offset (x,y) desejado
    #Não desenha o bloco
    def desloca_bloco(self, bloco, offset):
        self.ox = offset[0]
        self.oy = offset[1]
        self.bloco2 = [[0,0],[0,0],[0,0],[0,0],(0,0,0), 0, 0]
        #Atualiza todos os pixels do bloco com o offset
        self.bloco2[0][0] = bloco[0][0]+offset[0]
        self.bloco2[0][1] = bloco[0][1]+offset[1]
        self.bloco2[1][0] = bloco[1][0]+offset[0]
        self.bloco2[1][1] = bloco[1][1]+offset[1]
        self.bloco2[2][0] = bloco[2][0]+offset[0]
        self.bloco2[2][1] = bloco[2][1]+offset[1]
        self.bloco2[3][0] = bloco[3][0]+offset[0]
        self.bloco2[3][1] = bloco[3][1]+offset[1]

        self.bloco2[4] = bloco[4] #Cor
        self.bloco2[5] = bloco[5] #Tipo
        self.bloco2[6] = bloco[6] #Ponto Fixo
        
        #Retorna o bloco deslocado
        return self.bloco2

    #Verifica se as coordenadas do bloco passado então na área da matriz e se
    #todos o pixel tem cor igual a cor de fundo passada
    #Esse método serve para verificar se um bloco pode ocupar uma posição nova
    def testa_ocupacao(self, bloco, cor_fundo):
        #print('bloco =', bloco)
        #print(cor_fundo)

        #Verifica se está fora dos limites da matriz
        if self.num_pixel(bloco[0]) >= self.pixels \
        or self.num_pixel(bloco[1]) >= self.pixels \
        or self.num_pixel(bloco[2]) >= self.pixels \
        or self.num_pixel(bloco[3]) >= self.pixels:
            #Saiu dos limites
            print('Ocupação=True')  
            return True

        #Se na posição de todos os pixels do bloco a cor é igual a cor de fundo 
        if neopixel.NeoPixel.__getitem__(self, self.num_pixel(bloco[0])) == cor_fundo \
        and neopixel.NeoPixel.__getitem__(self, self.num_pixel(bloco[1])) == cor_fundo \
        and neopixel.NeoPixel.__getitem__(self, self.num_pixel(bloco[2])) == cor_fundo \
        and neopixel.NeoPixel.__getitem__(self, self.num_pixel(bloco[3])) == cor_fundo:
            #A posição não está ocupara
            print('Ocupação=False')  
            return False
        else:
            #A posição está ocupara
            print('True')            
            return True

    #Tenta deslocar um bloco uma linha para baixo
    def movimento_completo(self, bloco, cor_fundo):
        print('>>>>>>>>>>>>bloco =', bloco)

        #Se não chegou na última linha
        if (bloco[0][1] >= self.linhas) \
        or (bloco[1][1] >= self.linhas) \
        or (bloco[2][1] >= self.linhas) \
        or (bloco[3][1] >= self.linhas):
            #Retorna o bloco original
            print('Ultrapassou a última linha')
            return (False, bloco)

        #Desloca y+1
        self.bloco2 = self.desloca_bloco(bloco, [0,1])
        
        print('>>>>>>>>>>>>bloco2 =', self.bloco2)
        
        #Apaga bloco1
        self.apaga_bloco(bloco, cor_fundo)
        
        #Testa
        if self.testa_ocupacao(self.bloco2, cor_fundo) == False:
            #Desenha bloco2
            self.desenha_bloco(self.bloco2)
            #Retorna o estado e o bloco atualizado
            return (True, self.bloco2)
                    
        else:
            #Desenha bloco1 novamente
            self.desenha_bloco(bloco)
            #Retorna o estado e o bloco original
            return (False, bloco)
    
    #Rotaciona um bloco 90 graus em sentido horário
    def rotaciona_bloco(self, bloco):
        print('bloco=', bloco)
        #Se for um quadrado, não precisa rotacionar
        if bloco[5] == 3: 
            return bloco

        self.bloco_rot = [[0,0],[0,0],[0,0],[0,0],bloco[4],bloco[5],bloco[6]]
        #1 - Ponto-Referência (Ponto Fixo)
        self.ref = bloco[6]
        self.bloco_rot[0][0] = bloco[0][0] - bloco[self.ref][0]
        self.bloco_rot[0][1] = bloco[0][1] - bloco[self.ref][1]
        self.bloco_rot[1][0] = bloco[1][0] - bloco[self.ref][0]
        self.bloco_rot[1][1] = bloco[1][1] - bloco[self.ref][1]
        self.bloco_rot[2][0] = bloco[2][0] - bloco[self.ref][0]
        self.bloco_rot[2][1] = bloco[2][1] - bloco[self.ref][1]
        self.bloco_rot[3][0] = bloco[3][0] - bloco[self.ref][0]
        self.bloco_rot[3][1] = bloco[3][1] - bloco[self.ref][1]
        print('bloco_rot1=', self.bloco_rot)
        #2 - Inverte x e y
        self.aux = self.bloco_rot[0][0]
        self.bloco_rot[0][0] = self.bloco_rot[0][1]
        self.bloco_rot[0][1] = self.aux
        self.aux = self.bloco_rot[1][0]
        self.bloco_rot[1][0] = self.bloco_rot[1][1]
        self.bloco_rot[1][1] = self.aux
        self.aux = self.bloco_rot[2][0]
        self.bloco_rot[2][0] = self.bloco_rot[2][1]
        self.bloco_rot[2][1] = self.aux
        self.aux = self.bloco_rot[3][0]
        self.bloco_rot[3][0] = self.bloco_rot[3][1]
        self.bloco_rot[3][1] = self.aux
        print('bloco_rot2=', self.bloco_rot)
        #3 - Multiplica x por -1
        self.bloco_rot[0][0] = -self.bloco_rot[0][0]
        self.bloco_rot[1][0] = -self.bloco_rot[1][0]
        self.bloco_rot[2][0] = -self.bloco_rot[2][0]
        self.bloco_rot[3][0] = -self.bloco_rot[3][0]
        print('bloco_rot3=', self.bloco_rot)
        #4 - Ponto+Referência
        self.bloco_rot[0][0] = self.bloco_rot[0][0] + bloco[self.ref][0]
        self.bloco_rot[0][1] = self.bloco_rot[0][1] + bloco[self.ref][1]
        self.bloco_rot[1][0] = self.bloco_rot[1][0] + bloco[self.ref][0]
        self.bloco_rot[1][1] = self.bloco_rot[1][1] + bloco[self.ref][1]
        self.bloco_rot[2][0] = self.bloco_rot[2][0] + bloco[self.ref][0]
        self.bloco_rot[2][1] = self.bloco_rot[2][1] + bloco[self.ref][1]
        self.bloco_rot[3][0] = self.bloco_rot[3][0] + bloco[self.ref][0]
        self.bloco_rot[3][1] = self.bloco_rot[3][1] + bloco[self.ref][1]
        print('bloco_rot4=', self.bloco_rot)
        #5 - Retorna o novo bloco
        return self.bloco_rot

    #Ajusta o bloco para não ficar partido em duas partes após rotacionar
    def ajusta_posicao_bloco(self, bloco):
        #Ajusta o bloco para não ficar partido em duas partes após rotacionar
        self.bloco_aj = [[0,0],[0,0],[0,0],[0,0],(0,0,0), 0, 0]
        self.bloco_aj = [bloco[0],bloco[1],bloco[2],bloco[3],bloco[4],bloco[5],bloco[6]]
        #Ponto-Referência (Ponto Fixo)
        self.ref = bloco[6]
        #Ajuste feito
        self.ok = False
        #Loop de ajuste
        while self.ok == False:
            self.ok = True
            #Se a posição de um pixel é maior que o número de colunas ou menor que 0,
            #é sinal que houve partição do bloco
            #Deslocamento negativo em x
            if (self.bloco_aj[0][0] >= self.colunas) \
            or (self.bloco_aj[1][0] >= self.colunas) \
            or (self.bloco_aj[2][0] >= self.colunas) \
            or (self.bloco_aj[3][0] >= self.colunas):
                self.bloco_aj = self.desloca_bloco(self.bloco_aj, [-1,0])
                self.ok = False
                print('FalseX+')
                print('bloco_aj=', self.bloco_aj)
                #time.sleep_ms(1000)
            #Deslocamento positivo em x
            elif (self.bloco_aj[0][0] < 0) \
            or (self.bloco_aj[1][0] < 0) \
            or (self.bloco_aj[2][0] < 0) \
            or (self.bloco_aj[3][0] < 0):
                self.bloco_aj = self.desloca_bloco(self.bloco_aj, [1,0])
                self.ok = False
                print('FalseX-')
                print('bloco_aj=', self.bloco_aj)
                #time.sleep_ms(1000)

            #Se a posição de um pixel é maior que o número de linhas ou menor que 0,
            #é sinal que houve partição do bloco
            #Deslocamento negativo em y
            if (self.bloco_aj[0][1] >= self.linhas) \
            or (self.bloco_aj[1][1] >= self.linhas) \
            or (self.bloco_aj[2][1] >= self.linhas) \
            or (self.bloco_aj[3][1] >= self.linhas):
                self.bloco_aj = self.desloca_bloco(self.bloco_aj, [0,-1])
                self.ok = False
                print('FalseY+')
                print('bloco_aj=', self.bloco_aj)
                #time.sleep_ms(1000)
            #Deslocamento positivo em y
            elif (self.bloco_aj[0][1] < 0) \
            or (self.bloco_aj[1][1] < 0) \
            or (self.bloco_aj[2][1] < 0) \
            or (self.bloco_aj[3][1] < 0):
                self.bloco_aj = self.desloca_bloco(self.bloco_aj, [0,1])
                self.ok = False
                print('FalseY-')
                print('bloco_aj=', self.bloco_aj)
                #time.sleep_ms(1000)
        #Retorna o bloco ajustado
        return self.bloco_aj
    
    #Verifica se uma linha foi preenchida. Em caso positivo apaga seu
    #conteúdo de desloca as demais para baixo
    def testa_preenchimento_linha(self, cor_fundo):
        #Varre as linhas da última para primeira
        l = self.linhas - 1
        while l >= 0:
        
            print('>>>> l =',l)    
            
            #1-Verifica se a linha está preenchida
            igual = True
            for c in range(self.colunas):
                #Se uma dos pixel for igual a cor do fundo
                if neopixel.NeoPixel.__getitem__(self, self.num_pixel([c,l])) == cor_fundo:
                    #A linha não está preenchida
                    igual = False
            #2-Se a linha está preenchida
            if igual == True:
                #3-Apaga a linha
                for c in range(self.colunas):
                                                        #posição pixel         cor
                    neopixel.NeoPixel.__setitem__(self, self.num_pixel([c,l]), cor_fundo)
                #Atualiza a matriz
                neopixel.NeoPixel.write(self)
                time.sleep_ms(300)
                
                #4-Desloca o conteúdo das linhas anteriores um linha para baixo
                #Salva o valor da linha atual
                l_igual = l                
                #Ajusta todas as linhas anteriores
                while l_igual > 0:
                    
                    print('>>>> l_igual =',l_igual)
                    
                    for c in range(self.colunas):
                        #Lê a cor da linha anterior
                        cor_pixel_linha_anterior = neopixel.NeoPixel.__getitem__(self, self.num_pixel([c,l_igual-1]))
                        #Salva a cor na linha atual
                        neopixel.NeoPixel.__setitem__(self, self.num_pixel([c,l_igual]), cor_pixel_linha_anterior)
                    l_igual -= 1
                #Preenche a linha 0 com a cor de fundo
                for c in range(self.colunas):
                                                        #posição pixel         cor
                    neopixel.NeoPixel.__setitem__(self, self.num_pixel([c,0]), cor_fundo)
                #Atualiza a matriz
                neopixel.NeoPixel.write(self)
                time.sleep_ms(300)
                
                #5-Após deslocar todas é linhas é preciso voltar e testar a linha atual novamente,
                #porque a linha anterior que foi deslocada também pode ter sido preenchida
                l += 1
            #6-Decrementa uma linha (vai para próxima linha)
            l -= 1


tt = like_tetris(machine.Pin(4), colunas, linhas, "t_linha_zig_zag")
tt.fill((0,0,0))
while True:
    #Teste 1 - Desloca um pixel dentre os pontos de origem e destino por tempo
    '''
    tt.limpa_matriz((255,255,255))
    time.sleep_ms(1000)
    tt.desloca_od([9,12], [1,15], (255,255,255), (255,0,0), 100)
    time.sleep_ms(100)
    tt.desloca_od([1,12], [9,15], (255,255,255), (255,0,0), 100)
    time.sleep_ms(100)
    tt.desloca_od([1,5], [9,12], (255,255,255), (255,0,0), 100)
    time.sleep_ms(100)
    
    #Teste 2 - Desloca um ponto a partir da última posição (rodar com o teste 5)
    
    tt.desloca_delta((0,1), (255,255,255), (0,255,0), 100)
    tt.desloca_delta((0,1), (255,255,255), (0,255,0), 100)
    tt.desloca_delta((0,1), (255,255,255), (0,255,0), 100)
    #'''
    #Teste 3 - Desenho de linhas usando origem e destino e delta
    '''
    tt.limpa_matriz((255,255,255))
    time.sleep_ms(100)
    tt.linha_od((0,0), (9,9), (255,0,0), 0)
    tt.linha_delta((-9,9), (255,0,0), 0) #A classe salva a posição final da ultima linha
    time.sleep_ms(100)
    #'''
    #Teste 4 - Desenha todos os modelos de blocos
    '''
    bloco = tt.cria_bloco((2,0),0,(255,0,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco((1,2),1,(255,0,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco((5,2),2,(255,0,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco((2,5),3,(255,0,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco((2,8),4,(255,0,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco((1,11),5,(255,0,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco((5,11),6,(255,0,0))
    tt.desenha_bloco(bloco)
    print(bloco)
    time.sleep_ms(1000)
    #'''
    #Teste 5 - Deslocamento de bloco e verificação de fim da matriz
    '''
    bloco = tt.cria_bloco([0,0],2,(255,0,0))
    while True:
        if tt.desenha_bloco(bloco) == False:
            print('Acabou a matriz')
            bloco = tt.cria_bloco([0,0],2,(255,0,0))

        print(bloco)
        time.sleep_ms(100)
        tt.apaga_bloco(bloco, (0,0,0))
        bloco = tt.desloca_bloco(bloco, [1,1])
    #'''
    #Teste 6 - Testa deslocamento e ocupação de posição manual
    '''
    bloco = tt.cria_bloco([0,0],2,(255,255,0))
    if tt.testa_ocupacao(bloco, (0,0,0)) == False:
        tt.desenha_bloco(bloco)
        time.sleep_ms(1000)
    else:
        print('FIM')
        sys.exit()
    while True:
        #Desloca
        bloco2 = tt.desloca_bloco(bloco, [0,1])
        
        print('bloco =', bloco)
        print('bloco2 =', bloco2)
        
        #Apaga bloco1
        tt.apaga_bloco(bloco, (0,0,0))
        
        #Testa
        if tt.testa_ocupacao(bloco2, (0,0,0)) == False:
            #Desenha bloco2
            tt.desenha_bloco(bloco2)
            #Atualiza bloco
            bloco = bloco2
            #Atraso
            time.sleep_ms(200)
        else:
            #Desenha bloco1 novamente
            tt.desenha_bloco(bloco)            
            break    
    #'''
    #Teste 7 - Testa deslocamento e ocupação de posição por método
    '''
    bloco = tt.cria_bloco([0,0],0,(255,0,0))
    if tt.testa_ocupacao(bloco, (0,0,0)) == False:
        tt.desenha_bloco(bloco)
    time.sleep_ms(500)

    estado = True
    while estado == True:
        print('blocoR =', bloco)
        #Atraso
        time.sleep_ms(200)
        #Novo movimento
        estado, bloco = tt.movimento_completo(bloco, (0,0,0))
    #'''
    #Teste 8 - Referência de listas
    '''
    bloco = [[0,0],[1,1]]
    bloco2 = bloco
    print('bloco =', bloco)
    print('bloco2 =', bloco2)
    bloco2[1] = [3,3]
    print('bloco =', bloco)
    print('bloco2 =', bloco2)
    time.sleep_ms(20000)
    #'''
    #Teste 9 - Teste rotação dos blocos e choque com os limites da matriz
    '''
    bloco = tt.cria_bloco([0,0],0,(255,0,0))
    bloco_aux = bloco
    if tt.testa_ocupacao(bloco, (0,0,0)) == False:
        tt.desenha_bloco(bloco)
    time.sleep_ms(500)
    #Apaga o bloco
    tt.apaga_bloco(bloco, (0,0,0))

    estado = True
    while estado == True:
        print('blocoR =', bloco)
        #Rotaciona o bloco
        bloco = tt.rotaciona_bloco(bloco)
        #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
        #rotacionar ou deslocar)
        bloco_aux = tt.ajusta_posicao_bloco(bloco)
        #Desenha o bloco
        #tt.desenha_bloco(bloco) #Bloco original
        tt.desenha_bloco(bloco_aux) #Bloco ajustado
        #Atraso
        time.sleep_ms(500)
        #Apaga o bloco auxiliar (importante quando tem ajuste de posição)
        tt.apaga_bloco(bloco_aux, (0,0,0))
    #'''
    #Teste 10 - Mover um bloco por botões
    '''
    cor_fundo = (0,255,255)
    tt.limpa_matriz(cor_fundo)
    bloco = tt.cria_bloco([5,0],1,(255,0,0))
    if tt.testa_ocupacao(bloco, (0,0,0)) == False:
        tt.desenha_bloco(bloco)
        time.sleep_ms(1000)
    estado = True
    while estado == True:
        #Novo movimento
        estado, bloco = tt.movimento_completo(bloco, cor_fundo)
        
        if botaoEsq.value() == 0:
            print('botaoEsq = 0')   #Pull-up interno não funcionou
            #Apaga o bloco
            tt.apaga_bloco(bloco, (0,0,0))
            #Desloca
            bloco = tt.desloca_bloco(bloco, [-1,0])
            #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
            #rotacionar ou deslocar)
            bloco = tt.ajusta_posicao_bloco(bloco)
            #Desenha o bloco
            tt.desenha_bloco(bloco)
        
        if botaoDir.value() == 0:
            print('botaoDir = 0')
            #Apaga o bloco
            tt.apaga_bloco(bloco, (0,0,0))
            #Desloca
            bloco = tt.desloca_bloco(bloco, [1,0])
            #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
            #rotacionar ou deslocar)
            bloco = tt.ajusta_posicao_bloco(bloco)
            #Desenha o bloco
            tt.desenha_bloco(bloco)
        
        if botaoRot.value() == 0:
            print('botaoRot = 0')
            #Apaga o bloco
            tt.apaga_bloco(bloco, (0,0,0))
            #Rotaciona o bloco
            bloco = tt.rotaciona_bloco(bloco)
            #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
            #rotacionar ou deslocar)
            bloco_aux = tt.ajusta_posicao_bloco(bloco)
            #Desenha o bloco
            #tt.desenha_bloco(bloco) #Bloco original
            tt.desenha_bloco(bloco_aux) #Bloco ajustado
        
        time.sleep_ms(300)
    print('Fim')
    while True:
        time.sleep_ms(500)
    #'''
    #Teste 11 - Mover um bloco por botões, novo ajuste
    #'''    
    cor_fundo = (0,0,0)
    tt.limpa_matriz(cor_fundo)
    
    #Pré-ocupa algumas linhas parcialmente
    bloco = tt.cria_bloco([0,14],0,(15,15,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco([0,13],0,(15,15,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco([0,12],0,(15,15,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco([6,14],0,(15,15,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco([6,13],0,(15,15,0))
    tt.desenha_bloco(bloco)
    bloco = tt.cria_bloco([6,12],0,(15,15,0))
    tt.desenha_bloco(bloco)    
    
    while True:
        #1-Cria um novo bloco
        bloco = tt.cria_bloco([5,0],0,(15,15,0))
        
        #2-Teste se a posição já está ocupada
        if tt.testa_ocupacao(bloco, (0,0,0)) == False:
            tt.desenha_bloco(bloco)
            time.sleep_ms(1000)
        else:
            print('FIM DO JOGO')
            sys.exit()            
        
        #3-Inicia um loop de descida do bloco
        estado = True
        while estado == True:
            
            #Debug - mostra o bloca a ser movido
            print('bloco a ser movido =', bloco)
            
            #Novo movimento
            estado, bloco = tt.movimento_completo(bloco, cor_fundo)
            
            #Atraso entre um novo movimento
            time.sleep_ms(500)
            
            #Testa se o movimento foi possível
            if estado == False:
                break #Interrompe o laço
            
            #Testa os botões            
            
            #Botão esquerdo
            if botaoEsq.value() == 0:
                print('botaoEsq = 0')   #Pull-up interno não funcionou
                #Apaga o bloco
                tt.apaga_bloco(bloco, (0,0,0))
                #Desloca
                bloco2 = tt.desloca_bloco(bloco, [-1,0])
                #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
                #rotacionar ou deslocar)
                bloco2 = tt.ajusta_posicao_bloco(bloco2)
                #Testa
                if tt.testa_ocupacao(bloco2, cor_fundo) == False:
                    #Desenha bloco2
                    tt.desenha_bloco(bloco2)
                    #Atualiza o bloco1
                    bloco = bloco2
                else:
                    #Desenha bloco1
                    tt.desenha_bloco(bloco)
            
            #Botão esquerdo        
            if botaoDir.value() == 0:
                print('botaoDir = 0')
                #Apaga o bloco
                tt.apaga_bloco(bloco, (0,0,0))
                #Desloca
                bloco2 = tt.desloca_bloco(bloco, [+1,0])
                #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
                #rotacionar ou deslocar)
                bloco2 = tt.ajusta_posicao_bloco(bloco2)
                #Testa
                if tt.testa_ocupacao(bloco2, cor_fundo) == False:
                    #Desenha bloco2
                    tt.desenha_bloco(bloco2)
                    #Atualiza o bloco1
                    bloco = bloco2
                else:
                    #Desenha bloco1
                    tt.desenha_bloco(bloco)
            
            #Botão de rotação
            if botaoRot.value() == 0:
                print('botaoRot = 0')
                #Apaga o bloco
                tt.apaga_bloco(bloco, (0,0,0))
                #Rotaciona o bloco
                bloco2 = tt.rotaciona_bloco(bloco)
                #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
                #rotacionar ou deslocar)
                bloco2 = tt.ajusta_posicao_bloco(bloco2)
                #Testa
                if tt.testa_ocupacao(bloco2, cor_fundo) == False:
                    #Desenha bloco2
                    tt.desenha_bloco(bloco2)
                    #Atualiza o bloco1
                    bloco = bloco2
                else:
                    #Desenha bloco1
                    tt.desenha_bloco(bloco)
        
        #4-Verifica o preenchimento de linhas
        tt.testa_preenchimento_linha(cor_fundo)