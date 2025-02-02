# -*- coding: utf-8 -*-
"""Monte Carlo - Stability Ratio.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LvC9Hdb7Q_nVhIf31jjuW3fUiFlTC43I
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numpy.linalg import eig

# Definisi model SIR
def sir_model(y, t, beta, u, mu, gamma):
    S, I = y
    dSdt = mu - beta * (1 - u) * S * I  - (mu + u) * S
    dIdt = beta * (1 - u) * S * I  - (gamma + mu) * I
    return [dSdt, dIdt]

# Fungsi untuk menghitung Jacobian
def jacobian(S, I, beta, u, mu, gamma):

    J11 = -beta * (1 - u) * I  - (mu + u)
    J12 = -beta * (1 - u) * S
    J21 = beta * (1 - u) * I
    J22 = beta * (1 - u) * S  - (gamma + mu)
    return np.array([[J11, J12], [J21, J22]])

# Definisi R0
def compute_R0(beta, u, mu, gamma):
    return beta * mu * (1 - u) / ((u + mu) * (gamma + mu))

# Parameter
mu = 0.01
gamma = 0.01
beta_base = 0.3
u_base = 0.05

# Kondisi awal
S0 = 0.05
I0 = 0.01
y0 = [S0, I0]

# Waktu simulasi
t = np.linspace(0, 500, 1000)

# Monte Carlo Simulation
num_simulations = 1000
perturbed_beta =  np.random.uniform(0.4, 1, num_simulations)
perturbed_u = np.random.uniform(0.01, 0.4, num_simulations)

stability_ratios = []
stability_results = []

delta_threshold = 0.001  # Ambang kestabilan
stability_counter = 0
i = 0

for beta, u in zip(perturbed_beta, perturbed_u):
    R0 = compute_R0(beta, u, mu, gamma)
    if R0 > 1:
      # Integrate model with perturbed parameters
      sol = odeint(sir_model, y0, t, args=(beta, u, mu, gamma))

      # Estimasi ekuilibrium sebagai nilai akhir
      equilibrium = sol[-1]
      distance = np.linalg.norm(equilibrium - sol[-1])

      if distance < delta_threshold:
         stability_counter += 1
         i += 1
         stability_ratios.append(stability_counter/(i))

      stability_results.append((beta, u, R0))
      # Record stability ratio

# Convert lists to arrays for easier manipulation
stability_results = np.array(stability_results)

# Plotting using gridspec
fig = plt.figure(figsize=(8, 6))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.5])

# Plot 1: Area of Stability in the first row, first column
ax1 = fig.add_subplot(gs[0, 0])
scatter = ax1.scatter(stability_results[:, 0], stability_results[:, 1], c=stability_results[:, 2], cmap='viridis')
fig.colorbar(scatter, ax=ax1, label='$R_0$')
#ax1.scatter(stability_results[stable_mask, 0], stability_results[stable_mask, 1], color='green', label='Stable')
#ax1.scatter(stability_results[~stable_mask, 0], stability_results[~stable_mask, 1], color='red', label='Unstable')
ax1.set_xlabel('$\\beta$')
ax1.set_ylabel('$u$')
ax1.set_title('Area of Stability ($R_0 > 1$)')
ax1.legend()

# Plot 2: Dynamics of Infection in the first row, second column
ax2 = fig.add_subplot(gs[0, 1])
selected_beta, selected_u = 0.4, 0.05  # Example stable parameters
solution = odeint(sir_model, y0, t, args=(selected_beta, selected_u, mu, gamma))
ax2.plot(t, solution[:, 0], label='Susceptible')
ax2.plot(t, solution[:, 1], label='Infected')
ax2.set_xlabel('Time')
ax2.set_ylabel('Population')
ax2.set_title('Dynamics of Infection Over Time')
ax2.legend()

# Plot 3: Stability Ratio in the second row, spanning both columns
ax3 = fig.add_subplot(gs[1, :])
ax3.plot(range(stability_counter), stability_ratios, color='blue')
ax3.set_xlabel('Iteration')
ax3.set_ylabel('Stability Ratio')
ax3.set_title('Stability Ratio per Iteration')

plt.tight_layout()
# Save the figure
fig.savefig('simulation_stability_ratio.eps', format='eps')

plt.show()