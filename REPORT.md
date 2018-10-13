# Hanabi AI Agent: Prince of Nigeria

###  CITS3001 Major Project Research Report by Jakrin Juangbhanich



## Contents

1. Introduction
2. Literature Review
3. Selected Strategy
4. Implementation
5. Validation
6. References



## Introduction

Hanabi is a co-operative card game for 2-5 players. There are 50 cards in the deck, with five suits (red, green, blue, white, yellow) and five values (from 1 to 5). The cards must be played in a certain sequence (ascending order by suit), and the goal of the game is to play as many cards as possible before it is over. The key mechanic of this game is that players cannot see their own hand, but can see the other players' hands. During their turn, they may chose to play a card, discard a card, or give another player some information. The official rules can be found here: [Hanabi Card Game Rules PDF](https://www.spillehulen.dk/media/102616/hanabi-card-game-rules.pdf). Also, a perfect solution to this game is [considered to be NP Complete](http://teaching.csse.uwa.edu.au/units/CITS3001/project/2018/papers/HanabiNP.pdf).

The goal of this project is to build an AI agent to play the game, Hanabi. Current published strategies for playing the game fall largely into either Monte Carlo Tree search or some form of rules based system. I believe that there is a lot of information to be modelled during the game, so my approach was to augment a simple rules based agent with high quality information about the board state. In addition to this, I focused on building fast simulation and visualization pipelines so that I can gain deeper insight into how to improve an agent.

I developed a Hanabi simulator and GUI in Python for rapid experimentation and testing, and finally ported the agent to Java once I was satisfied with the results. The agent computes a probability matrix for each card in hand, as well as a value matrix for each possible hint that it can give to other players. By using this information with a simple rules engine, this agent is able to achieve an average score of **17.03** when playing a 4-player game with itself (over a sample size of 500 games).



## Literature Review

#### Hirotaka Osawa Agent: 2015

Osawa's paper presents several different agents, each one adding some incremental improvement on the previous agent. The most advanced agent in this paper demonstrates some understanding of its internal state and external state. Also, upon receiving a hint, the agent will attempt to simulate the previous state as seen from the hint giver's perspective. This is an attempt to predict what the hint giver's intention where, and thus gain more implicit information about the board.

This agent was simulation in a 2-player game, with *n-games* = 100. The average score was **15.85** using this "self recognition strategy." This is an impressive result, as I found that my agent struggles a lot more when there are fewer players.

However, I do not believe this to be a good general strategy. A large part of this strategy aims to model the world state from the previous player's perspective. In a 2 player scenario, this is much easier to simulate because there is only one other player. Also, any hint received by the agent is guarenteed to come from the single other player. This strategy also assumes that the other player is using the exact same strategy to play; that is, it assumes that it is playing a mirror-image of itself.

Whilst this may be specialized to deal with a mirror-match in a 2-player scenario, I do not think it will be robust to 3, 4 or 5 player games, and with different agents. Although the self-recognition agent was not tested in *Walton-River et al's paper (2017*), Osawa's outer-state agent demonstrated significantly lower scores when evaluated in a larger team game.

#### Van den Bergh Agent: 2015

Van den Bergh's paper examines the playability and properties of Hanabi. It also presents a general strategy for a game playing agent. The strategies are built around the natural intuition from human play. Primarily, this is to:

1. Play a card if certain that is playable.
2. Discard a card if certain that it can be discarded.
3. If hint tokens remain, give the most useful hint to another player.
4. Otherwise, discard the card most likley to be unplayable.

Of course, there are many parameters and policies for each of these steps. The author also presents the case for special situations, such as when the game is ending and the agent is better off 'guessing' a card than giving a hint.

Different strategies were simulated in a 3-player mirror match, with *n-games*=10. The simulation also tests 10,000 different paramter configurations with each strategy. The strongest combination with the following rules:

* Discard Rule: discard the card that seems most useless.
* Hint Rule: Giving a hint on the next useful card in sight or on the largest number of card.

