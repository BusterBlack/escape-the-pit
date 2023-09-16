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

Adjust learning run - RLexplore.py
Adjust learning architecture - ./player/agent.py

```
run script RLexplore.py
```
