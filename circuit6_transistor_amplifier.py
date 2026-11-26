import numpy as np
import matplotlib.pyplot as plt


def design_amplifier(Vcc, IC, beta, VC, VE, Vbe, drop_rth, gain):
    # Bias network and gain design
    RC = (Vcc - VC) / IC
    RE = VE / IC
    IB = IC / beta
    VB = VE + Vbe
    RTH = drop_rth / IB
    VTH = VB + drop_rth
    R2 = 2 * RTH
    R1 = R2 * (Vcc - VTH) / VTH
    RE1 = RC / gain
    RE2 = RE - RE1
    return {"RC": RC, "RE": RE, "IB": IB, "VB": VB, "RTH": RTH, "VTH": VTH,
            "R1": R1, "R2": R2, "RE1": RE1, "RE2": RE2}


def actual_bias(Vcc, R1, R2, RC, RE, beta, Vbe):
    # DC check of the finished design using the real R1 and R2
    VTH = Vcc * R2 / (R1 + R2)
    RTH = R1 * R2 / (R1 + R2)
    IB = (VTH - Vbe) / (RTH + (beta + 1) * RE)
    IC = beta * IB
    VE = (beta + 1) * IB * RE
    VC = Vcc - IC * RC
    return IC, VC, VE, VC - VE


def print_results(Vcc, IC, beta, VC, VE, Vbe, drop_rth, gain):
    d = design_amplifier(Vcc, IC, beta, VC, VE, Vbe, drop_rth, gain)
    print(f"RC = ({Vcc:.0f} - {VC:.0f}) / {IC*1e3:.0f} mA = {d['RC']:.0f} ohm")
    print(f"RE = RE1 + RE2 = {VE:.0f} / {IC*1e3:.0f} mA = {d['RE']:.0f} ohm")
    print(f"IB = {IC*1e3:.0f} mA / {beta} = {d['IB']*1e3:.1f} mA")
    print(f"VB = {VE:.0f} + {Vbe} = {d['VB']:.1f} V")
    print(f"RTH = {drop_rth} / {d['IB']*1e3:.1f} mA = {d['RTH']:.0f} ohm")
    print(f"VTH = {d['VB']:.1f} + {drop_rth} = {d['VTH']:.1f} V")
    print(f"R2 = 2 x RTH = {d['R2']:.0f} ohm")
    print(f"R1 = R2 x ({Vcc:.0f} - {d['VTH']:.1f}) / {d['VTH']:.1f} = {d['R1']:.0f} ohm")
    print(f"RE1 = RC / G = {d['RC']:.0f} / {gain} = {d['RE1']:.0f} ohm")
    print(f"RE2 = RE - RE1 = {d['RE']:.0f} - {d['RE1']:.0f} = {d['RE2']:.0f} ohm")

    IC_a, VC_a, VE_a, VCE_a = actual_bias(Vcc, d["R1"], d["R2"], d["RC"], d["RE"], beta, Vbe)
    print(f"DC check with these resistors: IC = {IC_a*1e3:.2f} mA, VC = {VC_a:.2f} V, "
          f"VE = {VE_a:.2f} V, VCE = {VCE_a:.2f} V")


def plot_results(Vcc, IC, beta, VC, VE, Vbe, drop_rth, gain):
    d = design_amplifier(Vcc, IC, beta, VC, VE, Vbe, drop_rth, gain)

    t = np.linspace(0, 2e-3, 1000)
    vin = 0.5 * np.sin(2 * np.pi * 1e3 * t)
    vc = VC - gain * vin

    VCE_sweep = np.linspace(0, Vcc, 100)
    load_line = (Vcc - VCE_sweep) / (d["RC"] + d["RE"])

    plt.figure(figsize=(11, 4.2))

    plt.subplot(1, 2, 1)
    plt.plot(t * 1e3, vin, label="VIN (ac, 1 V p-p)")
    plt.plot(t * 1e3, vc, label="Collector voltage (8 V dc + ac)")
    plt.axhline(10, linestyle=":", color="gray")
    plt.axhline(6, linestyle=":", color="gray")
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (V)")
    plt.title("Amplifier waveforms, gain = 4")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(VCE_sweep, load_line * 1e3, label="DC load line")
    plt.plot(VC - VE, IC * 1e3, "ro", label="Q point (4 V, 10 mA)")
    plt.xlabel("VCE (V)")
    plt.ylabel("IC (mA)")
    plt.title("Load line and operating point")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("circuit6_transistor_amplifier.png", dpi=200)
    plt.show()


def main():
    Vcc, IC, beta, VC, VE = 12.0, 10e-3, 100, 8.0, 4.0
    Vbe, drop_rth, gain = 0.6, 0.4, 4
    print_results(Vcc, IC, beta, VC, VE, Vbe, drop_rth, gain)
    plot_results(Vcc, IC, beta, VC, VE, Vbe, drop_rth, gain)


if __name__ == "__main__":
    main()
