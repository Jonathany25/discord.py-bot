from random import shuffle


class Card(object):
    SUITS = {"Spades": 4,
             "Hearts": 3,
             "Clubs": 2,
             "Diamonds": 1}
    RANKS = [number for number in range(2, 14 + 1)]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        if self.rank == 14:
            rank = "Ace"
        elif self.rank == 13:
            rank = "King"
        elif self.rank == 12:
            rank = "Queen"
        elif self.rank == 11:
            rank = "Jack"
        else:
            rank = self.rank
        return f"{rank} of {self.suit}"

    def __gt__(self, other):
        if self.rank == other.rank:
            return Card.SUITS.get(self.suit) > Card.SUITS.get(other.suit)
        else:
            return self.rank > other.rank


class Deck(object):
    def __init__(self):
        self.deck = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self):
        shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def deal(self):
        if len(self) == 0:
            return None
        else:
            return self.deck.pop(0)


class Capsa():
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        number_of_cards = 13
        number_of_players = 4

        for i in range(number_of_players):
            hand = []
            for j in range(number_of_cards):
                hand.append(self.deck.deal())
            self.hands.append(hand)

    def play(self):
        pass
