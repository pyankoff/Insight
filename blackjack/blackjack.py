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
        return hand_view, self.points

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


class Person(object):
    def __init__(self):
        self.hand = Hand()
        self.busted = False

    def deal_card(self, card):
        self.hand.add_card(card)
        self.hand.show()

    def deal_two_cards(self, deck):
        self.hand.add_card(deck.deal_card())
        self.hand.add_card(deck.deal_card())

    def close_hand(self):
        self.hand = Hand()
        self.busted = False


class Player(Person):
    def __init__(self):
        super(Player, self).__init__()
        self.chips = 100
        self.bet = 0
        self.action = 'stand'
    
    # check
    def validate_bet(self, bet): 
        if bet <= self.chips:
            return bet
        else: 
            return self.bet_input("(not enough chips)")

    def bet_input(self, message=''):
        print chr(27) + "[2J"
        print "Chips left: ", self.chips
        print "--------------------------------"
        bet = raw_input("Your bet%s >>> " % message) # !!!! make safe
        self.bet = self.validate_bet(bet)
        return self.bet

    def check_hand(self):
        if self.hand.points < 21:
            self.action = raw_input("Your action: hit(h) / stand(s) >>> ")
            message = ''
        elif self.hand.points > 21:
            self.action = 'stand'
            message = "You're busted"
            self.busted = True
        else:
            self.action = 'stand'
            message = "You've got BlackJack" # bj only 10+11
        return message

class Dealer(Person):
    pass



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

            self.hand_end()
            self.continue_or_exit()

        print "Thanks for playing!"

    def first_hand(self):
        self.player.deal_two_cards(self.deck)
        self.dealer.deal_two_cards(self.deck)
        self.show_table()
    

    def show_table(self, message=''):
        print chr(27) + "[2J"
        print "Your cards: %s (%s points)" % self.player.hand.show() 
        print ''
        print "Dealer cards: %s (%s points)" % self.dealer.hand.show()
        print '\n', message, '\n'
        print "Chips left: ", self.player.chips
        print "--------------------------------"

    def player_move(self):
        self.player.check_hand()
        while self.player.action.lower() in ['h', 'hit']:
            self.player.hand.add_card(self.deck.deal_card())
            self.show_table()
            message = self.player.check_hand()
            

    def dealer_move(self):
        self.show_table()
        while self.dealer.hand.points < 17 and not self.dealer.busted:
            self.dealer.hand.add_card(self.deck.deal_card())
            self.show_table()
            if self.dealer.hand.points > 21:
                self.dealer.busted = True

    def hand_end(self):
        if self.player.busted or (not self.dealer.busted and\
                    self.player.hand.points <= self.dealer.hand.points):
            self.player.chips -= self.player.bet
            self.show_table('You lost!')
        else:
            self.player.chips += self.player.bet
            self.show_table('You won!')

        self.player.close_hand()
        self.dealer.close_hand()

    def continue_or_exit(self):
        if raw_input("Do you want to continue? (y/n) >> ") in ['y', 'yes']:
            self.player.bet_or_exit(self.player.bet_input()) #clumsy
        else:
            self.player.bet = 0


if __name__ == "__main__":
    blackjack = Game()
    blackjack.play()
