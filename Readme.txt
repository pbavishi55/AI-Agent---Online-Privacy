# Data Broker Opt-Out Automation

This project automates the process of submitting opt-out requests to various data broker websites. It uses Selenium to interact with web forms and requests to check if a phone number exists on a broker's site.

## Prerequisites

- Python 3.x
- Google Chrome browser
- ChromeDriver (ensure it is installed and added to your system's PATH)

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages:

    ```bash
    pip install selenium requests beautifulsoup4
    ```

## Usage

1. Open the [import time.py](http://_vscodecontentref_/0) file.
2. Run the script:

    ```bash
    python import\ time.py
    ```

3. Enter the phone number and email when prompted.

## Script Details

### List of Known Data Broker Opt-Out URLs

The script contains a list of known data broker opt-out URLs:

```python
DATA_BROKER_URLS = [
    "https://www.spokeo.com/optout",
    "https://www.mylife.com/ccpa",
    "https://www.truepeoplesearch.com/removal",
    # Add more data brokers here
]