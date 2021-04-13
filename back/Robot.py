

class Robot:

    def __init__(self):
        self.win = 0
        self.money = 20000
        self.Max_money = 20000
        self.pot = 0
        self.bet_size = 100
        self.position = 'smallblind'
        self.cards = set()
        self.name = 'robot'

    @staticmethod
    def act(state=None):
        if state:
            return 'call'
        else:
            return 'call'

    def reset(self):
        self.money = 20000
        self.pot = 0
        self.bet_size = 100
        self.position = 'bigblind' if self.position == 'smallblind' else 'smallblind'
