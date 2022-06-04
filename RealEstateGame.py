# Author: Rebecca Chen
# GitHub username: rebeccachen8788
# Date: 5/23/2022
# Description: A

class RealEstateGame:
    """
    Will create a simplified version of Monopoly with 2 or more players.
    """

    def __init__(self):
        """
        Will create a RealEstateGame object.
        """
        self._spaces = {}
        self._players = {}
        self._current_players = []

    def create_spaces(self, go_money, rent_money_list):
        """
        Will take 2 parameters, the amount of money given to players when they land on the go space,
        and an array of 24 integers(varying rent amounts for 24 spaces besides GO).
        """
        if 0 not in self._spaces:
            self._spaces[0] = Spaces(0, go_money)
        for number in range(24):
            for rent in rent_money_list:
                real_space = number + 1
                self._spaces[real_space] = Spaces(real_space, rent)

    def create_player(self, unique_name, initial_balance):
        self._players[unique_name] = Player(unique_name, initial_balance)
        self._spaces[0].set_current_players(unique_name)
        self._players[unique_name].set_location(0)
        self._current_players.append(unique_name)

    def get_player_account_balance(self, unique_name):
        if unique_name in self._players:
            return self._players[unique_name].get_balance()

    def get_player_current_position(self, unique_name):
        if unique_name in self._players:
            if self._players[unique_name].get_location() == 0:
                return 0
            else:
                return self._players[unique_name].get_location()

    def buy_space(self, unique_name):
        current_space_name = self.get_player_current_position(unique_name)
        if current_space_name != 0 and self._spaces[current_space_name].get_owner() is None:
            current_space_object = self._spaces[current_space_name]
            if self.get_player_account_balance(unique_name) > current_space_object.get_purchase_price():
                purchase_price = current_space_object.get_purchase_price()
                reduce_account = -1*purchase_price
                self._players[unique_name].set_balance(reduce_account)
                self._players[unique_name].set_owned_spaces(current_space_name)
                current_space_object.set_owner(unique_name)
                return True
            else:
                return False
        return False

    def move_player(self, unique_name, number_spaces):
        owner = self._players[unique_name]
        if self._players[unique_name].get_balance == 0:
            return
        current_index = self.get_player_current_position(unique_name)
        true_position = number_spaces + current_index
        if true_position <= 25:
            if true_position != 0:
                for x in range(number_spaces):
                    potential_go = current_index + x + 1
                    space_object = self._spaces[potential_go]
                    if potential_go == 0:
                        money_given = space_object.get_money_amount()
                        self._players[unique_name].set_balance(money_given)
            true_space_object = self._spaces[true_position]
            rent = true_space_object.get_rent()
            if true_position == 0:
                self._players[unique_name].set_location(true_position)
                self._spaces[true_position].set_current_players(unique_name)
                money = self._spaces[true_position].get_money_amount()
                self._players[unique_name].set_balance(money)
                return
            if true_space_object.get_owner() is None or true_space_object.get_owner() == unique_name:
                self._players[unique_name].set_location(true_position)
                self._spaces[true_position].set_current_players(unique_name)
                return
            if true_space_object.get_owner() != unique_name and not None:
                if rent >= self._players[unique_name].get_balance():
                    rent_cost = self._spaces[true_position].get_rent()
                    rent_paid = self._players[unique_name].get_balance()
                    true_rent_paid = rent_cost - rent_paid
                    owner.set_balance(true_rent_paid)
                    self._players[unique_name].set_zero()
                    self._players[unique_name].clear_owned_spaces()
                    self._players[unique_name].set_location(true_position)
                    self._current_players.remove(unique_name)
                    return
                if rent < self._players[unique_name].get_balance():
                    negate_rent = -1*rent
                    self._players[unique_name].set_balance(negate_rent)
                    self._players[unique_name].set_location(true_position)
                    self._spaces[true_position].set_current_players(unique_name)
                    rent_cost = self._spaces[true_position].get_rent()
                    owner.set_balance(rent_cost)
                    return
        if true_position > 25:
            new_position = true_position - 25 - 1
            if new_position != 0:
                for x in range(number_spaces):
                    if x + current_index + 1 == 26:
                        space_object = self._spaces[0]
                        money_given = space_object.get_money_amount()
                        self._players[unique_name].set_balance(money_given)
            true_space_object = self._spaces[new_position]
            rent = true_space_object.get_rent()
            if new_position == 0:
                self._players[unique_name].set_location(new_position)
                self._spaces[new_position].set_current_players(unique_name)
                money = self._spaces[new_position].get_money_amount()
                self._players[unique_name].set_balance(money)
                return
            if true_space_object.get_owner() is None or true_space_object.get_owner() == unique_name:
                self._players[unique_name].set_location(new_position)
                self._spaces[new_position].set_current_players(unique_name)
                return
            if true_space_object.get_owner() != unique_name and not None:
                if rent >= self._players[unique_name].get_balance():
                    rent_cost = self._spaces[new_position].get_rent()
                    rent_paid = self._players[unique_name].get_balance()
                    true_rent_paid = rent_cost - rent_paid
                    owner.set_balance(true_rent_paid)
                    self._players[unique_name].set_zero()
                    self._players[unique_name].clear_owned_spaces()
                    self._players[unique_name].set_location(new_position)
                    self._spaces[new_position].set_current_players(unique_name)
                    self._current_players.remove(unique_name)
                    return
                if rent < self._players[unique_name].get_balance():
                    negate_rent = -1*rent
                    self._players[unique_name].set_balance(negate_rent)
                    self._players[unique_name].set_location(new_position)
                    self._spaces[new_position].set_current_players(unique_name)
                    rent_cost = self._spaces[new_position].get_rent()
                    owner.set_balance(rent_cost)
                    return

    def check_game_over(self):
        if len(self._current_players) == 1:
            return self._current_players[0]
        else:
            return ""


