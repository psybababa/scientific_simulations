import numpy as np
import matplotlib.pyplot as plt

def preprocess_data(data):
    # データの前処理を行う関数
    return np.array(data) - np.mean(data)

def visualize_wavefunction(x, wavefunction, title='Wavefunction'):
    # 波動関数を可視化する関数
    plt.figure(figsize=(10, 6))
    plt.plot(x, np.abs(wavefunction)**2, label='Probability Density')
    plt.title(title)
    plt.xlabel('Position')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.grid()
    plt.show()