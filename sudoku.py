import pygame, sys
from sudoku_generator import SudokuGenerator


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    sudoku.print_board()
    return board


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = ""

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_value(self):
        return self.value

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def get_sketched(self):
        return self.sketched_value

    def draw(self):
        if self.value != 0:
            num_font = pygame.font.Font(None, 100)
            cell_surf = num_font.render(str(self.value), 0, (31, 52, 158))
            cell_rect = cell_surf.get_rect(center=((self.row*80)-40, (self.col*80)-40))
            self.screen.blit(cell_surf, cell_rect)
        elif self.value == 0:
            pygame.draw.rect(self.screen, (255, 252, 243), (((self.row - 1) * 80)-2, ((self.col - 1) * 80)-2, 78, 78), 1)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        if difficulty == "easy":
            self.removed = 30
        elif difficulty == "medium":
            self.removed = 40
        elif difficulty == "hard":
            self.removed = 50
        self.initial_board = generate_sudoku(9, self.removed)

    cell_list = [[0 for x in range(9)] for y in range(9)]
    selected = False
    selected_cube = 0

    def draw(self):
        for i in range(1, 10):
            if i % 3 == 0:
                pygame.draw.line(self.screen, (33, 24, 5), (0, i * 80), (720, i * 80), 3)
            else:
                pygame.draw.line(self.screen, (33, 24, 5), (0, i * 80), (720, i * 80))
        for i in range(1, 9):
            if i % 3 == 0:
                pygame.draw.line(self.screen, (33, 24, 5), (i * 80, 0), (i * 80, 720), 3)
            else:
                pygame.draw.line(self.screen, (33, 24, 5), (i * 80, 0), (i * 80, 720))
        for i in range(0, 9):
            for j in range(0, 9):
                self.cell_list[i][j] = Cell(self.initial_board[i][j], i + 1, j + 1, self.screen)
        for i in range(0, 9):
            for j in range(0, 9):
                if self.cell_list[i][j].get_value() != 0:
                    self.cell_list[i][j].draw()

        board_fonts = pygame.font.Font(None, 30)
        pygame.draw.rect(screen_game, (0, 0, 153), pygame.Rect(100, 726, 130, 50), 4)
        pygame.draw.rect(screen_game, (153, 204, 255), pygame.Rect(110, 734, 110, 35))
        pygame.draw.rect(screen_game, (0, 0, 153), pygame.Rect(295, 726, 130, 50), 4)
        pygame.draw.rect(screen_game, (153, 204, 255), pygame.Rect(305, 734, 110, 35))
        pygame.draw.rect(screen_game, (0, 0, 153), pygame.Rect(490, 726, 130, 50), 4)
        pygame.draw.rect(screen_game, (153, 204, 255), pygame.Rect(500, 734, 110, 35))

        reset_surf = board_fonts.render('RESET', 0, (0, 0, 0))
        reset_rect = reset_surf.get_rect(center=(165, 752.5))
        screen_game.blit(reset_surf, reset_rect)

        restart_surf = board_fonts.render('RESTART', 0, (0, 0, 0))
        restart_rect = restart_surf.get_rect(center=(360, 752.5))
        screen_game.blit(restart_surf, restart_rect)

        exit_surf = board_fonts.render('EXIT', 0, (0, 0, 0))
        exit_rect = exit_surf.get_rect(center=(555, 752.5))
        screen_game.blit(exit_surf, exit_rect)


    def select(self, row, col):
        pygame.draw.rect(self.screen, (246, 27, 11), (((row-1)*80)+2, ((col-1)*80)+2, 77, 77), 3)
        self.selected_cube = self.cell_list[row-1][col-1]
        self.selected = True

    def deselect(self, row, col):
        pygame.draw.rect(self.screen, (255, 252, 243), (((row - 1) * 80) + 2, ((col - 1) * 80) + 2, 77, 77), 3)
        self.selected = False

    def click(self, x, y):
        if y < 721:
            for i in range(1, 10):
                if (80 * (i - 1)) < x and x <= (80 * i):
                    row = i
            for i in range(1, 10):
                if (80 * (i - 1)) < y and y <= (80 * i):
                    col = i
            return (row, col)
        return None

    def clear(self, row, col):
        if self.initial_board[row-1][col-1]==0:
            self.cell_list[row-1][col-1].set_cell_value(0)
            pygame.draw.rect(self.screen, (255,252,243),
                             (((row - 1) * 80) +5, ((col - 1) * 80) +5, 71, 71))

    def sketch(self, value):  # dont sketch in set cells
        self.clear(self.selected_cube.get_row(),self.selected_cube.get_col())
        if board.initial_board[board.selected_cube.get_row() - 1][board.selected_cube.get_col() - 1] == 0:
            num_font = pygame.font.Font(None, 40)
            if self.selected_cube.get_sketched() != '':
                sketched = int(self.selected_cube.get_sketched())
                if sketched > 0:
                    sketch_surf = num_font.render(str(sketched), 0, (255, 252, 243))
                    sketch_rect = sketch_surf.get_rect(center=((self.selected_cube.get_row() * 80) - 60, (self.selected_cube.get_col() * 80) - 60))
                    self.screen.blit(sketch_surf, sketch_rect)
            self.selected_cube.set_sketched_value(value)
            cell_surf = num_font.render(str(value), 0, (108, 105, 98))
            cell_rect = cell_surf.get_rect(center=((self.selected_cube.get_row() * 80) - 60, (self.selected_cube.get_col() * 80) - 60))
            self.screen.blit(cell_surf, cell_rect)

    def is_full(self):
        count = 0
        for i in range(0,9):
            for j in range(0,9):
                if self.cell_list[i][j].get_value()==0:
                    count +=1
        if count == 0:
            return True
        else:
            return False

    def check_board(self):
        cell_list_values=[[0 for x in range (9)]for y in range (9)]
        for i in range (0,9):
            for j in range (0,9):
                cell_list_values[i][j]= self.cell_list[i][j].get_value()

        for i in range(0,9):
            for j in range(0,9):
                # checks row
                count=0
                for value in cell_list_values[i]:
                    if value == cell_list_values[i][j]:
                        count +=1
                        if count>1:
                            return False

                #checks col
                count = 0
                for value in range(9):
                    if cell_list_values[value][j] == cell_list_values[i][j]:
                        count +=1
                        if count>1:
                            return False

                #checks box
                count = 0
                if 0 <= i < 3:
                    row_start = 0
                elif 3 <= i < 6:
                    row_start = 3
                elif i >= 6:
                    row_start = 6
                if 0 <= j < 3:
                    col_start = 0
                elif 3 <= j < 6:
                    col_start = 3
                elif j >= 6:
                    col_start = 6
                for x in range(col_start, col_start + 3):
                    for y in range(row_start, row_start + 3):
                        if cell_list_values[y][x] == cell_list_values[i][j]:
                            count += 1
                            if count>1:
                                return False


        return True





