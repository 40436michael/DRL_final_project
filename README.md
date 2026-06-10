# Multi-Objective Traffic Signal Control using Q-Learning and SUMO-RL

基於深度強化學習之多目標智慧交通號誌控制研究

> Deep Reinforcement Learning Final Project

---

## Introduction

交通號誌控制（Traffic Signal Control）是智慧交通系統（ITS）中的重要研究議題。

傳統固定時制（Fixed-Time Control）無法即時因應動態車流變化，而近年深度強化學習（Deep Reinforcement Learning, DRL）與強化學習（Reinforcement Learning, RL）逐漸被應用於智慧交通控制領域。

本專案使用 SUMO 與 SUMO-RL 建立 2×2 Grid Traffic Network，並利用 Q-Learning 訓練交通號誌控制代理（Agent），探討：

* Traffic Efficiency（交通效率）
* Fairness（公平性）
* Stability（穩定性）
* Switching Cost（切換成本）

之間的多目標權衡（Multi-objective Trade-off）。
## demo 影片
可看影片區

https://github.com/user-attachments/assets/c037321b-4dac-49ee-b092-973f6f45e996

## chat log with AI 

放在 chat_log.md
---

## Research Goal

本研究主要比較三種不同的獎勵函數設計：

| Method         | Description            |
| -------------- | ---------------------- |
| Original       | SUMO-RL 原始方法           |
| Ours Method    | 計畫書提出之多目標懲罰方法          |
| Ours Advantage | 改良後 Advantage-Based 方法 |

研究目標：

1. 驗證多目標獎勵函數是否可提升交通控制品質
2. 分析絕對值懲罰設計的問題
3. 探討 Delta-based Reward 的改善效果
4. 比較不同 Reward Design 對學習結果的影響

---

## Environment

### Simulation Platform

* SUMO
* SUMO-RL
* Python 3.x

### Traffic Network

* 2×2 Grid Network
* Multiple Intersections
* Dynamic Traffic Flow

### RL Algorithm

Q-Learning

### Hyperparameters

```python
alpha = 0.1
gamma = 0.99

epsilon_start = 0.05
epsilon_min = 0.005

min_green = 5
delta_time = 5

num_seconds = 80000
runs = 30
episodes = 4
```

---

## Project Structure

```text
.
├── original_ql_2x2grid.py
├── ours_ql_2x2grid_method.py
├── ours_ql_2x2grid_advantage.py
│
├── outputs/
│   ├── 2x2_our_full/
│   ├── 2x2_our_methods/
│   └── 2x2_our_advantage/
│
├── figures/
│   ├── mean_speed.pdf
│   ├── mean_waiting_time.pdf
│   ├── total_waiting_time.pdf
│   └── total_stopped.pdf
│
├── README.md
└── chat_log.md
```

---

# Method 1: Original Q-Learning

File:

```bash
original_ql_2x2grid.py
```

此方法採用 SUMO-RL 預設 Reward Function：

$$
R_t =
-\left(
WaitingTime_t
WaitingTime_{t-1}
\right)
$$

核心思想：

* 降低等待時間
* 提升交通效率
* 不考慮公平性
* 不考慮切換成本

作為本研究的 Baseline。

---

# Method 2: Multi-objective Reward

File:

```bash
ours_ql_2x2grid_method.py
```

依據研究計畫書提出的多目標獎勵函數：

$$
R_t
-(w_qQ+w_fF+w_sS+w_cC)
$$

其中：

### Queue Term

$$
Q=\sum queue_i
$$

代表總排隊車數。

---

### Fairness Term

$$
F=\sigma(queue)
$$

代表各車道排隊長度標準差。

用於避免特定方向長期等待。

---

### Stability Term

$$
S=
\begin{cases}
1,& phase\ changed\
0,& otherwise
\end{cases}
$$

避免頻繁切換號誌。

---

### Switching Cost

$$
C=
yellow_time
$$

考慮黃燈時間損失。

---

### Weights

```python
w_queue = 1.0
w_fairness = 0.5
w_stability = 0.2
w_switch = 0.1
```

---

## Problem of Method 2

實驗結果顯示：

* Vehicle Queue 快速累積
* Mean Speed 持續下降
* Waiting Time 急遽上升

最終產生：

> Gridlock（路口鎖死）

主要原因：

Agent 發現：

切換燈號

↓

立即受到懲罰

↓

選擇永遠不切換

↓

交通癱瘓

此現象屬於 Reward Design 的 Credit Assignment Problem。

---

# Method 3: Advantage-Based Reward

File:

```bash
ours_ql_2x2grid_advantage.py
```

為了解決 Method 2 的問題，本研究提出改良版 Reward。

---

## Queue Improvement

原始方法：

$$
-Q
$$

改為：

$$
Q_{t-1}-Q_t
$$

若排隊數下降：

Reward > 0

若排隊數增加：

Reward < 0

Agent 可直接知道：

> 這次動作是否改善交通狀況

---

## Fairness

$$
F=\sigma(queue)
$$

保留公平性約束。

---

## Switching Penalty

$$
S=
\begin{cases}
1,& switched\
0,& otherwise
\end{cases}
$$

僅保留輕量化懲罰。

---

## New Weights

```python
w_queue = 1.0
w_fairness = 0.05
w_switch = 0.02
```

並移除：

```python
Switching Cost
```

避免 Agent 因過度懲罰而失去探索能力。

---

# Experimental Results

## Original Method

特性：

* 最穩定
* Waiting Time 最低
* 收斂效果最佳

作為 Benchmark。

---

## Multi-objective Method

特性：

* 學習失敗
* Gridlock 發生
* 車流無法疏導

原因：

過高的切換懲罰與絕對值獎勵設計。

---

## Advantage Method

特性：

* 成功收斂
* Gridlock 消失
* Mean Speed 顯著提升
* Waiting Time 明顯下降
* 保留部分公平性控制能力

結果優於 Method 2。

---

# Key Findings

本研究發現：

## Absolute Reward Design

容易產生：

* Credit Assignment Problem
* Reward Scale Imbalance
* Gridlock

---

## Delta-Based Reward Design

利用：

$$
\Delta Queue
Q_{t-1}-Q_t
$$

能提供更有效的學習訊號。

優點：

* Faster Convergence
* Better Traffic Flow
* Reduced Waiting Time
* Improved Stability

---

# Future Work

未來可朝以下方向發展：

## Multi-Agent Reinforcement Learning

(MARL)

讓路口間共享資訊進行協同控制。

---

## PPO / DQN / A2C

測試更先進的強化學習演算法：

* DQN
* PPO
* A2C
* SAC

---

## Real-world Traffic Data

導入真實交通流量資料：

* Taiwan Traffic Dataset
* Open ITS Dataset

提升模型實務價值。

---

# References

1. Varaiya, P. (2013). Max Pressure Control of a Network of Signalized Intersections.
2. Wei, H., Zheng, G., Yao, H., & Li, Z. (2018). IntelliLight: A Reinforcement Learning Approach for Intelligent Traffic Light Control.
3. Sun, Q. W., Han, S. Y., Zhou, J., Chen, Y. H., & Yao, K. (2022). Deep Reinforcement-Learning-Based Adaptive Traffic Signal Control with Real-Time Queue Lengths.
4. Janota, A. et al. (2024). Evaluation of Adaptive Traffic Light Control on SUMO Platform Using Reinforcement Learning.
