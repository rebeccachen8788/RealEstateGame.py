# Author: Rebecca Chen
# GitHub username: rebeccachen8788
# Date: 5/23/2022
# Description: A simplified Monopoly game that will create a game-board based on a list of rent money, a go space
#              money, and will create a go space and 24 spaces in a circle. Individual players must be
#              created, with a minimum of 2 players in order to play. The go space will give money (but not when
#              players initially start on go, and players can move 1-6 spaces. Players can buy a space with their
#              money but must also pay rent if landing on unowned spaces. Passing by the go space will add money.
#              The game ends when only one player is left. Players lose by losing all of their account balance.

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
        for number in range(1, 25):
            rent = rent_money_list[number-1]
            self._spaces[number] = Spaces(number, rent)

    def create_player(self, unique_name, initial_balance):
        """
        Will take 2 parameters, the player's unique name and initial account balance and use that
        to create a Player object starting on the "GO" space with an initial account balance
        from "GO" space.
        """
        self._players[unique_name] = Player(unique_name, initial_balance)
        self._spaces[0].set_current_players(unique_name)
        self._players[unique_name].set_location(0)
        self._current_players.append(unique_name)

    def get_player_account_balance(self, unique_name):
        """
        Will take a player's unique name as a parameter and will return that player's account balance.
        """
        if unique_name in self._players:
            return self._players[unique_name].get_balance()

    def get_player_current_position(self, unique_name):
        """
        Will take a player's unique name as a parameter and will return that player's current position.
        """
        if unique_name in self._players:
            if self._players[unique_name].get_location() == 0:
                return 0
            else:
                return self._players[unique_name].get_location()

    def buy_space(self, unique_name):
        """
        Will take that player's unique name as a parameter and if that player's account balance is greater
        than the purchase price of the space they're on currently, and that space doesn't have an owner, they will
        buy that space. When the player buy's the space, the cost of the space will be deducted from the player's
        account balance. And if the player buys the space, the method returns True, otherwise it returns False."
        """
        current_space_name = self.get_player_current_position(unique_name)
        if current_space_name != 0 and self._spaces[current_space_name].get_owner() is None:
            # Checking if the space name is not the zero space, and that the space is free
            current_space_object = self._spaces[current_space_name]
            if self.get_player_account_balance(unique_name) > current_space_object.get_purchase_price():
                # Will buy space if account balance of buyer greater than space price
                purchase_price = current_space_object.get_purchase_price()
                reduce_account = (-1*purchase_price)
                self._players[unique_name].set_balance(reduce_account)
                self._players[unique_name].set_owned_spaces(current_space_name)
                current_space_object.set_owner(unique_name)
                return True
            else:  # If account balance, not greater than purchase cost, return False
                return False
        return False  # Return False is space name is 0.

    def move_player(self, unique_name, number_spaces):
        """
        Will take the player's unique name and the number of spaces to move as parameters. As long as the
        player's account balance is not equal to 0 (in which it will return nothing), then the player will move
        between spaces 1 to 6 inclusive across the board. If they land on or pass the "GO" space, they get the
        "GO" money. The player will pay rent if the space they landed on is owned by someone else
        and they cannot pay more rent than what they have to the owner of the space, and finally if balance after
        that interaction is 0, the player is done with the game and removed as the owner of any spaces. Otherwise,
        if the space is unowned, if the player has a greater amount of money than the space's purchase price they can
        buy the space and own it. If they have an equal or lesser amount of money than the unowned purchase
        price of the space, nothing will happen.
        """
        if self._players[unique_name].get_balance() == 0:  # If the balance of the player is zero, player can't move.
            return False
        current_index = self.get_player_current_position(unique_name)
        true_position = number_spaces + current_index
        if true_position <= 24:
            if true_position != 0:
                for x in range(number_spaces):
                    potential_go = current_index + x + 1
                    space_object = self._spaces[potential_go]
                    if potential_go == 0: # Checks if player passes 0 space, then they'll collect money
                        money_given = space_object.get_money_amount()
                        self._players[unique_name].set_balance(money_given)
            true_space_object = self._spaces[true_position]
            rent = true_space_object.get_rent()
            if true_position == 0:  # If they land on 0, collect money and update statuses.
                self._players[unique_name].set_location(true_position)
                self._spaces[true_position].set_current_players(unique_name)
                money = self._spaces[true_position].get_money_amount()
                self._players[unique_name].set_balance(money)
                return
            if true_space_object.get_owner() is None or true_space_object.get_owner() == unique_name:
                # If the land on an unowned space, just update location statuses.
                self._players[unique_name].set_location(true_position)
                self._spaces[true_position].set_current_players(unique_name)
                return
            if true_space_object.get_owner() != unique_name and true_space_object.get_owner() is not None:
                if rent >= self._players[unique_name].get_balance():
                    # If the rent cost of the space exceeds player balance, update player's balance to 0 and give
                    # the account balance of the player to the owner, and take the player out of the game and
                    # get rid of the spaces owned by the player.
                    owner = true_space_object.get_owner()
                    real_owner = self._players[owner]
                    rent_cost = self._spaces[true_position].get_rent()
                    rent_paid = self._players[unique_name].get_balance()
                    true_rent_paid = rent_cost - rent_paid
                    real_owner.set_balance(true_rent_paid)
                    self._players[unique_name].set_zero()
                    self._players[unique_name].clear_owned_spaces()
                    self._players[unique_name].set_location(true_position)
                    self._spaces[true_position].set_owner(None)
                    self._current_players.remove(unique_name)
                    return
                if rent < self._players[unique_name].get_balance():
                    # If players account balance exceeds rent, pay rent to owner
                    owner = true_space_object.get_owner()
                    real_owner = self._players[owner]
                    negate_rent = (-1*rent)
                    self._players[unique_name].set_balance(negate_rent)
                    self._players[unique_name].set_location(true_position)
                    self._spaces[true_position].set_current_players(unique_name)
                    rent_cost = self._spaces[true_position].get_rent()
                    real_owner.set_balance(rent_cost)
                    return
        if true_position >= 25:
            new_position = true_position - 25
            if new_position != 0:
                for x in range(number_spaces):
                    if x + current_index + 1 == 26:  # If passing by 0, collect money
                        space_object = self._spaces[0]
                        money_given = space_object.get_money_amount()
                        self._players[unique_name].set_balance(money_given)
            true_space_object = self._spaces[new_position]
            rent = true_space_object.get_rent()
            if new_position == 0:  # If landing position is 0, increase money
                self._players[unique_name].set_location(new_position)
                self._spaces[new_position].set_current_players(unique_name)
                money = self._spaces[new_position].get_money_amount()
                self._players[unique_name].set_balance(money)
                return
            if true_space_object.get_owner() is None or true_space_object.get_owner() == unique_name:
                # If landing on unowned space, update location statuses
                self._players[unique_name].set_location(new_position)
                self._spaces[new_position].set_current_players(unique_name)
                return
            if true_space_object.get_owner() != unique_name and true_space_object.get_owner() is not None:
                if rent >= self._players[unique_name].get_balance():
                    # If rent exceeds player account balance, pay up money to owner, set player balance to
                    # 0, remove player from game and refund owned properties.
                    owner = true_space_object.get_owner()
                    real_owner = self._players[owner]
                    rent_cost = self._spaces[new_position].get_rent()
                    rent_paid = self._players[unique_name].get_balance()
                    true_rent_paid = rent_cost - rent_paid
                    real_owner.set_balance(true_rent_paid)
                    self._players[unique_name].set_zero()
                    self._players[unique_name].clear_owned_spaces()
                    self._players[unique_name].set_location(new_position)
                    self._spaces[new_position].set_current_players(unique_name)
                    self._spaces[new_position].set_owner(None)
                    self._current_players.remove(unique_name)
                    return
                if rent < self._players[unique_name].get_balance():
                    # If player money exceeds rent, pay up money to owner and update statuses.
                    owner = true_space_object.get_owner()
                    real_owner = self._players[owner]
                    negate_rent = (-1*rent)
                    self._players[unique_name].set_balance(negate_rent)
                    self._players[unique_name].set_location(new_position)
                    self._spaces[new_position].set_current_players(unique_name)
                    rent_cost = self._spaces[new_position].get_rent()
                    real_owner.set_balance(rent_cost)
                    return

    def check_game_over(self):
        """
        Will take no parameters and return the winning player's name if all but one player has an account balance
        of 0. Otherwise, will return empty string.
        """
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
        """
        Will take the space name and money amount as parameters and create a Spaces object with initialized
        private data members such as a space name, money amount(for the "GO" space) or money amount
        (for the rent on the other 24 spaces), purchase price, the owner of the space,
        and current players on the space.
        """
        self._space_name = space_name
        self._money_amount = money_amount
        self._rent = money_amount
        self._purchase_price = (money_amount * 5)
        self._owner = None
        self._current_players = []

    def get_space_name(self):
        """
        Will return the name of the space
        """
        return self._space_name

    def get_rent(self):
        """
        Will return the rent price of the space, if not the "GO" space.
        """
        if self._space_name != 0:
            self._money_amount = 0
            return self._rent

    def get_money_amount(self):
        """
        Will return the money amount the space gives the player if the space is a "GO" space.
        """
        if self._space_name == 0:
            return self._money_amount

    def get_purchase_price(self):
        """
        Will return the purchase price of the space if the space is not a "GO" space.
        """
        return self._purchase_price

    def get_owner(self):
        """
        Will return the owner of a space, if the space is not a "GO" space."
        """
        return self._owner

    def get_current_players(self):
        """
        Will return the current players who are on the space.
        """
        return self._current_players

    def set_owner(self, player_name):
        """
        Will take the player name as the parameter and
        set the owner of the space if the player on the space buys the space and the space
        does not currently have a owner.
        """
        if self._owner is None:
            self._owner = player_name

    def set_current_players(self, player_name):
        """
        Will take the player name as the parameter and set who the current players are on that space.
        """
        self._current_players.append(player_name)

    def remove_current_players(self, player_name):
        """
        Will take the player name as the parameter removes the player from the game.
        """
        self._current_players.remove(player_name)


