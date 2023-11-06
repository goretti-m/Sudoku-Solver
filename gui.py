import pygame
import time
pygame.font.init()

class SudokuSolver:
    initial_board = [
        [0, 7, 9, 1, 3, 2, 0, 8, 5],
        [0, 6, 0, 5, 9, 0, 7, 0, 0],
        [5, 0, 8, 7, 0, 0, 2, 1, 0],
        [0, 8, 7, 0, 0, 0, 3, 0, 0],
        [9, 0, 3, 0, 0, 0, 5, 0, 8],
        [2, 5, 0, 0, 0, 0, 1, 9, 0]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[SudokuCell(self.initial_board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if self.is_valid_move(val, (row, col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows+1):
            thick = 4 if i % 3 == 0 and i != 0 else 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True
        else:
            row, col = empty_cell
        for val in range(1, 10):
            if self.is_valid_move(val, (row, col)):
                self.model[row][col] = val
                if self.solve():
                    return True
                self.model[row][col] = 0
        return False

    def solve_gui(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True
        else:
            row, col = empty_cell
        for val in range(1, 10):
            if self.is_valid_move(val, (row, col)):
                self.model[row][col] = val
                self.cubes[row][col].set(val)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
                if self.solve_gui():
                    return True
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)
        return False

    def find_empty_cell(self):
        for i in range(len(self.model)):
            for j in range(len(self.model[0])):
                if self.model[i][j] == 0:
                    return (i, j)
        return None

    def is_valid_move(self, num, pos):
        row, col = pos
        return self.is_valid_row(num, row) and self.is_valid_column(num, col) and self.is_valid_box(num, row, col)

    def is_valid_row(self, num, row):
        return num not in self.model[row]

    def is_valid_column(self, num, col):
        return num not in [self.model[i][col] for i in range(self.rows)]

    def is_valid_box(self, num, row, col):
        box_row = row // 3
        box_col = col // 3
        for i in range(box_row * 3, box_row * 3 + 3):
            for j in range(box_col * 3, box_col * 3 + 3):
                if self.model[i][j] == num:
                    return False
        return True

class SudokuCell:
    rows = 9
    cols = 9


    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    board.draw()
    pygame.display.update()

def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    mat = " " + str(minute) + ":" + str(sec)
    return mat

def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = SudokuSolver(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                            print("Wrong")
                            strikes += 1
                            key = None
                if board.is_finished():
                            print("Game over")
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                board.select(clicked[0], clicked[1])
                key = None

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

main()
pygame.quit()