# initializes the screen
pygame.init()
screen_game = pygame.display.set_mode((720, 780))  # + 780 to height
pygame.display.set_caption("Sudoku")
screen_game.fill((255, 252, 243))

# call to display the welcome screen
def welcome_screen():
    welcome_font = pygame.font.Font(None, 80)
    mode_font = pygame.font.Font(None, 50)
    difficulty_font = pygame.font.Font(None, 30)

    welcome_surf = welcome_font.render('Welcome to Sudoku', 0, (0, 0, 0))
    welcome_rect = welcome_surf.get_rect(center=(720 // 2, 720 // 5))
    screen_game.blit(welcome_surf, welcome_rect)

    mode_surf = mode_font.render('Select Game Mode:', 0, (0, 0, 0))
    mode_rect = mode_surf.get_rect(center=(720 // 2, 720 // 5 * 2.5))
    screen_game.blit(mode_surf, mode_rect)

    pygame.draw.rect(screen_game, (0, 0, 153), pygame.Rect(100, 450, 130, 65), 4)
    pygame.draw.rect(screen_game, (153, 204, 255), pygame.Rect(110, 460, 110, 45))
    pygame.draw.rect(screen_game, (0, 0, 153), pygame.Rect(295, 450, 130, 65), 4)
    pygame.draw.rect(screen_game, (153, 204, 255), pygame.Rect(305, 460, 110, 45))
    pygame.draw.rect(screen_game, (0, 0, 153), pygame.Rect(490, 450, 130, 65), 4)
    pygame.draw.rect(screen_game, (153, 204, 255), pygame.Rect(500, 460, 110, 45))

    easy_surf = difficulty_font.render('EASY', 0, (0, 0, 0))
    easy_rect = easy_surf.get_rect(center=(165, 482.5))
    screen_game.blit(easy_surf, easy_rect)

    medium_surf = difficulty_font.render('MEDIUM', 0, (0, 0, 0))
    medium_rect = medium_surf.get_rect(center=(360, 482.5))
    screen_game.blit(medium_surf, medium_rect)

    hard_surf = difficulty_font.render('HARD', 0, (0, 0, 0))
    hard_rect = hard_surf.get_rect(center=(555, 482.5))
    screen_game.blit(hard_surf, hard_rect)


def win_game():
    end_font = pygame.font.Font(None, 80)
    screen_game.fill((255, 252, 243))
    win_surf = end_font.render('Game Won!', 0, (0, 0, 0))
    win_rect = win_surf.get_rect(center=(720 // 2, 720 // 5 * 2))
    screen_game.blit(win_surf, win_rect)
    pygame.draw.rect(screen_game, (0, 0, 153), pygame.Rect(295, 440, 130, 65), 4)
    pygame.draw.rect(screen_game, (153, 204, 255), pygame.Rect(305, 450, 110, 45))

    exit_font = pygame.font.Font(None, 45)
    medium_surf = exit_font.render('EXIT', 0, (0, 0, 0))
    medium_rect = medium_surf.get_rect(center=(360, 474))
    screen_game.blit(medium_surf, medium_rect)
    #win = True
    #end_game = True


def lose_game():
    end_font = pygame.font.Font(None, 80)
    screen_game.fill((255, 252, 243))
    win_surf = end_font.render('Game Over :(', 0, (0, 0, 0))
    win_rect = win_surf.get_rect(center=(720 // 2, 720 // 5 * 2))
    screen_game.blit(win_surf, win_rect)
    pygame.draw.rect(screen_game, (0, 0, 153), pygame.Rect(295, 440, 130, 65), 4)
    pygame.draw.rect(screen_game, (153, 204, 255), pygame.Rect(305, 450, 110, 45))

    exit_font = pygame.font.Font(None, 33)
    medium_surf = exit_font.render('RESTART', 0, (0, 0, 0))
    medium_rect = medium_surf.get_rect(center=(360, 474))
    screen_game.blit(medium_surf, medium_rect)
    #win = False



welcome_screen()
welcome = True  # can use this to distinguish what screen the user is on
end_game = False
win = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and welcome:
            x, y = event.pos
            if 100 <= x <= 230 and 450 <= y <= 515:
                board = Board(720, 720, screen_game, 'easy')
                screen_game.fill((255, 252, 243))
                board.draw()
                welcome = False
            elif 295 <= x <= 425 and 450 <= y <= 515:
                board = Board(720, 720, screen_game, 'medium')
                screen_game.fill((255, 252, 243))
                board.draw()
                welcome = False
            elif 490 <= x <= 620 and 450 <= y <= 515:
                board = Board(720, 720, screen_game, 'hard')
                screen_game.fill((255, 252, 243))
                board.draw()
                welcome = False
        elif event.type == pygame.MOUSEBUTTONDOWN and end_game:
            x, y = pygame.mouse.get_pos()
            if 295 <= x <= 425 and 440 <= y <= 505:
                if win:
                    pygame.quit()
                    sys.exit()
                else:
                    end_game = False
                    screen_game.fill((255, 252, 243))
                    welcome_screen()
                    welcome = True
                    continue
        elif event.type == pygame.MOUSEBUTTONDOWN and (end_game is False) :
            x, y = pygame.mouse.get_pos()
            if 100 <= x <= 230 and 726 <= y <= 776:  # reset board ADD RESET
                screen_game.fill((255, 252, 243))
                board.draw()
            elif 295 <= x <= 425 and 726 <= y <= 776:  # restart
                screen_game.fill((255, 252, 243))
                welcome_screen()
                welcome = True
                continue
            elif 490 <= x <= 620 and 726 <= y <= 776:  # exit
                pygame.quit()
                sys.exit()
            elif board.selected:
                board.deselect(board.selected_cube.get_row(), board.selected_cube.get_col())
            click_result = board.click(x, y)
            if click_result is not None:
                row, col = click_result
                board.select(row, col)
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_DELETE) or (event.key == pygame.K_BACKSPACE):
                board.clear(board.selected_cube.get_row(), board.selected_cube.get_col())
            if event.key == pygame.K_LEFT:
                row, col = board.selected_cube.get_row() - 1, (board.selected_cube.get_col())
                if board.selected_cube.get_row() == 1:
                    row = 9
                board.deselect(board.selected_cube.get_row(), board.selected_cube.get_col())
                board.select(row, col)
            elif event.key == pygame.K_RIGHT:
                row, col = board.selected_cube.get_row() + 1, (board.selected_cube.get_col())
                if board.selected_cube.get_row() == 9:
                    row = 1
                board.deselect(board.selected_cube.get_row(), board.selected_cube.get_col())
                board.select(row, col)
            elif event.key == pygame.K_UP:
                row, col = (board.selected_cube.get_row(), board.selected_cube.get_col() - 1)
                if board.selected_cube.get_col() == 1:
                    col = 9
                board.deselect(board.selected_cube.get_row(), board.selected_cube.get_col())
                board.select(row, col)
            elif event.key == pygame.K_DOWN:
                row, col = (board.selected_cube.get_row(), board.selected_cube.get_col() + 1)
                if board.selected_cube.get_col() == 9:
                    col = 1
                board.deselect(board.selected_cube.get_row(), board.selected_cube.get_col())
                board.select(row, col)
            if event.key == pygame.K_1:
                board.sketch(1)
            elif event.key == pygame.K_2:
                board.sketch(2)
            elif event.key == pygame.K_3:
                board.sketch(3)
            elif event.key == pygame.K_4:
                board.sketch(4)
            elif event.key == pygame.K_5:
                board.sketch(5)
            elif event.key == pygame.K_6:
                board.sketch(6)
            elif event.key == pygame.K_7:
                board.sketch(7)
            elif event.key == pygame.K_8:
                board.sketch(8)
            elif event.key == pygame.K_9:
                board.sketch(9)

            if event.key == pygame.K_RETURN:
                if board.initial_board[board.selected_cube.get_row() - 1][board.selected_cube.get_col() - 1] == 0:

                    num_font = pygame.font.Font(None, 100)
                    current = board.selected_cube.get_value()
                    cell_surf = num_font.render(str(current), 0, (255, 252, 243))
                    cell_rect = cell_surf.get_rect(center=((board.selected_cube.get_row() * 80) - 40, (board.selected_cube.get_col() * 80) - 40))
                    screen_game.blit(cell_surf, cell_rect)

                    sketch_font = pygame.font.Font(None, 40)
                    sketched = board.selected_cube.get_sketched()
                    sketch_surf = sketch_font.render(str(sketched), 0, (255, 252, 243))
                    sketch_rect = sketch_surf.get_rect(center=((board.selected_cube.get_row() * 80) - 60, (board.selected_cube.get_col() * 80) - 60))
                    board.screen.blit(sketch_surf, sketch_rect)

                    board.selected_cube.set_cell_value(board.selected_cube.get_sketched())

                    cell_surf = num_font.render(str(board.selected_cube.get_sketched()), 0, (31, 52, 158))
                    cell_rect = cell_surf.get_rect(center=((board.selected_cube.get_row() * 80) - 40, (board.selected_cube.get_col() * 80) - 40))
                    screen_game.blit(cell_surf, cell_rect)

                    if board.is_full():
                        if board.check_board():
                            win_game()
                            end_game= True
                            win = True
                        else:
                            lose_game()
                            end_game = True
                            win = False

    pygame.display.update()
