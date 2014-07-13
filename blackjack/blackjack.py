import random
import sys
import time


class Hand(object):
    card_points = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
                   '7': 7, '8': 8, '9': 9, '10': 10, 
                   'J': 10, 'Q': 10, 'K': 10, 'A': 11}

    suits = {'s': u"\u2660",
             'h': u"\u2661",
             'd': u"\u2662",
             'c': u"\u2663"}

    def __init__(self):
        self.cards = []
        self.points = 0

    def add_card(self, card):
        self.cards.append(card)
        self.count_points()

    def count_points(self):
        self.points = sum([self.card_points[card[:-1]] for card in self.cards])

        # 'A's value adjusted from 11 to 1 if points > 21
        for card in self.cards:
            if 'A' in card and self.points > 21:
                self.points -= 10

    def show(self):
        hand_view = ''
        for card in self.cards:
            hand_view += '%s%s ' % (card[:-1], self.suits[card[-1]])
        return hand_view

    def show_first_card(self):
        card = self.cards[0]
        print "Dealer's card: %s%s" % (card[:-1], self.suits[card[-1]]),


class Deck(object):
    card_names = ['2', '3', '4', '5', '6', '7', '8',
                  '9', '10', 'J', 'Q', 'K', 'A']
    card_suits = ['s', 'h', 'd', 'c']

    def __init__(self, number_of_52card_decks=1):
        self.number_of_52card_decks = number_of_52card_decks
        self.shuffle()

    def initialize_deck(self):
        deck = []
        for name in self.card_names:
            for suit in self.card_suits:
                deck += [name + suit]
        return deck * self.number_of_52card_decks


    def shuffle(self):
        print "Shuffling the deck..."
        self.deck = self.initialize_deck()
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()


class Player(object):
    def __init__(self):
        self.hand = Hand()
        self.busted = False
        self.chips = 100
        self.bet = 0
        self.action = 'stand'

    def validate_bet(self, bet):
        try:            
            if int(bet) <= self.chips:
                self.bet = int(bet)
            else: 
                self.bet_input("(not enough chips)")
        except:
            self.bet_input("(number)")

    def bet_input(self, message=''):
        print chr(27) + "[2J"
        print "Chips left: ", self.chips
        print "--------------------------------"
        bet = raw_input("Your bet %s >>> " % message) # !!!! make safe
        self.validate_bet(bet)

    def show_hand(self):
        hand_view = self.hand.show()
        print "You: %s (%s points)" % \
                  (hand_view, self.hand.points)

    def check_hand(self):
        message = ''
        if self.hand.points < 21:
            self.action_input() 
        elif self.hand.points > 21:
            self.action = 'stand'
            self.busted = True
        else:
            self.action = 'stand'

    def action_input(self):
        action = raw_input("Your action: hit(h) / stand(s) >>> ")
        if action.lower() in ['h', 'hit']:
            self.action = 'hit'
        elif action.lower() in ['s', 'stand']:
            self.action = 'stand'
        else:
            self.action_input()

class Dealer(object):
    def __init__(self):
        self.hand = Hand()
        self.busted = False
        self.dealer_turn = False

    def show_hand(self):
        hand_view = self.hand.show()
        if self.dealer_turn:
            print "Dealer: %s (%s points)" % \
                  (hand_view, self.hand.points)
        else:
            print "Dealer: %s " % hand_view[:3]


class Game(object):
    def __init__(self):
        self.dealer = Dealer()
        self.player = Player()
        self.deck = Deck(number_of_52card_decks=2)
        self.player.bet_input()

    def play(self):
        while self.player.bet > 0:            
            self.first_hand()
            self.player_move()

            if not self.player.busted:
                self.dealer_move()

            self.determine_winner()
            self.continue_or_exit()

        print chr(27) + "[2J"
        print "Thanks for playing!\n"

    def first_hand(self):
        self.player.hand.add_card(self.deck.deal_card())
        self.player.hand.add_card(self.deck.deal_card())
        self.dealer.hand.add_card(self.deck.deal_card())
        self.dealer.hand.add_card(self.deck.deal_card())
        self.show_table()
    

    def show_table(self, message=''):
        print chr(27) + "[2J"
        self.player.show_hand()
        print ''
        self.dealer.show_hand()
        print '\n', message, '\n'
        print "Chips left: %d       " % (self.player.chips - self.player.bet),
        print "Your bet: %d" % self.player.bet
        print "--------------------------------"

    def player_move(self):
        self.player.check_hand()
        while self.player.action == 'hit':
            self.player.hand.add_card(self.deck.deal_card())
            self.show_table()
            self.player.check_hand()
            

    def dealer_move(self):
        self.show_table()
        time.sleep(1)
        self.dealer.dealer_turn = True
        self.show_table()
        while self.dealer.hand.points < 17 and not self.dealer.busted:
            time.sleep(1)
            self.dealer.hand.add_card(self.deck.deal_card())
            self.show_table()
            if self.dealer.hand.points > 21:
                self.dealer.busted = True

    def determine_winner(self):
        if self.player.busted or (not self.dealer.busted and\
                    self.player.hand.points <= self.dealer.hand.points):
            self.player.chips -= self.player.bet
            message = 'You lost!'
        else:
            self.player.chips += self.player.bet
            message = 'You won!'

        self.close_hand(message)

    def close_hand(self, message):
        self.player.bet = 0
        self.show_table(message)
        self.player.hand = Hand()
        self.dealer.hand = Hand()
        self.player.busted = False
        self.dealer.busted = False
        self.dealer.dealer_turn = False

    def continue_or_exit(self):
        if self.player.chips > 0:
            action = raw_input("Do you want to continue? (y/n) >> ") 
            if action in ['y', 'yes']:
                self.player.bet_input()
            elif action in ['n', 'no']:
                self.player.bet = 0
            else:
                self.continue_or_exit()
        else:
            time.sleep(2)


if __name__ == "__main__":
    blackjack = Game()
    blackjack.play()
