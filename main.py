from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QFrame, QPushButton, QLabel
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect
import sys


class GameBoard(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.setLayout(self.grid)
        self.cells = {}

    def add_cell(self, name, x, y):
        cell = QPushButton()
        cell.setObjectName(name)
        cell.setStyleSheet('background-color: white')
        self.grid.addWidget(cell, x, y)
        self.cells[name] = cell

    def mousePressEvent(self, event):
        if not self.parent().game_started:
            return
        if self.parent().current_player == 1:
            return
        for cell_name, cell in self.cells.items():
            if cell.geometry().contains(event.pos()):
                if cell_name in self.parent().player_2_ships:
                    self.parent().player_2_ships[cell_name] = 'H'
                    cell.setStyleSheet('background-color: red')
                else:
                    self.parent().player_2_ships[cell_name] = 'M'
                    cell.setStyleSheet('background-color: blue')
                self.parent().current_player = 1
                self.parent().update_status()
                self.parent().check_game_over()

    def reset(self):
        for cell in self.cells.values():
            cell.setStyleSheet('background-color: white')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Морской бой')
        self.current_player = 1
        self.game_started = False
        self.board_size = 10
        self.player_1_ships = {}
        self.player_2_ships = {}
        self.setup_ui()

    def setup_ui(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Расставьте корабли игрока 1')
        self.setFixedSize(500, 500)
        self.setup_boards()
        self.setup_buttons()

    def setup_boards(self):
        self.player_1_board = GameBoard(self)
        self.player_2_board = GameBoard(self)
        for x in range(self.board_size):
            for y in range(self.board_size):
                name = f'player_1_{x}_{y}'
                self.player_1_board.add_cell(name, x, y)
                self.player_1_ships[name] = ''
                name = f'player_2_{x}_{y}'
                self.player_2_board.add_cell(name, x, y)
                self.player_2_ships[name] = ''
        self.player_1_board.setGeometry(20, 20, 200, 200)
        self.player_2_board.setGeometry(280, 20, 200, 200)

    def setup_buttons(self):
        start_button = QPushButton('Начать игру', self)
        start_button.setGeometry(200, 450, 100, 30)
        start_button.clicked.connect(self.start_game)

        reset_button = QPushButton('Сброс', self)
        reset_button.setGeometry(200, 400, 100, 30)
        reset_button.clicked.connect(self.reset_game)

    def start_game(self):
        if not self.game_started:
            self.status_bar.showMessage('Ход игрока 1')
            self
