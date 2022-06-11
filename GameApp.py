import pygame
from pygame.locals import *
from PacMan import *
from GameMaze import *


class GameApp:
    def __init__(self):
        self.__pac_man = None
        self.__running = True
        self.__display_surface = None
        self.__client_wnd_width = 800
        self.__client_wnd_height = 600
        self.__client_size = (self.__client_wnd_width,
                              self.__client_wnd_height)
        self.__maze = None
        self.__sprite_group = None
        self.__frame_rate = None

    def __OnInit(self):
        pygame.init()
        self.__display_surface = pygame.display.set_mode(
            self.__client_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.__running = True
        self.__pac_man = PacMan()
        self.__pac_man.Load()
        self.__maze = GameMaze()
        self.__maze.Load()
        self.__pac_man.SetMaze(self.__maze)
        self.__sprite_group = pygame.sprite.Group()
        self.__sprite_group.add(self.__pac_man)
        self.__frame_rate = pygame.time.Clock()
        pygame.key.set_repeat(10, 15)

    def __OnEvent(self, event):
        if event.type == pygame.QUIT:
            self.__running = False
        self.__pac_man.Move(event)

    def __OnGameLoop(self):
        self.__frame_rate.tick(30)
        ticks = pygame.time.get_ticks()
        self.__sprite_group.update(ticks)
        self.__maze.UpdateItems(self.__pac_man.GetCenterPos())

    def __OnRender(self):
        self.__display_surface.fill((0, 0, 0))
        self.__maze.Draw(self.__display_surface)
        self.__pac_man.Draw(self.__display_surface)
        pygame.display.flip()

    def __OnCleapup(self):
        pygame.quit()

    def Run(self):
        if self.__OnInit() == False:
            self.__running = False

        while (self.__running):
            for event in pygame.event.get():
                self.__OnEvent(event)
            self.__OnGameLoop()
            self.__OnRender()

        self.__OnCleapup()


if __name__ == "__main__":
    theApp = GameApp()
    theApp.Run()
