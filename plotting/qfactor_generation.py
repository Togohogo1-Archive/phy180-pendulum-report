import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from pylab import loadtxt


def damped_sinusoid(t, a, tau, T, phi):
    return a*np.exp(-t/tau)*np.cos(2*np.pi*t/T+phi)


def exponential(t, a, tau):
    return a*np.exp(-t/tau)


def linear(t, m, b):
    return m*t+b


def quadratic(t, a, b, c):
    return a*t*2 + b*t + c


def powerlaw(t, a, b):
    return a*t**b

for i in range(1, 10):
# for i in range(4, 5):
    qfactor_txt_idx = i  # CHANGE REQUIRED
    init_tau = 120  # CHANGE REQUIRED?

    filename=f"qfactor_txt_files\\len{qfactor_txt_idx}.txt"
    # filename="max_amplitude_vs_time.txt"

    # Periods array, each index corresponds to txt file
    periods = [-1, 0.686666667, 0.84000, 0.92667, 1.00667, 1.11333, 1.19333, 1.27333, 1.33333, 1.40667]
    T = periods[qfactor_txt_idx]

    print("Approximate length:", (T/(2*np.pi))**2 * 9.81)


    def main():
        my_func = exponential

        plt.rcParams.update({'font.size': 14})
        plt.rcParams['figure.figsize'] = 10, 9

        data=loadtxt(filename, usecols=(0,1,2,3), skiprows=1, unpack=True)

        xdata = data[0]
        ydata = data[1]
        xerror = data[2]
        yerror = data[3]

        # [CHANGE REQUIRED] for 2nd value?
        init_guess = (ydata[0], init_tau)

        popt, pcov = optimize.curve_fit(my_func, xdata, ydata, sigma=yerror, p0=init_guess)

        a=popt[0]
        tau=popt[1]
        u_a=pcov[0,0]**(0.5)
        u_tau=pcov[1,1]**(0.5)

        start = min(xdata)
        stop = max(xdata)
        xs = np.arange(start,stop,(stop-start)/1000)
        curve = my_func(xs, *popt)

        fig, (ax1,ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})

        ax1.errorbar(xdata, ydata, yerr=yerror, xerr=xerror, fmt=".", label="data", color="black")
        ax1.plot(xs, curve, label="best fit", color="black")
        ax1.legend(loc='upper right')
        ax1.set_xlabel("xdata")
        ax1.set_ylabel("ydata")
        ax1.set_title("title")

        #ax1.set_xscale('log')
        #ax1.set_yscale('log')

        print("A:", a, "+/-", u_a)
        print("tau:", tau, "+/-", u_tau)
        per_u_a = u_a/a
        per_u_tau = u_tau/tau
        Q = np.pi*tau/T
        print("Q factor:", Q, "+/-", max(per_u_a, per_u_tau)*Q)
        print()

        residual = ydata - my_func(xdata, *popt)
        ax2.errorbar(xdata, residual, yerr=yerror, xerr=xerror, fmt=".", color="black")
        ax2.axhline(y=0, color="black")
        ax2.set_xlabel("title")
        ax2.set_ylabel("[change] Difference between measured and fitted angle /s", wrap=True)
        ax2.set_title("Residuals of the fit")

        fig.tight_layout()
        plt.show()
        fig.savefig("graph.png")

        return None

    main()
