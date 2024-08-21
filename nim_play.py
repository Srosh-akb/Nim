import math
import random
import time
import argparse

class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        # default piles and player settings
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        # Compute and return all possible actions for current game state
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        # Return the opposite player (0 or 1)
        return 0 if player == 1 else 1

    def switch_player(self):
        # Switch the turn to other player
        self.player = Nim.other_player(self.player)

    def move(self, action):
        # Execute a move and update the game state accordingly
        pile, count = action

        # Check if the game has already been won
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update the pile after the move
        self.piles[pile] -= count
        self.switch_player()

        # Check if the current player has won the game
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player

class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        # Initialize AI with learning parameters and an empty Q-learning dictionary
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        # Update the Q-value 
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        # Retrieve the Q-value 
        key = (tuple(state), action)
        return self.q.get(key, 0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        # Update the Q-value using the Q-learning formula
        self.q[(tuple(state), action)] = old_q + self.alpha * (reward + future_rewards - old_q)

    def best_future_reward(self, state):
        # Determine the best possible future reward for a given state
        actions = Nim.available_actions(state)
        if not actions:
            return 0
        return max(self.get_q_value(state, action) for action in actions)

    def choose_action(self, state, epsilon=True):
        # Choose an action based on the current state, using an epsilon-greedy strategy
        actions = list(Nim.available_actions(state))
        if not actions:
            return None

        # Find the best action based on Q-values
        best_action = max(actions, key=lambda action: self.get_q_value(state, action))

        # Use epsilon-greedy approach to sometimes choose a random action
        if epsilon:
            chosen_action = random.choices(
                [random.choice(actions), best_action],
                weights=[self.epsilon, 1 - self.epsilon],
                k=1
            )[0]
        else:
            chosen_action = best_action

        return chosen_action

def train(n):
    player = NimAI()

    # Play `n` games to train the AI
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop until there's a winner
        while True:
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make the move and get the new state
            game.move(action)
            new_state = game.piles.copy()

            # Update the AI with rewards if the game is over
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break
            # If game is still going, no immediate rewards
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")
    return player

def play(ai, human_player=None):
    # Randomly decide if the human player goes first or second
    if human_player is None:
        human_player = random.randint(0, 1)

    game = Nim()

    # Game loop until there's a winner
    while True:
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Human player's turn
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")
        # AI player's turn
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Execute the move
        game.move((pile, count))

        # Check if the game is over
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a Nim AI and play against it.")
    parser.add_argument("--games", type=int, default=10000, help="Number of games to train the AI with.")
    args = parser.parse_args()

    # Train the AI with the specified number of games
    ai = train(args.games)
    # Start the game against the trained AI
    play(ai)