class Spaces:
    """
    Will create a Spaces object which will have rent money for each space object, except GO,
    and a purchase price equivalent to 5 times the amount of rent money, and an owner.
    """

    def __init__(self, space_name, money_amount):
        self._space_name = space_name
        self._money_amount = money_amount
        self._rent = 0
        self._purchase_price = 0
        self._owner = None
        self._current_players = []

    def get_space_name(self):
        return self._space_name

    def get_rent(self):
        if self._space_name != 0:
            self._rent = self._money_amount
            self._money_amount = 0
            return self._rent

    def get_money_amount(self):
        if self._space_name == 0:
            return self._money_amount

    def get_purchase_price(self):
        if self._space_name != 0:
            self._purchase_price = (self._money_amount * 5)
            return self._purchase_price

    def get_owner(self):
        return self._owner

    def get_current_players(self):
        return self._current_players

    def set_owner(self, player_name):
        if self._owner is None:
            self._owner = player_name

    def set_current_players(self, player_name):
        self._current_players.append(player_name)

    def remove_current_players(self, player_name):
        self._current_players.remove(player_name)


class Player:
    """
    Will create a Player object which will hold a unique player name, player account balance,
    player location, and player owned spaces.
    """

    def __init__(self, unique_name, initial_balance):
        self._unique_name = unique_name
        self._balance = initial_balance
        self._owned_spaces = []
        self._location = 0

    def get_unique_name(self):
        return self._unique_name

    def get_balance(self):
        return self._balance

    def set_balance(self, money):
        self._balance += money

    def get_owned_spaces(self):
        return self._owned_spaces

    def set_owned_spaces(self, space_name):
        self._owned_spaces.append(space_name)

    def clear_owned_spaces(self):
        self._owned_spaces.clear()

    def get_location(self):
        return self._location

    def set_location(self, space_name):
        self._location = space_name

    def set_zero(self):
        self._balance = 0


if __name__ == '__main__':
    game = RealEstateGame()

    rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350, 350, 350]
    game.create_spaces(50, rents)

    game.create_player("Player 1", 1000)
    game.create_player("Player 2", 1000)
    game.create_player("Player 3", 1000)

    game.move_player("Player 1", 6)
    game.buy_space("Player 1")
    game.move_player("Player 2", 6)

    print(game.get_player_account_balance("Player 1"))
    print(game.get_player_account_balance("Player 2"))

    print(game.check_game_over())
