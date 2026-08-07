from enum import Enum


class Symbol(Enum):
    X = "X"
    O = "O"
    EMPTY = " "


class Player:
    def __init__(self, name: str, symbol: Symbol):
        self.name = name
        self.symbol = symbol


class Board:
    def __init__(self, size: int = 3):
        self.size = size
        self.grid = [[Symbol.EMPTY for _ in range(size)] for _ in range(size)]

    def place_mark(self, row: int, col: int, symbol: Symbol) -> bool:
        """Returns True if the move was valid and applied."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            print("Move out of bounds.")
            return False
        if self.grid[row][col] != Symbol.EMPTY:
            print("Cell already taken.")
            return False
        self.grid[row][col] = symbol
        return True

    def is_full(self) -> bool:
        return all(cell != Symbol.EMPTY for row in self.grid for cell in row)

    def check_winner(self, symbol: Symbol) -> bool:
        n = self.size
        # Check rows and columns
        for i in range(n):
            if all(self.grid[i][j] == symbol for j in range(n)):
                return True
            if all(self.grid[j][i] == symbol for j in range(n)):
                return True
        # Check diagonals
        if all(self.grid[i][i] == symbol for i in range(n)):
            return True
        if all(self.grid[i][n - 1 - i] == symbol for i in range(n)):
            return True
        return False

    def display(self):
        for row in self.grid:
            print(" | ".join(cell.value for cell in row))
            print("-" * (self.size * 4 - 1))


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.board = Board()
        self.players = [player1, player2]
        self.current_index = 0

    def current_player(self) -> Player:
        return self.players[self.current_index]

    def switch_turn(self):
        self.current_index = 1 - self.current_index

    def play_move(self, row: int, col: int) -> bool:
        player = self.current_player()
        placed = self.board.place_mark(row, col, player.symbol)
        if not placed:
            return False  # invalid move, same player tries again

        self.board.display()

        if self.board.check_winner(player.symbol):
            print(f"🎉 {player.name} wins!")
            return True

        if self.board.is_full():
            print("It's a draw!")
            return True

        self.switch_turn()
        return False


# --- Example usage ---
if __name__ == "__main__":
    p1 = Player("Alice", Symbol.X)
    p2 = Player("Bob", Symbol.O)
    game = Game(p1, p2)

    moves = [(0, 0), (1, 1), (0, 1), (2, 2), (0, 2)]  # Alice wins top row
    for r, c in moves:
        game_over = game.play_move(r, c)
        if game_over:
            break
