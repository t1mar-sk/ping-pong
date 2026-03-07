import pygame
from pygame import *
import socket
import json
from threading import Thread
from PIL import Image
import mixer


# ---ПУГАМЕ НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")
pygame.mixer.init()
n = 0
# ---СЕРВЕР ---
def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('192.168.88.29', 9090)) # ---- Підключення до сервера
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            return my_id, game_state, buffer, client
        except:
            pass


def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            game_state["winner"] = -1
            break

# --- ШРИФТИ ---
font_win = font.Font(None, 72)
font_main = font.Font(None, 36)
# --- ЗОБРАЖЕННЯ ----
img1 = Image.open("back.png")
img1 = img1.resize((WIDTH, HEIGHT))

mode1 = img1.mode
size1 = img1.size
data1 = img1.tobytes()

back1 = image.fromstring(data1, size1, mode1)

img = Image.open("high_cortisole.png")
img = img.resize((WIDTH, HEIGHT))

mode = img.mode
size = img.size
data = img.tobytes()

back = image.fromstring(data, size, mode)

img4 = Image.open("back.png")
img4 = img4.resize((20,100))

mode4 = img4.mode
size4 = img4.size
data4 = img4.tobytes()

platform1 = image.fromstring(data4, size4, mode4)

img3 = Image.open("high_cortisole.png")
img3 = img3.resize((20,100))

mode3 = img3.mode
size3 = img3.size
data3 = img3.tobytes()

platform = image.fromstring(data3, size3, mode3)

img2 = Image.open("back.png")
img2 = img2.resize((50,50))

mode2 = img2.mode
size2 = img2.size
data2 = img2.tobytes()

back2 = image.fromstring(data2, size2, mode2)


# --- ЗВУКИ ---
ball_hit = pygame.mixer.Sound('ball_hit.wav')
lose_song = pygame.mixer.Sound('lose.wav')
win_song = pygame.mixer.Sound('win.wav')

pygame.mixer.music.load("low_cortisol.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# --- ГРА ---
game_over = False
winner = None
you_winner = None
my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()
while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    if "countdown" in game_state and game_state["countdown"] > 0:
        screen.blit(back1, (0,0))
        countdown_text = font.Font(None, 72).render(str(game_state["countdown"]), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
        display.update()
        continue  # Не малюємо гру до завершення відліку

    if "winner" in game_state and game_state["winner"] is not None:
        pygame.mixer.music.stop()
        screen.blit(back1, (0,0))

        if you_winner is None:  # Встановлюємо тільки один раз
            if game_state["winner"] == my_id:
                you_winner = True
            else:
                you_winner = False



        if you_winner:
            if n == 0:
                win_song.play()
                n = 1
                text = "Ти low cortisol!"
                screen.blit(back1, (0, 0))
            else :
                text = "Ти low cortisol!"
                screen.blit(back1, (0, 0))

        else:
            if n == 0:
                lose_song.play()
                n = 1
                text = "Ти high cortisol!"
                screen.blit(back, (0, 0))
            else:
                text = "Ти high cortisol!"
                screen.blit(back, (0, 0))

        win_text = font_win.render(text, True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)

        text = font_win.render('К - рестарт', True, (255, 215, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(text, text_rect)

        display.update()
        continue

    if game_state:
        screen.blit(back1, (0,0))
        screen.blit(platform, (20, game_state['paddles']['0']))
        draw.rect(screen, (255, 0, 0), (20, game_state['paddles']['0'], 20, 100), 3)
        screen.blit(platform1, (WIDTH - 40, game_state['paddles']['1']))
        draw.rect(screen, (0, 255, 0), (WIDTH - 40, game_state['paddles']['1'], 20, 100), 3)
        draw.circle(screen, (255, 255, 255), (game_state['ball']['x'], game_state['ball']['y']), 10)
        screen.blit(back2, (game_state['ball']['x'] - 10, game_state['ball']['y'] - 10))
        score_text = font_main.render(f"{game_state['scores'][0]} : {game_state['scores'][1]}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH // 2 - 25, 20))

        if game_state['sound_event']:
            if game_state['sound_event'] == 'wall_hit':
                ball_hit.play()
                pass
            if game_state['sound_event'] == 'platform_hit':
                ball_hit.play()
                pass

    else:
        wating_text = font_main.render(f"Очікування гравців...", True, (255, 255, 255))
        screen.blit(wating_text, (WIDTH // 2 - 25, 20))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w]:
        client.send(b"UP")
    elif keys[K_s]:
        client.send(b"DOWN")
