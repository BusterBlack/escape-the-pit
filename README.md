# Escape The Pit - Game Self-Organising Multi-Agent System Evironment

This work was initially developed by the SOMAS2022/3 cohort at Imperial College London - https://github.com/SOMAS2022

## Programming Language

* Download [GoLang](https://go.dev/dl/) (1.19)

### Get Started

* [GoLang Get Started](https://go.dev/learn/)

## Structure

Below is the main file structures, including the game play (playGame.py) and game learning (RLexplore.py).
```
agent.py - learning agent class
game_env.py - game environment class
```

```
.
├── cmd
│   └── (Executable Outputs)
├── pkg
│   └── infra
│       └── (Infrastructure Implementation)
|       └── teams
|           └── (MAS Agent)
│   └── experiments
│       └── RLexplore.py
│       └── playGame.py
|       └── player
|           └── agent.py (Learning Agent Class)
|           └── game_env.py (Game Environment Class)
├── .env (Environmental variables for Infrastructure)
```


## Quick Start

```
git clone git@github.com:BusterBlack/escape-the-pit.git
cd escape-the-pit
make
```
If running a team experiment, eg for team 0, set the `MODE` env variable in `.env`
```
MODE=0
```

## Reinforcement Learning

To perform training on the learning agent

Import relevant packages
```
from pkg.player import (
    game_env,
    agent
)
```

Create game environment
```
env = game_env.escapeThePitEnv()
state = env.resetRL()
```

Create learning agent
```
agent = agent.agent(env.state_size, env.numNewAgents, 3)
```

Run the game for a set number of epsidoes
```
battles = 10
episodes = 20
batch_size = 32
for ep in range(episodes):
  state = env.resetRL()
  for battle in range(battles):
    action = agent.act(state)
    next_state, reward, done = env.step(action)
    agent.remember(state, action , reward, next_state, done)
    state = next_state
    if len(agent.memory) >= batch_size:
      agent.lr_decay(ep)
      agent.replay(batch_size)
```

OR --- Run the RL script 
```
python ./pkg/experiments/RLexplore.py
```


## Game Play

For _random_ game play use the "random" arguments to the playGame.py script. The second argument is the verbose setting ("true"|"false")
```
python ./pkg/experiments/plagGame.py "random" "false"
```

For _predicted_ game play
```
python ./pkg/experiments/playGame.py "predict" "false"
```

For _fixed_ game play
```
python ./pkg/experiments/playGame.py "fixed" "false"
```
