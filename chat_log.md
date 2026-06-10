# AI Development Log

Project: Multi-Objective Traffic Signal Control using Reinforcement Learning and SUMO-RL

Course: Deep Reinforcement Learning Final Project

---

## Phase 1 – Selecting a Traffic Simulation Platform

### User

I want to do a final project related to smart cities and intelligent traffic signal control. What simulation platforms are commonly used in reinforcement learning research?

### AI

Several traffic simulation platforms are widely used in intelligent transportation research:

1. SUMO (Simulation of Urban Mobility)
   - Open-source
   - Large research community
   - Supports traffic light control
   - Integrates with reinforcement learning frameworks

2. CityFlow
   - Designed for large-scale traffic networks
   - High simulation speed
   - Popular in multi-agent reinforcement learning research

3. CARLA
   - Realistic autonomous driving simulator
   - More suitable for self-driving vehicle research

4. VISSIM
   - Commercial software
   - Widely used in transportation engineering

For reinforcement learning-based traffic signal control, SUMO and CityFlow are currently the two most popular choices.

---

### User

Which one is better for a university final project?

### AI

Comparison:

| Feature | SUMO | CityFlow |
|----------|----------|----------|
| Documentation | Excellent | Moderate |
| Community Support | Very Large | Medium |
| RL Examples | Many | Some |
| Ease of Use | High | Medium |
| Traffic Signal Control | Excellent | Excellent |
| Research Reproducibility | High | High |

Recommendation:

For a course project with limited development time, SUMO is usually the safer choice because:

- More tutorials
- Better documentation
- Existing RL frameworks
- Easier experiment reproduction

---

### User

I will use SUMO then.

### AI

Good choice.

A recommended framework is:

SUMO + SUMO-RL

because SUMO-RL already provides:

- Traffic signal agents
- Observation spaces
- Reward functions
- Q-Learning examples
- DQN extensions

which can significantly reduce implementation effort.

---

## Phase 2 – Defining the Research Topic

### User

I do not want to simply reproduce an existing paper.

How can I add some novelty?

### AI

Most existing traffic signal control studies optimize only one objective:

- Waiting time
- Queue length
- Travel time

You can introduce a multi-objective reward function that considers:

1. Traffic efficiency
2. Fairness between directions
3. Signal switching stability
4. Switching cost

This would make the control strategy closer to real-world traffic management requirements.

---

### User

That sounds good.

I want to design a reward function with fairness and stability.

### AI

Possible reward design:

Reward =

- Queue Length
- Fairness Penalty
- Stability Penalty
- Switching Cost

where:

Queue Length:
Reduce congestion.

Fairness:
Avoid starving low-volume directions.

Stability:
Avoid excessive phase switching.

Switching Cost:
Represent yellow-light transition losses.

This can be formulated as a weighted multi-objective reward function.

---

## Phase 3 – Initial Reward Design

### User

I implemented the following reward:

R = -(wq*Q + wf*F + ws*S + wc*C)

where:

Q = total queue length

F = queue standard deviation

S = phase switching indicator

C = yellow-light cost

### AI

The formulation is mathematically reasonable and aligns with your proposal.

Potential advantages:

- Explicit congestion control
- Improved fairness
- Reduced unnecessary switching

Potential risk:

The switching penalties may dominate the reward signal and discourage exploration.

Careful tuning of the weights will be required.

---

## Phase 4 – Experimental Failure

### User

The experiment result is terrible.

Average speed keeps dropping.

Stopped vehicles increase continuously.

The intersection eventually becomes completely congested.

### AI

This behavior suggests a classic reinforcement learning reward design issue.

Possible causes:

1. Switching penalties are too strong.
2. Reward scale imbalance.
3. Credit assignment failure.

The agent may learn:

Switch Signal

↓

Immediate Negative Reward

↓

Avoid Switching

↓

Keep Current Phase Forever

↓

Traffic Collapse

This is known as a Gridlock situation.

---

### User

That is exactly what happened.

The traffic lights almost never switch.

### AI

Then the reward design is likely preventing effective exploration.

The agent is minimizing punishment instead of maximizing traffic efficiency.

---

## Phase 5 – Reward Redesign

### User

How can I fix it?

### AI

Instead of using absolute queue length:

Q

use queue improvement:

ΔQ = Q(t−1) − Q(t)

Advantages:

- Positive reward when congestion decreases.
- Negative reward when congestion increases.
- Direct feedback for useful actions.
- Better credit assignment.

New reward:

R = wq·ΔQ − wf·F − ws·S

Additionally:

- Reduce fairness penalty.
- Reduce switching penalty.
- Remove yellow-light cost.

This should encourage learning while preserving multi-objective characteristics.

---

### User

I implemented the new reward function.

### AI

Good.

Expected effects:

1. Faster convergence.
2. More signal switching when necessary.
3. Reduced congestion.
4. Better traffic flow.
5. Elimination of gridlock.

---

## Phase 6 – Improved Results

### User

The results improved significantly.

Average speed increased.

Waiting time decreased.

Gridlock disappeared.

### AI

Excellent.

This confirms that:

The original multi-objective reward suffered from:

- Reward scale imbalance
- Excessive switching penalties
- Credit assignment problems

The improved reward succeeds because it transforms the optimization target from:

Absolute State Evaluation

to

State Improvement Evaluation

which is generally easier for reinforcement learning algorithms to learn.

---

## Final Research Conclusion

### User

What is the main contribution of this project?

### AI

The key contribution is not merely adding fairness or stability terms.

The most important finding is:

A naive multi-objective reward based on absolute penalties can cause severe learning failures in traffic signal control.

By transforming the reward into a delta-based improvement signal:

ΔQueue = Q(t−1) − Q(t)

the agent receives clearer feedback and learns more effective traffic control policies.

This demonstrates the importance of reward engineering in reinforcement learning-based intelligent transportation systems.

---

## Final System Selection

Evaluated Platforms:

- CityFlow
- SUMO

Final Choice:

- SUMO
- SUMO-RL

Reasons:

- Better documentation
- Easier reproduction
- Existing RL examples
- Faster development process
- Suitable for academic research

---

## Final Methods

1. Original SUMO-RL Q-Learning Baseline
2. Multi-Objective Absolute Penalty Reward
3. Improved Delta-Based Advantage Reward

---

## Key Lessons Learned

1. Reward design is more important than adding complexity.
2. Absolute penalties can lead to unintended behaviors.
3. Traffic fairness and stability must be carefully weighted.
4. Delta-based rewards provide better learning signals.
5. SUMO-RL is an effective platform for reinforcement learning research in intelligent transportation systems.

---
End of AI Development Log
