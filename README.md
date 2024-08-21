# Nim
AI that teaches itself to play Nim through reinforcement learning.

## Instructions
1. Download this repository to your device.
2. Open a terminal or command prompt.
3. Navigate to the directory where you downloaded the repository.
4. Run the file with Python 3 using the following command, choosing the number of games the AI can train from by modifying the number.
```bash
python nim_play.py --games 1000
```
5. Follow the prompts by choosing a pile and then count number to make a move.
7. Watch the AI gain better strategy as it is allowed to play more and more games against itself.

## Background

The game [Nim](https://wild.maths.org/play-win-nim#:~:text=The%20rules%20of%20Nim&text=There%20are%20two%20players.,coins%20left%20after%20that%20move.) has a plethora of strategies that can increase the likelihood of winning. Q-Learning is used throughout this project for the AI to begin to understand strategy that can be used to win. The AI plays against itself multiple times, using reinforcement learning with rewards (+1 for win, -1 for loss) to train the AI to choose optimal moves throughout.#

The programme works by taking old states and performing actions to receive a reward. This reward can represent either a win or loss or future possibilities of wins and losses. By maximising rewards the model can train itself to choose moves that have the highest likelihood of success.

The programme can also adjust how many numbers of times it is allowed to play against itself, therefore changing the amount of strategy it can learn. As shown in the videos the more the programme plays against itself the better it becomes.
