import copy


def board_dimensions() -> list:
    """Returns a list of two integers that have been confirmed to be valid board dimensions."""
    dimensions = input("Enter your board dimensions: ")
    if dimensions_are_valid(dimensions):
        dimensions = list(map(int, dimensions.split()))
        return dimensions
    else:
        print("Invalid dimensions!")
        return board_dimensions()


def dimensions_are_valid(dimensions) -> bool:
    """Checks whether the given board dimensions are valid.

    Args:
        dimensions (str): '<dimension 1> <dimension 2>'
    """
    try:
        x = int(dimensions[0])
        y = int(dimensions[-1])
        is_valid = (x > 0) and (y > 0) and (len(dimensions.split()) == 2)
        return is_valid
    except IndexError:
        return False
    except ValueError:
        return False


def cell_size(dimensions):
    """Calculates a cell size based on the dimensions of the given board.

    Args:
        dimensions (list): a list in the form [int, int] that denotes the dimensions from which to calculate the cell
        size.

    Return:
        cell_size (int): The appropriate cell size for a board with dimensions of the given board.
    """
    rows = dimensions[1]
    columns = dimensions[0]
    size = len(str(rows) + str(columns))
    return size


def game_board(dimensions) -> list:
    """Returns a nested list matrix with the given dimensions.

    Args:
        dimensions (list): Dimensions of the board that will be generated; should be in the form [int, int]

    Return:
        board (nested list): A list of lists, where each internal list is a row on the board whose elements are
        one or more underscores, denoting an empty spot. This project uses Cartesian coordinates to reference locations on
        the board as opposed to standard matrix notation, which is why the rows and columns are the second and first
        entries of the list, respectively, instead of the other way around.
    """
    board = []
    rows = dimensions[1]
    columns = dimensions[0]
    cell_length = len(str(rows) + str(columns))
    row = ['_' * cell_length] * columns

    for _ in range(rows):
        board.append(copy.deepcopy(row))

    return board


def starting_position(board) -> list:
    """Returns the starting position for the knight on the board.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
            An * or X may be preceded by one or more spaces.

    Return: current_position (list): A list of two integers, representing the x and y Cartesian coordinates of the
    knight's starting location on the board.
    """
    xy = input("Enter the knight's starting position (space-separated integers): ")

    if move_is_valid(board, xy):
        current_position = list(map(int, xy.split()))
        return current_position
    else:
        print("Invalid position!")
        return starting_position(board)


def move_is_valid(board, new_position, current_position=None) -> bool:
    """Checks whether the given move is valid for the given board.

    Makes the following checks:
        - The coordinates of the given move are both positive integers
        - There are only two coordinates in the move, x and y
        - The new position hasn't been visited before; the spot on the board doesn't already contain '*', 'X' or <int>
        - The coordinates are within the range of the board
        - The knight can legally move from it's current position to the new position

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
                An * or X may be preceded by one or more spaces.
        new_position (str): A move to be validated, in the form '<x coordinate> <y coordinate>'
        current_position (list): The x and y location from which the knight will be moving, in the form [int, int]
    """
    try:
        x = int(new_position.split()[0])
        y = int(new_position.split()[1])
        move_spot = board[y - 1][x - 1]
        checks_1 = (move_spot.strip() not in ['*', 'X']) and (not move_spot.strip().isdigit())
        checks_2 = (0 < x <= len(board[0])) and (0 < y <= len(board)) and (len(new_position.split()) == 2)
        if not current_position:
            check_3 = True
        else:
            check_3 = [x, y] in possible_next_moves(current_position[0], current_position[1])
        move_available = checks_1 and checks_2 and check_3
        return move_available
    except IndexError:
        return False
    except ValueError:
        return False


def possible_next_moves(x, y) -> list:
    """Gives a list of potential moves from the given coordinates.

    Given an x and y coordinate, gives a list of the eight relative positions in Cartesian coordinates that a chess
    knight would be able to move to.

    Args:
        x (int): The x Cartesian coordinate of the knight.
        y (int): The y Cartesian coordinate of the knight.

    Return:
        move (nested list): A list of lists, where each internal list is a Cartesian position [x, y]
    """
    moves = [
        [x - 2, y + 1],
        [x - 1, y + 2],
        [x + 1, y + 2],
        [x + 2, y + 1],
        [x + 2, y - 1],
        [x + 1, y - 2],
        [x - 1, y - 2],
        [x - 2, y - 1]
    ]
    return moves


