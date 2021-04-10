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
SPEED = 15


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

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_p:
                    print("pause pressed")
                    self.bIsGamePaused = not (self.bIsGamePaused)
                elif event.key == pygame.K_ESCAPE:
                    print("user quit")
                    game_over = True
                    return game_over, self.score

        if self.bIsGamePaused:
            game_over = False
            return game_over, self.score

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock

        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            print("snake ran into a wall")
            return True
        elif self.head in self.snake[1:]:
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

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGameAI()

    # game loop
    while True:
        game_over, score = game.play_step()
        game._update_ui()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
