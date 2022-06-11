import pygame
import GameDef


class GameMaze(pygame.sprite.Sprite):

    def __init__(self) -> None:
        self.image = pygame.image.load("Resources/pac_tiles-4-4-1.png")
        self.rect = self.image.get_rect()
        self.__maze_tile_data = []
        self.m_nNumItems = 0
        self.__blank_tile_rect = pygame.Rect(
            GameDef.TILE_BLANK * GameDef.TILE_WIDTH, 0, GameDef.TILE_WIDTH, GameDef.TILE_HEIGHT)
        self.__blank_tile_subsurface = None

    def Load(self):
        map_file = open("Resources/mapdata.txt")

        for colume in range(GameDef.MAP_ROW_COUNT):  # 地图文件共15行
            onelineStr = map_file.readline()
            for c in onelineStr:  # 每行共20个字符，共二十列
                if c == '0':
                    idx = GameDef.TILE_BLOCK
                    src_rect = pygame.Rect(
                        idx * GameDef.TILE_WIDTH, 0, GameDef.TILE_WIDTH, GameDef.TILE_HEIGHT)
                    sub_surface = self.image.subsurface(src_rect)
                    self.__maze_tile_data.append([idx, sub_surface])
                elif c == '2':
                    idx = GameDef.TILE_ITEM
                    src_rect = pygame.Rect(
                        idx * GameDef.TILE_WIDTH, 0, GameDef.TILE_WIDTH, GameDef.TILE_HEIGHT)
                    sub_surface = self.image.subsurface(src_rect)
                    self.__maze_tile_data.append([idx, sub_surface])
                elif c == '3':
                    idx = GameDef.TILE_POWERUP
                    src_rect = pygame.Rect(
                        idx * GameDef.TILE_WIDTH, 0, GameDef.TILE_WIDTH, GameDef.TILE_HEIGHT)
                    sub_surface = self.image.subsurface(src_rect)
                    self.__maze_tile_data.append([idx, sub_surface])

        map_file.close()
        self.__blank_tile_subsurface = self.image.subsurface(
            self.__blank_tile_rect)

    def Draw(self, surface):
        for row in range(GameDef.MAP_ROW_COUNT):
            for colume in range(GameDef.MAP_COLUME_COUNT):
                idx = row*GameDef.MAP_COLUME_COUNT+colume
                dst_rect = pygame.Rect(colume*40, row*40, 40, 40)
                surface.blit(self.__maze_tile_data[idx][1], dst_rect)

    # @param new_center_rect 角色将要移动过去的新的矩形
    # @param char_half_width 角色矩形的半宽
    # @param char_half_height 角色矩形的半高
    # @param rush_dir 角色的移动方向
    def IsBlock(self, new_center_rect, rush_dir):
        check_pos_1 = None
        check_pos_2 = None

        if GameDef.DIR_LEFT == rush_dir:  # 向左移动，检查左上角和左下角
            check_pos_1 = (new_center_rect.left, new_center_rect.top)  # 左上角
            check_pos_2 = (new_center_rect.left, new_center_rect.bottom)  # 左下角
        elif GameDef.DIR_RIGHT == rush_dir:  # 向右移动，检查右上角和右下角
            check_pos_1 = (new_center_rect.right, new_center_rect.top)  # 右上角
            check_pos_2 = (new_center_rect.right,
                           new_center_rect.bottom)  # 右下角
        elif GameDef.DIR_UP == rush_dir:  # 向上移动，检查左上角和右上角
            check_pos_1 = (new_center_rect.left, new_center_rect.top)  # 左上角
            check_pos_2 = (new_center_rect.right, new_center_rect.top)  # 右上角
        elif GameDef.DIR_DOWN == rush_dir:  # 向下移动，检查左下角和右下角
            check_pos_1 = (new_center_rect.left, new_center_rect.bottom)  # 左下角
            check_pos_2 = (new_center_rect.right,
                           new_center_rect.bottom)  # 右下角

        maze_width = GameDef.TILE_WIDTH * GameDef.MAZE_SIZE_X
        maze_height = GameDef.TILE_HEIGHT * GameDef.MAZE_SIZE_Y

        # 超出地图范围了
        if check_pos_1[0] < 0 or check_pos_1[0] > maze_width or check_pos_1[1] < 0 or check_pos_1[1] > maze_height or check_pos_2[0] < 0 or check_pos_2[0] > maze_width or check_pos_2[1] < 0 or check_pos_2[1] > maze_height:
            return False

        idx_x_1 = int(check_pos_1[0] / GameDef.TILE_WIDTH)
        idx_y_1 = int(check_pos_1[1] / GameDef.TILE_HEIGHT)
        target_rect_1 = self.__GetMazeTileRect(idx_x_1, idx_y_1)
        target_tile_type_1 = self.__GetMazeTileType(idx_x_1, idx_y_1)

        idx_x_2 = int(check_pos_2[0] / GameDef.TILE_WIDTH)
        idx_y_2 = int(check_pos_2[1] / GameDef.TILE_HEIGHT)
        target_rect_2 = self.__GetMazeTileRect(idx_x_2, idx_y_2)
        target_tile_type_2 = self.__GetMazeTileType(idx_x_2, idx_y_2)

        if target_tile_type_1 != GameDef.TILE_BLOCK and target_tile_type_2 != GameDef.TILE_BLOCK:
            # 两个都不是block，直接返回true
            return False
        elif target_tile_type_1 == GameDef.TILE_BLOCK and target_tile_type_2 != GameDef.TILE_BLOCK:
            # 2是block，则检查有没有和1相交,有相交的话就返回true，否则false
            return new_center_rect.colliderect(target_rect_1)
        elif target_tile_type_1 != GameDef.TILE_BLOCK and target_tile_type_2 == GameDef.TILE_BLOCK:
            # 2是block，则检查有没有和1相交,有相交的话就返回true，否则false
            return new_center_rect.colliderect(target_rect_2)
        elif target_tile_type_1 == GameDef.TILE_BLOCK and target_tile_type_2 == GameDef.TILE_BLOCK:
            return new_center_rect.colliderect(target_rect_2) or new_center_rect.colliderect(target_rect_1)

    # 获取到第y_row行，第x_column列的TILE的类型
    def __GetMazeTileType(self, x_column, y_row):
        idx = y_row * GameDef.MAZE_SIZE_X + x_column
        return self.__maze_tile_data[idx][0]

    # 获取到第y_row行，第x_column列的TILE的矩形，基于世界坐标
    def __GetMazeTileRect(self, x_column, y_row):
        left = x_column * GameDef.TILE_WIDTH
        top = y_row * GameDef.TILE_HEIGHT
        return pygame.rect.Rect(left, top, GameDef.TILE_WIDTH, GameDef.TILE_HEIGHT)

    def ToAdjacentPosition(self, pos, rush_dir):
        pos_x = pos[0]
        pos_y = pos[1]
        if rush_dir == GameDef.DIR_UP:
            pos_y -= 1
        elif rush_dir == GameDef. DIR_DOWN:
            pos_y += 1
        elif rush_dir == GameDef.DIR_LEFT:
            pos_x -= 1
        elif rush_dir == GameDef.DIR_RIGHT:
            pos_x += 1

        return (pos_x, pos_y)

    def __MakeTileBlank(self, tile_index):
        self.__maze_tile_data[tile_index][0] = GameDef.TILE_BLANK
        self.__maze_tile_data[tile_index][1] = self.__blank_tile_subsurface

    def UpdateItems(self, pacmanCenterPos):
        ret = self.__CanEatItem(pacmanCenterPos)
        if ret[0]:
            if self.__maze_tile_data[ret[1]][0] == GameDef.TILE_ITEM:
                self.__MakeTileBlank(ret[1])
                self.m_nNumItems = self.m_nNumItems - 1
            elif self.__maze_tile_data[ret[1]][0] == GameDef.TILE_POWERUP:
                self.__MakeTileBlank(ret[1])
                self.m_nNumItems = self.m_nNumItems - 1

        if self.m_nNumItems == 0:
            pass  # 游戏结束

        return False

    # 判断能否吃到点
    def __CanEatItem(self, pacman_center_pos):
        x = int(pacman_center_pos[0] / GameDef.TILE_WIDTH)
        y = int(pacman_center_pos[1] / GameDef.TILE_HEIGHT)
        tile_center_x = (x+0.5)*GameDef.TILE_WIDTH
        tile_center_y = (y+0.5)*GameDef.TILE_HEIGHT
        is_x = abs(pacman_center_pos[0] -
                   tile_center_x) <= GameDef.TILE_WIDTH * 0.125
        is_y = abs(pacman_center_pos[1] -
                   tile_center_y) <= GameDef.TILE_HEIGHT * 0.125
        return is_x and is_y, y*GameDef.MAZE_SIZE_X + x
