import helpers


class KnightsTour:
    def __init__(self):
        self.starting_position = [0, 0]
        self.board_dimensions = [0, 0]

        self.previous_position = [None, None]
        self.current_position = [0, 0]

        self.board = []
        self.board_with_counts = []
        self.cell_size = 0
        self.possible_moves = []

    def main_call(self):
        self._set_board_dimension()
        self._set_cell_size()
        self._set_board()
        self._set_starting_position()
        wants_to_try = helpers.user_wants_to_attempt()

        if helpers.respond_to_user(wants_to_try, self.board, self.starting_position):
            return

        self._update_board(self.board, self.starting_position, 'X')
        self.current_position = self.starting_position
        while True:
            self._update_board_with_counts(self.board, self.current_position)
            helpers.print_board(self.board_with_counts, [self.board_dimensions[1], self.board_dimensions[0]])

            if helpers.game_is_won(self.board):
                print("What a great tour! Congratulations!")
                return
            if helpers.board_is_dead_end(self.board_with_counts):
                print(f"No more possible moves! Your knight visited {helpers.spots_visited(self.board)} squares!")
                return

            self.previous_position = self.current_position
            self.current_position = helpers.new_move(self.board, self.current_position)
            self.board = helpers.make_move(self.board, self.previous_position, '*')
            self.board = helpers.make_move(self.board, self.current_position, 'X')

    def _set_board_dimension(self):
        """Sets the board_dimension attribute."""
        self.board_dimensions = helpers.board_dimensions()
        return

    def _set_cell_size(self):
        """Sets the cell_size attribute."""
        self.cell_size = helpers.cell_size(self.board_dimensions)

    def _set_board(self):
        """Sets the board using the previously validated dimensions."""
        self.board = helpers.game_board(self.board_dimensions)
        return

    def _set_starting_position(self):
        """Sets the starting_position attribute via user input."""
        self.starting_position = helpers.starting_position(self.board)
        return

    def _update_board(self, board, move, character):
        """Updates the game board with the given character at the specified move."""
        self.board = helpers.make_move(board, move, character)
        return

    def _update_board_with_counts(self, board, current_position):
        """Updates the board_with_counts attribute using the current board."""
        self.board_with_counts = helpers.board_with_warnsdorff_counts(board, current_position)
        return


game = KnightsTour()
game.main_call()
