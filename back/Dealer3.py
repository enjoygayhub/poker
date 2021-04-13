import random
from itertools import chain
from collections import Counter
from itertools import combinations


class Dealer:
    def __init__(self):
        self.poker = set((x, y) for x in range(4) for y in range(13))
        self.round_card = []
        self.round = 0
        self.pot = 0

    def rank(self, cards5):  # 判断5张牌的牌型
        cards = list(chain(*cards5))
        flower_counter = Counter(cards[::2])  # 花色计数器
        _, max_number_of_flowers = flower_counter.most_common(1)[0]  # 记录卡牌花色最多的数量
        all_num = sorted(cards[1::2], reverse=True)
        number_counter = Counter(all_num)   # 牌值计数器
        most_four = number_counter.most_common(4)   # 牌值出现频率
        if max_number_of_flowers == 5:     # 同花顺
            if all_num[0]-all_num[-1] == 4:
                return [8, all_num[0]]
            elif all_num == [12, 3, 2, 1, 0]:    # 同花顺12345
                return [8, all_num[1]]
            else:
                return [5]+all_num     # 同花
        elif most_four[0][1] == 4:    # 4条
            return [7, most_four[0][0], most_four[1][0]]
        elif most_four[0][1] == 3:
            if most_four[1][1] == 2:   # 葫芦
                return [6, most_four[0][0], most_four[1][0]]
            else:
                return [3, most_four[0][0], most_four[1][0], most_four[2][0]]  # 3条
        elif most_four[0][1] == 2:
            if most_four[1][1] == 2:
                return [2, most_four[0][0], most_four[1][0], most_four[2][0]]    # 2 对
            else:
                return [1, most_four[0][0], most_four[1][0], most_four[2][0], most_four[3][0]]    # 一对
        elif all_num[0]-all_num[-1] == 4:       # 顺子
            return [4, all_num[0]]
        elif all_num == [12, 3, 2, 1, 0]:    # 顺12345
            return [4, all_num[1]]
        else:
            return [0]+all_num   # 高牌

    def deal(self):
        self.round_card.clear()
        self.pot = 0
        self.round += 1
        self.round_card = random.sample(self.poker, 9)
        print(self.round_card)

    def preflop_message(self):
        addr = ['SMALLBLIND', 'BIGBLIND']
        player1 = 'preflop|'+addr[self.round % 2] + \
                  '|{0[0]}|{0[1]}|{1[0]}|{1[1]}'.format(self.round_card[0], self.round_card[1])
        player2 = 'preflop|'+addr[(self.round + 1) % 2] + \
                  '|{0[0]}|{0[1]}|{1[0]}|{1[1]}'.format(self.round_card[7], self.round_card[8])
        return (player1, player2)

    def oppo_cards(self):
        player1 = 'oppo_hands|{0[0]}|{0[1]}|{1[0]}|{1[1]}'.format(self.round_card[0], self.round_card[1])
        player2 = 'oppo_hands|{0[0]}|{0[1]}|{1[0]}|{1[1]}'.format(self.round_card[7], self.round_card[8])
        return (player1, player2)

    def flop_message(self):
        message = 'flop|{0[0]}|{0[1]}|{1[0]}|{1[1]}|{2[0]}|{2[1]}'. \
            format(self.round_card[2], self.round_card[3], self.round_card[4])
        return message

    def turn_message(self):
        message = 'turn|{0[0]}|{0[1]}'.format(self.round_card[5])
        return message

    def river_message(self):
        message = 'river|{0[0]}|{0[1]}'.format(self.round_card[6])
        return message

    def judge(self):
        mine = self.round_card[:7]
        opponent = self.round_card[2:]
        val1 = max(map(self.rank, combinations(mine,5)))
        val2 = max(map(self.rank, combinations(opponent,5)))
        if val1 > val2:
            return 1, val1
        elif val1 < val2:
            return -1, val2
        else:
            return 0, val1


if __name__ == '__main__':
    e=Dealer()
    for _ in range(5):
        e.deal()
        mess=e.preflop_message()
        print(mess)
        print(e.flop_message())
        print(e.river_message())
        print(e.oppo_cards())
        print(e.judge())
    pass
    # name1 = [2,3,4,5,6,7,8,9,10,'J','Q',"K",'A']
    # name = ['高牌', "一对", '二对', '三条', '顺子', '同花', "葫芦", "四条", '同花顺']
    # temp = pd.DataFrame(columns=name, data=result)
    # temp.to_csv('temp.csv')


