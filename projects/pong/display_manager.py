from machine import Pin, I2C, ADC
import lib.ssd1306 as ssd1306
from framebuf import FrameBuffer, MONO_VLSB
from pong.shapes import Rectangle, Player, Ball
from time import sleep
from random import randint
from common.button_parser import voltage_to_value


SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
GAME_LENGTH = 5
STARTER_TICK_RATE = 0.006

def setup_display():
    i2c = I2C(scl=Pin(22), sda=Pin(21))
    oled = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)
    return oled

def init_buttons():
    buttons1 = ADC(Pin(34))
    buttons2 = ADC(Pin(35))
    return buttons1, buttons2
    
def init_shapes():
    shapes = []
    ball = Ball(randint(33, 95), randint(0, 55), 6, 6, x_velocity=2, y_velocity=2)
    shapes.append(ball)
    #rectangle2 = Rectangle(117, 1, x_velocity=-2, y_velocity=1)
    #shapes.append(rectangle2)
    #rectangle3 = Rectangle(117, 53, x_velocity=-2, y_velocity=1)
    #shapes.append(rectangle3)
    return shapes

def run_round(oled, buttons1, buttons2):
    print("Starting Round")
    shapes = init_shapes()
    player_1 = Player(16, 16, 4, 16)
    player_1.register_button_pads(buttons1)
    player_2 = Player(104, 16, 4, 16)
    player_2.register_button_pads(buttons2)
    shapes.append(player_1)
    shapes.append(player_2)
    round_end = False
    game_time = 0
    tick_rate = STARTER_TICK_RATE
    while not round_end:
        oled.fill(0)
        for shape in shapes:
            for collider in [collider for collider in shapes if collider is not shape]:
                shape.collision(collider)
            shape.bound_collision(SCREEN_WIDTH, SCREEN_HEIGHT)
            shape.next()
            shape.draw(oled) 
            if isinstance(shape, Ball):
                round_end = bool(shape.round_end)
                if round_end:
                    score = int(not bool(shape.collision_wall))
        oled.show()
        sleep(tick_rate)
        game_time += 1
        if game_time % 100 == 0:
            tick_rate /= 2
    return score

def manager():
    oled = setup_display()
    buttons1, buttons2 = init_buttons()    
    score = [0, 0]
    game_over = False
    while not game_over:
        round_score = run_round(oled, buttons1, buttons2)
        score[round_score] += 1
        game_over = score[0] >= GAME_LENGTH or score[1] >= GAME_LENGTH
        if not game_over:
            oled.fill(0)
            oled.text(f"{score[0]} - {score[1]}", 44, 28)
            #oled.text("Blue to continue",0,56)
            oled.text("Press Both Blue!",2,56)
            oled.show()
            while voltage_to_value(buttons1.read()) != 5 or voltage_to_value(buttons2.read()) != 5:
                sleep(0.1)
            
    oled.fill(0)
    oled.text("Game Over!", 28, 24)
    oled.text(f"{score[0]} - {score[1]}", 44, 36)
    oled.show()
    print("Done")