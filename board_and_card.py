class Tile:

    def __init__(self, edges, edge_obj, has_monastery=False, has_shield=False, is_placed = False):
        self.edges = edges # объекты на краях; нужно для проверки возможности установки
        self.edge_obj = edge_obj # связи между объектами
        self.has_monastery = has_monastery # маркер наличия монастыря; обыграем потом, это сложно
        self.has_shield = has_shield # Маркер наличия щита; удваивает очки за клетку
        self.miples = {"E": "",
                       "S": "",
                       "W": "", # Маркер занятости объектов
                       "N": ""}
        self.is_placed = is_placed # маркер установки на поле; блокирует некоторые функции


    def rotate(self): # переворот тайла
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
            return self

        else:
            print("this tile is already placed! you can`t rotate it!")


    def set_to_board(self): # маркер установки на доску, блокирующий некоторые функции
        if self.is_placed:
            print("this tile is already in game")
        else:
            self.is_placed = True


    def set_miple(self, edge, player): # установка мипла на тот или иной край (объект)
        if self.miples[edge] != "":     # юзается при подсчете очков и чтобы не миплать уже занятую клетку
            print("this object is already mipled!")
        else:
            for i in self.edge_obj:
                if edge in i:
                    for j in i:
                        self.miples[j] = player


    def get_edge_obj(self): # запрос связей между объектами; для функции подсчета
        return self.edge_obj


    def get_edges(self): # запрос расположения объектов по сторонам; для функции установки на доску
        return self.edges



    def check(self): # проверка характеристик тайла (функция разработчика)
        print(self.edges)
        print(self.miples)
        print(self.edge_obj)
        print(self.has_monastery)
        print(self.has_shield)
        print(self.is_placed)
        return self




test_edges = {"E": "road", "S": "city", "W": "road", "N": "field"}
test_edge_obj = ["EW", "N", "S"]
test = Tile(test_edges, test_edge_obj, False, False)

test.check()
test.rotate()
test.check()
test.set_miple('S', 'Roma')
test.set_to_board()
test.check()
test.set_to_board()
test.check()








class Board:
    def __init__(self): # создание доски с начальной клеткой посередине
        start_tile = Tile({"E": "road", "S": "city", "W": "road", "N": "field"}, ["E", "N", "S", "W"], False, False)
        self.board = []
        for i in range(9):
            a = []
            for j in range(9):
                a.append(Tile({"E": "none", "S": "none", "W": "none", "N": "none"}, ["E", "N", "S", "W"], False, False))
            self.board.append(a)
        self.board[4][4] = start_tile
        self.monasteries = [] # заготовка для подсчета очков за монастыри



    def place(self, tile, x, y):
        neighbours = {"E": "none", "S": "none", "W": "none", "N": "none"}
        if x < 8:
            neighbours['E'] = self.board[x+1][y].get_edges['W']
        if x > 0:
            neighbours['W'] = self.board[x-1][y].get_edges['E']
        if y < 8:
            neighbours['S'] = self.board[x][y+1].get_edges['N']
        if y > 0:
            neighbours['N'] = self.board[x][y-1].get_edges['S']

        if all([i == 'none' for i in neighbours.values()]):
            print('bro, choose a place near placed tiles!')
        elif not all([i == 'none' for i in board[x][y].get_edges()]):
            print('there is a tile already on this place!')
        elif all([tile.get_edges[i] == neighbours[i] or neighbours[i] == 'none' for i in ["E", "N", "S", "W"]]):
            self.board[x][y] = tile
            tile.set_to_board()
        else:
            print('you can`t place your tile here')


    def count_points_by_monasteries(self):
        pass # подсчет очков за монастыри


    def count_points(self):
        pass # подсчет очков









