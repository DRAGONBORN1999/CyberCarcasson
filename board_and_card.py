class Board:
    def __init__(self):  # создание доски с начальной клеткой посередине
        start_tile = Tile({"E": "road", "S": "city", "W": "road", "N": "field"}, ["E", "N", "S", "W"],
                          [['.', '.', '.'], ['R', 'R', 'R'], ['.', 'C', '.']], False, False)
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0  # Размеры поля
        self.board = dict()
        self.board[(0, 0)] = start_tile
        self.monasteries = []  # заготовка для подсчета очков за монастыри

    def place(self, tile, x, y):  # помещение карточки на поле
        flag = 1
        if (x, y) in self.board.keys():
            flag = 0
        if (x, y - 1) in self.board.keys() and not tile.is_connect(self.board[(x, y - 1)], "S"):
            flag = 0
        if (x, y + 1) in self.board.keys() and not tile.is_connect(self.board[(x, y + 1)], "N"):
            flag = 0
        if (x - 1, y) in self.board.keys() and not tile.is_connect(self.board[(x - 1, y)], "W"):
            flag = 0
        if (x + 1, y) in self.board.keys() and not tile.is_connect(self.board[(x + 1, y)], "E"):
            flag = 0
        if flag == 1 and ((x, y - 1) in self.board.keys() or (x, y + 1) in self.board.keys() or (x - 1,
                                                                                                 y) in self.board.keys() or (
                                  x + 1, y) in self.board.keys()):
            tile.set_to_board()
            self.board[(x, y)] = tile
            self.xmin = min(self.xmin, x)
            self.xmax = max(self.xmax, x)
            self.ymin = min(self.ymin, y)
            self.ymax = max(self.ymax, y)

        else:
            return 'you can`t place your tile here'
        return 'OK'

    def count_points_by_monasteries(self):
        pass  # подсчет очков за монастыри

    def count_points(self):
        pass  # подсчет очков

    def set_miple(self, player, edge, x, y):
        if (x, y) not in self.board.keys():
            print("No tile at given coordinates")
            return
        data = self.board[(x, y)].set_miple(edge, player)
        if data == "this object is already mipled!":
            return ("this object is already mipled!")

    def print_board(self):  # кустарный вывод доски на экран
        y_coord_size = max(len(str(self.ymax)), len(str(self.ymin)))
        view = ''
        view += ' ' * (y_coord_size + 1)
        for x in range(self.xmin, self.xmax + 1):  # вывод координат по оси x
            view += f"{str(x):^5}" + ' '
            if x == self.xmax:
                view += '\n'

        # Вывод клеток поля
        for y in range(self.ymax, self.ymin - 1, -1):
            for s in range(3):
                if s != 1:
                    view += ' ' * (y_coord_size + 1)
                else:
                    view += f"{str(y):^{y_coord_size}}" + ' '  # Вывод координат по оси y
                for x in range(self.xmin, self.xmax + 1):
                    if (x, y) not in self.board.keys():  # если там нет карточки
                        view += ' ' * 6
                    else:  # если там есть карточка
                        view += self.board[(x, y)].view[s][0] + ' ' + self.board[(x, y)].view[s][1] + ' ' + self.board[(x, y)].view[s][2] + ' '
                    if x == self.xmax:
                        view += '\n' # перевод строки
        return view

class Tile:

    def __init__(self, edges, edge_obj, view, has_monastery=False, has_shield=False, is_placed=False):
        self.edges = edges  # объекты на краях; нужно для проверки возможности установки
        self.edge_obj = edge_obj  # связи между объектами
        self.has_monastery = has_monastery  # маркер наличия монастыря; обыграем потом, это сложно
        self.has_shield = has_shield  # Маркер наличия щита; удваивает очки за клетку
        self.view = view  # Отображение карточки (пока текстовое)
        self.miples = {"E": "",
                       "S": "",
                       "W": "",  # Маркер занятости объектов
                       "N": ""}
        self.is_placed = is_placed  # маркер установки на поле; блокирует некоторые функции

    def rotate(self):  # переворот тайла
        if not self.is_placed:
            directions = ['N', 'E', 'S', 'W']
            new_edges = {}
            new_miples = {}
            for d in directions:
                new_dir = directions[(directions.index(d) + 1) % 4]
                new_edges[new_dir] = self.edges[d]
                new_mip = directions[(directions.index(d) + 1) % 4]
                new_miples[new_mip] = self.miples[d]
            self.edges = new_edges
            self.miples = new_miples
            for i in range(len(self.edge_obj)):
                new_obj = ''
                for j in self.edge_obj[i]:
                    if j == 'N':
                        new_obj += 'E'
                    elif j == 'E':
                        new_obj += 'S'
                    elif j == 'S':
                        new_obj += 'W'
                    elif j == 'W':
                        new_obj += 'N'
                self.edge_obj[i] = new_obj
            self.view = [[self.view[2][0], self.view[1][0], self.view[0][0]],
                         [self.view[2][1], self.view[1][1], self.view[0][1]],
                         [self.view[2][2], self.view[1][2], self.view[0][2]]]
            return self

        else:
            print("this tile is already placed! you can`t rotate it!")

    def set_to_board(self):  # маркер установки на доску, блокирующий некоторые функции
        if self.is_placed:
            print("this tile is already in game")
        else:
            self.is_placed = True

    def set_miple(self, edge, player):  # установка мипла на тот или иной край (объект)
        if self.miples[edge] != "":  # юзается при подсчете очков и чтобы не миплать уже занятую клетку
            return ("this object is already mipled!")
        else:
            for i in self.edge_obj:
                if edge in i:
                    for j in i:
                        self.miples[j] = player
                    return (i)

    def get_edge_obj(self):  # запрос связей между объектами; для функции подсчета
        return self.edge_obj

    def get_edges(self):  # запрос расположения объектов по сторонам; для функции установки на доску
        return self.edges

    def check(self):  # проверка характеристик тайла (функция разработчика)
        print(self.edges)
        print(self.miples)
        print(*self.view)
        print(self.edge_obj)
        print(self.has_monastery)
        print(self.has_shield)
        print(self.is_placed)
        return self

    def is_connect(self, other_tile,
                   edge):  # проверяет, можно ли присоединить к ней другую карточку с определённой стороны
        check = self.edges[edge]
        if edge == "E":
            if check == other_tile.edges["W"]:
                return True
        elif edge == "S":
            if check == other_tile.edges["N"]:
                return True
        elif edge == "W":
            if check == other_tile.edges["E"]:
                return True
        elif edge == "N":
            if check == other_tile.edges["S"]:
                return True
        else:
            print("Error")
        return False

    def tile_view(self):  # Визуализация карточки
        return (self.view[0][0] + ' ' + self.view[0][1] + ' ' + self.view[0][2] + '\n' +
                self.view[1][0] + ' ' + self.view[1][1] + ' ' + self.view[1][2] + '\n' +
                self.view[2][0] + ' ' + self.view[2][1] + ' ' + self.view[2][2] + '\n')
