# import threading as td
from Dealer3 import Dealer
from Robot import Robot
import time
import sys



class Player:
    Max_money = 20000

    def __init__(self, client, position='bigblind'):
        self.client = client
        self.name = 'admin'
        self.money = self.Max_money
        self.win = 0
        self.position = position

    def reset(self):
        self.money = self.Max_money
        self.position = 'bigblind' if self.position == 'smallblind' else 'smallblind'


class Game:
    def __init__(self, player1):
        self.player1 = player1
        self.robot = Robot()
        self.dealer = Dealer()

    def start(self):
        pass


    @staticmethod
    def send_message(player, message):
        try:
            if player.name == 'admin':
                player.client.send(message)
            else:
                pass
            # time.sleep(0.1)
        except Exception as e:
            print('错误类型是', e.__class__.__name__)
            print('错误明细', e)
            sys.exit(-1)

    @staticmethod
    def recv_message(player):
        try:
            if player.name == 'admin':
                message = player.client.recv()
            else:
                message = player.act()
            print('get message from {0}:{1}'.format(player.name, message))
            return message
        except Exception as e:
            # if e.__class__.__name__ == 'timeout':
            #     print('错误类型是', e.__class__.__name__)
            #     print(player.name, end=' ')
            #     print('  超时错误！！！！')
            #     return ''

            print('错误类型是', e.__class__.__name__)
            sys.exit(-1)

    def payoff(self, winer, loser, non_tie=1):   # 结账
        cash = winer.money + self.dealer.pot//non_tie - winer.Max_money
        winer.win += cash
        loser.win -= cash
        self.send_message(winer, "earnChips " + str(cash))
        self.send_message(loser, "earnChips " + str(-cash))
        time.sleep(0.1)
        print("round {0}:{1} win {2}".format(self.dealer.round, winer.name, cash))
        print("round {0}:{1} lost {2}".format(self.dealer.round, loser.name, cash))

    @staticmethod
    def _print(player, action):
        print(player.name, end=' ')
        print(': ' + action)

    def pre_bet(self, players):
        players[0].money -= 100
        players[1].money -= 50
        self.dealer.pot += 150
        times = 1  # 响应次数
        bet_size = 100
        while times < 8:
            message = self.recv_message(players[times % 2])  # small blind act first time
            if not message:   # 超时
                self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
                return 1  # 返回该局结束
            if message == 'fold':
                self.send_message(players[(times+1) % 2], message)
                self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
                return 1  # 返回该局结束
            elif message == 'call':
                players[times % 2].money = players[(times+1) % 2].money
                self.dealer.pot = (players[times % 2].Max_money-players[times % 2].money)*2
                if times == 1:
                    self.send_message(players[(times+1) % 2], message)
                else:
                    self.send_message(players[(times+1) % 2], message)
                    return 0   # preflop下注结束
            # elif message == 'check':
            #     if players[0].money != players[1].money:
            #         print('illegal check!')
            #         self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
            #         return 1
            #     else:
            #         self.send_message(players[(times+1) % 2], message)
            #         return 0   # 仅第二次响应大盲注可以cheak,小盲call为前提

            elif message == 'allin':
                self.send_message(players[(times+1) % 2], message)
                self.dealer.pot += players[times % 2].money
                players[times % 2].money = 0
                message1 = self.recv_message(players[(times+1) % 2])
                if message1 == 'fold':
                    self.send_message(players[times % 2], message)
                    self.payoff(players[times % 2], players[(times+1) % 2])  # 结账
                    return 1  # 返回该局结束
                elif message1 == 'call':
                    self.send_message(players[times % 2], message)
                    players[(times+1) % 2].money = players[times % 2].money
                    self.dealer.pot = (players[times % 2].Max_money-players[times % 2].money)*2
                    return 2  # 直接比牌阶段
                else:
                    print('unkown message to call allin')
                    self.payoff(players[times % 2], players[(times+1) % 2])  # 结账
                    return 1
            else:
                info = message.split()
                if info[0] == "raise":
                    temp = int(eval(info[1]))
                    if temp < players[times % 2].money-players[(times+1) % 2].money+bet_size or temp> players[times % 2].money:
                        print("raise money error！")
                        self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
                        return 1
                    self.send_message(players[(times+1) % 2], message)
                    players[times % 2].money -= temp
                    self.dealer.pot += temp
                    bet_size = abs(players[times % 2].money-players[(times+1) % 2].money)
                else:
                    print('unkown message')
                    self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
                    return 1
            times += 1   # next bet

    def bet(self, players):
        times = 0
        bet_size = 100
        while times < 8:
            message = self.recv_message(players[times % 2])
            if not message:   # 超时
                self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
                return 1  # 返回该局结束
            if message == 'fold':
                self.send_message(players[(times+1) % 2], message)
                self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
                return 1  # 返回该局结束
            elif message == 'call':
                players[times % 2].money = players[(times + 1) % 2].money
                self.dealer.pot = (players[times % 2].Max_money - players[times % 2].money) * 2
                if times == 0:
                    self.send_message(players[(times + 1) % 2], message)
                else:
                    self.send_message(players[(times + 1) % 2], message)
                    return 0  # preflop下注结束

            # elif message == 'check':
            #     if players[times % 2].money != players[(times+1) % 2].money:
            #         print('illegal check!')
            #         self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
            #         return 1
            #     else:
            #         self.send_message(players[(times+1) % 2], message)
            #         if times == 1:
            #             return 0  # bet over

            elif message == 'allin':
                self.send_message(players[(times+1) % 2], message)
                self.dealer.pot += players[times % 2].money
                players[times % 2].money = 0
                message1 = self.recv_message(players[(times+1) % 2])
                if message1 == 'fold':
                    self.send_message(players[times % 2], message)
                    self.payoff(players[times % 2], players[(times+1) % 2])  # 结账
                    return 1  # 返回该局结束
                elif message1 == 'call':
                    self.send_message(players[times % 2], message)
                    players[(times+1) % 2].money = 0
                    self.dealer.pot = (players[times % 2].Max_money-players[times % 2].money)*2
                    return 2  # 直接比牌阶段
                else:
                    print('ukown message')
                    self.payoff(players[times % 2], players[(times+1) % 2])  # 结账
                    return 1
            else:
                info = message.split()
                if info[0] == "raise":
                    temp = int(eval(info[1]))
                    if temp < players[times % 2].money-players[(times+1) % 2].money+bet_size or temp> players[times % 2].money:
                        print("raise money error！")
                        self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
                        return 1
                    self.send_message(players[(times+1) % 2], message)
                    players[times % 2].money -= temp
                    self.dealer.pot += temp
                    bet_size=abs(players[times % 2].money-players[(times+1) % 2].money)
                else:
                    print('unkown message!')
                    self.payoff(players[(times+1) % 2], players[times % 2])  # 结账
                    return 1
            times += 1   # next bet

    def round(self):
        self.dealer.deal()   # 重置桌面信息，产生9张牌，发牌进入preflop阶段
        print('round {0} begin! '.format(self.dealer.round))
        print('{0}:{1}'.format(self.player1.name, self.player1.position))
        print('{0}:{1}'.format(self.robot.name, self.robot.position))

        while True:
            # "'发送preflop，盲注位，牌信息'"
            pre_message = self.dealer.preflop_message()   # 0索引固定为player1的牌，1索引固定robot的牌
            self.send_message(self.player1, pre_message[0])
            self.send_message(self.robot, pre_message[1])

            # "'下注位，大在前，奇数局player1为大盲'"
            players = (self.player1, self.robot) if self.dealer.round % 2 else (self.robot, self.player1)
            if self.pre_bet(players):
                break

            flop_message = self.dealer.flop_message()
            self.send_message(self.player1, flop_message)
            self.send_message(self.robot, flop_message)

            if self.bet(players):
                break

            turn_message = self.dealer.turn_message()
            self.send_message(self.player1, turn_message)
            self.send_message(self.robot, turn_message)

            if self.bet(players):
                break

            river_message = self.dealer.river_message()
            self.send_message(self.player1, river_message)
            self.send_message(self.robot, river_message)

            if self.bet(players):
                break
            self.showdown()  # 正常结束比牌
            break
        if self.player1.money == 0 and self.robot.money == 0:
            self.showdown()  # allin 比牌
        self.player1.reset()
        self.robot.reset()
        pass

    def showdown(self):

        win, val = self.dealer.judge()
        if win == 1:
            self.payoff(self.player1, self.robot)
        elif win == -1:
            self.payoff(self.robot, self.player1)
        else:
            self.payoff(self.player1, self.robot, 2)

        oppo = self.dealer.oppo_cards()   # 0索引固定为player1的牌，1索引固定robot的牌
        self.send_message(self.robot, oppo[0])
        self.send_message(self.player1, oppo[1])

    def end(self):
        print('the result is:')
        print(self.player1.name, end='')
        print(self.player1.win)
        print(self.robot.name, end='')
        print(self.robot.win)

    def run(self):
        # self.start()
        for _ in range(10):
            self.round()
            time.sleep(5)
        self.end()
        pass






