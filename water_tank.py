# TODO: Students, fill out statement of work header
# Student Name in Canvas: Cheng Erxi
# Penn ID: 62196105
# Did you do this homework on your own (yes / no): yes
# Resources used outside course materials: none

# import statements
from random import shuffle
import random
# TODO: Write the functions as described in the instructions
def get_user_input(question):
    """
    Prompt the user with the given question and process the input.
    
    Parameters:
    - question (str): The question or prompt to show to the user.
    
    Returns:
    - int: if the input is a number.
    - str: if the input is a power card (uppercase) or any other string (lowercase).
    """
    while True:  # Keep asking until valid input is provided
        user_input = input(question).strip()  # Prompt user and strip whitespaces
        
        if len(user_input) == 0:  # If input is empty, reprompt
            continue
        
        # Check if the input is a number
        if user_input.isdigit():
            return int(user_input)  # Cast to integer and return
        
        # Check if the input is a power card
        power_cards = ["SOH", "DOT", "DMT"]
        if user_input.upper() in power_cards:
            return user_input.upper()  # Return the power card in uppercase
        
        # If the input is any other string
        return user_input.lower()  # Return the string in lowercase

def setup_water_cards():
    """
    Creates a shuffled list of water cards with specific values and quantities.
    
    Returns:
    - list[int]: A shuffled list of water card values.
    """
    # Define the values and their quantities
    water_values = {
        1: 30,
        5: 15,
        10: 8
    }
    
    # Create a list based on the quantities
    water_cards = [value for value, quantity in water_values.items() for _ in range(quantity)]
    
    # Shuffle the cards
    shuffle(water_cards)
    
    return water_cards

def setup_power_cards():
    """
    Creates a shuffled list of power cards with specific values and quantities.
    
    Returns:
    - list[str]: A shuffled list of power card strings.
    """
    # Define the power card values and their quantities
    power_values = {
        'SOH': 10,  # Steal half opponent's tank value
        'DOT': 2,   # Drain opponent's tank
        'DMT': 3    # Double my tank's value
    }
    
    # Create a list based on the quantities
    power_cards = [value for value, quantity in power_values.items() for _ in range(quantity)]
    
    # Shuffle the cards
    shuffle(power_cards)
    
    return power_cards

def setup_cards():
    """
    Sets up both water card and power card piles.
    
    Returns:
    - tuple[list, list]: A tuple containing the water cards pile and the power cards pile.
    """
    water_cards = setup_water_cards()
    power_cards = setup_power_cards()
    
    return water_cards, power_cards

def get_card_from_pile(pile, index):
    """
    Removes and returns the entry at the specified index of the given pile (water or power).
    
    Parameters:
    - pile (list): The pile (water or power) from which the card needs to be retrieved.
    - index (int): The index from which the card should be retrieved.
    
    Returns:
    - The card from the specified index.
    """
    return pile.pop(index)

def arrange_cards(cards_list):
    """
    Arrange the player's cards with the following specifications:
    - The first three indices are water cards, sorted in ascending order.
    - The last two indices are power cards, sorted in alphabetical order.
    
    Parameters:
    - cards_list (list): The list of player's cards containing a mix of water and power cards.
    
    Note:
    This function modifies the original list in place and doesn't return anything.
    """

    # Separate the cards into water cards and power cards
    water_cards = sorted([card for card in cards_list if isinstance(card, int)])
    power_cards = sorted([card for card in cards_list if isinstance(card, str)])
    
    # Update the original cards_list
    cards_list.clear()
    cards_list.extend(water_cards[:3])
    cards_list.extend(power_cards[:2])

def deal_cards(water_cards_pile, power_cards_pile):
    """
    Deal cards to player 1 and player 2. Each player would get 3 water cards and 2 power cards.
    After dealing, arrange the cards using the arrange_cards function.
    
    Parameters:
    - water_cards_pile (list): The pile of water cards.
    - power_cards_pile (list): The pile of power cards.

    Returns:
    tuple: A 2-tuple containing the cards of player 1 and player 2, respectively.
    """

    player_1_cards = []
    player_2_cards = []

    # Dealing water cards
    for _ in range(3):
        player_1_cards.append(water_cards_pile.pop(0))
        player_2_cards.append(water_cards_pile.pop(0))

    # Dealing power cards
    for _ in range(2):
        player_1_cards.append(power_cards_pile.pop(0))
        player_2_cards.append(power_cards_pile.pop(0))

    # Arranging the cards
    arrange_cards(player_1_cards)
    arrange_cards(player_2_cards)

    return player_1_cards, player_2_cards