def make_move(board, move, character='X') -> list:
    """Updates the given board with the given move.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
                An * or X may be preceded by one or more spaces.
        move (list): A Cartesian coordinate in the form [x, y]
        character (str): The character that will be placed on board at the given move.

    Return:
        board (list): The same board, but with the given character placed in the given location.

    """
    spaces = len(str(len(board[0])) + str(len(board)))
    board[move[1] - 1][move[0] - 1] = (' ' * (spaces - len(character))) + character
    return board


def board_with_warnsdorff_counts(board, current_position) -> list:
    """Adds potential move counts from future moves onto the board.

    Takes <board>, finds the valid moves from <current_position>, counts the number of possible valid next moves from
    each one of those valid moves (called the Warnsdorff count), then adds that number to that spot on the board. For
    instance, if I could move to spot [x, y] from <current_position> and then make 6 more valid moves from [x,
    y], the board will have a '6' at [x, y].

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
                An * or X may be preceded by one or more spaces.
        current_position (list): The position from which you want to count future moves, in the form of Cartesian
                coordinates [x, y]

    Return:
        board_with_counts (list): A game board similar to <board>, but with all of the Warnsdorrf counts (described
                above) filled in.
    """
    current_x = current_position[0]
    current_y = current_position[1]
    board_with_counts = copy.deepcopy(board)

    moves_to_check = possible_next_moves(current_x, current_y)
    for move in moves_to_check:
        move_for_validation = f'{str(move[0])} {str(move[1])}'  # The validation function expects a string
        if move_is_valid(board, move_for_validation, current_position):
            future_moves = warnsdorff_count(board, move)
            board_with_counts = make_move(board_with_counts, move, str(future_moves))

    return board_with_counts


def warnsdorff_count(board, move) -> int:
    """Give the number of moves possible if the given move is valid and was played on the board.

    This function takes <board>, which contextually is the current state of the game, plays <move> on it, and then
    counts how many moves can then be played.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
                An * or X may be preceded by one or more spaces.
        move (list): Cartesian coordinates of the form [x, y]

    Return:
        warnsdorff_number (int): The number of moves that can be played after <move> has been played on <board>
    """
    x = move[0]
    y = move[1]
    future_board = make_move(copy.deepcopy(board), move, 'X')
    possible_future_moves = possible_next_moves(x, y)

    warnsdorff_number = 0
    for future_move in possible_future_moves:
        move_for_validation = f'{str(future_move[0])} {str(future_move[1])}'  # The validation function expects a str.
        if move_is_valid(future_board, move_for_validation):
            warnsdorff_number += 1

    return warnsdorff_number


def print_board(board, dimensions) -> None:
    """Prints the given board with appropriate formatting.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
                An * or X may be preceded by one or more spaces.
        dimensions (list): Should be the dimensions of the given board, given in the format [int, int].
    """
    rows = dimensions[0]
    columns = dimensions[1]
    cell_length = len(str(rows) + str(columns))
    border_length = columns * (cell_length + 1) + 3
    print(' ' + '-' * border_length)

    for i in reversed(range(rows)):
        print(f'{i + 1}| {" ".join(board[i])} |')

    print(' ' + '-' * border_length)
    print('    ', end='')

    column_numbers = [str(i + 1) for i in range(columns)]
    gap = ' ' * cell_length
    print(gap.join(column_numbers))
    return


def game_is_won(board) -> bool:
    """Checks if the game is won and exits if so.

    Checks for a win by determining if there are any spaces left on the board that haven't been previously visited (*)
    other than the position that the knight is currently in (X).

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
                An * or X may be preceded by one or more spaces.

    """
    for row in board:
        for item in row:
            if '*' not in item and 'X' not in item:
                return False

    return True


def board_is_dead_end(board_with_counts) -> bool:
    """Checks for a dead end by looking for Warnsdorff counts in any spots.

    A board that has been passed through the warnsdorff_count function is meant to be used here.
    If there are any possible moves remaining, a Warnsdorff number will be present in the available spot.

    Args:
        board_with_counts (list): A list of lists, whose internal elements are either underscores, 'X', '*', or an integer
                denoting how many moves could be made from that position. An * or X may be preceded by one or more
                spaces.
    """
    for row in board_with_counts:
        for item in row:
            if item.strip().isnumeric():
                return False

    return True


