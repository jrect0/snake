import pygame, sys
import random

angle = 0
SIZE = 40
BACKGROUND = pygame.image.load('Background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (520, 520))
END_IMAGE = pygame.image.load('died.png')
END_IMAGE = pygame.transform.scale(END_IMAGE, (520, 520))
green = (0, 255, 0)
blue = (0, 0, 255)
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("monkey.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,460)
        self.y = random.randint(0,460)

class Snake():
    
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.head_image = pygame.image.load('snake head down.png').convert()
        self.head_down_image = pygame.image.load('snake head down.png').convert()
        self.head_down_image = pygame.transform.scale(self.head_down_image, (40, 40))
        self.head_up_image = pygame.image.load('snake head up.png').convert()
        self.head_up_image = pygame.transform.scale(self.head_up_image, (40, 40))
        self.head_left_image = pygame.image.load('snake head left.png').convert()
        self.head_left_image = pygame.transform.scale(self.head_left_image, (40, 40))
        self.head_right_image = pygame.image.load('snake head right.png').convert()
        self.head_right_image = pygame.transform.scale(self.head_right_image, (40, 40))
        self.body_image = pygame.image.load("snake block.jpg").convert()
        self.body_image = pygame.transform.scale(self.body_image, (40, 40))
        self.direction = 'down'
        self.length = 1
        self.head_x = 40
        self.head_y = 40
        self.body_x = []
        self.body_y = []
        self.moveup = False
        self.movedown = False
        self.moveleft = False
        self.moveright = False
        self.angle = 0
        self.head_surface = pygame.Surface((SIZE, SIZE))
        self.head_surface.fill(green)    
    def move_left(self):
        if self.moveright == False:
            self.angle = 180
            self.moveleft = True
            self.direction = 'left'
            self.moveup = False
            self.movedown = False
            self.moveright = False
            pygame.display.update()

    def move_right(self):
        if self.moveleft == False:
            self.angle = 90
            self.direction = 'right'
            self.moveright = True
            self.moveup = False
            self.moveleft = False
            self.movedown = False
            pygame.display.update()

    def move_up(self):
        if self.movedown == False:
            self.angle = 180
            self.direction = 'up'
            self.moveup = True
            self.movedown = False
            self.moveleft = False
            self.moveright = False
            pygame.display.update()

    def move_down(self):
        if self.moveup == False:
            self.angle = 0
            self.direction = 'down'
            self.movedown = True
            self.moveup = False
            self.moveleft = False
            self.moveright = False
            pygame.display.update()

    def walk(self):
        # update body
        if self.length > 1:
            self.body_x.append(self.head_x)
            self.body_y.append(self.head_y)
            for i in range(self.length-2, -1, -1):
                self.body_x[i+1] = self.body_x[i]
                self.body_y[i+1] = self.body_y[i]
            self.body_x[0] = self.head_x
            self.body_y[0] = self.head_y

        # update head
        if self.direction == 'left':
            self.head_x -= SIZE
            
        if self.direction == 'right':
            self.head_x += SIZE
        if self.direction == 'up':
            self.head_y -= SIZE
        if self.direction == 'down':
            self.head_y += SIZE

    def check_collision(self):
        collide = pygame.Rect.colliderect(self.head_surface, self.body_image)
        head_rect = pygame.Rect(self.head_x, self.head_y, SIZE, SIZE)
        for i in range(1, self.length):
            body_rect = pygame.Rect(self.body_x[i], self.body_y[i], SIZE, SIZE)
            if head_rect.colliderect(body_rect):
                self.died = True
                return True
        return False
               
        
    def draw(self):
        self.parent_screen.blit(self.head_surface, (self.head_x, self.head_y))
        if self.direction == 'down':
            head_image = self.head_down_image
        elif self.direction == 'up':
            head_image = self.head_up_image
        elif self.direction == 'left':
            head_image = self.head_left_image
        elif self.direction == 'right':
            head_image = self.head_right_image

        self.parent_screen.blit(head_image, (self.head_x, self.head_y))
        for i in range(self.length-1):
            self.parent_screen.blit(self.body_image, (self.body_x[i], self.body_y[i]))

        pygame.display.update()
class Game:
    def __init__(self): # make it move by score
        self.surface = pygame.display.set_mode((520, 520))
        pygame.display.set_caption('Snake Game')
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.died = False
        self.score= 0
        self.lvl1 = False

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def play(self):
        snake_rect = pygame.Rect(self.snake.head_x, self.snake.head_y, SIZE, SIZE)
        apple_rect = pygame.Rect(self.apple.x, self.apple.y, SIZE, SIZE)

        if snake_rect.colliderect(apple_rect):
            self.snake.length += 1
            self.score+= 1
            self.snake.body_x.append(self.snake.head_x)
            self.snake.body_y.append(self.snake.head_y)
            self.apple.move()

        for i in range(self.snake.length - 1):
            self.body_rect = pygame.Rect(self.snake.body_x[i], self.snake.body_y[i], SIZE, SIZE)

        if self.snake.head_x < 0 or self.snake.head_x >= 500 or self.snake.head_y < 0 or self.snake.head_y >= 500:
            self.died = True

        if self.snake.head_x < 0 or self.snake.head_x >= 420 or self.snake.head_y < 0 or self.snake.head_y >= 420:
            if self.lvl1 == True:
                self.died = True

        if self.score == 15:
            self.surface = pygame.display.set_mode((400, 400))
            self.lvl1 = True
        if self.score != 15:
            self.lvl1 = False
            

        self.snake.walk()
        self.surface.blit(BACKGROUND, (0, 0))
        self.snake.draw()
        self.apple.draw()
        self.draw_score()
        pygame.display.flip()


    def draw_end_screen(self):
         self.surface.blit(END_IMAGE, (0,0))
         pygame.display.update()
         

    def draw_score(self):
         self.font = pygame.font.SysFont('freesansbold.ttf', 32)
         self.text = self.font.render(f'{self.score}', True, green, blue)
         self.surface.blit(self.text, (240, 5))
 
         
         



    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            
            clock.tick(10)       
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pause = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                         pause = True
                         if pause == True:
                            pygame.time.wait(100)
                    elif event.key == pygame.K_r:
                        pause = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.snake.move_left()
                        
                    elif event.key == pygame.K_RIGHT:
                        self.snake.move_right()

                    elif event.key == pygame.K_UP:
                        self.snake.move_up()

                    elif event.key == pygame.K_DOWN:
                        self.snake.move_down()
            if self.died == True:
                 self.draw_end_screen()
                 print(self.died)
                 pygame.time.wait(1000)
                 pygame.quit()
            if self.score== 5:
                if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.key == pygame.K_LEFT:
                        self.snake.move_right()
                        self.snake.moveright = False
                elif event.key == pygame.K_RIGHT:
                        self.snake.move_left()
                        self.snake.moveleft = False
                elif event.key == pygame.K_UP:
                        self.snake.move_down()
                        self.snake.movedown = False
                elif event.key == pygame.K_DOWN:
                        self.snake.move_up()
                        self.snake.moveup = False
            self.play()
        pygame.quit()
def play_game():
        pygame.init()
        pygame.font.init()
        game = Game()
        game.run()
if __name__ == '__main__':
        play_game()
