import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigsh


class Solver:
    def __init__(self, N: int, L: float, hbar: float, m: float, a: float):
        self.N = N  # 格子点数
        self.L = L  # カットオフ（範囲 [-L, L]）
        self.a = a  # ポテンシャルの幅
        self.dx = 2 * L / (N - 1)  # 格子間隔
        self.hbar = hbar
        self.m = m
        self.x = np.linspace(-L, L, N)

    def potential_construct(
        self, V0: float, potential_type: str, **kwargs
    ) -> np.ndarray:
        
        #各ポテンシャルに必要なオプションの説明
        # potential_type: "free", "double_well", "well", "harmonic", "linear"
        # "free"の場合は、infinite_sideが必要
        # "double_well"の場合は、wells_distanceとwell_depthsが必要
        # "well"の場合は、V0が必要
        # "harmonic"の場合は、kが必要
        # "linear"の場合は、slopeが必要
        
        # ポテンシャルの構築
        if self.a > self.L:
            # ポテンシャルの幅が範囲を超えている場合
            raise ValueError("a must be less than L")
        elif self.a <= 0:
            # ポテンシャルの幅が負の場合
            raise ValueError("a must be positive")

        if potential_type == "free":
            # 自由粒子ポテンシャル(無限大の井戸ポテンシャル)
            V = np.zeros(self.N)
            infinite_side = kwargs.get("infinite_side", 'both')
            if infinite_side == "left":
                V[self.x < -self.a] = 1e6
            elif infinite_side == "right":
                V[self.x > self.a] = 1e6
            elif infinite_side == "both":
                V[self.x < -self.a] = 1e6
                V[self.x > self.a] = 1e6
            return V
        
        if potential_type =="double_well":
            # 二重井戸ポテンシャル
            wells_distance = kwargs.get('wells_distance', 1.0)
            well_depths = kwargs.get('well_depths', (V0, V0))
            depth1, depth2 = well_depths

            left_well_right_edge = -(wells_distance / 2)
            left_well_left_edge = left_well_right_edge - 2 * self.a
            right_well_left_edge = wells_distance / 2
            right_well_right_edge = right_well_left_edge + 2 * self.a

            V = np.zeros(self.N,)
            V[np.logical_and(self.x >= left_well_left_edge, self.x <= left_well_right_edge)] = -depth1
            V[np.logical_and(self.x >= right_well_left_edge, self.x <= right_well_right_edge)] = -depth2
            V[np.logical_and(self.x > left_well_right_edge, self.x < right_well_left_edge)] = 0.0
            V[np.logical_or(self.x < left_well_left_edge, self.x > right_well_right_edge)] = 1e6
        
        elif potential_type == "well":
            # 有限井戸ポテンシャル
            V = np.where(np.abs(self.x) < self.a, -V0, 0.0)

        elif potential_type == "harmonic":
            k = kwargs.get("k", 1.0)
            V = 0.5 * k * self.x**2

        elif potential_type == "linear":
            slope = kwargs.get("slope", 1.0)
            V = slope * self.x

        else:
            raise ValueError("other potential types are not implemented")

        return V

    def hamiltonian_construct(self, V: np.ndarray) -> np.ndarray:
        # 運動エネルギー項（三重対角行列）とポテンシャル項を組み合わせてハミルトニアンを構築
        t = self.hbar**2 / (2 * self.m * self.dx**2)
        main_diag = V + 2 * t
        off_diag = -t * np.ones(self.N - 1)
        H = np.diag(main_diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1)
        return H

    def diagonalize(self, H: np.ndarray, num_eigenvalues: int) -> np.ndarray:
        # ハミルトニアンの対角化,固有値と固有ベクトルの計算と正規化

        # 疎行列用の固有値計算
        eigenvalues, eigenvectors = eigsh(H, k=num_eigenvalues, which="SA")
        # 規格化
        for i in range(num_eigenvalues):
            norm = np.sqrt(np.sum(np.abs(eigenvectors[:, i]) ** 2) * self.dx)
            eigenvectors[:, i] /= norm
        return eigenvalues, eigenvectors

    def plot_wavefunctions(
        self,
        eigenvectors: np.ndarray,
        eigenvalues: np.ndarray,
        num_eigenvalues: int,
        save_path: str = None,
    ) -> None:
        # 固有ベクトルのプロット
        plt.figure(figsize=(10, 6))
        for i in range(num_eigenvalues):
            plt.plot(
                self.x, eigenvectors[:, i], label=f"n={i+1}, E={eigenvalues[i]:.3f}"
            )
        plt.xlabel("x")
        plt.ylabel("Wave function")
        plt.legend()
        plt.title("Wave Functions")
        plt.grid(True)
        if save_path:
            plt.savefig(save_path)
        print(f"Wavefunction plot saved to {save_path}")
        plt.show()

    def save_results(
        self, eigenvalues: np.ndarray, eigenvectors: np.ndarray, filename: str
    ) -> None:
        # 固有値を保存
        np.savetxt(filename, eigenvalues, delimiter=",", header="Eigenvalues")
        # 固有ベクトルを追記
        with open(filename, "a") as f:
            f.write("\nEigenvectors\n")
            np.savetxt(f, eigenvectors.T, delimiter=",", fmt="%.10e")
        # 固有値と固有ベクトルをCSVファイルに保存
        print(f"Results saved to {filename}")
        imgfile = filename.rsplit(".", 1)[0] + ".png"
        self.plot_wavefunctions(
            eigenvectors, eigenvalues, eigenvectors.shape[1], save_path=imgfile
        )
        print("Eigenvalues and eigenvectors have been successfully saved and plotted.")


if __name__ == "__main__":
    # テスト用
    N = 1000
    L = 5.0
    hbar = 1.0
    m = 1.0
    a = 1.0
    V0 = 10.0
    potential_type = "free"  
    num_eigenvalues = 3
    filename = "results_infinite_well.csv"
    solver = Solver(N, L, hbar, m, a)
    V = solver.potential_construct(V0, potential_type)
    H = solver.hamiltonian_construct(V)
    eigenvalues, eigenvectors = solver.diagonalize(H, num_eigenvalues)
    solver.save_results(eigenvalues, eigenvectors, filename)
