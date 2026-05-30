import argparse
import os
import sys
import numpy as np
import pandas as pd

last_phase = {}
switch_count = {}

def multi_objective_reward(ts):

    ts_id = ts.id

    # =========================
    # 1. Queue Term
    # =========================
    queues = ts.get_lanes_queue()

    Q = sum(queues)

    # =========================
    # 2. Fairness Term
    # =========================
    F = np.std(queues)

    # =========================
    # 3. Stability Term
    # =========================
    current_phase = ts.green_phase

    if ts_id not in last_phase:
        last_phase[ts_id] = current_phase
        switch_count[ts_id] = 0

    switched = int(current_phase != last_phase[ts_id])

    switch_count[ts_id] += switched

    S = switched

    # =========================
    # 4. Switching Cost
    # =========================
    C = switched * ts.yellow_time

    # =========================
    # Update phase memory
    # =========================
    last_phase[ts_id] = current_phase

    # =========================
    # weights
    # =========================
    w_queue = 1.0
    w_fairness = 0.5
    w_stability = 0.2
    w_switch = 0.1
    reward = (
        -w_queue * Q
        -w_fairness * F
        -w_stability * S
        -w_switch * C
    )

    return reward

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from sumo_rl import SumoEnvironment
from sumo_rl.agents import QLAgent
from sumo_rl.exploration import EpsilonGreedy


if __name__ == "__main__":
    alpha = 0.1
    gamma = 0.99
    decay = 1
    runs = 30
    episodes = 4

    env = SumoEnvironment(
        net_file="sumo_rl/nets/2x2grid/2x2.net.xml",
        route_file="sumo_rl/nets/2x2grid/2x2.rou.xml",
        use_gui=False,
        num_seconds=80000,
        min_green=5,
        delta_time=5,
        reward_fn=multi_objective_reward,
    )

    for run in range(1, runs + 1):
        initial_states = env.reset()
        ql_agents = {
            ts: QLAgent(
                starting_state=env.encode(initial_states[ts], ts),
                state_space=env.observation_space,
                action_space=env.action_space,
                alpha=alpha,
                gamma=gamma,
                exploration_strategy=EpsilonGreedy(initial_epsilon=0.05, min_epsilon=0.005, decay=decay),
            )
            for ts in env.ts_ids
        }

        for episode in range(1, episodes + 1):
            if episode != 1:
                initial_states = env.reset()
                for ts in initial_states.keys():
                    ql_agents[ts].state = env.encode(initial_states[ts], ts)

            infos = []
            done = {"__all__": False}
            while not done["__all__"]:
                actions = {ts: ql_agents[ts].act() for ts in ql_agents.keys()}

                s, r, done, info = env.step(action=actions)

                for agent_id in s.keys():
                    ql_agents[agent_id].learn(next_state=env.encode(s[agent_id], agent_id), reward=r[agent_id])

            env.save_csv(f"outputs/2x2_our_methods/ql-2x2grid_run{run}", episode)

    env.close()
