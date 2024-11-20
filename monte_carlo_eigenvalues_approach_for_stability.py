# -*- coding: utf-8 -*-
"""Monte Carlo - Eigenvalues approach for Stability.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AdNdFzhCYhYC4RxEC9faxvLURmuhRgUw
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numpy.linalg import eig

# Definisi model SIR
def sir_model(y, t, beta, u, mu, gamma):
    S, I = y
    #N = S + I
    dSdt = mu - beta * (1 - u) * S * I  - (mu + u) * S
    dIdt = beta * (1 - u) * S * I  - (gamma + mu) * I
    return [dSdt, dIdt]

# Fungsi untuk menghitung Jacobian
def jacobian(S, I, beta, u, mu, gamma):
    #N = S + I
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

# Perturbasi parameter beta dan u
num_simulations = 1000
beta_samples = np.random.uniform(0.4, 1, num_simulations)
u_samples = np.random.uniform(0.01, 0.4, num_simulations)

# Untuk menyimpan hasil
stability_results = []
eigenvalues = []

for beta, u in zip(beta_samples, u_samples):
    R0 = compute_R0(beta, u, mu, gamma)
    if R0 > 1.25:
        # Integrasikan model dengan perturbasi
        sol = odeint(sir_model, y0, t, args=(beta, u, mu, gamma))
        S, I = sol[-1]

        # Hitung Jacobian di akhir simulasi
        J = jacobian(S, I, beta, u, mu, gamma)
        eigen_vals, _ = eig(J)

        # Simpan hasil
        stability_results.append((beta, u, R0, S, I))
        eigenvalues.append(eigen_vals)

# Convert lists to arrays for easier manipulation
stability_results = np.array(stability_results)
eigenvalues = np.array(eigenvalues)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(7, 6))

# Area Stability Plot
scatter = axs[0, 0].scatter(stability_results[:, 0], stability_results[:, 1], c=stability_results[:, 2], cmap='viridis')
fig.colorbar(scatter, ax=axs[0, 0], label='$R_0$')
axs[0, 0].set_xlabel('$\\beta$')
axs[0, 0].set_ylabel('$u$')
axs[0, 0].set_title('Area of Stability ($R_0 > 1$)')

# Dynamics of Infection Plot
selected_beta, selected_u = 0.4, 0.05  # Example parameters that are stable
solution = odeint(sir_model, y0, t, args=(selected_beta, selected_u, mu, gamma))
axs[0, 1].plot(t, solution[:, 0], label='Susceptible')
axs[0, 1].plot(t, solution[:, 1], label='Infected')
axs[0, 1].set_xlabel('Time')
axs[0, 1].set_ylabel('Population')
axs[0, 1].set_title('Dynamics of Infection Over Time')
axs[0, 1].legend()

# Histogram of First Eigenvalue
axs[1, 0].hist(np.real(eigenvalues[:, 0]), bins=30, color='blue', alpha=0.7)
axs[1, 0].set_xlabel('Real Part of First Eigenvalue')
axs[1, 0].set_ylabel('Frequency')
axs[1, 0].set_title('Histogram of First Eigenvalue')

# Histogram of Second Eigenvalue
axs[1, 1].hist(np.real(eigenvalues[:, 1]), bins=30, color='blue', alpha=0.7)
axs[1, 1].set_xlabel('Real Part of Second Eigenvalue')
axs[1, 1].set_ylabel('Frequency')
axs[1, 1].set_title('Histogram of Second Eigenvalue')

plt.tight_layout()
# Save the figure
fig.savefig('simulation_results_eigenvalues.eps', format='eps')

plt.show()