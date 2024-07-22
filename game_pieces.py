from termcolor import colored
import random

from helpers import get_move, inty



class mine:
    def __init__(self, value, neighbors):
        self.value = value
        self.neighbors = neighbors
        self.occupancy = 'white'
        self.visited = 0
        self.liberties = 0
        self.temp_dead = 0


class board:
    """
            0 1 2
            3 4 5
            6 7 8
    """
    def __init__(self):
        self.mines = []
        self.deck = []
        self.discard = []

    def build_mines(self):
        self.mines.append(mine(6, [4]))
        self.mines.append(mine(3, [2, 5]))
        self.mines.append(mine(4, [1, 5]))
        self.mines.append(mine(3, [6, 7]))
        self.mines.append(mine(1, [0, 5, 7, 8]))
        self.mines.append(mine(2, [1, 2, 4, 8]))
        self.mines.append(mine(4, [3, 7]))
        self.mines.append(mine(2, [3, 4, 6, 8]))
        self.mines.append(mine(3, [4, 5, 7]))

    def build_deck(self):
        for i in range(0,5):
            self.deck.append('MR')
        for i in range(0,4):
            self.deck.append('Exc')
        for i in range(0,2):
            self.deck.append('RM')
        for i in range(0,2):
            self.deck.append('FG')
        self.deck.append('CC')
        self.deck.append('D')
        self.deck.append('+3')
        self.deck.append('+2')
        self.deck.append('+1')
        self.deck.append('-1')

    def deal(self):
        if len(self.deck) == 0:
            self.deck = self.discard
        random.shuffle(self.deck)
        hand1 = []
        hand2 = []
        for i in range(0,3):
            hand1.append(self.deck.pop(0))
        for i in range(0,3):
            hand2.append(self.deck.pop(0))

        return [hand1, hand2]



    def reset_visit(self):
        for mine in self.mines:
            mine.visited = 0

    def reset_temp(self):
        for mine in self.mines:
            mine.temp_dead = 0

    def empty_adj(self, index):
        libs = 0
        for neighb in self.mines[index].neighbors:
            if self.mines[neighb].occupancy == 'white':
                libs += 1
        return libs

    def check_life(self, index, player):
        libs = -1
        self.mines[index].visited = 1
        if self.mines[index].occupancy == player:
            self.mines[index].visited = 1
            libs = self.empty_adj(index)
            for neighb in self.mines[index].neighbors:
                if self.mines[neighb].occupancy == player and self.mines[neighb].visited == 0:
                    libs += self.check_life(neighb, player)

        return libs

    def update_board(self, player):
        for i in range(0,9):
            self.reset_visit()
            if self.check_life(i, player) == 0:
                self.mines[i].temp_dead = 1
        for i in range(0,9):
            if self.mines[i].temp_dead == 1:
                self.mines[i].occupancy = 'white'


    def show_board(self):
        row1 = colored(self.mines[0].value, self.mines[0].occupancy) + colored(self.mines[1].value, self.mines[1].occupancy) + colored(self.mines[2].value, self.mines[2].occupancy)
        row2 = colored(self.mines[3].value, self.mines[3].occupancy) + colored(self.mines[4].value, self.mines[4].occupancy) + colored(self.mines[5].value, self.mines[5].occupancy)
        row3 = colored(self.mines[6].value, self.mines[6].occupancy) + colored(self.mines[7].value, self.mines[7].occupancy) + colored(self.mines[8].value, self.mines[8].occupancy)
        print('')
        print(row1)
        print(row2)
        print(row3)

class Player:
    def __init__(self, color, humanity):
        self.humanity = humanity
        self.coins = 10
        self.miners = 2
        self.board_miners = 0
        self.points = 0
        self.debts = 0
        self.fgs = 0
        self.hand = []
        self.color = color

    def place_miner(self, board, selection):
        if self.miners > 0:
            board.mines[selection].occupancy = self.color



