import random


class Puzzle:
    # Each entry is the (row, col) offset applied to the blank's position.
    # "w" slides the blank up, "s" down, "a" left, "d" right.
    DIRECTIONS = {
        "w": (-1, 0),
        "s": (1, 0),
        "a": (0, -1),
        "d": (0, 1),
    }

    OPPOSITE = {
        "w": "s",
        "s": "w",
        "a": "d",
        "d": "a",
    }

    def __init__(self, size=4, scramble_moves=None):
        self.size = size
        self.board = self.make_board(scramble_moves=scramble_moves)

    def make_board(self, scramble_moves=None):
        # Begin with the solved arrangement.
        tiles = list(range(1, self.size * self.size)) + [0]

        previous_direction = None

        # Scramble using legal moves instead of arbitrary permutations.
        # Every resulting board is therefore reachable from the goal.
        if scramble_moves is None:
            scramble_moves = self.size * self.size * 10

        for _ in range(scramble_moves):
            blank_index = tiles.index(0)
            r, c = divmod(blank_index, self.size)

            legal_directions = []

            if r > 0:
                legal_directions.append("w")
            if r < self.size - 1:
                legal_directions.append("s")
            if c > 0:
                legal_directions.append("a")
            if c < self.size - 1:
                legal_directions.append("d")

            # Avoid immediately reversing the previous move.
            if previous_direction is not None:
                reverse = self.OPPOSITE[previous_direction]
                legal_directions = [
                    direction
                    for direction in legal_directions
                    if direction != reverse
                ]

            # Handles a board with no legal moves, such as a 1x1 board.
            if not legal_directions:
                break

            direction = random.choice(legal_directions)
            dr, dc = self.DIRECTIONS[direction]

            neighbor_index = (r + dr) * self.size + (c + dc)

            # Make one legal swap between the blank and an adjacent tile.
            tiles[blank_index], tiles[neighbor_index] = (
                tiles[neighbor_index],
                tiles[blank_index],
            )

            previous_direction = direction

        # Convert the flat list into a two-dimensional board.
        return [
            tiles[row * self.size:(row + 1) * self.size]
            for row in range(self.size)
        ]

    def blank_pos(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def move(self, direction):
        """Slide the blank in `direction`. Returns True only if a tile moved."""
        if direction not in self.DIRECTIONS:
            return False

        blank = self.blank_pos()
        if blank is None:
            return False

        r, c = blank
        dr, dc = self.DIRECTIONS[direction]

        nr, nc = r + dr, c + dc

        if not (0 <= nr < self.size and 0 <= nc < self.size):
            return False

        self.board[r][c], self.board[nr][nc] = (
            self.board[nr][nc],
            self.board[r][c],
        )

        return True

    def solved(self):
        flat = sum(self.board, [])
        return flat == list(range(1, self.size * self.size)) + [0]