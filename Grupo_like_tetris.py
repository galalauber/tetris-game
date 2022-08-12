#Neopixel
#https://docs.micropython.org/en/latest/library/neopixel.html
#https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
#Exemplo do uso de canvas: https://wokwi.com/projects/330751728413573715
#Outro exemplo: https://github.com/wokwi/wokwi-features/issues/237
#Exemplos da bilbioteca: https://wokwi.com/arduino/libraries/Adafruit_NeoPixel
#Tetris online: https://tetris.com/play-tetris

import time
import machine
import sys
from like_tetris import like_tetris
from machine import Pin
import random

botaoEsq = Pin(34, Pin.IN, Pin.PULL_UP) #Pull-up interno não funcionou
botaoDir = Pin(21, Pin.IN, Pin.PULL_UP)
botaoRot = Pin(25, Pin.IN, Pin.PULL_UP)

linhas = 15     #O objeto canvas no Wokwi só funciona com linhas pares
colunas = 10    #O objeto canvas no Wokwi só funciona com linhas pares
posicao = (0,0)
tt = like_tetris(machine.Pin(4), colunas, linhas, "t_linha_zig_zag")
tt.fill((0,0,0))
while True:
    cor_fundo = (0,0,0)
    tt.limpa_matriz(cor_fundo)

    while True:
        X = random.randint(0,6)
        R = 0
        G = 0
        B = 0
        if X == 0:
            R = 64
        if X == 1:
            R = 32
            G = 32
        if X == 2:
            G = 64
        if X == 3:
            R = 32
            B = 32
        if X == 4:
            B = 64
        if X == 5:
            G = 32
            B = 32
        if X == 6:
            R = 32
            G = 48
            B = 48
            
        #1-Cria um novo bloco
        bloco = tt.cria_bloco([5,0],X,(R,G,B))
        #Faz ajuste de posição (testa se o bloco ficou partido em duas partes após
        #rotacionar ou deslocar)
        bloco = tt.ajusta_posicao_bloco(bloco)
        #2-Teste se a posição já está ocupada
        if tt.testa_ocupacao(bloco, (0,0,0)) == False:
            tt.desenha_bloco(bloco)
            time.sleep_ms(1000)
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
        else:

            print('FIM DO JOGO')
            for repete in range(4):
                cor_fundo = (64,64,64)
                tt.limpa_matriz(cor_fundo)
                time.sleep_ms(500)
                cor_fundo = (0,0,0)
                tt.limpa_matriz(cor_fundo)
                time.sleep_ms(500)
            
            while (botaoRot.value() != 0) and (botaoDir.value() != 0) and (botaoEsq.value() != 0):
                time.sleep_ms(100)
