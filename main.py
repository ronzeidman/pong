import pygame
import pygame.freetype

from assets import get_initial_assets

# flappy bird
# dinasaur jump
# pong
# brick breaker
# astroids
# shooting balls
# aliens

# -----------------------------------------------------------------------

SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600 
WINDOW_COLOR = (30, 30, 30)
FPS = 60
# ------------------------------------------------------------------------

pygame.init()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Pong")

def main():
  clock = pygame.time.Clock()

  prev_assets = get_initial_assets(WIN)
  while True:
    clock.tick(FPS)
    WIN.fill(WINDOW_COLOR)
    next_assets = []
    for asset in prev_assets:
      asset.update(WIN, prev_assets, next_assets)
    pygame.display.update()
    prev_assets = next_assets
    # Exiting
    run = True
    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        run = False
    if not run:
      break

  pygame.quit()

if __name__ == "__main__":
  main()