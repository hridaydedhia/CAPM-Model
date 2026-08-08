# CAPM (Capital Asset Pricing Model)

A Python implementation of the **Capital Asset Pricing Model** — calculates a stock's beta and expected return relative to the market, using two independent methods (covariance-based and regression-based), and visualizes the relationship with a fitted CAPM line.

## Overview

CAPM describes the relationship between a stock's risk (relative to the overall market) and its expected return:

```
E(R) = Rf + β(Rm − Rf)
```

Where:
- **E(R)** — expected return of the stock
- **Rf** — risk-free rate
- **β (Beta)** — the stock's sensitivity to market movements
- **Rm** — expected return of the market

This project pulls real historical price data, computes monthly log returns, derives beta two different ways, and plots the regression line that visually represents the model.

## Stocks Used

- **Stock**: `IBM`
- **Market benchmark**: `^GSPC` (S&P 500 Index)
- **Date range**: 2010–2026, resampled to **monthly** closing prices

## Tech Stack

- `numpy` — covariance, variance, and linear regression (`polyfit`)
- `pandas` — data handling, resampling, returns calculation
- `yfinance` — historical price data
- `matplotlib` — CAPM regression line visualization

## Methodology

**1. Data Collection & Resampling**
Daily price data is downloaded via `yfinance` and resampled to **month-end** frequency, since CAPM is typically estimated on monthly returns rather than daily ones (reduces noise from daily volatility).

**2. Log Returns**
Monthly log returns are calculated for both the stock and the market index:
```
return = log(price_t / price_t-1)
```

**3. Beta — Covariance Method**
```
β = Cov(stock, market) / Var(market)
```
Beta measures how much the stock moves relative to the market. A beta of 1 means the stock moves in line with the market; above 1 means it's more volatile than the market; below 1 means it's less volatile.

**4. Beta & Alpha — Regression Method**
A linear regression (`np.polyfit`) is fitted between market returns (x-axis) and stock returns (y-axis):
```
R_stock = β × R_market + α
```
This gives beta as the slope of the line and **alpha** as the intercept — the stock's return that isn't explained by market movement (i.e., excess performance).

**5. Expected Return**
Using the regression beta, the CAPM formula is applied with an assumed risk-free rate of 5% annualized:
```
E(R) = Rf + β × (annualized market return − Rf)
```

**6. Visualization**
A scatter plot of market return vs. stock return is generated, with the fitted regression line overlaid — this is the visual representation of the CAPM relationship, where the slope of the red line is beta.

## Installation

```bash
pip install numpy pandas yfinance matplotlib
```

## Usage

```bash
python CAPM.py
```

This will:
1. Download and resample IBM and S&P 500 price data (2010–2026)
2. Calculate beta using the covariance method
3. Calculate beta and alpha using linear regression
4. Print the expected return based on CAPM
5. Plot the regression line with data points

## Sample Output

```
Beta value is  0.87
Beta value from regression is  0.87
Alpha value is  0.0023
Expected return is  0.091
```

*(exact values will vary based on the data pulled at runtime)*

## Project Structure

```
├── CAPM.py         # CAPM class — data pipeline, beta calculation, regression, plotting
└── README.md
```

## Key Learnings

- Beta calculated via covariance/variance and via regression slope should match — a good sanity check that the model is implemented correctly.
- Alpha (the regression intercept) represents the stock's excess return not explained by market movement — the foundation of how "outperformance" is measured in finance.
- Monthly resampling is a deliberate choice — CAPM's assumptions hold better over longer return intervals than noisy daily data.

## Future Improvements

- [ ] Allow the risk-free rate to be pulled dynamically (e.g., current T-bill yield) instead of hardcoded
- [ ] Test the model across multiple stocks and compare betas
- [ ] Add a rolling beta calculation to see how a stock's risk profile changes over time
- [ ] Include R² of the regression to show how well the market explains the stock's returns

## Disclaimer

This project is for educational purposes only and does not constitute financial advice. Historical performance does not guarantee future results.

## Author

Built by Hriday as part of self-directed quant finance preparation.
