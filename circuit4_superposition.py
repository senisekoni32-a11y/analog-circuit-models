import numpy as np
import matplotlib.pyplot as plt


def parallel(Ra, Rb):
    return Ra * Rb / (Ra + Rb)


def vout_from_v1(V1, R1, R2, R3):
    # V2 grounded, V1 divides across R1 and (R2 || R3)
    Rp = parallel(R2, R3)
    return V1 * Rp / (R1 + Rp)


def vout_from_v2(V2, R1, R2, R3):
    # V1 grounded, V2 divides across R3 and (R1 || R2)
    Rp = parallel(R1, R2)
    return V2 * Rp / (R3 + Rp)


def vout_total(V1, V2, R1, R2, R3):
    # Add the two contributions algebraically
    return vout_from_v1(V1, R1, R2, R3) + vout_from_v2(V2, R1, R2, R3)


def vout_node(V1, V2, R1, R2, R3):
    # Check with one node equation: (V1-Vo)/R1 + (V2-Vo)/R3 = Vo/R2
    return (V1 / R1 + V2 / R3) / (1 / R1 + 1 / R3 + 1 / R2)


def print_results(V1, V2, R1, R2, R3):
    Rp1 = parallel(R2, R3)
    VO1 = vout_from_v1(V1, R1, R2, R3)
    print(f"V2 grounded: R2||R3 = {R2:.0f} x {R3:.0f} / ({R2:.0f} + {R3:.0f}) = {Rp1:.1f} ohm")
    print(f"VOUT1 = {V1} x {Rp1:.1f} / ({R1:.0f} + {Rp1:.1f}) = {VO1:.3f} V")

    Rp2 = parallel(R1, R2)
    VO2 = vout_from_v2(V2, R1, R2, R3)
    print(f"V1 grounded: R1||R2 = {R1:.0f} x {R2:.0f} / ({R1:.0f} + {R2:.0f}) = {Rp2:.1f} ohm")
    print(f"VOUT2 = {V2} x {Rp2:.1f} / ({R3:.0f} + {Rp2:.1f}) = {VO2:.3f} V")

    print(f"VOUT = VOUT1 + VOUT2 = {VO1:.3f} + {VO2:.3f} = {VO1 + VO2:.3f} V")
    print(f"Node-equation check: VOUT = {vout_node(V1, V2, R1, R2, R3):.3f} V")


def plot_results(V1, V2, R1, R2, R3):
    V2_sweep = np.linspace(-10, 10, 200)
    VO1 = vout_from_v1(V1, R1, R2, R3)
    VO2 = vout_from_v2(V2, R1, R2, R3)

    plt.figure(figsize=(11, 4.2))

    plt.subplot(1, 2, 1)
    plt.plot(V2_sweep, vout_total(V1, V2_sweep, R1, R2, R3), label="VOUT total")
    plt.plot(V2_sweep, vout_from_v2(V2_sweep, R1, R2, R3), "--", label="VOUT2 (from V2)")
    plt.axhline(VO1, linestyle="--", color="gray", label="VOUT1 (from V1)")
    plt.axvline(-V1, linestyle=":", color="red", label="V2 = -V1: VOUT = 0")
    plt.xlabel("V2 (V)")
    plt.ylabel("VOUT (V)")
    plt.title("Superposition: VOUT vs V2 (V1 = 6 V)")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.bar(["VOUT1", "VOUT2", "VOUT"], [VO1, VO2, VO1 + VO2],
            color=["tab:blue", "tab:orange", "tab:green"])
    plt.ylabel("Voltage (V)")
    plt.title("Contributions at V1 = 6 V, V2 = 3 V")
    plt.grid(alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig("circuit4_superposition.png", dpi=200)
    plt.show()


def main():
    V1, V2 = 6.0, 3.0
    R1, R2, R3 = 1e3, 2e3, 1e3
    print_results(V1, V2, R1, R2, R3)
    plot_results(V1, V2, R1, R2, R3)


if __name__ == "__main__":
    main()