def apply_overflow(tank_level):
    """
    Apply the overflow rule to the tank level if necessary.
    
    Parameters:
    - tank_level (int): Current tank level.

    Returns:
    int: The adjusted tank level after considering overflow.
    """
    
    MAX_FILL_VALUE = 80
    
    # If overflow occurs
    if tank_level > MAX_FILL_VALUE:
        overflow = tank_level - MAX_FILL_VALUE
        tank_level = MAX_FILL_VALUE - overflow
    
    return tank_level

def use_card(player_tank, card_to_use, player_cards, opponent_tank):
    """
    Use a card from the player's hand and update tank levels accordingly.
    
    Parameters:
    - player_tank (int): Player's current tank level.
    - card_to_use (str or int): The card to be used.
    - player_cards (list): List of player's cards.
    - opponent_tank (int): Opponent's current tank level.

    Returns:
    tuple: A 2-tuple containing the player's tank and the opponent's tank after using the card.
    """
    
    # Remove the used card from the player's hand
    player_cards.remove(card_to_use)
    
    # If the card is a water card (integer)
    if isinstance(card_to_use, int):
        player_tank += card_to_use
    else:
        # Check if it's a power card and apply its effect
        if card_to_use == "SOH":
            # Steal half opponent's tank value
            steal_amount = int(opponent_tank / 2)
            player_tank += steal_amount
            opponent_tank -= steal_amount
        elif card_to_use == "DOT":
            # Drain opponent's tank
            opponent_tank = 0
        elif card_to_use == "DMT":
            # Double my tank's value
            player_tank *= 2
    print("Playing with card:{}".format(card_to_use))
    # Apply overflow if necessary
    player_tank = apply_overflow(player_tank)
    
    return player_tank, opponent_tank

def discard_card(card_to_discard, player_cards, water_cards_pile, power_cards_pile):
    """
    Discard a card from the player's hand and place it at the bottom of the appropriate pile.
    
    Parameters:
    - card_to_discard (str or int): The card to be discarded.
    - player_cards (list): List of player's cards.
    - water_cards_pile (list): List of water cards.
    - power_cards_pile (list): List of power cards.
    """
    
    # Remove the discarded card from the player's hand
    player_cards.remove(card_to_discard)
    
    # If the card is a water card, add it to the bottom of the water cards pile
    if isinstance(card_to_discard, int):
        water_cards_pile.append(card_to_discard)
    else:
        # Otherwise, add it to the bottom of the power cards pile
        power_cards_pile.append(card_to_discard)

def filled_tank(tank):
    """
    Determine if the tank level is between the maximum and minimum fill values (inclusive).
    
    Parameters:
    - tank (int): Current tank level.
    
    Returns:
    - bool: True if the tank is filled, False otherwise.
    """
    
    MIN_FILL_VALUE = 75
    MAX_FILL_VALUE = 80
    
    return MIN_FILL_VALUE <= tank <= MAX_FILL_VALUE


def check_pile(pile, pile_type):
    """
    Checks if the given pile is empty. If so, call the pile’s setup function to replenish the pile.
    
    Parameters:
    - pile (list): List of cards in the pile.
    - pile_type (str): Type of the pile - either "water" or "power".
    
    Returns:
    None
    """
    
    if not pile:
        if pile_type == "water":
            pile.extend(setup_water_cards())
        elif pile_type == "power":
            pile.extend(setup_power_cards())

def human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, opponent_tank):
    """
    Handles the human player's turn.
    
    Parameters:
    - human_tank (int): The current water level in the human's tank.
    - human_cards (list): The cards in the human's hand.
    - water_cards_pile (list): The pile of water cards.
    - power_cards_pile (list): The pile of power cards.
    - opponent_tank (int): The current water level in the computer's tank.

    Returns:
    A tuple containing the updated human's tank level and the computer's tank level.
    """
    # Show the human player's water level and the computer player's water level
    print(f"Your water level at: {human_tank}")
    print(f"Computer's water level: {opponent_tank}")

    # Show the human player their hand
    print(f"Your cards are: {human_cards}")
    
    # Ask if they want to use or discard a card
    action = get_user_input("Do you want to use a card or discard a card? (u / d): ").lower()

    while action not in ['u', 'd']:
        action = get_user_input("Do you want to use a card or discard a card? (u / d): ").lower()

    card = get_user_input("Which card do you want to use/discard? ")

    while card not in human_cards:
        card = get_user_input("Which card do you want to use/discard? ")

    # Apply the chosen action
    if action == "u":
        # Use the card and update the tanks
        human_tank, opponent_tank = use_card(human_tank, card, human_cards, opponent_tank)
    else:
        discard_card(card, human_cards, water_cards_pile, power_cards_pile)

    # Draw a new card
    if isinstance(card, int):  # It's a water card
        new_card = get_card_from_pile(water_cards_pile, 0)
        print("Drawing water card: {}".format(new_card))
    else:  # It's a power card
        new_card = get_card_from_pile(power_cards_pile, 0)
        print("Drawing power card: {}".format(new_card))
    
    # Add the new card to the human's hand and arrange
    human_cards.append(new_card)
    arrange_cards(human_cards)
    print(f"Your water level at: {human_tank}")
    print(f"Computer's water level: {opponent_tank}")
    print(f"Your cards are: {human_cards}\n")
    return human_tank, opponent_tank