The score of this agent is **15.4**.

Van den Bergh also explores the idea of using Monte-Carlo Tree Search. But the results seem poor, with high simluation costs only achieving an average score of **14.5**. The author cites that MCTS can be awkward to apply to Hanabi because of the nature of hidden information in the game, and the limited fuses for each player to make a mistake.

#### Evaluating Hanabi Agents: 2017

Watlon-River's paper *Evaluating and Modelling Hanabi Playing Agents* discusses the above two agents, as well as some other ones (most notably the Predictor IS-MCTS model). The simluations included mirror-match benchmarks, as well as 2, 3, 4 and 5 player games using a different combination of agents. The authors also included intentionally flawed agents to evaluate how other agents would perform when playing with a non-optimal team-mate.

The authors point out that MCTS has the desirable property of being to operate without domain specific knowledge. The most performant agent in this paper was the Predictor IS-MCTS model. However, the downside of this agent is that it must be provided with a model for each of the other agents that it is playing with. Also, it is quite slow - the authors had to limit its time per move to 1 second (whereas a rules based agent could complete an entire game in that same time).

What was most notable for me in this paper was the care that the authors had taken to create perfect simulation environments. All the non-determinism was seeded to ensure that each agent was evaluated under the same conditions. Large n-game sizes were used, and the tests covered many different possible combination of agent pairings.

Because the simluation method was different, I am unable to use the leading score (**12.14** in a 3-player game with the IS-MCTS agent) in any meaningful way (since I only have the capacity to test mirror match set ups).



## Selected Strategy

For my agent, I have used a rules-based strategy (Van den Bergh) as my starting point. I wanted to use as much common sense and intuition in developing this agent as I can, and I believe that the best place to start is to produce as much useful data as possible. No matter if the agent's main mechanism is hard coded rules, or a neural network, I think that the more data it has available, the better it will perform.

Here is an outline of my development strategy:

* **Implement a Hanabi CQRS and GUI for analysis**: In order to design and improve the strategy, the first step was to make powerful tools that allowed me to look at each game in great detail. Firstly I created a GUI for the game state, allowing me to interact with the cards and see their data visually. I used a CQRS (command queue) design pattern to simulate the game, meaning that I could click through a history of all the moves, to see the state before and after each move.
* **Apply Bayesian Reasoning**: For each card in hand, the agent computes a probability score (for each possible color and value combination), and a rating (for whether it should be played or discarded). This will allow the agent to make better decisions.
* **Analyse and Experiment**: Once I have a basic agent running with the above information, I can analyse the games played and develop some intuition about ways to improve the agent.

The agent itself is very simple. It has two main components:

#### Card Value Matrix

The agent's main function is to compute a probability matrix for an unknown card. The matrix must contain the following information for each possible **color** and **value** combination:

| Key              | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| `probability`    | The probability that this unknown card matches this **color** and **value**. |
| `play_rating`    | Either `1.0` or `0.0`, indicating if this card can be immediately played or not. |
| `discard_rating` | A number between `0.0` and `1.0`. The higher the number, the more desirable it is for this card to be discarded. |

The matrix will be 5 x 5. Finally, it can compute a heuristic value for how playable or how discardable an unknown card is, by summing the product of each element's probability with its ratings.

The matrix will be produced with the following procedure, for each unknown card in the player's hand:

* First, a duplicate of the initial deck is used as the starting pool.
* All cards from the discard pile, fireworks pile, and observed in all other players' hands are removed from this pool.
* The pool is further updated according to the hints received by this card.
* Finally, the card will also have a history of hints that it was present for, but not targeted for. This means that it can also elimate a lot of options from the pool.
* Now we have a matrix of all possible cards that this unknown card could be.

#### Gameplay Policy

The matrix above will help the agent work out the probability of a certain move being successful. I then pair this information with a simple rules based engine to play the game.

