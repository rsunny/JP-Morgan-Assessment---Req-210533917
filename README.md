# Global Beverage Corporation Exchange

This project is designed to manage and analyze stock data. It includes classes and methods to represent stocks, trades, and calculate a few financial metrics such as dividend yield, PE ratio, and volume-weighted stock price. Additionally, the project includes a Global Beverage Corporation Exchange (GBCE) class to manage multiple stocks and calculate the GBCE All Share Index, which is a measure of the overall performance of the stock market.

## Requirements

- Python 3.9+
- pip
- Docker (optional)

## Setup (non docker)

### 1. Install Dependencies

Before executing this command, it is recommended to create a python environment

```bash
make install # installs the requirements
```

### 2. Run the tests

To run the tests, use the following command

```bash
make test # executes the pytests
```

## Setup (docker)

### 1. Build docker image

```bash
make docker-build # a docker image named gbce-prasanth is created
```

### 2. Execute the container which runs the tests

```bash
make docker-run # executes the docker image and runs the tests
```

# Assumptions

- If the `price` is 0, the `dividend_yield` is 0.
- If the `dividend_yield` is 0 or the `price` is 0, the `pe_ratio` is 0.
- If the `quantity` is 0, the `volume_weighted_stock_price` is 0.
- Quantity is not `added or subtracted` based on the trade's `buy` or `sell` aspect. It is always `added`.
- Trades added to the stock are not in a `time series` order.

  ## Approach 1 (Trades are not added in timeseries order) (Assumed):

  - Since trades are not added in a time series order, the trade timestamps and trade details are pushed as a tuple into a `min-heap`.
  - This allows us to pre-compute the volume_weighted_stock_price every time a trade is added, in constant time.
  - When the volume_weighted_stock_price is requested, we efficiently remove older trades from the heap, helping to compute the current volume_weighted_stock_price.
  - This approach has an extra `O(n) memory complexity` and an `asymptotic time complexity of O(log n)` for each volume_weighted_stock_price computation, where n is the number of trades.

  ## Approach 2 (Trades are added in timeseries order):

  - If the trades are in a time series order, a `simple pointer` can be used to keep moving forward until it reaches the trade within the 5-minute range.
  - The volume_weighted_stock_price is still precomputed every time a trade is added.
  - While moving the pointer, the volume_weighted_stock_price value is adjusted by removing the trades that fall outside the desired range.
  - This approach requires `no extra memory` and has an `asymptotic time complexity of constant time` for each volume_weighted_stock_price computation.

  ### Note:

  In both approaches, the trades are `not lost`; all trades are stored in a private list variable. They can be fetched at any point using the get_trades method.

## Usage:

- There is no main.py or a driver file to create objects and load data into memory. However, a comprehensive set of test fixtures and scenarios are included to test the classes, features, and data loading functionality.
- GBCE have load_stocks, when called load all the stocks from the data/stocks.
