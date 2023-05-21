# AASMA
Autonomous Agents and Multi-Agent Systems


## Installation

- Setup:
   ```bash
      pip install 'pip<=23.0.1'
   ```
- Install package:
   - Using PyPI:
      ```bash
      pip install ma-gym
      sudo apt-get install ffmpeg
      ```


## Usage:
```python
import gym

env = gym.make('ma_gym:Switch2-v0')
done_n = [False for _ in range(env.n_agents)]
ep_reward = 0

obs_n = env.reset()
while not all(done_n):
    env.render()
    obs_n, reward_n, done_n, info = env.step(env.action_space.sample())
    ep_reward += sum(reward_n)
env.close()
```

## How to run Example agents
```bash
random_agent.py [-h] [--env ENV] [--episodes EPISODES]

options:
  -h, --help           show this help message and exit
  --env ENV            Name of the environment (default: Checkers-v0) ((Nosso é: TrafficJunction10-v0)
  --episodes EPISODES  episodes (default: 1)
```
