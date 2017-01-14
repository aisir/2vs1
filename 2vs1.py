# 俩子抵一个
# 游戏规则
# 1 黑白双方各四枚棋，棋盘 4X4
# 2 黑棋先
# 3 横向或竖向 三枚棋子连续 黑棋2枚白棋一枚则该枚白棋出局，反之亦然。
# 4 一方剩余棋子小于2枚，则另一方胜



class Chess(object):

    def __init__(self, uid, flag, location=None):
        self.uid = uid
        self.flag = flag
        self.location = location

    def __str__(self):
        return self.flag


class Board(object):
    dir = {'u': (-1, 0), 'r': (0, 1), 'd': (1, 0), 'l': (0, -1)}
    error = 'ERROR'

    def __init__(self, flag1, flag2):
        self.layout = [[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]
        self.flag1 = flag1
        self.flag2 = flag2
        str1 = self.flag1+self.flag1+self.flag2
        str2 = self.flag2+self.flag2+self.flag1
        self.label =[str1, str2]
        self.chesses = {flag1: [], flag2: []}
        for x in range(4):
            self.layout[0][x] = self.flag1+str(x+1)
            self.layout[3][x] = self.flag2+str(x+1)
            a = Chess(x, self.flag1+str(x+1), (0, x))
            self.chesses[flag1].append(a)
            b = Chess(x, self.flag2+str(x+1), (3, x))
            self.chesses[flag2].append(b)

    def __rule(self):
        lay = self.layout
        label = self.label
        result = None
        for x in range(4):
            for y in range(4):
                a = lay[x][y]
                if a == 0:
                    continue
                else:
                    a = a[0]
                if x < 2:
                    b = lay[x - 3][y]
                    b = b[0] if b != 0 else b
                    c = lay[x - 2][y]
                    c = c[0] if c != 0 else c
                    abc = str(a) + str(b) + str(c)
                    if abc in label or abc[::-1] in label:
                        if a == b:
                            lay[x - 2][y] = 0
                            result = x+2, y
                            break
                        else:
                            lay[x][y] = 0
                            result = x, y
                            break
                if y < 2:
                    b = lay[x][y - 3]
                    b = b[0] if b != 0 else b
                    c = lay[x][y - 2]
                    c = c[0] if c != 0 else c
                    abc = str(a) + str(b) + str(c)
                    if abc in label or abc[::-1] in label:
                        if a == b:
                            lay[x][y - 2] = 0
                            result = x, y + 2
                            break
                        else:
                            lay[x][y] = 0
                            result = x, y
                            break

        return result

    def __update(self):
        a = self.__rule()
        info =''
        if a:
            ch1 = len(self.chesses[self.flag1])
            self.chesses[self.flag1] = [ch for ch in self.chesses[self.flag1] if ch.location != a]
            self.chesses[self.flag2] = [ch for ch in self.chesses[self.flag2] if ch.location != a]
            if len(self.chesses[self.flag1]) < ch1:
                info = '【'+self.flag1+'】失去一枚棋子'
            else:
                info = '【' + self.flag2 + '】失去一枚棋子'

        return info

    def chess_move(self, flag, num, d):
        chess = [x for x in self.chesses[flag] if x.uid == (num-1)][0]
        a, b = chess.location
        x = a + Board.dir[d][0]
        y = b + Board.dir[d][1]
        info =''
        if x < 0 or x > 3 or y < 0 or y > 3 or self.layout[x][y] != 0:
            return Board.error
        else:
            self.layout[a][b] = 0
            chess.location = x, y
            self.layout[x][y] = chess.flag
            print('【'+flag+'】移动了棋子{}-->{}'.format((a, b), (x, y)))
            rst = self.__update()
            print(rst)
            print(self.layout)
            if len(self.chesses[self.flag1]) < 2:
                info = '【'+self.flag2+'】获胜，GAME OVER'
            if len(self.chesses[self.flag2]) < 2:
                info = '【' + self.flag1 + '】获胜，GAME OVER '

            return info


class Gamer(object):

    def __init__(self, flag):
        self.flag = flag

    def move_chess(self, num, d, bd):
        return bd.chess_move(self.flag, num, d)

if __name__ == '__main__':
    person1 = Gamer('b')
    person2 = Gamer('w')
    board = Board(person1.flag, person2.flag)
    while True:
        print(board.layout)
        tmp = '【{}】拥有棋子：{};【{}】拥有棋子：{}'
        info1, info2 = '', ''
        for x in board.chesses[person1.flag]:
            info1 += x.flag+' '
        for x in board.chesses[person2.flag]:
            info2 += x.flag+' '
        print(tmp.format(person1.flag, info1, person2.flag, info2))
        print('【' + person1.flag + '】请选择棋子,输入棋子数字')
        c = int(input())
        print('请选择移动方向 u:上，r:右 d:下 l:左')
        direction = input()
        result = person1.move_chess(c, direction, board)
        if "GAME OVER" in result:
            print(result)
            break
        elif result == "ERROR":
            print("重新开始")
            continue
        else:
            print(result)
        print('【' + person2.flag + '】请选择棋子,输入棋子数字')
        c = int(input())
        print('请选择移动方向 u:上，r:右 d:下 l:左')
        direction = input()
        result = person2.move_chess(c, direction, board)
        if "GAME OVER" in result:
            print(result)
            break
        elif result == "ERROR":
            print("重新开始")
            continue
        else:
            print(result)
