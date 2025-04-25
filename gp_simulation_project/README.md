# GP Simulation Project

## Overview
This project implements a simulation framework for studying Gross-Pitaevskii (GP) equations using the Monte Carlo Variational method and the Split-Step method. The goal is to analyze various GP equations, including those with nonlinear and magnetic terms, and to observe phenomena such as vortices in two-dimensional systems.

## Project Structure
The project is organized as follows:

```
gp_simulation_project
├── src
│   ├── __init__.py
│   ├── base_gp_equation.py        # Contains the BaseGPEquation class for GP equations.
│   ├── monte_carlo_variational.py # Implements the MonteCarloVariational class for basis function calculations.
│   ├── split_step_method.py       # Implements the SplitStepMethod class for time evolution of wave functions.
│   ├── simulation.py              # Manages the overall simulation process.
│   └── utils.py                   # Contains utility functions for data processing and visualization.
├── tests
│   ├── __init__.py
│   ├── test_base_gp_equation.py   # Unit tests for the BaseGPEquation class.
│   ├── test_monte_carlo_variational.py # Unit tests for the MonteCarloVariational class.
│   ├── test_split_step_method.py   # Unit tests for the SplitStepMethod class.
│   └── test_simulation.py          # Unit tests for the Simulation class.
├── requirements.txt                # List of required Python packages.
└── README.md                       # Project documentation.
```

## Installation
To install the required packages, run the following command:

```
pip install -r requirements.txt
```

## Usage
1. Import the necessary classes from the `src` package.
2. Create an instance of the `Simulation` class to manage the simulation.
3. Configure the GP equation parameters and run the simulation.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.