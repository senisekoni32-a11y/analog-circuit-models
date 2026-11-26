import numpy as np
import matplotlib.pyplot as plt


def branch_currents(I, R1, R2):
    # I2 = I * R1 / (R1 + R2), and I1 = I * R2 / (R1 + R2)
    I1 = I * R2 / (R1 + R2)
    I2 = I * R1 / (R1 + R2)
    return I1, I2


def print_results(I, R1, R2):
    I1, I2 = branch_currents(I, R1, R2)
    print(f"I2 = {I*1e3:.1f} mA x {R1:.0f} / ({R1:.0f} + {R2:.0f}) = {I2*1e3:.3f} mA")
    print(f"I1 = {I*1e3:.1f} mA x {R2:.0f} / ({R1:.0f} + {R2:.0f}) = {I1*1e3:.3f} mA")

    # Checks: Kirchhoff's current law and equal branch voltages
    print(f"KCL: I1 + I2 = {I1*1e3:.3f} + {I2*1e3:.3f} = {(I1 + I2)*1e3:.3f} mA")
    print(f"V = I1 x R1 = {I1*1e3:.3f} mA x {R1:.0f} = {I1*R1:.3f} V")
    print(f"V = I2 x R2 = {I2*1e3:.3f} mA x {R2:.0f} = {I2*R2:.3f} V")


def plot_results(I, R1, R2):
    I1, I2 = branch_currents(I, R1, R2)

    R2_sweep = np.linspace(100, 20e3, 400)
    I1_sweep, I2_sweep = branch_currents(I, R1, R2_sweep)

    plt.figure(figsize=(11, 4.2))

    plt.subplot(1, 2, 1)
    plt.plot(R2_sweep / 1e3, I1_sweep * 1e3, label="I1 (through R1)")
    plt.plot(R2_sweep / 1e3, I2_sweep * 1e3, label="I2 (through R2)")
    plt.axvline(R2 / 1e3, linestyle=":", color="red", label="R2 = 3 kΩ")
    plt.xlabel("R2 (kΩ)")
    plt.ylabel("Current (mA)")
    plt.title("Branch currents vs R2 (R1 = 1 kΩ)")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.bar(["I (total)", "I1", "I2"], np.array([I, I1, I2]) * 1e3,
            color=["gray", "tab:blue", "tab:orange"])
    plt.ylabel("Current (mA)")
    plt.title("Current split at R1 = 1 kΩ, R2 = 3 kΩ")
    plt.grid(alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig("circuit2_current_divider.png", dpi=200)
    plt.show()


def main():
    I, R1, R2 = 10e-3, 1e3, 3e3
    print_results(I, R1, R2)
    plot_results(I, R1, R2)


if __name__ == "__main__":
    main()
