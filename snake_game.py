import numpy as np
import pygame
import random
from enum import Enum
from collections import namedtuple

# ______________________________________________
pygame.init()
font = pygame.font.Font('arial.ttf', 25)


# reset
# reward
# play(action) -> direction
# game_iteration
# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
GREEN = (40, 180, 20)
DARKGRAY = (50, 50, 50)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
BLOCK_INNER_OFFSET = 2
SPEED = 1000


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.bIsGamePaused = False

        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frameIteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frameIteration += 1

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             self.direction = Direction.LEFT
        #         elif event.key == pygame.K_RIGHT:
        #             self.direction = Direction.RIGHT
        #         elif event.key == pygame.K_UP:
        #             self.direction = Direction.UP
        #         elif event.key == pygame.K_DOWN:
        #             self.direction = Direction.DOWN
        #         elif event.key == pygame.K_p:
        #             print("pause pressed")
        #             self.bIsGamePaused = not (self.bIsGamePaused)
        #         elif event.key == pygame.K_ESCAPE:
        #             print("user quit")
        #             game_over = True
        #             return game_over, self.score
        #
        # if self.bIsGamePaused:
        #     game_over = False
        #     return reward, game_over, self.score

        # 2. move
        self._move(action)  # update the head     # self.direction # <- for human player
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        bIsSnakeDoingNothing = self.frameIteration > 100 * len(self.snake)
        if self.is_collision() or bIsSnakeDoingNothing:
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, point=None):
        if point == None:
            point = self.head
        # hits boundary
        if point.x > self.w - BLOCK_SIZE or point.x < 0 or point.y > self.h - BLOCK_SIZE or point.y < 0:
            print("snake ran into a wall")
            return True
        # hits itself
        elif point in self.snake[1:]:
            print("snake ate itself")
            return True

        return False

    def _update_ui(self):
        self.display.fill(DARKGRAY)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLACK, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + BLOCK_INNER_OFFSET, pt.y + BLOCK_INNER_OFFSET,
                                                              BLOCK_SIZE - 2 * BLOCK_INNER_OFFSET,
                                                              BLOCK_SIZE - 2 * BLOCK_INNER_OFFSET))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        if self.bIsGamePaused:
            text = font.render("Pause", True, WHITE, BLACK)
            self.display.blit(text, [self.w / 2 - text.get_width() / 2, self.h / 2 - text.get_height() / 2])
        else:
            text = font.render("Score: " + str(self.score), True, WHITE)
            self.display.blit(text, [20, 10])

        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


# if __name__ == '__main__':
#     game = SnakeGameAI()
#
#     # game loop
#     while True:
#         reward, game_over, score = game.play_step()
#         game._update_ui()
#
#         if game_over == True:
#             break
#
#     print('Final Score', score)
#
#     pygame.quit()
