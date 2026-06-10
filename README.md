# deep reinforcement learning 期末報告
# Multi-Objective Traffic Signal Control using Q-Learning and SUMO-RL

基於深度強化學習之多目標智慧交通號誌控制研究

## Overview

本專案為深度強化學習（Deep Reinforcement Learning）課程期末專題，使用 SUMO 與 SUMO-RL 模擬智慧交通號誌控制問題，並探討多目標獎勵函數（Multi-objective Reward Function）對交通效率、公平性與控制穩定性的影響。

研究中建立 2×2 Grid Network 交通環境，並以 Q-Learning 作為控制代理（Agent），比較以下三種交通號誌控制策略：

1. Original Baseline（SUMO-RL 預設方法）
2. Multi-objective Absolute Penalty（初始提出方法）
3. Advantage-based Multi-objective Method（改良後方法）

---

## Research Motivation

現有交通號誌控制研究多以降低等待時間或排隊長度為主要目標，但真實交通環境中仍需考慮：

* Traffic Efficiency（交通效率）
* Fairness（公平性）
* Stability（穩定性）
* Switching Cost（切換成本）

若僅追求吞吐量最佳化，容易產生：

* 特定方向長時間紅燈（Starvation）
* 過度頻繁切換號誌
* 實際部署困難

因此本研究嘗試設計多目標獎勵函數，使 Agent 能在多種交通指標間取得平衡。

---

## Environment

### Simulation Platform

* SUMO (Simulation of Urban Mobility)
* SUMO-RL
* Python 3.10+

### Road Network

* 2×2 Grid Network
* Multiple Intersections
* Dynamic Traffic Flow

---

## Reinforcement Learning Setup

### Algorithm

Q-Learning

### Hyperparameters

```python
alpha = 0.1
gamma = 0.99

epsilon_start = 0.05
epsilon_min = 0.005

delta_time = 5
min_green = 5

num_seconds = 80000
```

---

## Methods

### 1. Original Method (Baseline)

SUMO-RL 預設獎勵函數：

[
R_t = -(\sum WaitingTime_t - \sum WaitingTime_{t-1})
]

利用等待時間變化量作為回饋訊號。

---

### 2. Multi-objective Absolute Penalty

本研究初始提出方法：

[
R_t =
-(w_qQ_t+w_fF_t+w_sS_t+w_cC_t)
]

其中：

* Q：總排隊車數
* F：公平性（Queue Std）
* S：是否切換相位
* C：切換成本（Yellow Time）

權重設定：

```python
w_queue = 1.0
w_fairness = 0.5
w_stability = 0.2
w_switch = 0.1
```

---

### 3. Advantage-based Method

改良後方法：

[
R_t =
w_q(Q_{t-1}-Q_t)
-w_fF_t
-w_sS_t
]

改進重點：

* 使用 Queue Improvement 取代 Absolute Queue
* 降低 Fairness Penalty
* 降低 Phase Switching Penalty
* 移除 Yellow Time Cost

權重設定：

```python
w_queue = 1.0
w_fairness = 0.05
w_switch = 0.02
```

---

## Experimental Results

### Absolute Penalty Method

觀察結果：

* Gridlock 發生
* 平均速度下降至 2 m/s 以下
* 停等車輛數接近飽和

原因：

高額切換懲罰導致 Agent 學習出：

> 永遠不切換燈號

進而造成整個路網阻塞。

---

### Advantage Method

改善結果：

* Mean Speed 提升至 5~7.5 m/s
* Waiting Time 顯著下降
* Queue Length 明顯改善
* Fairness 與 Stability 兼顧

---

## Key Findings

本研究發現：

### Absolute Reward

存在 Credit Assignment Problem

Agent 無法判斷：

* 哪個動作真正改善交通
* 哪個動作導致惡化

---

### Delta-based Reward

使用：

[
Q_{t-1}-Q_t
]

作為改善訊號後：

* 收斂速度提升
* Gridlock 消失
* 控制效果大幅改善

---

## Project Structure

```text
├── experiment/
│   ├── ours_ql_2x2grid_method.py
│   ├── ours_ql_2x2grid_advantage.py
├── outputs/
│   ├── 2x2_our_methods/
│   └── 2x2_our_advantage/
├── figures/
│   ├── mean_speed.pdf
│   ├── total_waiting_time.pdf
│   ├── mean_waiting_time.pdf
│   └── total_stopped.pdf
└── README.md
```

---

## Run

### Original Multi-objective Method

```bash
python ours_ql_2x2grid_method.py
```

### Advantage Method

```bash
python ours_ql_2x2grid_advantage.py
```

---

## Future Work

未來可朝以下方向進行研究：

### Multi-Agent Reinforcement Learning

* MARL
* CTDE Framework
* Neighbor Communication

### Better Reward Design

融合：

* Queue Length
* Waiting Time
* Throughput
* CO₂ Emission

### Large-scale Network

* 4×4 Grid
* 6×6 Grid
* Real-world Traffic Dataset

---

## References

1. Varaiya, P. (2013). Max Pressure Control of a Network of Signalized Intersections.
2. Wei, H. et al. (2018). IntelliLight: A Reinforcement Learning Approach for Intelligent Traffic Light Control.
3. Sun, Q. W. et al. (2022). Deep Reinforcement-Learning-Based Adaptive Traffic Signal Control with Real-Time Queue Lengths.
4. Janota, A. et al. (2024). Reinforcement Learning Approach to Adaptive Traffic Signal Control using SUMO-RL.

---

## Author

National Chin-Yi University of Technology

Deep Reinforcement Learning Final Project

Multi-Objective Traffic Signal Control using Q-Learning and SUMO-RL
