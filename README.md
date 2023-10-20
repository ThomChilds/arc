# Network Science Project - Metric Comparison for Prediction of Influential Spreaders in Real-Life Networks
Repo for network science project, Group 30.

## Setup

### Prerequisites

* [python 3.9.13](https://www.python.org/downloads/release/python-3913/)


### Installation

Create and activate a virtual environment

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install the dependencies using pip, all given in the requirements.txt file:

```bash
$ pip install -r requirements.txt --extra-index-url https://pypi.org/simple/
```

## Project Structure

    .
    ├── data                    # physical network data (.gml, .txt)
    ├── debugging               # folder for storing the reuslts of the simulations (.mat)
    ├── output                  # folder for saving the plots produced by analysis scripts
    ├── references              # folder with papers describing the implemented methods
    ├── sandbox                 # folder with the .py scripts used for analysis
        ├── *_network_characterisation.py                   # for characterising the networks
        ├── *_process_simulation_each_node.py               # for simulating spreading process
        ├── network_infectiousness_characterisation.py      # for heatmap of spreading potential based on simulation results
        ├── *_process_analysis.py                           # for relating the spreading potential of each node with its topological characteristics
        └── sir_model_parameter_tuning.py                   # for tuning the SIR modesl parameters to each network
    └── README.md               # setup instructions

## Maintainers
For further questions about this project, you can reach out to:

- Thomas Childs \<thomas.m.childs@tecnico.ulisboa.pt\>
- Miguel Carreiro \<miguel.t.carreiro@tecnico.ulisboa.pt\>