class Player:
    """
    Will create a Player object which will hold a unique player name, player account balance,
    player location, and player owned spaces.
    """

    def __init__(self, unique_name, initial_balance):
        """
        Will use the unique name and initial balance as the parameters and
        create a Player object with initialized private data members
        such as a player name, account balance, owned spaces, and current location.
        """
        self._unique_name = unique_name
        self._balance = initial_balance
        self._owned_spaces = []
        self._location = 0

    def get_unique_name(self):
        """
        Will return the player name.
        """
        return self._unique_name

    def get_balance(self):
        """
        Will return the player's account balance.
        """
        return self._balance

    def set_balance(self, money):
        """
        Will use the money amount as the parameter and set
        the player's account balance depending on if they are paying rent, if they are buying a space,
        if they are receiving rent from another player, or if they landed on or passed a "GO" space.
        """
        self._balance += money

    def get_owned_spaces(self):
        """
        Will return the spaces the player owns.
        """
        return self._owned_spaces

    def set_owned_spaces(self, space_name):
        """
        Will add a space to the player's owned spaces.
        """
        self._owned_spaces.append(space_name)

    def clear_owned_spaces(self):
        """
        Clears out owned spaces if player lost game.
        """
        self._owned_spaces.clear()

    def get_location(self):
        """
        Will return the current location the player is at (space-wise).
        """
        return self._location

    def set_location(self, space_name):
        """
        Will take the space name as the parameter and set the location of the player.
        """
        self._location = space_name

    def set_zero(self):
        """
        Set's balance to zero.
        """
        self._balance = 0


