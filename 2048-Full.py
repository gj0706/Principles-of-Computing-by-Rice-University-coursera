"""
Clone of 2048 game.
"""

import poc_2048_gui
#import poc_simpletest
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def move_to_left(line):
    """
    First step of merging: 
    Move all the numbers in the list to
    the left, keep all the zeros to the right
    """
    result = [] 
    for indx in range(len(line)):
            if line[indx] != 0:
                result.append(line[indx])
    # make the result list the same length as the original list
    # by adding zeros to the end of result list.
    result.extend([0] * (len(line)- len(result)))
    return result

def double_pair(line):
    """
    Second step of merging: 
    Loop through pairs of numbers with the same values 
    in the list, replace each pair with a doubled value
    and a zero, then add the values to the result list.
    """
    new_line = line[:]
    result = []
    for indx in range(len(line) - 1): 
        if new_line[indx] == new_line[indx + 1]:
            result.append(new_line[indx] * 2)
            new_line[indx + 1] = 0          
        elif new_line[indx] != new_line[indx + 1]:
            result.append(new_line[indx])
    # fix the off-by-one bug
    result.append(new_line[-1])
    # fix the length of result list
    result.extend([0] * (len(new_line)- len(result)))
    return result

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    line1 = move_to_left(line)
    line2 = double_pair(line1)
    line3 = move_to_left(line2)
    return line3


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width  
        self.reset()
        self._dir_indices = {UP:[(0, col) for col in range(self._grid_width)],
                       DOWN:[(self._grid_height - 1, col) for col in range(self._grid_width)],
                       LEFT:[(row, 0) for row in range(self._grid_height)],
                       RIGHT:[(row, self._grid_width - 1) for row in range(self._grid_height)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_width)]
                                        for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
                       
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)
            
        

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width
   
    def traverse_grid(self, start_cell, direction, steps):
        """
        Function that iterates through the cells in a grid
        in a linear direction

        """
        temp = []
        for step in range(steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            temp.append(self._grid[row][col])          
        return temp
    
    def apply_merged_list(self, start_cell, direction, steps, merged_list):
        """
        Copy merged list back to the grid
        """
      
        for step in range(steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            self._grid[row][col] = merged_list[step]
        return self._grid[row][col]

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        for cell in self._dir_indices[direction]:         
            start = cell
            if direction == UP or direction == DOWN:
                steps = self.get_grid_height()
            elif direction == LEFT or direction == RIGHT:
                steps = self.get_grid_width()
            merge_list = self.traverse_grid(start, OFFSETS[direction], steps)  
            merged_list = merge(merge_list)
            if merged_list != merge_list:
                moved = True
            self.apply_merged_list(start, OFFSETS[direction], steps, merged_list)
        if moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tiles = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._grid[row][col] == 0: 
                    tiles.append((row, col))
        probablity = random.random()    
        new_tile = random.choice(tiles)
        if len(tiles) != 0:                        
            if probablity >= 0.1:                
                 self._grid[new_tile[0]][new_tile[1]] = 2
            else:
                 self._grid[new_tile[0]][new_tile[1]] = 4
        
                                           
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

