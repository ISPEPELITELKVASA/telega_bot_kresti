
class SessionGame:
    cross = None # 232323
    zero = None # 123123
    walk = None # Кто ходит в данный момент
    matrix = [n for n in range(0, 9)]
    coord_win = ((0,1,2), (3,4,5), (6,7,8), (0,3,6),
                (1,4,7), (2,5,8), (0,4,8), (2,4,6))
    
    def __init__(self, user_id1, user_id2):
        self.cross = self.walk = user_id1
        self.zero = user_id2
        self.matrix = [n for n in range(0, 9)]

    def move(self, pos, user_id):
        # Совершение хода
        if not self.check_move(pos, user_id): return False
        if self.walk == self.cross:
            self.matrix[pos] = 'X'
        elif self.walk == self.zero:
            self.matrix[pos] = '0'
        # Передаем очередь хода противоположному игроку
        self.walk = self.cross if self.walk == self.zero else self.zero
        return True
    
    def check_move(self, pos, user_id):
        '''Проверка занята ли клетка, а так же проверка
        может ли ходить указанный игрок (id) в данный момент'''
        if isinstance(self.matrix[pos], str):
            return False
        if self.walk == user_id: # Может ли ходить в данный момент user_id
            return True

    def check_win(self):
        for coords in self.coord_win:
            if self.matrix[coords[0]] == self.matrix[coords[1]] == self.matrix[coords[2]]:
                print('Победил ' + str(self.matrix[coords[0]]))
                return str(self.matrix[coords[0]])
        return False
    
    def nichya(self):
        for x in self.matrix:
            if type(x) == int:
                return False
        return True
    
    
    def get_ids(self):
        return self.cross, self.zero
    
    
    def check_draw(self):
        for x in self.matrix:
            if type(x) == int:
                return True
        return False

    def draw(self):
        drawing = ''
        for i in range(3):
            drawing += ('|' + str(self.matrix[0+i*3]) + '|' +
                        str(self.matrix[1+i*3]) + '|' +
                        str(self.matrix[2+i*3]) + '|')
            drawing += '-' * 13
        return drawing