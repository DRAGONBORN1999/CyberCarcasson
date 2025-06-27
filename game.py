import json
from board_and_card import Tile, Board
import random
import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk
import threading


class Game(tk.Tk):
    def __init__(self, players):  # Создание игры
        super().__init__()
        self.geometry("800x700")
        self.title("THE BEST CYBERCARCASSON GAME")  # название окна
        self.board = Board()
        self.names = players
        self.players = [Player(name) for name in players]
        self.cur_player_label = tk.Label(self, text="Current player:")
        self.cur_player_name = tk.Entry(self)
        self.cur_player_name.config(state="readonly")
        self.cur_player_label.pack(fill='both')
        self.cur_player_name.pack()
        self.view_board = scrolledtext.ScrolledText(self, width="60", height="20")
        self.view_board.pack(fill='both')

        self.xscrollbar = tk.Scrollbar(self, orient="horizontal")  # Вериткальная полоса прокрутки
        self.view_board.config(xscrollcommand=self.xscrollbar.set)
        self.xscrollbar.pack(fill="x")

        self.system_alarms = tk.Text(self, width=50, height="8")
        self.system_alarms.config(state="disabled")
        self.system_alarms.pack(fill='both')

        self.players_points = tk.Text(self, width=50, height="2")
        self.players_points.config(state="disabled")
        self.players_points.pack(fill='both')

        self.what_to_do = ttk.Combobox(self, values=['Rotate', 'Place card', 'Set miple', 'Finish'])
        self.what_to_do.config(state="readonly")
        self.what_to_do.pack()

        self.input_command = tk.Entry(self)
        self.input_command.pack()

        self.do_something = tk.Button(self, text="Do this!", width=10, height=2, command=self.action_done)
        self.do_something.pack()

        self.start_this_game = tk.Button(self, text="START THIS GAME!!!", width=20,
                                         height=3, bg='red',
                                         command=lambda: threading.Thread(target=self.start_game, daemon=True).start())
        self.start_this_game.pack(anchor='s', side='bottom', fill='both')

        # Импорт базы данных с карточками для игры
        with open("database.json", 'r') as read_file:
            database = json.load(read_file)
        self.tiles = []
        self.used = 0
        i = 1
        while True:
            if f"Card_{i}" in database.keys():  # Добавляем загруженную базу с карточками во внутриигровую базу карточек
                new_tile = Tile(database[f"Card_{i}"]["edges"],
                                database[f"Card_{i}"]["edge_obj"],
                                database[f"Card_{i}"]["view"],
                                database[f"Card_{i}"]["has_shield"],
                                database[f"Card_{i}"]["has_monastery"])
                self.tiles.append(new_tile)
                i += 1
            else:
                break

        self.command_chosen = ''
        self.input_chosen = ''
        self.flag_chosen = 0

    def action_done(self):
        self.command_chosen = self.what_to_do.get()
        self.input_chosen = self.input_command.get()
        self.flag_chosen = 1

    def system_alarm_update(self, new_text):  # изменение того, что выдаёт система на экран
        self.system_alarms.config(state="normal")
        self.system_alarms.delete('1.0', tk.END)
        self.system_alarms.insert('1.0', new_text)
        self.system_alarms.config(state="disabled")

    def start_game(self):  # запуск игры
        self.start_this_game.config(state="disabled")
        while True:
            player = self.players.pop(0)
            self.players.append(player)
            text_in = str('This is turn of ' + player.get_name() + '! Yea!\n')
            self.cur_player_name.config(state="normal")
            self.cur_player_name.delete(0, tk.END)
            self.cur_player_name.insert(1, player.get_name())
            self.cur_player_name.config(state="disabled")

            self.view_board.delete('1.0', tk.END)

            self.view_board.insert('1.0', self.board.print_board())

            cur_tile = None
            if self.used == len(self.tiles):  # ОКОНЧАНИЕ ИГРЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫЫ
                score = self.board.count_points(self.names)
                score_m = self.board.count_points_by_monasteries(self.names)
                for i in score.keys():
                    score[i] += score_m[i]
                max_key = max(score, key=score.get)
                self.system_alarm_update(
                    'End!\n' + 'The winner is ' + max_key + ' with ' + str(score[max_key]) + ' points')

            while True:  # Выбираем следующую карточку
                number_of_tile = random.randrange(0, len(self.tiles))
                if not self.tiles[number_of_tile].is_placed and self.board.can_placed(self.tiles[number_of_tile]):
                    cur_tile = self.tiles[number_of_tile]
                    self.used += 1
                    break
            if cur_tile == None:
                self.system_alarm_update("Error, can't find a card")
                break
            instr = (
                    text_in + "You can add this tile to board:\n" + cur_tile.tile_view() + "Choose rotate if you want to rotate it clockwise\n"
                    + "Choose 'place card' and type coordinates x y if you want to move it to place (x, y) on the board")
            self.system_alarm_update(instr)
            while True:  # установка карточки на поле
                self.flag_chosen = 0
                while True:
                    if self.flag_chosen == 1:
                        break
                data = []
                if self.command_chosen == "Rotate":  # поворот карточки
                    cur_tile.rotate()
                    instr = (
                                "You can add this tile to board:\n" + cur_tile.tile_view() + "Choose rotate if you want to rotate it clockwise\n"
                                + "Choose 'place card' and type coordinates x y if you want to move it to place (x, y) on the board")
                    self.system_alarm_update(instr)
                elif self.command_chosen == "Place card":
                    data = self.input_chosen.split()
                    try:
                        cur_x, cur_y = data[0], data[1]
                        self.board.place(cur_tile, int(data[0]), int(data[1]))
                        if cur_tile.is_placed:
                            break
                        else:
                            instr = (
                                    "You can't place your tile here\n" + "You can add this tile to board:\n" + cur_tile.tile_view() + "Choose rotate if you want to rotate it clockwise\n"
                                    + "Choose 'place card' and type coordinates x y if you want to move it to place (x, y) on the board")
                            self.system_alarm_update(instr)
                    except ValueError:
                        self.system_alarm_update("Incorrect input\n" + instr)
                else:
                    self.system_alarm_update("Incorrect command\n" + instr)

            for i in self.board.get_miples()[:]:  # МИПЛИНГ
                if i[3] == 'M':
                    continue
                self.board.mipling(i)
                remv = self.board.remipling()
                if remv:
                    for j in self.players:
                        if j.is_name(i[0]):
                            j.return_miple()
                            self.board.del_miple(i)
                            self.board.get_board()[(i[1], i[2])].del_miple_from_view(i[3])

            score = self.board.count_points(self.names)  # ПОДСЧЕТ ОЧКОООООООООООООООООООООООООООООООООООООООВ
            score_m = self.board.count_points_by_monasteries(self.names)
            for i in score.keys():
                score[i] += score_m[i]

            pts_output = ''  # Вывод очков на экран
            for i in score.keys():
                if pts_output != '':
                    pts_output += '\n'
                score[i] += score_m[i]
                pts_output = pts_output + str(i) + ': ' + str(score[i])
            self.players_points.config(state="normal")
            self.players_points.delete('1.0', tk.END)
            self.players_points.insert('1.0', pts_output)
            self.players_points.config(state="disabled")

            local_flag = 0  # установка мипла
            instr = ('Now you have ' + str(player.get_miples()) + ' miples!\n' +
                     'You can set your miple! Choose finish, if you dont want to do this\n' +
                     'Choose set miple and type coordinates (x, y) and a side (N, W, S, E), if you want to set your miple')
            self.system_alarm_update(instr)
            while True:
                self.view_board.delete('1.0', tk.END)

                self.view_board.insert('1.0', self.board.print_board())

                miples = player.get_miples()
                self.flag_chosen = 0
                if miples == 0:
                    break
                else:
                    while True:
                        if self.flag_chosen == 1:
                            break
                    if self.command_chosen == 'Finish':
                        local_flag = 1
                    elif self.command_chosen == 'Set miple':
                        data = list(map(str, self.input_chosen.split()))
                        try:
                            data[0], data[1] = int(data[0]), int(data[1])
                            if (data[2] not in ['E', 'W', 'S', 'N', 'M']) or (
                                    data[2] == 'M' and not self.board.get_board()[(data[0], data[1])].is_monastery()):
                                self.system_alarm_update("Wrong input! Try again!\n" + instr)
                                self.flag_chosen = 0
                            elif (data[0], data[1]) not in self.board.get_board().keys():
                                self.system_alarm_update("This tile is not on the board!!!\n" + instr)
                                self.flag_chosen = 0
                            elif self.board.get_board()[(data[0], data[1])].is_mipled(data[2]):
                                self.system_alarm_update("This tile is already mipled! Chose another one!\n" + instr)
                                self.flag_chosen = 0
                            elif data[2] == 'M':
                                self.board.append_miple(player.get_name(), data[0], data[1], data[2])
                                self.board.get_board()[(data[0], data[1])].set_miple(data[2], player.get_name())
                                player.set_miple()
                                self.board.get_board()[(data[0], data[1])].set_miple_on_view(data[2], player.get_name())
                                # print('Miple successfully placed!')  # ЯРИК, ЭТО СИСТЕМНЫЕ СООБЩЕНИЯ ДЛЯ ОТСЛЕЖИВАНИЯ МИПЛОВ
                                # print(self.board.get_board()[(data[0], data[1])].get_miples())
                                local_flag = 1
                            elif self.board.get_board()[(data[0], data[1])].get_edges()[data[2]] == 'field':
                                self.system_alarm_update(
                                    "Bro, we are playing without fields! Chose another edge...\n" + instr)
                                self.flag_chosen = 0
                            else:
                                self.board.append_miple(player.get_name(), data[0], data[1],
                                                        self.board.get_board()[(data[0], data[1])].get_claster(data[2]))
                                self.board.get_board()[(data[0], data[1])].set_miple(data[2], player.get_name())
                                player.set_miple()
                                self.board.get_board()[(data[0], data[1])].set_miple_on_view(data[2], player.get_name())
                                # print('Miple successfully placed!')  # ЯРИК, ЭТО СИСТЕМНЫЕ СООБЩЕНИЯ ДЛЯ ОТСЛЕЖИВАНИЯ МИПЛОВ
                                # print(self.board.get_board()[(data[0], data[1])].get_miples())
                                local_flag = 1
                        except ValueError:
                            self.system_alarm_update("V Incorrect input\n" + instr)
                            self.flag_chosen = 0
                        # except KeyError:
                        #    self.system_alarm_update("K Incorrect input\n" + instr)
                        #    self.flag_chosen = 0
                    else:
                        self.system_alarm_update("Incorrect command\n" + instr)
                        self.flag_chosen = 0
                if local_flag == 1:
                    break

            for i in self.board.get_miples()[:]:  # МИПЛИНГ
                if i[3] == 'M':
                    continue
                self.board.mipling(i)
                remv = self.board.remipling()
                if remv:
                    for j in self.players:
                        if j.is_name(i[0]):
                            j.return_miple()
                            self.board.del_miple(i)
                            self.board.get_board()[(i[1], i[2])].del_miple_from_view(i[3])
            # print(self.board.get_miples())

            score = self.board.count_points(self.names)  # ПОДСЧЕТ ОЧКОООООООООООООООООООООООООООООООООООООООВ
            score_m = self.board.count_points_by_monasteries(self.names)

            pts_output = ''  # Вывод очков на экран
            for i in score.keys():
                if pts_output != '':
                    pts_output += '\n'
                score[i] += score_m[i]
                pts_output = pts_output + str(i) + ': ' + str(score[i])
            # print(pts_output)
            self.players_points.config(state="normal")
            self.players_points.delete('1.0', tk.END)
            self.players_points.insert('1.0', pts_output)
            self.players_points.config(state="disabled")


class Player:
    def __init__(self, name):
        self.miples = 7
        self.name = name

    def get_miples(self):
        return self.miples

    def get_name(self):
        return self.name

    def set_miple(self):
        self.miples -= 1

    def return_miple(self):
        self.miples += 1

    def is_name(self, name):
        if self.name == name:
            return True
        else:
            return False

