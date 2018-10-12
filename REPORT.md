# Hanabi AI Agent: Research Report

###### Jakrin Juangbhanich 2178928 : CITS3001 Major Project



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