class Game:
    def __init__(self, players):
        self.players = [Player('green', players[0]), Player('blue', players[1])]
        self.board = board()
        self.map = {0: 'Green', 1: 'Blue'}
        self.turn = 1

    def show_stats(self):
        print('')
        print("Green hand:" + str(self.players[0].hand))
        print("Green has %d points, %d miners, %d coins, %d fool's golds, and %d debt" % (self.players[0].points, self.players[0].miners, self.players[0].coins, self.players[0].fgs, self.players[0].debts))
        print('')
        print("Blue hand:" + str(self.players[1].hand))
        print("Blue has %d points, %d miners, %d coins, %d fool's gold, and %d debt" % (self.players[1].points, self.players[1].miners, self.players[1].coins, self.players[1].fgs, self.players[1].debts))
        print('')

    def mining_rights(self, player):
        if player == 0:
            move = inty(raw_input("Where do you play, Green? "), )
        else:
            move = inty(raw_input("Where do you play, Blue? "))
        if move in range(0,8):
            if self.board.mines[move].occupancy == 'white':
                self.players[player].place_miner(self.board, move)
                if player == 0:
                    self.board.update_board('blue')
                    self.board.update_board('green')
                else:
                    self.board.update_board('green')
                    self.board.update_board('blue')
                self.players[player].miners -= 1
                self.players[player].board_miners += 1

    def gain_points(self, player, card):
        if card[0] == '+':
            if self.players[player].debts <= self.players[1-player].debts:
                self.players[player].points += int(card[1])
        else:
            self.players[player].points = max(0, self.players[player].points - 1)

    def excavate(self):
        green_loot = 0
        blue_loot = 0
        for mine in self.board.mines:
            if mine.occupancy == 'green':
                green_loot += mine.value
            if mine.occupancy == 'blue':
                blue_loot += mine.value
        self.players[0].coins += green_loot
        self.players[1].coins += blue_loot

    def con_col(self, player):
        if player == 0 and self.players[1].board_miners > 0:
            removal = inty(raw_input("Which miner do you remove, Green? "))
            if removal in range(0, 8):
                if self.board.mines[removal].occupancy == 'blue':
                    self.players[1].board_miners -= 1
                    self.board.mines[removal].occupancy = 'white'

        if player == 1 and  self.players[0].board_miners > 0:
            removal = inty(raw_input("Which miner do you remove, Blue?"))
            if removal in range(0, 8):
                if self.board.mines[removal].occupancy == 'green':
                    self.players[0].board_miners -= 1
                    self.board.mines[removal].occupancy = 'white'

    def win_card(self, card, player, bid):
        self.players[player].coins -= bid
        while self.players[player].coins < 0 and self.players[player].debts < 4:
            self.players[player].coins += 10
            self.players[player].debts += 1
        self.players[player].coins = max(0,self.players[player].coins) 
        if card == 'Exc':
            self.excavate()
        if card == 'FG':
            self.players[player].fgs += 1
        if card == 'RM':
            if self.players[player].miners + self.players[player].board_miners < 4:
                self.players[player].miners += 1
        if card == 'CC':
            self.con_col(player)
        if card == 'D':
            self.players[1-player].points = max(0, self.players[1-player].points - 1)
        if card in ['+3','+2','+1','-1']:
            self.gain_points(player, card)
        if card == 'MR':
            if self.players[player].miners > 0:
                self.mining_rights(player)

    def fgs_sequence(self, bid, winner):
        bonus = 0
        if self.players[1-winner].fgs > 0 and bid > 0:
            bonus = inty(raw_input("How many fool's golds do you play, %s? " % (self.map[1-winner])))
            if bonus in range(1,3) and bonus <= self.players[1-winner].fgs:
                self.players[1-winner].fgs -= bonus
                self.board.discard.append('FG')
        if self.players[winner].fgs > 0 and bid < 0:
            bonus = inty(raw_input("How many fool's golds do you play, %s? " % (self.map[winner])))
            if bonus in range(1,3) and bonus <= self.players[winner].fgs:
                self.players[winner].fgs -= bonus
                self.board.discard.append('FG')
        return 1+bonus

    def play_card(self, card, turn):
        if turn == 1:
            player = 0
        else:
            player = 1
        if self.players[player].hand[card] != 'FG':
            self.board.discard.append(self.players[player].hand.pop(card))
        else:
            self.players[player].hand.pop(card)
        if len(self.board.deck)>0:
            self.players[player].hand.append(self.board.deck.pop(0))

        if len(self.players[0].hand) == 0 and len(self.players[1].hand) == 0:
            hands = self.board.deal()
            self.players[0].points += 1
            self.players[1].points += 1
            self.players[0].hand = hands[0]
            self.players[1].hand = hands[1]


    def run(self):
        self.board.build_mines()
        self.board.build_deck()
        hands = self.board.deal()


        self.players[0].hand = hands[0]
        self.players[1].hand = hands[1]
        turn = 1
        while self.players[0].points < 7 and self.players[1].points < 7:
            self.board.show_board()
            self.board.reset_temp()
            self.show_stats()

            if turn == 1:
                if self.players[0].debts > 0 and self.players[0].coins > 10:
                    payoff = inty(raw_input("Do you pay off a debt, Green? "))
                    if payoff == 1:
                        self.players[0].debts -= 1
                        self.players[0].coins -= 11
                card = -1
                while card not in range(0, len(self.players[0].hand)):
                    card = inty(raw_input("What card do you play, Green? "))
                if self.players[0].hand[card] != 'Exc':
                    bluebid, greenbid = -11, -11
                    while greenbid not in range(-10, self.players[0].coins+11):
                        greenbid = inty(raw_input("What's your bid, Green? "))
                    while bluebid not in range(-10, self.players[1].coins+11):
                        bluebid = inty(raw_input("What's your bid, Blue? "))
                    if bluebid > greenbid:
                        multi = self.fgs_sequence(bluebid, 1)
                        self.win_card(self.players[0].hand[card], 1, bluebid*multi)
                    else:
                        multi = self.fgs_sequence(greenbid, 0)
                        self.win_card(self.players[0].hand[card], 0, greenbid*multi)
                else:
                    self.win_card('Exc', 1, 0)

            if turn == -1:
                if self.players[0].debts > 0 and self.players[0].coins > 10:
                    payoff = inty(raw_input("Do you pay off a debt, Blue? "))
                    if payoff == 1:
                        self.players[0].debts -= 1
                        self.players[0].coins -= 11
                card = -1
                while card not in range(0, len(self.players[1].hand)):
                    card = inty(raw_input("What card do you play, Blue? "))
                if self.players[1].hand[card] != 'Exc':
                    bluebid, greenbid = -11, -11
                    while bluebid not in range(-10, self.players[1].coins+10):
                        bluebid = inty(raw_input("What's' your bid, Blue? "))
                    while greenbid not in range(-10, self.players[0].coins+10):
                        greenbid = inty(raw_input("What's your bid, Green? "))
                    if greenbid > bluebid:
                        multi = self.fgs_sequence(greenbid, 0)
                        self.win_card(self.players[1].hand[card], 0, greenbid*multi)
                    else:
                        multi = self.fgs_sequence(bluebid, 1)
                        self.win_card(self.players[1].hand[card], 1, bluebid*multi)
                else:
                    self.win_card('Exc', 1, 0)

            self.play_card(card, turn)
            turn *= -1

        green_score = (self.players[0].points * 1000) - (self.players[0].debts * 100) + self.players[0].coins
        blue_score = (self.players[1].points * 1000) - (self.players[1].debts * 100) + self.players[1].coins
        if green_score > blue_score:
            print("Green wins!")
            print("Green: %d, Blue: %d" % (self.players[0].points, self.players[1].points))
        elif blue_score>green_score:
            print("Blue wins!")
            print("Blue: %d, Green: %d" % (self.players[0].points, self.players[1].points))
        else:
            print("It's a draw!")
            print("Green: 7, Blue: 7")


if raw_input("Is P1 human? ") in ['Y', 'y', 'yes', 'Yes']:
    player1 = 0
else:
    player1 = 1
if raw_input("Is P2 human? ") in ['Y', 'y', 'yes', 'Yes']:
    player2 = 0
else:
    player2 = 1
coloma = Game([player1, player2])
coloma.run()





