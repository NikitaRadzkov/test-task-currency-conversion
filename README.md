# Currency Conversion

This repository contains code for fetching exchange rate data from the European Central Bank (ECB) API and performing currency conversion.

## Requirements

- Python 3.7+
- pandas library
- requests library

## Installation

1. Navigate to the project directory:

   ```bash
   cd test-task-currency-conversion
   ```

2. Install the required dependencies:

   ```bash
   pipenv sync
   ```

## Usage

The service provides three main functions:

1. `get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame`

Fetches the exchange rate data from the ECB API for the specified source and target currencies.

* source: The source currency code (e.g., "USD").
* target: The target currency code (default is "EUR").
Returns a Pandas DataFrame containing the exchange rate data.

Example usage:

```python
exchange_rate = get_exchange_rate("GBP", "EUR")
print(exchange_rate)
```

2. `get_raw_data(identifier: str) -> pd.DataFrame`

Fetches the raw data from the ECB API for the specified identifier.

* **identifier**: The identifier for the data to fetch.
Returns a Pandas DataFrame containing the raw data.

Example usage:

```python
raw_data = get_raw_data("example_identifier")
print(raw_data)
```

3. `get_data(identifier: str, target_currency: Optional[str] = None) -> pd.DataFrame`

Fetches the raw data from the ECB API for the specified identifier and performs optional currency conversion.
* **identifier**: The identifier for the data to fetch.
* **target_currency**: The target currency code for conversion (default is None).

Returns a Pandas DataFrame containing the processed data.

Example usage:

```python
data = get_data("example_identifier", "GBP")
print(data)
```


## Running the Tests

To run the tests, execute the following command:

   ```bash
   pytest
   ```

By default, pytest will discover and run all the test files in the current directory and its subdirectories.
The test results will be displayed in the terminal.

If you want to generate a detailed test report with coverage information, you can use the following command:

   ```bash
   pytest --cov
   ```

This command will generate a coverage report that shows the percentage of code coverage for your tests.
