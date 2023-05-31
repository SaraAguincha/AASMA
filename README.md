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


## How to run Example agents
```bash

python3 single_agent.py [--episodes] [N_EPISODES]

python3 multi_agents.py [--episodes] [N_EPISODES]

```


## Notes

```
 - Changes to the environment made:
      - Grid changed to be 5x5
      - Now the observation of the agent is a array of arrays (same elements, but more easy to understand)
         - The change was made in this line: agent_obs.append(mask_view.flatten())
      - For some reason they used a typedfloat32 for the positions coordinates, and now its int. Before was: pos[i]/(grid_size - 1)
         - The change was made in this line: mask_view = np.zeros((*self._agent_view_mask, len(agent_no_mask_obs[0])), dtype=np.float32)
      - The grid is now with 5x5, having the agent in the middle cell


 - Starting positions for the cars are (starting from the top): (6,13), (13,7), (7,0), (0,6)
 
 - To change the grid view of observation, we need to change this lines of code in the environment:
         - self._agent_view_mask = (3, 3)
         
         for row in range(max(0, pos[0] - 2), min(pos[0] + 1 + 2, self._grid_shape[0])):
                for col in range(max(0, pos[1] - 2), min(pos[1] + 1 + 2, self._grid_shape[1])):

         - mask_view[row - (pos[0] - 1), col - (pos[1] - 1), :] = agent_no_mask_obs[_id]

 - The observation array has the following structure:
      It starts with an empty mask, if its a 5x5 grid it will be an array of arrays, each array with 5 subarrays, to define each cell.
      Each array, has n_elements: n_agents + 2 + 3. 2 for the coordinates and 3 for the route.
      At the end of the get_agent_obs() function, it returns an array of arrays with all the cells the agent can observe.

 - Route an array of 3 elements, the 1 is which the agent is going:
      - [Forward Right Left], per example, going to the right is: [0 1 0]

```


## TODO

```
   - convention, decide who goes first based on the observation + route of each
```