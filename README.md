# GandALF
GandALF (GAussian N-Dimensional Active Learning Framework) is an **Active Learning** tool for design-of-experiments

This repository contains the latest version of the active learning framework presented by **https://doi.org/10.1016/j.fuel.2022.125340**.

## Installation
GandALF can be used by cloning this repository directly to the desired local folder. 
It can be executed from the command window or Anaconda terminal:
- Open the desired terminal in the local folder which contains the "GandALF.py" script
- Execute the command ` python GandALF.py ` to execute the experimental selection

## Dependencies
GandALF makes use of several packages which can all be installed with `pip`
- Python 3.6 or higher
- Numpy
- Scipy
- Scikit-learn
- Pandas
- GPy
- GPyOpt

## 1. Determine the Design Space
The design space determines the variables which are altered when performing experiments, and in which range these variables should remain.
The design space can be adapted in the "GandAlF.csv" file. The first row contains the name of the studied variables, below the minimum and maximum values of the variables can be specified. Next, the type of the parameter can be determined this can be 'discrete' or 'continuous' depending on whether only integer values for the variable are allowed or not.
The number of variables can be freely chosen by adding an extra column with a specified variable name, range and type before the "output" column. It is advised not to use more than 20 variables as this will increase the required computation time and the performance of the experimental selection.

## 2.a (Optional) Add Initial Data
Initial data from literature or past experiments can be added below the "type"-row. This data should contain the value of every variable and a corresponding output value.
If this data is present no initial experiments will be performed and GandALF will sequentially select the following optimal experiments.

## 2.b (Optional) Select Initial Experiments
If no initial data is available, GandALF will select a desired number of experiments specified by the value of `n_init` in "GandALF.py".

## 3. Sequential Selection of Experiments
When the initial experiments are executed, GandALF will sequentially select the following optimal experiments. These experiments can be executed and the values can be added manually to the "GandALF.csv" file or when these are computational experiments an objective function can be specified which determines the experimental output.

## Reference
https://doi.org/10.1016/j.fuel.2022.125340
