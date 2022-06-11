import pygame
import GameDef


class PacMan(pygame.sprite.Sprite):
    FRAME_HEIGHT = 36
    FRAME_WIDTH = 36

    def __init__(self):
        super().__init__()
        self.__sub_surface = []
        self.__current_frame = 0
        self.first_frame = 0  # 第一帧编号
        self.last_frame = 5  # 最后一帧编号
        self.last_time = 0
        self.__center_pos = [60, 60]
        self.__pos_rect = pygame.Rect(
            0, 0, PacMan.FRAME_WIDTH, PacMan.FRAME_HEIGHT)
        self.__pos_rect.left = self.__center_pos[0] - PacMan.FRAME_WIDTH/2
        self.__pos_rect.top = self.__center_pos[1] - PacMan.FRAME_HEIGHT/2
        self.__maze = None

    def Draw(self, surface):
        surface.blit(self.__sub_surface[self.__current_frame], self.__pos_rect)

    def SetMaze(self, m):
        self.__maze = m

    def Load(self):
        self.image = pygame.image.load(
            "Resources/pac-6-1-6.png").convert_alpha()
        self.__BuildSubSurface()

    def __BuildSubSurface(self):
        for i in range(6):
            src_rect = pygame.Rect(
                0, i*PacMan.FRAME_HEIGHT, PacMan.FRAME_WIDTH, PacMan.FRAME_HEIGHT)
            self.__sub_surface.append(self.image.subsurface(src_rect))

    def update(self, current_time, rate=60):
        # 更新动画帧
        if current_time > self.last_time + rate:
            self.__current_frame += 1
            if self.__current_frame > self.last_frame:
                self.__current_frame = self.first_frame
            self.last_time = current_time

    def Move(self, event):
        self.__move_speed = 2
        cx = self.__center_pos[0]
        cy = self.__center_pos[1]

        key_pressed = pygame.key.get_pressed()
        # IsBlock(self, new_center_rect, rush_dir):
        if key_pressed[pygame.K_LEFT]:
            cx = cx - self.__move_speed
            new_rect = pygame.rect.Rect(
                cx-PacMan.FRAME_WIDTH/2, cy-PacMan.FRAME_HEIGHT/2, PacMan.FRAME_WIDTH, PacMan.FRAME_HEIGHT)
            is_block = self.__maze.IsBlock(new_rect, GameDef.DIR_LEFT)
            if not is_block:
                self.__center_pos[0] = cx
        elif key_pressed[pygame.K_RIGHT]:
            cx = cx+self.__move_speed
            new_rect = pygame.rect.Rect(
                cx-PacMan.FRAME_WIDTH/2, cy-PacMan.FRAME_HEIGHT/2, PacMan.FRAME_WIDTH, PacMan.FRAME_HEIGHT)
            is_block = self.__maze.IsBlock(new_rect, GameDef.DIR_RIGHT)
            if not is_block:
                self.__center_pos[0] = cx
        elif key_pressed[pygame.K_UP]:
            cy = cy-self.__move_speed
            new_rect = pygame.rect.Rect(
                cx-PacMan.FRAME_WIDTH/2, cy-PacMan.FRAME_HEIGHT/2, PacMan.FRAME_WIDTH, PacMan.FRAME_HEIGHT)
            is_block = self.__maze.IsBlock(new_rect, GameDef.DIR_UP)
            if not is_block:
                self.__center_pos[1] = cy
        elif key_pressed[pygame.K_DOWN]:
            cy = cy+self.__move_speed
            new_rect = pygame.rect.Rect(
                cx-PacMan.FRAME_WIDTH/2, cy-PacMan.FRAME_HEIGHT/2, PacMan.FRAME_WIDTH, PacMan.FRAME_HEIGHT)
            is_block = self.__maze.IsBlock(new_rect, GameDef.DIR_DOWN)
            if not is_block:
                self.__center_pos[1] = cy

        self.__pos_rect.left = self.__center_pos[0] - PacMan.FRAME_WIDTH/2
        self.__pos_rect.top = self.__center_pos[1] - PacMan.FRAME_HEIGHT/2

    def GetCenterPos(self):
        return self.__center_pos
