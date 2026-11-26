import numpy as np
import matplotlib.pyplot as plt


def divider_output(V, R1, R2):
    # VD = V * R2 / (R1 + R2)
    return V * R2 / (R1 + R2)


def parallel(Ra, Rb):
    return Ra * Rb / (Ra + Rb)


def loaded_output(V, R1, R2, RL):
    # The load sits in parallel with R2, then the same divider rule applies
    return divider_output(V, R1, parallel(R2, RL))


def print_results(V, R1, R2):
    VD = divider_output(V, R1, R2)
    print(f"Unloaded: VD = {V} x {R2:.0f} / ({R1:.0f} + {R2:.0f}) = {VD:.3f} V")

    RL = 10 * R2
    R2p = parallel(R2, RL)
    VD_loaded = loaded_output(V, R1, R2, RL)
    err = (VD - VD_loaded) / VD * 100
    print(f"RL = 10 x R2 = {RL:.0f}: R2||RL = {R2p:.1f}, "
          f"VD = {VD_loaded:.3f} V, error = {err:.2f} %")


def plot_results(V, R1, R2):
    VD = divider_output(V, R1, R2)
    RL_10x = 10 * R2

    R2_sweep = np.linspace(0, 50e3, 400)
    RL = np.logspace(2, 6, 400)

    plt.figure(figsize=(11, 4.2))

    plt.subplot(1, 2, 1)
    plt.plot(R2_sweep / 1e3, divider_output(V, R1, R2_sweep))
    plt.xlabel("R2 (kΩ)")
    plt.ylabel("VD (V)")
    plt.title("Unloaded divider: VD vs R2")
    plt.grid(alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.semilogx(RL, loaded_output(V, R1, R2, RL), label="Loaded VD")
    plt.axhline(VD, linestyle="--", color="gray", label="Unloaded VD")
    plt.axvline(RL_10x, linestyle=":", color="red", label="RL = 10 x R2")
    plt.xlabel("Load RL (Ω)")
    plt.ylabel("VD (V)")
    plt.title("Loading effect on VD")
    plt.legend()
    plt.grid(alpha=0.3, which="both")

    plt.tight_layout()
    plt.savefig("circuit1_voltage_divider.png", dpi=200)
    plt.show()


def main():
    V, R1, R2 = 12.0, 10e3, 10e3
    print_results(V, R1, R2)
    plot_results(V, R1, R2)


if __name__ == "__main__":
    main()
