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

botaoEsq = Pin(34, Pin.IN, Pin.PULL_UP) #Pull-up interno não funcionou
botaoDir = Pin(21, Pin.IN, Pin.PULL_UP)
botaoRot = Pin(25, Pin.IN, Pin.PULL_UP)

linhas = 15     #O objeto canvas no Wokwi só funciona com linhas pares
colunas = 10    #O objeto canvas no Wokwi só funciona com linhas pares
posicao = (0,0)
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
    bloco = tt.cria_bloco([0,0],1,(255,0,0))
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
        cor_fundo = (0,0,0)
    tt.limpa_matriz(cor_fundo)
    
    while True:
        bloco = tt.cria_bloco([5,0],1,(255,255,0))
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
            
            time.sleep_ms(500)
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
     #'''