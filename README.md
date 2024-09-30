# Programming_Exercise

## Overview
This application reads data from `trainings.txt` and generates three output JSON files:

1. **`output1.json`**: Lists each completed training with a count of how many people have completed it.
2. **`output2.json`**: For specified trainings and a fiscal year, lists people who completed those trainings in that fiscal year.
3. **`output3.json`**: For a given date, finds people with expired or soon-to-expire trainings.

## Prerequisites
- Python3
- `dateutil` library (for `relativedelta`)

## Setup
1. Clone the repository: git clone <repository_url>
2. Navigate to the cloned folder.
3. Run the application: python3 app.py

## Outputs
The output files will be saved in the root directory as:
- `output1.json`
- `output2.json`
- `output3.json`
