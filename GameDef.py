DIR_NONE = 0
DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4

MAZE_SIZE_X = 20
MAZE_SIZE_Y = 15

TILE_BLOCK = 0  # 墙，不能通过的tile
TILE_BLANK = 1  # 路，能通过的tile
TILE_ITEM = 2  # 物品，就是“豆子”
TILE_POWERUP = 3  # 力量，player吃了之后能够吃掉ghost
MAP_COLUME_COUNT = 20
MAP_ROW_COUNT = 15
TILE_WIDTH = 40
TILE_HEIGHT = 40

#-------------------------恶魔的状态定义 开始-------------------------#
GHOST_STATE_STRONG = 0      # 强壮的状态，这时候player可以被恶魔杀害
GHOST_STATE_FLASHING = 1    # 恶魔闪烁的状态
GHOST_STATE_WEAK = 2
GHOST_STATE_DEAD = 3		# 恶魔死亡的状态
#-------------------------恶魔的状态定义 结束-------------------------#

#-------------------------恶魔的AI定义 开始-------------------------#
GHOST_AI_AGGRESIVE = 0 # 追击player
GHOST_AI_PASSIVE = 1   # 
GHOST_AI_EVASIVE = 2   # 逃避player
#-------------------------恶魔的AI定义 结束-------------------------#