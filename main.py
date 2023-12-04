import pygame
import sqlite3
import random
import os


pygame.init()


largura = 800
altura = 600
tamanho_carta = 100
cor_fundo = (255, 255, 255)
cor_carta = (0, 0, 0)


db_path = "memory_game.db"

if not os.path.exists(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    
    cursor.execute('''
        CREATE TABLE memory_game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            pair_id INTEGER
        )
    ''')

 
    images = ["imagem1.png", "imagem2.png", "imagem3.png", "imagem4.png", "imagem5.png", "imagem6.png"]
    random.shuffle(images)
    for i, image in enumerate(images):
        cursor.execute("INSERT INTO memory_game (image_path, pair_id) VALUES (?, ?)", (image, i // 2))

    connection.commit()
    connection.close()


connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("SELECT image_path FROM memory_game")
images = [row[0] for row in cursor.fetchall()]
connection.close()


cartas = images * 2


random.shuffle(cartas)


tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Memória")


viradas = []
pares_encontrados = 0
tentativas = 0


jogo_ativo = True
while jogo_ativo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_ativo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and len(viradas) < 2:
            pos_mouse = pygame.mouse.get_pos()
            carta_clicada = (pos_mouse[0] // tamanho_carta, pos_mouse[1] // tamanho_carta)
            if carta_clicada not in viradas:
                viradas.append(carta_clicada)
                tentativas += 1


    if len(viradas) == 2:
        pygame.time.wait(500) 
        if cartas[viradas[0][1] * 6 + viradas[0][0]] == cartas[viradas[1][1] * 6 + viradas[1][0]]:
            pares_encontrados += 1
            if pares_encontrados == len(images):
                print("Parabéns! Você encontrou todos os pares!")
                jogo_ativo = False
        viradas = []

    
    tela.fill(cor_fundo)
    for i in range(altura // tamanho_carta):
        for j in range(largura // tamanho_carta):
            pygame.draw.rect(tela, cor_carta, (j * tamanho_carta, i * tamanho_carta, tamanho_carta, tamanho_carta))
            if (j, i) in viradas:
                image_path = cartas[i * 6 + j]
                image = pygame.image.load(image_path)
                tela.blit(image, (j * tamanho_carta, i * tamanho_carta))

    
    pygame.display.flip()



pygame.quit()







