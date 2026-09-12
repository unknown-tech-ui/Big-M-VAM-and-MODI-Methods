# Optimization Case Studies: Big-M Simplex & Transportation Methods

## Overview
This repository contains Python implementations for solving two well-known optimization problems. It was created as part of an assignment requiring the mathematical formulation and computational solution of Linear Programming (LPP) and Transportation models.

## Case Studies Formulated
1. **Chemical Blending Cost Minimization (Big-M Simplex Method)**
   * **Problem:** Minimizing the cost of blending two chemicals while strictly adhering to equality and inequality constraints for active ingredients, viscosity, and toxicity limits.
   * **Method:** The LPP was converted to standard form using slack, surplus, and artificial variables, and solved iteratively using the Big-M Simplex method to handle the artificial variables.

2. **Supply Chain Logistics (Transportation Problem)**
   * **Problem:** Minimizing the transportation cost of shipping solar panels from 3 factories (sources) to 4 distribution hubs (destinations) with specific supply capacities and demands.
   * **Methods Used:** 
     * **VAM (Vogel’s Approximation Method):** Used to calculate the Initial Basic Feasible Solution (IBFS).
     * **MODI (u-v) Method:** Used to test the IBFS for strict optimality by calculating dual variables and opportunity costs (deltas).

## Repository Structure / Files Included
* `Big_M-Simple.py` : Python script containing the Big-M method implementation and step-by-step tableau generation.
* `VAM_MODI.py` : Python script calculating the VAM allocation and MODI optimality test.
* `Big-M_output.txt` : Text file containing the raw terminal output of the Simplex iterations.
* `VAM_MODI-output.txt` : Text file containing the raw terminal output of the VAM and MODI steps.
* `Optimization_Assignment.pdf` : Final assignment submission file containing screenshots of the code and terminal outputs as per the instructions.

## Prerequisites
* **Python 3.x**
* No external libraries are required. The code is written using standard core Python lists and built-in functions.

## How to Run the Code
To verify the outputs on your local machine, open a terminal or command prompt in this directory and run:

For the Big-M Simplex Method:
```bash
python Big_M-Simple.py
```

For the Transportation Problem (VAM & MODI):
```bash
python VAM_MODI.py
```

