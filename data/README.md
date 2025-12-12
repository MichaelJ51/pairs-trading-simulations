# Data Folder

You can either:

1. Place your own historical price data files here and run the script in **file mode**, or
2. Ignore this folder and use the **automatic download mode** with Yahoo Finance.

## File mode

Expected format for CSV or Excel:

- One row per date
- Column for the date (e.g., `Date`)
- Columns for each asset (e.g., `AAPL`, `MSFT`)

Example CSV:
I have provided 30 days sample feel free to add you own data set. 

Date,AAPL,MSFT
2023-01-02,130.03,239.82
2023-01-03,125.07,234.53
...

Then run:
ex: python -m examples.run_pairs_trading --file data/aapl_msft_sample.csv --asset1 AAPL --asset2 MSFT --file-type csv
```bash
python examples/run_pairs_trading.py \
  --file data/my_pair.csv \
  --asset1 AAPL \
  --asset2 MSFT \
  --file-type csv
```
