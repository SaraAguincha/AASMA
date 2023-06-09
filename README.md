# AASMA
Autonomous Agents and Multi-Agent Systems

## Project by:

- Francisco Sousa, 95579
- Miguel Porfírio, 95641
- Sara Aguincha, 95675

## Installation

- Setup:
   ```bash
      pip install 'pip<=23.0.1'
   ```
- Install packages:
   - Using PyPI:
      ```bash
      pip install -r requirements.txt
      sudo apt-get install ffmpeg
      ```

- All the testing was done in `Python 3.10.8`

## How to run Example agents
```bash

python3 single_agent.py [--episodes] [N_EPISODES]

python3 multi_agents.py [--flags]

```

## `multi_agents.py` flags

- `--episodes` `-e`  number of episodes to be ran
- `--agents` `-a`    number of agents in the environment
- `--maxsteps` the max number of steps each episode can have
- `--render` whether or not to render the environment
- `--random` `-r` create Random agent team
- `--greedy` `-g` create Greedy agent team
- `--conventional` `-con` create Conventional agent team
- `--communicating` `-r` create Communicating agent team
- `--waiting` `-w` create Waiting agent team
- `--all` `-a` create a team for each type of agent
