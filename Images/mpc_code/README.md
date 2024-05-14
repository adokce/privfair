This is for the scenario where clients (Alice and Bob) outsource computations to a set of servers (2, 3 or n).
The clients secret share their data in chunks (see variable 'steps' in method one_run() in client_mpc.cpp)
The clients aggregate the computed metrics and recieve the result in fixed point notation.

List of files:


1. client_mpc.cpp : Code for clients to secret share their data and aggregate the shares

2. eval_fairness.mpc : MP-SPDZ code for the MPC protocols to evaluate fairness metrics - Equalized odds and sub-group accuracy.