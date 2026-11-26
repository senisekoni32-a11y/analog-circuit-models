import numpy as np
import matplotlib.pyplot as plt


def collector_resistor(Vcc, Vout_off, Iout):
    # RC sized with the transistor off
    return (Vcc - Vout_off) / Iout


def collector_current(Vcc, RC, IL):
    # IC = Vcc/RC + IL, with VCE neglected
    return Vcc / RC + IL


def base_resistor(Vcc, Vbe, beta, IC):
    # IB = IC/beta, RB = (Vcc - VBE)/IB
    IB = IC / beta
    return (Vcc - Vbe) / IB


def print_results(Vcc, Vout_off, Iout, IL, beta, Vbe, Vce_sat):
    RC = collector_resistor(Vcc, Vout_off, Iout)
    print(f"RC = ({Vcc:.0f} - {Vout_off:.0f}) / {Iout*1e3:.0f} mA = {RC:.0f} ohm")

    IC = collector_current(Vcc, RC, IL)
    print(f"IC = {Vcc:.0f} / {RC:.0f} + {IL*1e3:.0f} mA = {IC*1e3:.1f} mA")

    IB = IC / beta
    print(f"IB = {IC*1e3:.1f} mA / {beta} = {IB*1e3:.2f} mA")

    RB = base_resistor(Vcc, Vbe, beta, IC)
    print(f"RB = ({Vcc:.0f} - {Vbe}) / {IB*1e3:.2f} mA = {RB:.0f} ohm")

    IC_req = (Vcc - Vce_sat) / RC + IL
    print(f"Check with VCE(sat) = {Vce_sat} V: IC needed = ({Vcc:.0f} - {Vce_sat}) / {RC:.0f} "
          f"+ {IL*1e3:.0f} mA = {IC_req*1e3:.1f} mA")
    print(f"Available beta x IB = {beta} x {IB*1e3:.2f} mA = {beta*IB*1e3:.1f} mA "
          f"(>= {IC_req*1e3:.1f} mA, so saturated)")

    Vout_check = Vcc - Iout * RC
    print(f"Off state: VOUT = {Vcc:.0f} - {Iout*1e3:.0f} mA x {RC:.0f} = {Vout_check:.1f} V")


def plot_results(Vcc, Vout_off, Iout, IL, beta, Vbe, Vce_sat):
    RC = collector_resistor(Vcc, Vout_off, Iout)
    IC = collector_current(Vcc, RC, IL)
    RB = base_resistor(Vcc, Vbe, beta, IC)

    RB_sweep = np.linspace(10e3, 100e3, 300)
    available = beta * (Vcc - Vbe) / RB_sweep

    plt.figure(figsize=(11, 4.2))

    plt.subplot(1, 2, 1)
    plt.plot(RB_sweep / 1e3, available * 1e3, label="Available beta x IB")
    plt.axhline(IC * 1e3, linestyle="--", color="gray", label=f"Required IC = {IC*1e3:.0f} mA")
    plt.axvline(RB / 1e3, linestyle=":", color="red", label=f"RB = {RB/1e3:.1f} kΩ")
    plt.xlabel("RB (kΩ)")
    plt.ylabel("Current (mA)")
    plt.title("Base resistor sizing for saturation")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.bar(["Off (VIN < 0.05 V)", "On (VIN = 12 V)"], [Vout_off, Vce_sat],
            color=["tab:green", "tab:red"])
    plt.axhline(Vout_off, linestyle="--", color="gray")
    plt.ylabel("VOUT (V)")
    plt.title("Output levels (on = assumed VCE(sat))")
    plt.grid(alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig("circuit5_saturated_transistor.png", dpi=200)
    plt.show()


def main():
    Vcc, Vout_off, Iout = 12.0, 10.0, 1e-3
    IL, beta, Vbe, Vce_sat = 10e-3, 50, 0.6, 0.4
    print_results(Vcc, Vout_off, Iout, IL, beta, Vbe, Vce_sat)
    plot_results(Vcc, Vout_off, Iout, IL, beta, Vbe, Vce_sat)


if __name__ == "__main__":
    main()
