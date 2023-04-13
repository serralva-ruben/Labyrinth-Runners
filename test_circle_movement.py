import pygame
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

radius = 50
cover_surf = pygame.Surface((radius*2, radius*2))
cover_surf.fill(0)
cover_surf.set_colorkey((255, 255, 255))
pygame.draw.circle(cover_surf, (255, 255, 255), (radius, radius), radius)

run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clip_center = pygame.mouse.get_pos()

    # clear screen and set clipping region
    screen.fill(0)    
    clip_rect = pygame.Rect(clip_center[0]-radius, clip_center[1]-radius, radius*2, radius*2)
    screen.set_clip(clip_rect)

    # draw the scene
    for x in range(10):
        for y in range(10):
            color = (255, 255, 255) if (x+y) % 2 == 0 else (255, 0, 0)
            pygame.draw.rect(screen, color, (x*50, y*50, 50, 50))
    # draw transparent circle and update display
    screen.blit(cover_surf, clip_rect)
    pygame.display.flip()
