# Schwab SPY Analysis

This project retrieves historical data for the SPY ETF using the Schwab Developer API and creates visualizations of its performance.

## Prerequisites

- Python 3.8+
- Schwab Developer API credentials
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yunallen/schwab-spy-analysis.git
   cd schwab-spy-analysis
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with your Schwab API credentials:
   ```
   SCHWAB_CLIENT_ID=your_client_id_here
   SCHWAB_CLIENT_SECRET=your_client_secret_here
   SCHWAB_REDIRECT_URI=your_redirect_uri_here
   ```

## Usage

Run the main script to fetch SPY data and generate visualizations:

```
python main.py
```

By default, this will:
- Retrieve 1 year of historical data for SPY
- Calculate various performance metrics
- Generate a visualization in `output/charts/`
- Save the raw and processed data in `output/data/`

## Configuration

You can modify the analysis parameters by editing the `main.py` file:
- Change the date range
- Adjust visualization settings
- Add or remove performance metrics

## Project Structure

- `src/schwab_analysis/`: Core functionality modules
  - `auth.py`: Authentication with Schwab API
  - `data.py`: Data retrieval functions
  - `analysis.py`: Data analysis functions
  - `visualization.py`: Plotting functions
- `output/`: Directory for saved results
  - `data/`: CSV files and other data exports
  - `charts/`: Generated visualizations

## License

[MIT License](LICENSE)