# if __name__ == '__main__':
#     game = RealEstateGame()
#
#     rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350, 350, 350]
#     game.create_spaces(50, rents)
#
#     game.create_player("Player 1", 1000)
#     game.create_player("Player 2", 1000)
#     game.create_player("Player 3", 1000)
#
#     game.move_player("Player 1", 6)
#     game.buy_space("Player 1")
#     game.move_player("Player 2", 6)
#
#     print(game.get_player_account_balance("Player 1"))
#     print(game.get_player_account_balance("Player 2"))
#     print(game.get_player_account_balance("Player 3"))
#
#     game.move_player("Player 3", 6)
#     game.move_player("Player 2", 6)
#
#     print(game.get_player_account_balance("Player 1"))
#     print(game.get_player_account_balance("Player 2"))
#     print(game.get_player_account_balance("Player 3"))
#
#     game.buy_space("Player 2")
#
#     print(game.get_player_account_balance("Player 2"))
#
#     game.move_player("Player 3", 6)
#
#     print(game.get_player_account_balance("Player 2"))
#     print(game.get_player_account_balance("Player 3"))
#
#     game.move_player("Player 3", 6)
#     game.move_player("Player 3", 6)
#     game.move_player("Player 3", 1)
#
#     print(game.get_player_account_balance("Player 3"))
#
#     game.move_player("Player 3", 6)
#
#     print(game.get_player_account_balance("Player 3"))
#
#     print(game.check_game_over())
