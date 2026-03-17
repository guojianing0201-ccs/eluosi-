import pygame
import random
from typing import List, Tuple


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
BLOCK_SIZE = 25
PLAY_WIDTH = 10 * BLOCK_SIZE
PLAY_HEIGHT = 20 * BLOCK_SIZE
PLAY_TOP_LEFT_X = (WINDOW_WIDTH - PLAY_WIDTH) // 2
PLAY_TOP_LEFT_Y = WINDOW_HEIGHT - PLAY_HEIGHT - 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (200, 30, 30)
GREEN = (30, 200, 30)
BLUE = (30, 30, 200)
CYAN = (0, 180, 180)
YELLOW = (220, 220, 0)
MAGENTA = (200, 0, 200)
ORANGE = (255, 140, 0)

SHAPES = [
    [[".....",
      ".....",
      ".00..",
      ".00..",
      "....."]],
    [[".....",
      "..0..",
      "..0..",
      "..0..",
      "..0.."],
     [".....",
      "0000.",
      ".....",
      ".....",
      "....."]],
    [[".....",
      ".0...",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..00.",
      "..0..",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "...0.",
      "....."],
     [".....",
      "..0..",
      "..0..",
      ".00..",
      "....."]],
    [[".....",
      "...0.",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..0..",
      "..00.",
      "....."],
     [".....",
      ".....",
      ".000.",
      ".0...",
      "....."],
     [".....",
      ".00..",
      "..0..",
      "..0..",
      "....."]],
    [[".....",
      "..00.",
      ".00..",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..00.",
      "...0.",
      "....."]],
    [[".....",
      ".00..",
      "..00.",
      ".....",
      "....."],
     [".....",
      "..0..",
      ".00..",
      ".0...",
      "....."]],
    [[".....",
      "..0..",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      ".000.",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "..0..",
      "....."],
     [".....",
      "..0..",
      ".00..",
      "..0..",
      "....."]],
]

SHAPE_COLORS = [YELLOW, CYAN, ORANGE, BLUE, GREEN, RED, MAGENTA]


class Piece:
    def __init__(self, x: int, y: int, shape_index: int):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.rotation = 0

    @property
    def shape(self) -> List[str]:
        return SHAPES[self.shape_index][self.rotation % len(SHAPES[self.shape_index])]

    @property
    def color(self) -> Tuple[int, int, int]:
        return SHAPE_COLORS[self.shape_index]


def create_grid(locked: dict) -> List[List[Tuple[int, int, int]]]:
    grid = [[BLACK for _ in range(10)] for _ in range(20)]
    for (x, y), color in locked.items():
        if 0 <= y < 20 and 0 <= x < 10:
            grid[y][x] = color
    return grid