1. If there are more than 1 fuse tokens, play a card with rating >= ` K_NORMAL_PLAY_LIMIT`. Otherwise, play a card with rating >= `K_SAFE_PLAY_LIMIT`.
2. **(Bonus Step: Hint Boosting)** If no cards were played initially, then look at the cards again. Any cards that have received a hint will have their ratings boosted to a factor of `K_HINT_PLAY_BOOST`. We then see if any cards can be played with the ratings boost. This is done assume that other agents will favor hinting towards immediately playable cards. However, if the other agents are unknown, it may be best to disable this feature by setting the co-efficient to `1.0`.
3. If there is a card with a discard rating >= ` K_DISCARD_LIMIT` then discard the card.
4. If hint tokens remain, then give a hint to another player according to the agent's **hint policy**.
5. Otherwise, desparate times calls for desparate measures... discard the card with the highest discard rating.

The default parameters are:

```python
K_NORMAL_PLAY_LIMIT = 0.85
K_SAFE_PLAY_LIMIT = 1.00
K_DISCARD_LIMIT = 0.85
K_HINT_PLAY_BOOST = 1.35
```

#### Hint Policy

The agent will also compute a matrix, this time from its target's point of view, to decide how best to reward its next hint.

The hints will be played aggresively, prioritizing these factors:

* Whether or not this hint can immediately enable the target player to play a new card with 100% confidence.
* Whether or not this is a card that can be played (even if the hint doesn't give the player full information).
* Whether or not this will allow the player to discard this card with 100% confidence.
* Otherwise, maximise the `play_rating` gain from giving this hint to another player.
* All other things equal, players closer to the current player will be prioritized.



## Implementation



## Validation



## References



### Version 1: Bayesian Agent

* Agent creates a probability matrix for each card in their hand, based on all the information that they have.
* Agent assigns a 'play rating' and a 'discard rating' to each card.
* Each matrix then weighs this rating with the probability, resulting in an overall play or discard score for the card. A score of **1.0** means absolute certainty.
* The agent then has a hard-coded policy to act based on this information. It will play or discard a card that it is at least 90% certain about. Otherwise, it will give a hint to another agent, based on what it percieves the biggest net gain will be. If no hint tokens remain, it will discard the card with the highest discard rating.

Simulation result after 100 games: **15.75**

### Version 2: Discard Model

* Know when a full color suite is useless.

Simulation result after 100 games: **15.12**

### Version 3: Fuse Guard

Simulation result after 100 games: **15.57**

### Version 4: Hint Accounting

Simulation result after 100 games: **15.71**

### Version 5: Improved Hint Policy

* Prioritize giving hint to 5's.
* Prioritize cards that can be played.

| Hint Policy                                                  | Result |
| ------------------------------------------------------------ | ------ |
| Play enabling, then highest play rating gain + 0.5 highest discard rating gain. | 16.05  |
| Same as above, with discard enablers scored after play enablers. | 14.43  |
| With vital reveal.                                           | 14.77  |
| No discard_max rating.                                       | 15.40  |
| total rating instead of max                                  | 15.58  |
| discard policy only when 2 or more.                          | 15.87  |
| prioritize hinting cards that can be played                  | 16.68  |
| decreased 'play limit' parameter                             | 16.69  |
| Agent increases probability of hinted cards (1.25 boost)     | 16.92  |
| Same (1.50 boost)                                            | 17.05  |
| Same (1.35 boost)                                            | 17.15  |
| Aggressive 1.35 boost without discard policy.                | 17.48  |

Simulation result after 100 games: **17.27**

### Version 4: Hint Fixing

For version 4 of the agent, we will make the assumption that the agent is playing with copies of itself. Here it can do logical deductions for things not possible if it were playing other agents.

The key point I would like to create here, is that if an agent recieves a hint for a single card, and that card

Simulation result after 100 games: **???**

### Future Optimizations

* Agent should take into account 'final round' actions. The current model still tries to give hints or discard on the last round. Instead, if there are fuse tokens remaining, it will be better off taking calculated risks.



