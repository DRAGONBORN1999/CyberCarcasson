import json
from board_and_card import Tile, Board
import random

class Game:

    def __init__(self): #Создание игры
        self.board = Board()

        #Импорт базы данных с карточками для игры
        with open("database.json", 'r') as read_file:
            database = json.load(read_file)
        self.tiles = []
        self.used = 0
        i = 1
        while True:
            if f"Card{i}" in database.keys(): #Добавляем загруженную базу с карточками во внутриигровую базу карточек
                new_tile = Tile(database[f"Card{i}"]["edges"],
                                database[f"Card{i}"]["edge_obj"],
                                database[f"Card{i}"]["view"],
                                database[f"Card{i}"]["has_shield"],
                                database[f"Card{i}"]["has_monastery"])
                self.tiles.append(new_tile)
                i += 1
            else:
                break

    def play_game(self): #запуск игры
        while True:
            self.board.print_board()
            cur_tile = None
            if self.used == len(self.tiles):
                print("End!")
                break # Пока так, потом сюда надо будет добавить вывод результатов
            while True: # Выбираем следующую карточку
                number_of_tile = random.randrange(0, len(self.tiles))
                if not self.tiles[number_of_tile].is_placed:
                    cur_tile = self.tiles[number_of_tile]
                    self.used += 1
                    break
            if cur_tile == None:
                print("Error, can't find a card")
                break
            while True:
                print("You can add this tile to board:")
                cur_tile.tile_view()
                print("Write: rotate, if you want to rotate it clockwise")
                print("Write: place x y if you want to move it to place (x, y) on the board")
                s = input()
                if s == "rotate": # поворот карточки
                    cur_tile.rotate()
                else:
                    data = list(map(str, s.split()))
                    if data[0] == 'place':
                        try:
                            self.board.place(cur_tile, int(data[1]), int(data[2]))
                        except ValueError:
                            print("Incorrect input")
                    else:
                        print("Incorrect input")
                if cur_tile.is_placed:
                    break






