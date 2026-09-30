import pygame
import random
import os

pygame.init()

LARGURA = 800
ALTURA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SquareGame")
clock = pygame.time.Clock()

BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
CINZA = (50, 50, 50)
DOURADO = (255, 215, 0)

TAMANHO_JOGADOR = 40
VELOCIDADE_JOGADOR = 5
jogador_x = LARGURA // 2
jogador_y = ALTURA // 2

TAMANHO_INIMIGO = 40
VELOCIDADE_INIMIGO = 2
inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
inimigo_y = random.randint(0, ALTURA - TAMANHO_INIMIGO)

pontuacao = 0
fonte = pygame.font.SysFont(None, 30)
fonte_game_over = pygame.font.SysFont(None, 60)

ARQUIVO_RECORDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recorde.txt")

def carregar_recorde():
    if os.path.exists(ARQUIVO_RECORDE):
        try:
            with open(ARQUIVO_RECORDE, "r") as arquivo:
                conteudo = arquivo.read().strip()
                return int(conteudo) if conteudo else 0
        except ValueError:
            return 0
    return 0


def salvar_recorde(valor):
    with open(ARQUIVO_RECORDE, "w") as arquivo:
        arquivo.write(str(valor))

recorde = carregar_recorde()
bateu_recorde = False

def reiniciar_jogo():
    global jogador_x, jogador_y
    global inimigo_x, inimigo_y
    global pontuacao, VELOCIDADE_INIMIGO
    global bateu_recorde

    jogador_x = LARGURA // 2
    jogador_y = ALTURA // 2
    inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
    inimigo_y = random.randint(0, ALTURA - TAMANHO_INIMIGO)
    pontuacao = 0
    VELOCIDADE_INIMIGO = 2
    bateu_recorde = False


def desenhar_jogo():
    tela.fill(BRANCO)

    pygame.draw.rect(
        tela, AZUL,
        (jogador_x, jogador_y, TAMANHO_JOGADOR, TAMANHO_JOGADOR)
    )
    pygame.draw.rect(
        tela, VERMELHO,
        (inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO)
    )

    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

    texto_recorde = fonte.render(f"Recorde: {recorde}", True, PRETO)
    tela.blit(texto_recorde, (10, 40))


def mostrar_game_over():
    tela.fill(CINZA)

    texto_game_over = fonte_game_over.render("GAME OVER", True, VERMELHO)
    texto_pontuacao = fonte.render(f"Pontuação final: {pontuacao}", True, BRANCO)

    cor_recorde = DOURADO if bateu_recorde else BRANCO
    mensagem_recorde = "NOVO RECORDE!" if bateu_recorde else f"Recorde: {recorde}"
    texto_recorde = fonte.render(mensagem_recorde, True, cor_recorde)

    texto_reiniciar = fonte.render(
        "Pressione ENTER para jogar novamente", True, BRANCO
    )

    tela.blit(texto_game_over, texto_game_over.get_rect(center=(LARGURA // 2, 180)))
    tela.blit(texto_pontuacao, texto_pontuacao.get_rect(center=(LARGURA // 2, 270)))
    tela.blit(texto_recorde, texto_recorde.get_rect(center=(LARGURA // 2, 320)))
    tela.blit(texto_reiniciar, texto_reiniciar.get_rect(center=(LARGURA // 2, 390)))

rodando = True
jogando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if not jogando and evento.key == pygame.K_RETURN:
                reiniciar_jogo()
                jogando = True

    if jogando:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            jogador_y -= VELOCIDADE_JOGADOR
        if teclas[pygame.K_DOWN]:
            jogador_y += VELOCIDADE_JOGADOR
        if teclas[pygame.K_LEFT]:
            jogador_x -= VELOCIDADE_JOGADOR
        if teclas[pygame.K_RIGHT]:
            jogador_x += VELOCIDADE_JOGADOR

        if jogador_x < 0:
            jogador_x = 0
        if jogador_x > LARGURA - TAMANHO_JOGADOR:
            jogador_x = LARGURA - TAMANHO_JOGADOR
        if jogador_y < 0:
            jogador_y = 0
        if jogador_y > ALTURA - TAMANHO_JOGADOR:
            jogador_y = ALTURA - TAMANHO_JOGADOR

        if inimigo_x < jogador_x:
            inimigo_x += VELOCIDADE_INIMIGO
        elif inimigo_x > jogador_x:
            inimigo_x -= VELOCIDADE_INIMIGO
        if inimigo_y < jogador_y:
            inimigo_y += VELOCIDADE_INIMIGO
        elif inimigo_y > jogador_y:
            inimigo_y -= VELOCIDADE_INIMIGO

        jogador_rect = pygame.Rect(jogador_x, jogador_y, TAMANHO_JOGADOR, TAMANHO_JOGADOR)
        inimigo_rect = pygame.Rect(inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO)

        if jogador_rect.colliderect(inimigo_rect):
            jogando = False
            if pontuacao > recorde:
                recorde = pontuacao
                salvar_recorde(recorde)
                bateu_recorde = True
        else:
            pontuacao += 1
            if pontuacao % 300 == 0:
                VELOCIDADE_INIMIGO += 0.5

        desenhar_jogo()
    else:
        mostrar_game_over()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()