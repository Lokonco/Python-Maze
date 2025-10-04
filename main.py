""""
Classes can be put into separate files
for ease of my repo & lazy-ness I made all in one file
"""""
import random
import time
from tkinter import Tk, Canvas

#----Window class declaration--------------#
class Window:
    # Constructor
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Generator & Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close) #links x button to close
        self.__canvas = Canvas(self.__root, width=width, height=height, background="white")
        self.__canvas.pack()
        self.__running = False
    #--------------Class Functions-------------------#
    def redraw(self):
        self.__root.update_idletasks() #Process events with update & refresh window
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def get_canvas(self):
        return self.__canvas

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)
#--------------------------------------#

#---------Point-Class------------------#
class Point:
    # Constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
#--------------------------------------#

#--------------Line-Class--------------#
class Line:
    # Constructor
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
    #------------Class Functions---------#
    def draw(self, canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y,
                           self.p2.x, self.p2.y,
                           fill=fill_color, width=2)
#-------------------------------------------#

#---------------CELL-Class------------------#
class Cell:
    def __init__(self, win=None):
        # Walls
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.has_right_wall = True
        self.visited = False
        #Cords
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.win = win
    #------------Functions--------------#
    def draw(self, x1, y1, x2, y2):
        if self.win is None:
            return
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.win.draw_line(line, "black")
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.win.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.win.draw_line(line, "black")
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.win.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.win.draw_line(line, "black")
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.win.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.win.draw_line(line, "black")
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        if self.win is None:
            return

        # Calc center of cell
        x_mid = (self.x1 + self.x2) // 2
        y_mid = ((self.y1 + self.y2) //2)

        # Calc center of target
        to_x_mid = (to_cell.x1 + to_cell.x2) // 2
        to_y_mid = (to_cell.y1 + to_cell.y2) // 2

        # Color
        fill_color = "gray" if undo else "red" # Red for path, grey for undo

        # Draw line between cells
        line = Line(Point(x_mid, y_mid), Point(to_x_mid, to_y_mid))
        self.win.draw_line(line, fill_color)
#-----------------------------------------#

#-------------MAZE Class-------------------#
class Maze:
    def __init__(self, x1, y1, num_rows ,num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            random.seed(seed)
        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls(0,0)
        self.reset_cells_visited()

    def create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self.cells.append(col_cells)
        # Draw cells
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cells(i, j)

    def draw_cells(self, i, j):
        if self.win is None:
            return
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.draw_cells(0,0)
        self.cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        self.draw_cells(self.num_cols-1, self.num_rows-1)

    #-------------- depth first traversal----------------#
    def break_walls(self, i, j):
        self.cells[i][j].visited = True
        self.animate()
        while True:
            next_index_list = []
            # Left side
            if i > 0 and not self.cells[i-1][j].visited:
                next_index_list.append((i-1, j))
            # Right Side
            if i < self.num_cols - 1 and not self.cells[i+1][j].visited:
                next_index_list.append((i+1, j))
            # Up
            if j > 0 and not self.cells[i][j-1].visited:
                next_index_list.append((i, j-1))
            # Down
            if j < self.num_rows - 1 and not self.cells[i][j+1].visited:
                next_index_list.append((i, j+1))

            # Check if there's no neighbors visited
            if len(next_index_list) == 0:
                self.draw_cells(i, j)
                return

            # Randomly visit cell
            direction_index = random.randrange(len(next_index_list))
            next_i, next_j = next_index_list[direction_index]

            # Remove walls between cells and next cell to visit
            # Right
            if next_i == i+1:
                self.cells[i][j].has_right_wall = False
                self.cells[i+1][j].has_left_wall = False
            #Left side
            elif next_i == i-1:
                self.cells[i][j].has_left_wall = False
                self.cells[i-1][j].has_right_wall = False
            # Bottom side
            elif next_j == j+1:
                self.cells[i][j].has_bottom_wall = False
                self.cells[i][j+1].has_top_wall = False
            # Top side
            elif next_j == j-1:
                self.cells[i][j].has_top_wall = False
                self.cells[i][j-1].has_bottom_wall = False

            #Continue
            self.break_walls(next_i, next_j)
        #---------------------------------------------#

    def reset_cells_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    # This uses depth-first for solving
    def solve_r(self, i, j):
        self.animate()
        self.cells[i][j].visited = True # Mark current cell as visited
        #self.draw_cells(i, j) # Draw current cell
        # Check if end was reached
        if i == self.num_cols-1 and j == self.num_rows-1:
            return True
        #---------Directions-------------#
        # Right
        if (i < self.num_cols-1 and not self.cells[i][j].has_right_wall and
            not self.cells[i+1][j].visited):
            self.cells[i][j].draw_move(self.cells[i+1][j], True)
            if self.solve_r(i+1, j):
                return True
            #If this is reached we undo
            self.cells[i][j].draw_move(self.cells[i+1][j], True)
        # Down
        if (j < self.num_rows-1 and not self.cells[i][j].has_bottom_wall and
                not self.cells[i][j+1].visited):
            self.cells[i][j].draw_move(self.cells[i][j+1])
            if self.solve_r(i, j+1):
                return True
            self.cells[i][j].draw_move(self.cells[i][j+1], True)
        # Left
        if(i > 0 and not self.cells[i][j].has_left_wall and
        not self.cells[i-1][j].visited):
            self.cells[i][j].draw_move(self.cells[i-1][j])
            if self.solve_r(i-1, j):
                return True
            self.cells[i][j].draw_move(self.cells[i-1][j], True)
        # Up
        if (j > 0 and not self.cells[i][j].has_top_wall and
            not self.cells[i][j-1].visited):
            self.cells[i][j].draw_move(self.cells[i][j-1])
            if self.solve_r(i, j-1):
                return True
            self.cells[i][j].draw_move(self.cells[i][j-1], True)
        #If all directions tried & none worked/ not a solution
        return False
        #--------------------------------#

    def solve(self):
        self.reset_cells_visited()
        result = self.solve_r(0,0)
        if self.win is not None:
            self.win.redraw()
        return result
#------------------------------------------#

#-------------MAIN---------------------#
def main():
    win = Window(800, 600)

    maze = Maze(50, 50, 10, 10, 30, 30, win)

    result = maze.solve()
    print(f"Maze solved: {result}")

    win.wait_for_close()
if __name__ == "__main__":
    main()
#--------------------------------------#

# Things to do
# Refactor
# Add bfs
# Add timer
# Add random maze generation
# Add restart button
