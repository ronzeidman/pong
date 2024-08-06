from __future__ import annotations
from math import cos, pi, sin
from random import randrange, uniform
import pygame
from typing import List
import pygame.freetype


def left_bound_collision(x: int):
  return x < 0

def right_bound_collision(x: int, width: int, surface: pygame.Surface):
  return x > surface.width - width

def top_bound_collision(y: int):
  return y < 0

def bottom_bound_collision(y: int, height: int, surface: pygame.Surface):
  return y > surface.height - height


class Asset:
  def __init__(self, surface: pygame.Surface) -> None:
    self.rect = None

  def update(self, prev_assets: List[Asset], next_assets: List[Asset]):
    pass


class Ball(Asset):
  def __init__(self, surface: pygame.Surface) -> None:
    super().__init__(surface)
    size = (20, 20)
    initial_position = (surface.width / 2 - size[0] / 2, surface.height / 2 - size[1] / 2)
    self.rect = pygame.Rect(*initial_position, *size)
    self.speed = 7
    self.angle = uniform(pi / 4, pi * 3 / 4) + (randrange(0, 1) * pi) # 0 = down, pi / 2 = right, pi = up, 3pi / 2 = left
    # print(f'ball angle start {self.angle * 180 / pi}')
    self.color = (175, 75, 0)

  def update(self, surface: pygame.Surface, prev_assets: List[Asset], next_assets: List[Asset]):
    player1 = None
    player2 = None
    for player in prev_assets:
      if isinstance(player, Player):
        if player.num == 1:
          player1 = player
        else:
          player2 = player
        if player.rect.colliderect(self.rect):
          middle = self.rect.y + (self.rect.height / 2)
          relative_pos = (middle - player.rect.y) / player.rect.height
          if player.num == 1 and self.angle > pi:
            self.angle = pi / 2 * (1 - relative_pos) + pi / 4
            # print(f'ball angle player collision changed to {self.angle * 180 / pi}')
          elif player.num != 1 and self.angle < pi:
            self.angle = pi / 2 * relative_pos + pi * 5 / 4
            # print(f'ball angle player collision changed to {self.angle * 180 / pi}')

    (x_update, y_update) = self.update_speeds()
    left_collision = left_bound_collision(self.rect.x + x_update)
    right_collision = right_bound_collision(self.rect.x, self.rect.width, surface)
    if left_collision or right_collision:
      self.angle = 2*pi - self.angle
      # print(f'ball angle changed to {self.angle * 180 / pi}')
      (x_update, y_update) = self.update_speeds()
      if left_collision:
        player2.score += 1
      else:
        player1.score += 1
    if top_bound_collision(self.rect.y + y_update) or bottom_bound_collision(self.rect.y, self.rect.height, surface):
      self.angle = pi - self.angle
      # print(f'ball angle changed to {self.angle * 180 / pi}')
      (x_update, y_update) = self.update_speeds()
    self.rect.x += x_update
    self.rect.y += y_update
    while self.angle < 0:
      self.angle += 2 * pi
    while self.angle > 2 * pi:
      self.angle -= 2 * pi
    pygame.draw.ellipse(surface, self.color, self.rect)
    next_assets.append(self)
  
  def update_speeds(self) -> tuple[float, float]:
    return (self.speed * sin(self.angle), self.speed * cos(self.angle))


class Player(Asset):
  def __init__(self, surface: pygame.Surface, player: int) -> None:
    super().__init__(surface)
    self.score_font = pygame.freetype.SysFont('Comic Sans MS', 30)
    self.num = player
    self.score = 0
    margin = 50
    size = (20, 80)
    initial_y = surface.height / 2 - size[1] / 2
    if player == 1:
      initial_position = (margin, initial_y)
      self.score_pos = (margin + 200, margin)
      self.color = (175, 0, 0)
      self.up_key = pygame.K_w
      self.down_key = pygame.K_s
    else:
      initial_position = (surface.width - margin - size[0] , initial_y)
      self.score_pos = (surface.width - margin - 200, margin)
      self.color = (0, 175, 0)
      self.up_key = pygame.K_UP
      self.down_key = pygame.K_DOWN
    self.speed = 10
    self.rect = pygame.Rect(*initial_position, *size)

  def update(self, surface: pygame.Surface, prev_assets: List[Asset], next_assets: List[Asset]):
    key = pygame.key.get_pressed()
    if key[self.up_key]:
      if top_bound_collision(self.rect.y - self.speed):
        self.rect.y = 0
      else:
        self.rect.y -= self.speed
    if key[self.down_key]:
      if bottom_bound_collision(self.rect.y + self.speed, self.rect.height, surface):
        self.rect.y = surface.height - self.rect.height
      else:
        self.rect.y += self.speed
    self.score_font.render_to(surface, self.score_pos, str(self.score), self.color)
    pygame.draw.rect(surface, self.color, self.rect)
    next_assets.append(self)

# class Ball(Asset):
#   def __init__(self, surface: pygame.Surface) -> None:
#     self.rect = pygame.Rect(400, 300, 30, 30)
#     self.speed = 3

#   def update(self, surface: pygame.Surface, prev_assets: List[Asset], next_assets: List[Asset]):
#     if self.rect.x > surface.width - self.rect.width:
#       self.rect.x = 0
#     self.rect.x = self.rect.x + self.speed
#     pygame.draw.ellipse(surface, (170, 100, 50), self.rect)
#     next_assets.append(self)


# class Player(Asset):
#   def __init__(self, surface: pygame.Surface, num: int) -> None:
#     self.num = num
#     if num == 1:
#       self.rect = pygame.Rect(20, 30, 30, 100)
#       self.color = (100, 0, 30)
#       self.up_key = pygame.K_z
#       self.down_key = pygame.K_x
#     if num == 2:
#       self.rect = pygame.Rect(750, 30, 30, 100)
#       self.color = (0, 100, 0)
#       self.up_key = pygame.K_KP_2
#       self.down_key = pygame.K_KP_3
#     self.speed = 3


#   def update(self, surface: pygame.Surface, prev_assets: List[Asset], next_assets: List[Asset]):
#     key = pygame.key.get_pressed()
#     if key[self.up_key] and self.rect.y > 0:
#       self.rect.y = self.rect.y - self.speed
#     if key[self.down_key] and self.rect.y < surface.height - self.rect.height:
#       self.rect.y = self.rect.y + self.speed
#     pygame.draw.rect(surface, self.color, self.rect)
#     next_assets.append(self)

# def get_initial_assets(surface: pygame.Surface) -> List[Asset]:
#   return [Player(surface, 1), Player(surface, 2), Ball(surface)] 

def get_initial_assets(surface: pygame.Surface) -> List[Asset]:
  return [Ball(surface), Player(surface,1), Player(surface,2)]

