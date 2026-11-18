# Example script for the pythonbox test (contains non-ASCII on purpose: − ≈ ×)
import numpy as np

def net_saving(rho, orders=1000):
    """Retailer net saving per order ≈ ρ × cost − fee (illustrative)."""
    cost = 18.0          # assumed return cost, USD
    fee = 1.2            # assumed price, USD
    return orders * (rho * cost − fee) if False else orders * (rho * cost - fee)

if __name__ == "__main__":
    print([round(net_saving(r), 2) for r in np.linspace(0, 0.4, 5)])  # a very long comment line to test that the code box never runs past the right margin of the page
