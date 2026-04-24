import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    # Variant data
    n = 15
    S0 = 3000 + n * 50          # 3750
    S1_up = 3500 + n * 100      # 5000
    S1_down = 2600 + n * 50     # 3350
    K = S0
    N = 1
    a = 0
    B0 = 1
    B1 = 1

    # Model parameters
    beta = S1_up / S0 - 1
    alpha = S1_down / S0 - 1
    p_star = (a - alpha) / (beta - alpha)

    # Option payoff
    f_up = max(S1_up - K, 0)
    f_down = max(S1_down - K, 0)

    # Fair price
    C = (1 + a) ** (-N) * (f_up * p_star + f_down * (1 - p_star))
    X0 = C

    # Initial portfolio
    beta0 = 0
    gamma0 = X0 / S0

    # Hedge strategy
    gamma1 = (f_up - f_down) / (S0 * (beta - alpha))
    beta1 = X0 - gamma1 * S0

    # Hedge check
    X1_up = beta1 * B1 + gamma1 * S1_up
    X1_down = beta1 * B1 + gamma1 * S1_down

    # Output
    print("Seminar task 5")
    print(f"Variant n = {n}\n")

    print(f"S0 = {S0} грн")
    print(f"S1^up = {S1_up} грн")
    print(f"S1^down = {S1_down} грн")
    print(f"K = {K} грн")
    print(f"N = {N}, a = {a}, B0 = {B0}, B1 = {B1}\n")

    print(f"beta = {beta:.6f}")
    print(f"alpha = {alpha:.6f}")
    print(f"p* = {p_star:.6f}\n")

    print(f"f(S1^up) = {f_up:.2f} грн")
    print(f"f(S1^down) = {f_down:.2f} грн")
    print(f"Fair price C = {C:.2f} грн\n")

    print(f"X0 = {X0:.2f} грн")
    print(f"beta0 = {beta0:.6f}")
    print(f"gamma0 = {gamma0:.6f}\n")

    print(f"gamma1* = {gamma1:.6f}")
    print(f"beta1* = {beta1:.2f} грн\n")

    print("Hedge check:")
    print(f"X1 (up) = {X1_up:.2f} грн, payoff = {f_up:.2f} грн")
    print(f"X1 (down) = {X1_down:.2f} грн, payoff = {f_down:.2f} грн")

    # Folder for plots
    out_dir = Path("sem5_plots")
    out_dir.mkdir(exist_ok=True)

    # 1. Call option payoff at maturity
    s = np.linspace(2500, 5500, 400)
    payoff = np.maximum(s - K, 0)

    plt.figure(figsize=(8, 5))
    plt.plot(s, payoff)
    plt.axvline(K, linestyle="--")
    plt.xlabel("Ціна 100 USD у момент T, грн")
    plt.ylabel("Виплата опціону, грн")
    plt.title("Європейський call-опціон: функція виплати")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_dir / "01_option_payoff.png", dpi=160)
    plt.close()

    # 2. One-step price tree
    plt.figure(figsize=(7, 5))
    plt.plot([0, 1], [S0, S1_up], marker="o")
    plt.plot([0, 1], [S0, S1_down], marker="o")
    plt.text(0, S0, f"  S0 = {S0}")
    plt.text(1, S1_up, f"  S1^up = {S1_up}")
    plt.text(1, S1_down, f"  S1^down = {S1_down}")
    plt.xlim(-0.1, 1.2)
    plt.xticks([0, 1], ["t = 0", "t = 1"])
    plt.ylabel("Ціна 100 USD, грн")
    plt.title("Однокрокове біноміальне дерево ціни")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_dir / "02_price_tree.png", dpi=160)
    plt.close()

    # 3. Hedge portfolio value vs option payoff
    states = ["down", "up"]
    payoff_states = [f_down, f_up]
    hedge_states = [X1_down, X1_up]
    x = np.arange(len(states))
    width = 0.35

    plt.figure(figsize=(7, 5))
    plt.bar(x - width / 2, payoff_states, width, label="Виплата опціону")
    plt.bar(x + width / 2, hedge_states, width, label="Капітал хеджу")
    plt.xticks(x, states)
    plt.ylabel("грн")
    plt.title("Порівняння виплати опціону і капіталу хеджу")
    plt.legend()
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(out_dir / "03_hedge_check.png", dpi=160)
    plt.close()

    print(f"\nГрафіки збережено в папку: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
