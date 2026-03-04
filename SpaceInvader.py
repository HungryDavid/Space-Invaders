import math
import random
import time
import turtle as t
import pygame

pygame.mixer.init()
pygame.mixer.music.load("sounds/spaceinvaders1.mpeg")
pygame.mixer.music.play(loops=-1) 
shoot = pygame.mixer.Sound("sounds/shoot.wav")
invaderkilled = pygame.mixer.Sound("sounds/invaderkilled.wav")
explosion = pygame.mixer.Sound("sounds/explosion.wav")
victory = pygame.mixer.Sound("sounds/victory.mp3")

def display_screen(screen):
  screen.bgcolor("black")
  screen.title("Space Invaders")
  screen.tracer(0)

class player_module():
  def __init__(self):
    self.playerspeed = 20
    self.player = t.Turtle()
    self.player.color("blue")
    self.player.shape("triangle")
    self.player.penup()
    self.player.speed(0)
    self.player.setposition(0, -250)
    self.player.setheading(90)

    self.bulletspeed = 10
    self.bullets = []
    self.last_shot_time = 0
    self.shoot_cooldown = 0.3
    self.bulletstate = "available"

  def move_left(self):
    x = self.player.xcor()
    x -= self.playerspeed
    if x < -280:
      x = -280
    self.player.setx(x)

  def move_right(self):
    x = self.player.xcor()
    x += self.playerspeed
    if x > 280:
      x = 280
    self.player.setx(x)
  
  def fire_bullet(self):
    if self.bulletstate == "available":
      current_time = time.time()

      if current_time - self.last_shot_time >= self.shoot_cooldown:
        self.last_shot_time = current_time
        bullet = t.Turtle()
        bullet.color("Yellow")
        bullet.shape("circle")
        bullet.penup()
        bullet.speed(0)
        bullet.setheading(90)
        bullet.shapesize(0.5, 0.5)

        x = self.player.xcor()
        y = self.player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
        shoot.play()
        self.bullets.append(bullet)
  
  def bullet_move(self):
    for bullet in self.bullets:
      y = bullet.ycor()
      y += self.bulletspeed
      bullet.sety(y)

    for bullet in self.bullets[:]:
      if bullet.ycor() > 275:
        bullet.hideturtle()
        if bullet in self.bullets:
          self.bullets.remove(bullet)

class enemy_module():
  def __init__(self, x=0, y=0):
    #self.enemyspeed = random.uniform(0.2, 1)
    self.enemyspeed = 0.5
    self.enemy = t.Turtle()
    self.enemy.color("red")
    self.enemy.shape("square")
    self.enemy.penup()
    self.enemy.speed(0)
    self.enemy.setposition(x, y)

  def enemy_move(self):
    x = self.enemy.xcor()
    x += self.enemyspeed
    self.enemy.setx(x)


def create_writer(writer):
  writer.hideturtle()
  writer.penup()
  writer.color("white")
  writer.goto(-280, 260)

def display_score(writer):
  writer.clear()
  writer.write(f"Score: {score}", font=("Arial", 12, "normal"))

def isCollision(player, enemies, writer):
  global score
  for bullet in player.bullets[:]:
    for enemy in enemies:
      if (abs(bullet.xcor() - enemy.enemy.xcor()) < 10 and abs(bullet.ycor() - enemy.enemy.ycor()) < 15):
        bullet.hideturtle()
        if bullet in player.bullets:
          player.bullets.remove(bullet)
        enemy.enemy.hideturtle()
        enemies.remove(enemy)
        invaderkilled.play()
        score += 1
        display_score(writer)

def game_over(player, enemies, writer):
  for enemy in enemies:
    if ((abs(player.player.xcor() - enemy.enemy.xcor()) < 10 and abs(player.player.ycor() - enemy.enemy.ycor()) < 15) or enemy.enemy.ycor() < -255):
      if player.bulletstate == "available":
        pygame.mixer.music.stop()
        explosion.play()
      player.bulletstate = "unavailable"
      player.player.hideturtle()
      for enemy in enemies:
        enemy.enemy.hideturtle()
      writer.clear()
      over = t.Turtle()
      over.hideturtle()
      over.penup()

      over.goto(0, 0)
      over.color("white")

      over.write("Game Over!", align="center", font=("Arial", 25, "normal"))
      over.goto(0, -50)
      over.write(f"Final Score: {score}", align="center", font=("Arial", 13, "normal"))

  if(not enemies):
      if player.bulletstate == "available":
        pygame.mixer.music.stop()
        victory.play()
      player.bulletstate = "unavailable"
      player.player.hideturtle()
      for enemy in enemies:
        enemy.enemy.hideturtle()
        enemies.remove(enemy)
      writer.clear()
      over = t.Turtle()
      over.hideturtle()
      over.penup()

      over.goto(0, 0)
      over.color("white")

      over.write("You Win", align="center", font=("Arial", 25, "normal"))
      over.goto(0, -50)
      over.write(f"Final Score: {score}", align="center", font=("Arial", 13, "normal"))


def create_enemies(enemies):
  x_start = -280
  y_start = 250
  x_spacing = 70
  y_spacing = 50

  for row in range(3):
    for col in range(8):
        enemy = enemy_module() 
        x = x_start + col * x_spacing
        y = y_start - row * y_spacing
        enemy.enemy.setposition(x, y)
        enemies.append(enemy)

def move_enemy(enemies):
  for enemy in enemies:
    enemy.enemy_move()

    if enemy.enemy.xcor() > 320:
      for enemy in enemies:
        y = enemy.enemy.ycor()
        y -= 40
        enemy.enemyspeed *= -1
        enemy.enemy.sety(y)

    if enemy.enemy.xcor() < -320:
      for enemy in enemies:
        y = enemy.enemy.ycor()
        y -= 40
        enemy.enemyspeed *= -1
        enemy.enemy.sety(y)
  
def main():
  global score 
  score = 0
  screen = t.Screen()
  writer = t.Turtle()
  player = player_module()
  enemies = []
  display_screen(screen)
  create_writer(writer)
  display_score(writer)
  create_enemies(enemies)

  def game_loop():
    screen.listen()
    screen.onkeypress(player.move_left, "Left")
    screen.onkeypress(player.move_right, "Right")
    screen.onkey(player.fire_bullet, "space")
    move_enemy(enemies)
    player.bullet_move()
    isCollision(player, enemies, writer)
    game_over(player, enemies, writer)
    screen.update()
    screen.ontimer(game_loop, 16) 
  game_loop()
  screen.mainloop()

  

main()
