from sys import exit
from random import choice

import pygame
from pygame.locals import QUIT, KEYDOWN

TITLE = '--By shy'

WIDTH = 660
HEIGHT = 500
SNAKE_SIZE = 20
BOARD_COLOR = (0, 0, 100)


class Vector():
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError

    def copy(self):
        type_self = type(self)
        return type_self(self.x, self.y)

    def move(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Vector):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    def __repr__(self):
        type_self = type(self)
        name = type_self.__name__
        return '{}({!r}, {!r})'.format(name, self.x, self.y)


class Snake:
    def __init__(self):

        self.map = {(x, y): 0
                    for x in range(1,
                                   int(WIDTH / SNAKE_SIZE) - 2)
                    for y in range(1,
                                   int(HEIGHT / SNAKE_SIZE) - 2)}

        self.body = [
            Vector(5 * SNAKE_SIZE, 5 * SNAKE_SIZE),
            Vector(6 * SNAKE_SIZE, 5 * SNAKE_SIZE)
        ]
        self.head = self.body[-1].copy()
        self.color = (0, 0, 0)

        self.direction = {
            'right': Vector(SNAKE_SIZE, 0),
            'left': Vector(-SNAKE_SIZE, 0),
            'up': Vector(0, -SNAKE_SIZE),
            'down': Vector(0, SNAKE_SIZE)
        }

        self.move_direction = 'right'
        self.speed = 4
        self.score = 0


        self.food = Vector(0, 0)
        self.food_color = (255, 0, 0)
        self.generate_food()


        self.game_started = False

    def generate_food(self):
        empty_pos = [
            pos for pos in self.map.keys()
            if Vector(pos[0] * SNAKE_SIZE, pos[1] *
                      SNAKE_SIZE) not in self.body
        ]
        result = choice(empty_pos)
        self.food.x = result[0] * 20
        self.food.y = result[1] * 20

    def move(self):

        self.head = self.body[-1].copy()

        self.head.move(self.direction[self.move_direction])

        if not self._islive(self.head):

            return False

        self.body.append(self.head)

        if self.head == self.food:
            self.score += 1
            if self.score % 5 == 0:
                self.speed += 2
            self.generate_food()
        else:

            self.body.pop(0)
        return True

    def _islive(self, head):
        return 0 < head.x < WIDTH - SNAKE_SIZE and 0 < head.y < HEIGHT - SNAKE_SIZE and head not in self.body


KEY_DIRECTION_DICT = {
    119: 'up',  # W
    115: 'down',  # S
    97: 'left',  # A
    100: 'right',  # D
    273: 'up',  # UP
    274: 'down',  # DOWN
    276: 'left',  # LEFT
    275: 'right',  # RIGHT
}


def press(events, snake):
    for event in events:
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == 13:
                snake.game_started = True
            if snake.game_started and event.key in KEY_DIRECTION_DICT:
                return direction_check(snake.move_direction,
                                       KEY_DIRECTION_DICT[event.key])


def draw_score(screen, score, position):
    tips_font = pygame.font.SysFont('arial', 20)
    screen.blit(
        tips_font.render('Score: {}'.format(score), True, (0, 0, 205),
                         (255, 255, 255)), position)


def game_continue(screen, snake):

    init_board(screen)
    draw_score(screen, snake.score, (500, 0))

    for seg in snake.body:
        pygame.draw.rect(screen, snake.color, [seg[0], seg[1], 20, 20], 0)
    pygame.draw.rect(screen, snake.food_color,
                     [snake.food[0], snake.food[1], 20, 20], 0)


def game_over(screen, fonts, score):

    screen.blit(fonts['game_over'], (250, 100))
    draw_score(screen, score, (290, 200))
    screen.blit(fonts['start'], (220, 310))
    snake = Snake()
    return snake


def direction_check(move_direction, change_direction):

    directions = [['up', 'down'], ['left', 'right']]
    if move_direction in directions[0] and change_direction in directions[1]:
        return change_direction
    elif move_direction in directions[1] and change_direction in directions[0]:
        return change_direction

    return move_direction


def init(fonts):
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    screen.fill((255, 255, 255))
    screen.blit(fonts['welcome'], (177, 100))
    screen.blit(fonts['start'], (195, 310))
    return fps_clock, screen


def init_board(screen):
    board_width = int(WIDTH / SNAKE_SIZE)
    board_height = int(HEIGHT / SNAKE_SIZE)
    color = BOARD_COLOR
    width = 0
    for i in range(board_width):
        pos = i * SNAKE_SIZE, 0, SNAKE_SIZE, SNAKE_SIZE
        pygame.draw.rect(screen, color, pos, width)
        pos = i * SNAKE_SIZE, (board_height -
                               1) * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE
        pygame.draw.rect(screen, color, pos, width)


    for i in range(board_height - 1):
        pos = 0, SNAKE_SIZE + i * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE
        pygame.draw.rect(screen, color, pos, width)
        pos = (
            board_width - 1
        ) * SNAKE_SIZE, SNAKE_SIZE + i * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE
        pygame.draw.rect(screen, color, pos, width)


def font_setting():
    title_font = pygame.font.SysFont('arial', 32)
    welcome_words = title_font.render('Welcome to My Snake', True, (0, 0, 0),
                                      (255, 255, 255))
    tips_font = pygame.font.SysFont('arial', 24)
    start_game_words = tips_font.render('Press Enter to Start Game', True,
                                        (0, 0, 0), (255, 255, 255))
    gameover_words = title_font.render('GAME OVER', True, (205, 92, 92),
                                       (255, 255, 255))
    win_words = title_font.render('THE SNAKE IS LONG ENOUGH AND YOU WIN!',
                                  True, (0, 0, 205), (255, 255, 255))
    return {
        'welcome': welcome_words,
        'start': start_game_words,
        'game_over': gameover_words,
        'win': win_words
    }


def main():
    pygame.init()
    fonts = font_setting()
    fps_clock, screen = init(fonts)

    snake = Snake()  # 创建snake对象
    direction = snake.move_direction
    while True:
        events = pygame.event.get()
        new_direction = press(events, snake)
        if snake.game_started:
            if new_direction:
                snake.move_direction = new_direction
            screen.fill((255, 255, 255))
            if not snake.move():

                snake = game_over(screen, fonts, snake.score)
                direction = snake.move_direction
            else:

                game_continue(screen, snake)


        pygame.display.update()

        fps_clock.tick(snake.speed)


if __name__ == '__main__':
    main()