def convert_shape_format(piece: Piece) -> List[Tuple[int, int]]:
    positions = []
    shape = piece.shape

    for i, line in enumerate(shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions


def valid_space(piece: Piece, grid: List[List[Tuple[int, int, int]]]) -> bool:
    accepted_positions = [
        (j, i)
        for i in range(20)
        for j in range(10)
        if grid[i][j] == BLACK
    ]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions and pos[1] > -1:
            return False
    return True


def check_lost(locked: dict) -> bool:
    for (_, y) in locked.keys():
        if y < 1:
            return True
    return False


def get_new_piece() -> Piece:
    return Piece(5, 0, random.randint(0, len(SHAPES) - 1))


def clear_rows(grid, locked):
    rows_to_clear = []
    for i in range(len(grid) - 1, -1, -1):
        if BLACK not in grid[i]:
            rows_to_clear.append(i)

    if not rows_to_clear:
        return 0

    for row in rows_to_clear:
        for x in range(10):
            try:
                del locked[(x, row)]
            except KeyError:
                continue

    for row in sorted(rows_to_clear):
        for (x, y) in sorted(list(locked.keys()), key=lambda p: p[1]):
            if y < row:
                color = locked.pop((x, y))
                locked[(x, y + 1)] = color

    return len(rows_to_clear)


def draw_grid(surface):
    for i in range(21):
        pygame.draw.line(
            surface,
            GRAY,
            (PLAY_TOP_LEFT_X, PLAY_TOP_LEFT_Y + i * BLOCK_SIZE),
            (PLAY_TOP_LEFT_X + PLAY_WIDTH, PLAY_TOP_LEFT_Y + i * BLOCK_SIZE),
            1,
        )

    for j in range(11):
        pygame.draw.line(
            surface,
            GRAY,
            (PLAY_TOP_LEFT_X + j * BLOCK_SIZE, PLAY_TOP_LEFT_Y),
            (PLAY_TOP_LEFT_X + j * BLOCK_SIZE, PLAY_TOP_LEFT_Y + PLAY_HEIGHT),
            1,
        )


def draw_window(surface, grid, score, high_score):
    surface.fill(BLACK)

    title_font = pygame.font.SysFont("arial", 32, bold=True)
    label = title_font.render("俄罗斯方块", True, WHITE)
    surface.blit(label, (WINDOW_WIDTH / 2 - label.get_width() / 2, 10))

    score_font = pygame.font.SysFont("arial", 20)
    score_label = score_font.render(f"得分: {score}", True, WHITE)
    hs_label = score_font.render(f"最高分: {high_score}", True, WHITE)
    surface.blit(score_label, (20, 60))
    surface.blit(hs_label, (20, 90))

    for i in range(20):
        for j in range(10):
            color = grid[i][j]
            if color != BLACK:
                pygame.draw.rect(
                    surface,
                    color,
                    (
                        PLAY_TOP_LEFT_X + j * BLOCK_SIZE,
                        PLAY_TOP_LEFT_Y + i * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                )

    pygame.draw.rect(
        surface,
        WHITE,
        (
            PLAY_TOP_LEFT_X,
            PLAY_TOP_LEFT_Y,
            PLAY_WIDTH,
            PLAY_HEIGHT,
        ),
        3,
    )

    draw_grid(surface)


def draw_piece(surface, piece: Piece):
    formatted = convert_shape_format(piece)
    for (x, y) in formatted:
        if y >= 0:
            pygame.draw.rect(
                surface,
                piece.color,
                (
                    PLAY_TOP_LEFT_X + x * BLOCK_SIZE,
                    PLAY_TOP_LEFT_Y + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                ),
            )


def draw_next_shape(surface, piece: Piece):
    font = pygame.font.SysFont("arial", 20)
    label = font.render("下一个：", True, WHITE)
    start_x = PLAY_TOP_LEFT_X + PLAY_WIDTH + 20
    start_y = PLAY_TOP_LEFT_Y + 40

    surface.blit(label, (start_x, PLAY_TOP_LEFT_Y))

    shape = piece.shape
    for i, line in enumerate(shape):
        for j, char in enumerate(line):
            if char == "0":
                pygame.draw.rect(
                    surface,
                    piece.color,
                    (
                        start_x + j * BLOCK_SIZE,
                        start_y + i * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                )


def main():
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("俄罗斯方块 - Python 版本")

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5

    locked_positions = {}
    current_piece = get_new_piece()
    next_piece = get_new_piece()
    score = 0
    high_score = 0

    running = True

    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[(pos[0], pos[1])] = current_piece.color
                cleared = clear_rows(grid, locked_positions)
                if cleared:
                    score += cleared * 100
                    fall_speed = max(0.1, fall_speed - 0.02 * cleared)
                current_piece = next_piece
                next_piece = get_new_piece()
                if check_lost(locked_positions):
                    high_score = max(high_score, score)
                    locked_positions = {}
                    current_piece = get_new_piece()
                    next_piece = get_new_piece()
                    score = 0
                    fall_speed = 0.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(
                        SHAPES[current_piece.shape_index]
                    )
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(
                            SHAPES[current_piece.shape_index]
                        )
                if event.key == pygame.K_SPACE:
                    while True:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                            break

        draw_window(win, grid, score, high_score)
        draw_piece(win, current_piece)
        draw_next_shape(win, next_piece)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