def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
    """
    Handles the computer player's turn using a deterministic strategy.
    """
    print(f"Computer's water level: {computer_tank}")
    print(f"Your water level at: {opponent_tank}")
    # Filter out water and power cards
    water_cards = [card for card in computer_cards if isinstance(card, int)]
    power_cards = [card for card in computer_cards if isinstance(card, str)]
    
    action = "use"  # By default, computer will use a card
    card_to_use_or_discard = None

    # 1. Try to fill the tank if it's far from being full
    if computer_tank  < 20:
        card_to_use_or_discard = max(water_cards)
    # 2. Try to fiil the tank with the water card if it's almost being full
    elif computer_tank> 65:
        card_to_use_or_discard = max(water_cards)
    # 3. Use DMT if close to half-full
    elif 30<computer_tank <40 and 'DMT' in power_cards:
        card_to_use_or_discard = 'DMT'

    # 4. Use SOH if opponent's tank is over half
    elif opponent_tank > 50 and 'SOH' in power_cards:
        card_to_use_or_discard = 'SOH'

    # 5. Play the lowest water card
    elif len(water_cards) > 0:
        card_to_use_or_discard = min(water_cards)

    # 6. Discard DOT, as besides 1~4 situation, there is no longer benefit for a computer use DOT
    elif 'DOT' in power_cards:
        card_to_use_or_discard = 'DOT'
        action = "discard"
    # 7. As default, computer will use the max water card
    else:
        card_to_use_or_discard = max(water_cards)
    # Carry out the action
    if action == "use":
        computer_tank, opponent_tank = use_card(computer_tank, card_to_use_or_discard, computer_cards, opponent_tank)
    else:
        discard_card(card_to_use_or_discard, computer_cards, water_cards_pile, power_cards_pile)
    
    print(f"Computer {action}s {card_to_use_or_discard}.")

    # Draw a new card and arrange
    if isinstance(card_to_use_or_discard, int):
        new_card = get_card_from_pile(water_cards_pile, 0)
    else:
        new_card = get_card_from_pile(power_cards_pile, 0)

    computer_cards.append(new_card)
    arrange_cards(computer_cards)
    print(f"Computer's water level is now at: {computer_tank}")
    print(f"Your water level at: {opponent_tank}\n")
    return computer_tank, opponent_tank

def main():
    print("Welcome to the WATER TANK game and play against the computer!")
    print("The first player to fill their tank wins the game.")
    print("Good luck!\n")
    # Setup cards and Deal cards
    water_cards_pile, power_cards_pile = setup_cards()
    human_cards, computer_cards = deal_cards(water_cards_pile, power_cards_pile)
    human_tank = 0
    computer_tank = 0
    # Randomly choose whether human or computer go first
    starting_player = "Human" if random.choice([True, False]) else "Computer"
    print(f"The {starting_player} Player has been selected to go first!\n")
    current_player = starting_player
    
    while True:
        if current_player == "Human":
            print("===Human Player's turn!===")
            
            # Human Player makes a move
            human_tank, computer_tank = human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, computer_tank)
            
            # Check if Human won
            if filled_tank(human_tank):
                print("Human player won!")
                break
            
            # Check piles
            check_pile(water_cards_pile, "water")
            check_pile(power_cards_pile, "power")
            
            # Set the next turn to Computer Player 
            current_player = "Computer"
            
        elif current_player == "Computer":
            print("===Computer Player's turn!===")
            
            # Computer Player makes a move
            computer_tank, human_tank = computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, human_tank)
            
            # Check if Computer Player won
            if filled_tank(computer_tank):
                print("Computer Player won!")
                break
            
            # Check piles
            check_pile(water_cards_pile, "water")
            check_pile(power_cards_pile, "power")
            
            # Set the next turn to Human
            current_player = "Human"




if __name__ == '__main__':
    main()
