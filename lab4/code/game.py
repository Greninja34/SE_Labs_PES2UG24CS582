import time

from puzzle import Puzzle


class _Quit(Exception):
    """Raised when the player sends EOF (Ctrl+D) or interrupts (Ctrl+C)."""


class SlidingPuzzle:
    def __init__(self, scramble_moves=None):
        # Per-session settings: not reset when a new board starts.
        self.scramble_moves = scramble_moves
        self.session_started = time.monotonic()
        self.total_moves = 0

        # Per-board state: reset by start_new_board().
        self.size = 4
        self.puzzle = None
        self.moves = 0
        self.board_started = time.monotonic()

    def start_new_board(self, size):
        self.size = size
        self.puzzle = Puzzle(size, scramble_moves=self.scramble_moves)
        self.moves = 0
        self.board_started = time.monotonic()
        # session_started, total_moves, scramble_moves are intentionally not reset.

    def board_elapsed(self):
        return int(time.monotonic() - self.board_started)

    def session_elapsed(self):
        return int(time.monotonic() - self.session_started)

    def display(self):
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))
        print(
            f"Size: {self.size}x{self.size}  "
            f"Board moves: {self.moves}  Board time: {self.board_elapsed()}s  "
            f"Session moves: {self.total_moves}  Session time: {self.session_elapsed()}s"
        )

    def print_help(self):
        # The keys slide the blank; the tile next to it moves into the blank's
        # old position. This wording matches what Puzzle.move actually does.
        print("Commands:")
        print("  W/A/S/D  slide the blank up/left/down/right")
        print("           (the adjacent tile slides into the blank's old spot)")
        print("  N        start a new board with the same size")
        print("  C        change the board size")
        print("  Q        quit")

    def read_input(self, prompt="> "):
        """Read one line, lower-cased and stripped. Quits cleanly on Ctrl+D/Ctrl+C."""
        try:
            return input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            raise _Quit()

    def prompt_size(self):
        while True:
            choice = self.read_input("Choose size (3/4/5) [4]: ")
            if choice == "":
                return 4
            if choice in {"3", "4", "5"}:
                return int(choice)
            print("Please enter 3, 4, or 5.")

    def handle_move(self, key):
        """Attempt a slide. Returns True only if a tile actually moved."""
        if not self.puzzle.move(key):
            print("That move is not possible.")
            return False
        self.moves += 1
        self.total_moves += 1
        return True

    def run(self):
        try:
            self._run()
        except _Quit:
            print("Goodbye.")
        except (EOFError, KeyboardInterrupt):
            # Belt-and-suspenders: nothing should reach here, but quit cleanly.
            print()
            print("Goodbye.")

    def _run(self):
        print("Sliding Puzzle")
        self.print_help()

        size = self.prompt_size()
        self.start_new_board(size)

        while True:
            self.display()

            if self.puzzle.solved():
                print("Solved!")
                print(
                    f"Board moves: {self.moves}  Board time: {self.board_elapsed()}s"
                )
                print(
                    f"Session moves: {self.total_moves}  "
                    f"Session time: {self.session_elapsed()}s"
                )
                print("Options: N = new board (same size), C = change size, Q = quit.")

                while True:
                    key = self.read_input("> ")
                    if key == "q":
                        return
                    if key == "n":
                        self.start_new_board(self.size)
                        break
                    if key == "c":
                        new_size = self.prompt_size()
                        self.start_new_board(new_size)
                        break
                    print("After solving, use N, C, or Q.")
                continue

            key = self.read_input("> ")

            if key == "q":
                return

            if key == "n":
                self.start_new_board(self.size)
                continue

            if key == "c":
                new_size = self.prompt_size()
                self.start_new_board(new_size)
                continue

            if key in {"w", "a", "s", "d"}:
                moved = self.handle_move(key)
                if moved and not self.puzzle.solved():
                    print("Moved.")
                continue

            print("Use W/A/S/D, N, C, or Q.")