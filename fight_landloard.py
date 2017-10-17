# -*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import collections
import random
import re

Card = collections.namedtuple("Card", ['rank', 'suit'])
card_queue = []

class Acard:
    ranks = [str(n) for n in range(3, 10)] + list('LJQKAT')
    suits = '黑桃 梅花 方片 红桃'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

class Fight_loardlan:
    card_pat = re.compile(r"[^2-9JQKAFMLT\s]")
    THREE_THREE_TWO = '332_'
    THREE_THREE_ONE = '331_'
    THREE_THREE = '33_'
    THREE_TWO = '32_'
    THREE_ONE = '31_'
    THREE = '3_'
    FOUR_TWO = '42_'
    FOUR = '4_'
    TWO = '2_'
    TWO_QUEUE = '22_'
    ONE = '1_'
    ONE_QUEUE = '11_'
    BIG_BOMB = '0_'

    turn_name = ['地主', '农民一', '农民二']
    letter_to_num = {
        "L": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
        "T": 16,
        "F": 99,
        "M": 100
    }

    def __init__(self):
        self.turn = 0
        self.master = 0
        self.cards = [card for card in Acard()] + [Card(suit='小王', rank='F'), Card(suit='大王', rank='M')]
        self.deal_cards()
        self.card_queue = []

    def deal_cards(self):
        length = len(self.cards)
        random_cards = []
        while len(self.cards) > 0:
            position = random.randint(0, length - 1)
            random_cards.append(self.cards.pop(position))
            length -= 1

        landlord = []
        former1 = []
        former2 = []


        landlord.extend(random_cards[:-3:3])
        former1.extend(random_cards[1:-3:3])
        former2.extend(random_cards[2:-3:3])
        landlord.extend(random_cards[-3:])

        self.landlord = sorted(landlord, key=lambda x: self.cat_to_int(x.rank))
        self.former1 = sorted(former1, key=lambda x: self.cat_to_int(x.rank))
        self.former2 = sorted(former2, key=lambda x: self.cat_to_int(x.rank))

        self.cards_all = [
            [x.rank for x in self.landlord],
            [x.rank for x in self.former1],
            [x.rank for x in self.former2]
        ]

        self.print_card()

    def get_card(self, card):
        if card == 'F':
            return '小王F'
        elif card == 'M':
            return '大王M'
        elif card == 'L':
            return '10'
        elif card == 'T':
            return '2'
        else:
            return card

    def print_card(self):
        print_encoding("\n地主的牌：")
        for _ in self.landlord:
            print_encoding("%s_%s" % (_.suit, self.get_card(_.rank)))

        print_encoding("\n农民一的牌：")
        for _ in self.former1:
            print_encoding("%s_%s" % (_.suit, self.get_card(_.rank)))

        print_encoding("\n农民二的牌：")
        for _ in self.former2:
            print_encoding("%s_%s" % (_.suit, self.get_card(_.rank)))

    def print_card_num(self):
        print_encoding("\n地主的牌：")
        cards = [self.get_card(x) for x in self.cards_all[0]]
        print_encoding(",  ".join(cards))

        print_encoding("\n农民一的牌：")
        cards = [self.get_card(x) for x in self.cards_all[1]]
        print_encoding(",  ".join(cards))

        print_encoding("\n农民二的牌：")
        cards = [self.get_card(x) for x in self.cards_all[2]]
        print_encoding(",  ".join(cards))

    def comp_card(self, card1, card2):
        """
        :param card1: 前一次出牌 
        :param card2: 后一次出牌
        :return: 1：后一次大于前一次， -1：后一次小于前一次，0：格式不匹配
        """
        cs1 = card1.split('_')
        cs2 = card2.split('_')

        if cs2[0] + '_' == self.BIG_BOMB:
            return 1
        elif cs2[0] + '_' == self.FOUR:
            if cs1[0] + '_' == self.BIG_BOMB or (cs1[0] + '_' == self.FOUR and cs1[1] > cs2[1]):
                return -1
            else:
                return 1
        elif cs2[0] != cs1[0] or len(cs2) != len(cs1):
            print_encoding('跟上家牌模式不匹配')
            # 出牌格式不正确，不匹配
            return 0
        elif self.card_cmp(cs2[1], cs1[1]):
            return 1
        else:
            return -1

    def out_card(self, card):
        turn_card = self.cards_all[self.turn]
        cs = card.split('_')

        if cs[0] + '_' == self.BIG_BOMB:
            if 'f' in turn_card and 'M' in turn_card:
                turn_card.remove('F')
                turn_card.remove('M')
            else:
                return False
        elif cs[0] + '_' == self.THREE_THREE_TWO or cs[0] + '_' == self.THREE_TWO:
            for i in range(1, len(cs) / 2 + 1):
                if turn_card.count(cs[i]) < 3:
                    return False
            for i in range(len(cs) / 2 + 1, len(cs)):
                if turn_card.count(cs[i]) < 2:
                    return False

            for i in range(1, len(cs) / 2 + 1):
                for k in range(0, 3):
                    turn_card.remove(cs[i])
            for i in range(len(cs) / 2 + 1, len(cs)):
                for k in range(0, 2):
                    turn_card.remove(cs[i])
        elif cs[0] + '_' == self.THREE_THREE_ONE or cs[0] + '_' == self.THREE_ONE:
            for i in range(1, len(cs) / 2 + 1):
                if turn_card.count(cs[i]) < 3:
                    return False
            for i in range(len(cs) / 2 + 1, len(cs)):
                if turn_card.count(cs[i]) < 1:
                    return False

            for i in range(1, len(cs) / 2 + 1):
                for k in range(0, 3):
                    turn_card.remove(cs[i])
            for i in range(len(cs) / 2 + 1, len(cs)):
                turn_card.remove(cs[i])
        elif cs[0] + '_' == self.THREE_THREE:
            for i in range(1, len(cs)):
                if turn_card.count(cs[i]) < 3:
                    return False

            for i in range(1, len(cs)):
                for k in range(0, 3):
                    turn_card.remove(cs[i])
        elif cs[0] + '_' == self.FOUR_TWO:
            if turn_card.count(cs[1]) < 4 or turn_card.count(cs[2]) < 2:
                return False

            for k in range(0, 4):
                turn_card.remove(cs[1])
            for k in range(0, 2):
                turn_card.remove(cs[2])
        elif cs[0] + '_' == self.FOUR:
            if turn_card.count(cs[1]) < 4:
                return False

            for k in range(0, 4):
                turn_card.remove(cs[1])
        elif cs[0] + '_' == self.TWO_QUEUE or cs[0] + '_' == self.TWO:
            for i in range(1, len(cs)):
                if turn_card.count(cs[i]) < 2:
                    return False

            for i in range(1, len(cs)):
                for k in range(0, 2):
                    turn_card.remove(cs[i])
        elif cs[0] + '_' == self.ONE_QUEUE or cs[0] + '_' == self.ONE:
            for i in range(1, len(cs)):
                if turn_card.count(cs[i]) < 1:
                    return False

            for i in range(1, len(cs)):
                turn_card.remove(cs[i])

        return True

    def cat_to_int(self, card):
        return int(card) if card.isdigit() else self.letter_to_num[card]

    def calc_diff(self, a, b):
        return abs(self.cat_to_int(a) - self.cat_to_int(b))

    def card_cmp(self, a, b):
        return cmp(self.cat_to_int(a), self.cat_to_int(b)) > 0

    # 检查数组是否连续
    def check_consecutive(self, arr):
        for i in range(1, len(arr)):
            if self.calc_diff(arr[i], arr[i - 1]) != 1:
                return False

        return True

    def check_card(self, data):
        checked = True
        msg = None
        if len(data[3]) > 0:
            if len(data[3]) > 1:
                checked = False
                msg = '四个不能连对出'
            elif len(data[0]) > 0 or len(data[1]) > 1 or len(data[2]) > 0:
                checked = False
                msg = '四个只能带一对或者不带（最为炸弹）'

        elif len(data[2]) > 0:
            if len(data[0]) > 0 and len(data[0]) != len(data[2]) and (len(data[0]) + len(data[1]) * 2) != len(data[2]):
                checked = False
                msg = '三个只能带一个或者不带，小飞机必须都带单或者都不带'
            else:
                if not self.check_consecutive(data[2]):
                    msg = '小飞机必须是连续的'
        elif len(data[1]) > 0:
            if len(data[0]) > 0:
                checked = False
                msg = '对不能带单'
            else:
                if len(data[1]) == 2 or not self.check_consecutive(data[1]):
                    checked = False
                    msg = '连对至少三组连续的对'
        elif len(data[0]) > 0:
            if not (len(data[0]) == 2 and data[0][0] == 'f' and data[0][1] == 'm'):
                if 1 < len(data[0]) < 5 or (len(data[0]) > 4 and not self.check_consecutive(data[0])):
                    checked = False
                    msg = '顺子至少需要连续的五张单'

        return msg if checked else False

    def name_card(self, data):
        card_this = None

        if len(data[3]) > 0:
            if len(data[1]) == 1:
                card_this = self.FOUR_TWO + data[3][0] + '_' + data[1][0]
            else:
                card_this = self.FOUR + data[3][0]
        elif len(data[2]) > 0:
            if len(data[2]) > 1:
                if (len(data[0]) == len(data[2])) or (len(data[0]) + len(data[1]) * 2 == len(data[2])):
                    _card = self.THREE_THREE_ONE + '_'.join(data[2])
                    if len(data[0]) > 0:
                        _card += '_' + '_'.join(data[0])
                    if len(data[1]) > 0:
                        _card += '_' + '_'.join(repeat_arr(data[1]))

                    card_this = _card
                elif len(data[1]) > 0:
                    card_this = self.THREE_THREE_TWO + '_'.join(data[2]) + '_' + '_'.join(data[1])
                else:
                    card_this = self.THREE_THREE + '_'.join(data[2])
            else:
                if len(data[1]) > 0:
                    card_this = self.THREE_TWO + data[2][0] + '_' + data[1][0]
                elif len(data[0]) > 0:
                    card_this = self.THREE_ONE + data[2][0] + '_' + data[0][0]
                else:
                    card_this = self.THREE + data[2][0]
        elif len(data[1]) > 0:
            if len(data[1]) > 2:
                card_this = self.TWO_QUEUE + '_'.join(data[1])
            else:
                card_this = self.TWO + data[1][0]
        elif len(data[0]) > 0:
            if len(data[0]) == 1:
                card_this = self.ONE + data[0][0]
            elif len(data[0]) == 2:
                card_this = self.BIG_BOMB
            else:
                card_this = self.ONE_QUEUE + '_'.join(data[0])

        return card_this

    def turn_next(self):
        self.turn = 0 if self.turn == 2 else (1 if self.turn == 0 else 2)

    def deal_input(self, row):
        out = sorted([x.strip() for x in row.split()], cmp=self.card_cmp)
        data = [[], [], [], []]
        pos = 0
        for i in range(1, len(out)):
            if out[i] != out[i - 1]:
                char_len = i - pos
                data[char_len - 1].append(out[pos])
                pos = i
        if len(out) == 1:
            data[0].append(out[0])
        elif out[-1] != out[-2]:
            data[0].append(out[-1])
        else:
            data[len(out) - pos - 1].append(out[pos])

        return data

    def read_card(self):
        """
        :return: 0: 不出， -1：出牌格式错误，data: 出的牌 
        """

        self.print_card_num()
        if self.last_card():
            print_encoding("上家出牌：" + self.turn_name[self.master] + ": " + self.last_card())

        print "--------------------------------------------------------------------------------------------"
        card_out = raw_input(en_coding('%s出牌' % self.turn_name[self.turn])).replace("10", "L").replace("2", "T").strip()
        if not card_out == '0':
            if len(self.card_pat.findall(card_out)) > 0:
                print_encoding('请出正确的牌！')
                return -1
            else:
                data = self.deal_input(card_out)
                msg = self.check_card(data)
                if msg:
                    print_encoding(msg)

                    return -1

                card_this = self.name_card(data)
                return card_this

        else:
            #不出
            return 0

    def state(self):
        if len(self.cards_all[0]) == 0:
            return 1
        elif len(self.cards_all[1]) == 0 or len(self.cards_all[2]) == 0:
            return 2
        else:
            return 0

    def is_master(self):
        return self.turn == self.master

    def set_master(self):
        self.master = self.turn

    def in_queue(self, card):
        self.card_queue.append(card)
        self.out_card(card)
        self.turn_next()

    def last_card(self):
        return self.card_queue[-1] if len(self.card_queue) > 0 else None



coding = sys.stdin.encoding
def repeat_arr(arr):
    arr.extend(arr[:])
    return arr

def print_encoding(msg):
    print(msg.encode(coding))

def en_coding(msg):
    return b"\n" + msg.encode(coding) + b"\n"

if __name__ == "__main__":
    fight = Fight_loardlan()

    while fight.state() == 0:
        card = fight.read_card()

        if card == 0:
            fight.turn_next()
        elif card == -1:
            continue
        else:
            if not fight.is_master():
                cmp_result = fight.comp_card(fight.last_card(), card)
                if cmp_result > 0:
                    fight.set_master()
                    fight.in_queue(card)
                else:
                    print_encoding('你的牌太小了，重新出吧！')
            else:
                fight.in_queue(card)

    if fight.state() == 1:
        print_encoding('地主干翻农民啦')
    else:
        print_encoding('农民翻身做主啦')