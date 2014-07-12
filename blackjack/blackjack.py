import random
import sys
import time


class Hand(object):
    def __init__(self):
        self.cards = []
        self.points = 0

    def add_card(self, card):
        self.cards.append(card)
        self.count_points()

    def count_points(self):
        card_points = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
                       '7': 7, '8': 8, '9': 9, '10': 10, 
                       'J': 10, 'Q': 10, 'K': 10, 'A': 11}

        self.points = sum([card_points[i] for i in self.cards])

        # 'A's value adjusted from 11 to 1 if points > 21
        for i in xrange(self.cards.count('A')):
            if self.points > 21:
                self.points -= 10



class Deck(object):
    def __init__(self, number_of_52card_decks=1):
        self.card_names = ['2', '3', '4', '5', '6', '7', '8',
                           '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = 4
        self.default_full_deck = self.card_names * self.suits * number_of_52card_decks
        self.cards = self.default_full_deck
        self.shuffle()

    def shuffle(self):
        print "Shuffling the deck..."
        self.deck = self.default_full_deck
        random.shuffle(self.deck)

    def deal_card(self):
        return self.cards.pop()


class Person(object):
    def __init__(self):
        self.hand = Hand()
        self.busted = False

    def deal_card(self, card):
        self.hand.add_card(card)
        self.show_hand()

    def deal_two_cards(self, deck):
        self.hand.add_card(deck.deal_card())
        self.hand.add_card(deck.deal_card())

    def show_hand(self):
        for card in self.hand.cards:
            print card, 
        print '\n'

    def close_hand(self):
        self.hand = Hand()
        self.busted = False


class Player(Person):
    def __init__(self):
        super(Player, self).__init__()
        self.chips = 100
        self.bet = 0

    def bet_or_exit(self, player_input):
        if player_input.isdigit():
            self.bet = self.validate_bet(int(player_input))
        else:
            self.bet = 0

    # check
    def validate_bet(self, bet): 
        if bet <= self.chips:
            return bet
        else:
            print "You don't have enough chips (%d)." % self.player.chips
            self.bet_or_exit(self.bet_input())

    def bet_input(self):
        return raw_input("Your bet (0 or other to leave the game) >>> ") # !!!! make safe

    def hit_or_stand(self):
        return raw_input("\nYour action: hit(h) / stand(s) >>> ")

    def action(self):
        if self.hand.points < 21:
            action = self.hit_or_stand()
        elif self.hand.points > 21:
            print "\nYou're busted"
            self.busted = True
            action = 'stand'
        else:
            print "\nYou've got BlackJack" # bj only 10+11
            action = 'stand'
        return action

    def move(self, action, deck):
        while action.lower() in ['h', 'hit']:
            self.hand.add_card(deck.deal_card())
            self.show_hand()
            action = self.action()

class Dealer(Person):

    def move(self, deck):
        print "Dealer's cards: "
        self.show_hand()
        while self.hand.points < 17 and not self.busted:
            self.hand.add_card(deck.deal_card())
            print "Dealer's cards: "
            self.show_hand()
            if self.hand.points > 21:
                self.busted = True
                self.hand.points = 0

    def show_first_card(self):
        print "Dealer's card: %s" % self.hand.cards[0]

class Game(object):
    def __init__(self):
        self.dealer = Dealer()
        self.player = Player()
        self.deck = Deck(number_of_52card_decks=2)
        self.player.bet_or_exit(self.player.bet_input())

    def play(self):
        while self.player.bet > 0:            
            action = self.first_hand()
            self.player.move(action, self.deck)

            if not self.player.busted:
                self.dealer.move(self.deck)

            self.hand_end()
            self.player.bet_or_exit(self.player.bet_input()) #clumsy

        print "Thanks for playing!"


    def first_hand(self):
        self.player.deal_two_cards(self.deck)
        self.player.show_hand()

        self.dealer.deal_two_cards(self.deck)
        self.dealer.show_first_card()

        return self.player.action()        


    def hand_end(self):
        if self.player.busted or self.player.hand.points <= self.dealer.hand.points:
            print '\nDealer wins'
            self.player.chips -= self.player.bet
        else:
            print '\nPlayer wins'
            self.player.chips += self.player.bet

        print "Chips left: ", self.player.chips
        print "--------------------------------"

        self.player.close_hand()
        self.dealer.close_hand()

if __name__ == "__main__":
    blackjack = Game()
    blackjack.play()
