# Heuristic-Based Decision Engines in domain with large State-Space Variance
### Comparative Analysis of Autonomous Agents in Pokémon Showdown

## Project Overview
This project explores the application of custom heuristic functions to navigate high-dimensional, non-deterministic state spaces. Using the Pokémon Showdown environment via the `poke-env` library, I developed and benchmarked several autonomous agents to evaluate the efficacy of weighted-utility decision-making against stochastic baselines.

The core challenge involves managing **hidden information** and **stochasticity** (probabilities of move success/failure) while pruning a massive branching factor of possible move and switch combinations.



## System Architecture
To ensure rigorous testing and modularity, the repository is organized into distinct components:

* **`agents.py`**: The core library containing agent definitions. This follows an inheritance-based structure:
    * `RandomPlayer`: A stochastic baseline for control trials.
    * `MaxDamagePlayer`: A "Greedy" agent prioritizing immediate damage output.
    * `SmarterPlayer`: My primary heuristic agent, which evaluates state variables including type-matchups, HP thresholds, and long-term utility.
* **`benchmarks.py`**: A cross-evaluation framework that runs thousands of simulated trials to produce statistically significant performance data.

## Heuristic Logic
The `SmarterPlayer` utilizes a weighted heuristic function to assign a "fitness score" to potential future states. Rather than simple pattern matching, the logic focuses on:

* **Type-Advantage Calculus**: Predicting opponent switches and valuing defensive positioning.
* **Resource Management**: Weighting the preservation of "sweepers" (high-damage units) versus "walls" (defensive units) based on current HP.
* **Outcome Weighting**: Accounting for move accuracy and secondary effects to mitigate the risks of non-deterministic failure.



## Experimental Results
Initial trials indicate that while a "Max Damage" (Greedy) strategy outperforms random movement, the integrated heuristic approach in `SmarterPlayer` achieves a significantly higher win rate. 

**Key Finding:** In stochastic environments, prioritizing "survival probability" and "long-term utility" over "immediate damage" leads to a more robust win-rate across 1,000+ trials. This project served as my primary introduction to the challenges of AI safety and agent alignment in unpredictable environments.

## Installation & Usage

### Prerequisites
* Python 3.8+
* A local instance of the [Pokémon Showdown Server](https://github.com/smogon/pokemon-showdown) is recommended for high-speed benchmarking to avoid public server rate-limiting.

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/pokemon-ai-battle-agent.git](https://github.com/yourusername/pokemon-ai-battle-agent.git)