def new_move(board, current_position) -> list:
    """Returns a new move, specified by the user, to be played on the given board from the current_position.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
                An * or X may be preceded by one or more spaces.
        current_position (list): Cartesian position [x, y] from which a move will be made.

    Return:
        move (list): A move in Cartesian coordinates, [x, y]
    """
    xy = input("Enter your next move: ")
    if move_is_valid(board, xy, current_position):
        move = list(map(int, xy.split()))
        return move
    else:
        print("Invalid move! ", end='')
        return new_move(board, current_position)


def spots_visited(board):
    """Counts the number of spots the knight has occupied (at any point) on the given board.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, 'X', or '*'.
                An * or X may be preceded by one or more spaces.

    Return:
        count (int): The count of spots on the board that the knight has already visited.
    """
    count = 1  # The 1 here counts the spot the knight is currently occupying
    for row in board:
        for spot in row:
            if spot.strip() == '*':
                count += 1

    return count


def winning_board(board, starting_move) -> list:
    """The main call of the algorithm that determines if a given board with a given starting move is solvable.

    This function is recursive. It will evaluate all possible sequences of allowable moves stemming from the starting
    move until it generates a solved board, in which case it returns the solved board. If all possible move sequences
    are exhausted without a solution, it returns and empty list.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, or digits.
                A digit may be preceded by one or more spaces.
        starting_move (list): A pair of Cartesian coordinates, in the form [x, y].

    Return:
        board (list): Either a solved board with the spots fill with integers (the order in which they were played), or
        an empty list if not solution is found.
    """
    character = next_algorithm_character(board)
    board = make_move(copy.deepcopy(board), starting_move, character)

    if board_is_solved(board):
        return board

    potential_next_moves = possible_next_moves(starting_move[0], starting_move[1])
    valid_next_moves = []

    for move in potential_next_moves:
        if move_is_valid(board, f'{str(move[0])} {str(move[1])}', starting_move):
            valid_next_moves.append(move)

    if not valid_next_moves:
        return []

    for move in valid_next_moves:
        result = winning_board(board, move)
        if result:
            return result

    return []


def board_is_solved(board) -> bool:
    """Determines whether the board has been solved by the computer.

    If the board is full of numbers, returns True, and otherwise False.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, or digits.
                A digit may be preceded by one or more spaces."""
    for row in board:
        for spot in row:
            if not spot.strip().isdigit():
                return False

    return True


def next_algorithm_character(board):
    """Returns a string that is numerically one greater than the previous move played.

    This is part of the algorithm to determine if a board is winnable or not, and is not used in the case that the user
    opts not to attempt the board. If a move has yet to be played on <board>, it returns '1'.

    Args:
        board (list): A list of lists, whose internal elements are either underscores, or digits.
                A digit may be preceded by one or more spaces.

    Return:
        character (str): A string that is one more than the maximum integer on the board.
    """
    played_integers = []
    for row in board:
        for spot in row:
            if spot.strip().isdigit():
                played_integers.append(int(spot.strip()))

    if not played_integers:
        return '1'
    else:
        character = str(max(played_integers) + 1)
        return character


def user_wants_to_attempt() -> bool:
    """Returns a boolean to determine if the user wants to attempt to solve the board, or if the computer will try."""
    answer = input("Do you want to try the puzzle? (y/n):\n")
    if answer == 'y':
        return True
    elif answer == 'n':
        return False
    else:
        print("Invalid input!")
        return user_wants_to_attempt()


def respond_to_user(wants_to_try, board, start_position) -> bool:
    """Prints the appropriate information based on whether or not the user wants to try the puzzle.

    Args:
        wants_to_try (bool): True if the user wants to attempt the board, False if they do not.
        board (list): A list of lists, whose internal elements should only be underscores, as this board should not have
                been played on yet.
        start_position (list): A starting position in Cartesian coordinates given previously by the user, [x, y].

    Return:
        boolean: If the user does not want to try to solve the board from the starting position, the user will
    either be shown the solution or told that there is no solution. If the user does want to try the board but there
    is no solution, they will be notified. These cases will return True. If the user wants to try the board,
    and it does have a solution, False will be returned, since the user was not given any immediate information as to
    the nature of the solution.
    """
    result_board = winning_board(board, start_position)
    if wants_to_try and result_board:
        return False

    if not result_board:
        print("No solution exists!")
    elif result_board:
        rows = len(result_board)
        columns = len(result_board[0])
        print("\nHere's the solution!")
        print_board(result_board, [rows, columns])
    return True
