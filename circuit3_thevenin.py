import numpy as np
import matplotlib.pyplot as plt


def thevenin_voltage(V, R1, R2):
    # Open-circuit voltage at X-Y, by the voltage divider rule
    return V * R2 / (R1 + R2)


def thevenin_resistance(R1, R2):
    # Source shorted, R1 in parallel with R2
    return R1 * R2 / (R1 + R2)


def vout_thevenin(V, R1, R2, R3, R4):
    # VOUT = VTH * R4 / (RTH + R3 + R4)
    VTH = thevenin_voltage(V, R1, R2)
    RTH = thevenin_resistance(R1, R2)
    return VTH * R4 / (RTH + R3 + R4)


def vout_mesh(V, R1, R2, R3, R4):
    # The hard way: two loop equations solved together
    #   V = I1(R1 + R2) - I2*R2
    #   0 = -I1*R2 + I2(R2 + R3 + R4)
    A = np.array([[R1 + R2, -R2],
                  [-R2, R2 + R3 + R4]])
    b = np.array([V, 0.0])
    I1, I2 = np.linalg.solve(A, b)
    return I2 * R4


def print_results(V, R1, R2, R3, R4):
    VTH = thevenin_voltage(V, R1, R2)
    print(f"VTH = {V} x {R2:.0f} / ({R1:.0f} + {R2:.0f}) = {VTH:.3f} V")

    RTH = thevenin_resistance(R1, R2)
    print(f"RTH = {R1:.0f} x {R2:.0f} / ({R1:.0f} + {R2:.0f}) = {RTH:.1f} ohm")

    VOUT = vout_thevenin(V, R1, R2, R3, R4)
    print(f"VOUT = {VTH:.3f} x {R4:.0f} / ({RTH:.1f} + {R3:.0f} + {R4:.0f}) = {VOUT:.4f} V")

    VOUT_mesh = vout_mesh(V, R1, R2, R3, R4)
    print(f"Loop-equation check: VOUT = {VOUT_mesh:.4f} V")


def plot_results(V, R1, R2, R3, R4):
    R4_sweep = np.linspace(100, 20e3, 200)
    R3_sweep = np.linspace(0, 10e3, 200)

    R4_dots = R4_sweep[::20]
    R3_dots = R3_sweep[::20]
    mesh_R4 = [vout_mesh(V, R1, R2, R3, r) for r in R4_dots]
    mesh_R3 = [vout_mesh(V, R1, R2, r, R4) for r in R3_dots]

    plt.figure(figsize=(11, 4.2))

    plt.subplot(1, 2, 1)
    plt.plot(R4_sweep / 1e3, vout_thevenin(V, R1, R2, R3, R4_sweep), label="Thevenin")
    plt.plot(R4_dots / 1e3, mesh_R4, "o", label="Loop equations")
    plt.axvline(R4 / 1e3, linestyle=":", color="red", label="R4 = 2 kΩ")
    plt.xlabel("R4 (kΩ)")
    plt.ylabel("VOUT (V)")
    plt.title("VOUT vs R4")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(R3_sweep / 1e3, vout_thevenin(V, R1, R2, R3_sweep, R4), label="Thevenin")
    plt.plot(R3_dots / 1e3, mesh_R3, "o", label="Loop equations")
    plt.axvline(R3 / 1e3, linestyle=":", color="red", label="R3 = 1 kΩ")
    plt.xlabel("R3 (kΩ)")
    plt.ylabel("VOUT (V)")
    plt.title("VOUT vs R3")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("circuit3_thevenin.png", dpi=200)
    plt.show()


def main():
    V, R1, R2, R3, R4 = 12.0, 1e3, 2e3, 1e3, 2e3
    print_results(V, R1, R2, R3, R4)
    plot_results(V, R1, R2, R3, R4)


if __name__ == "__main__":
    main()
