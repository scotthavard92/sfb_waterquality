import csv
import requests
from typing import List


ALAMEDA_SOURCE_URL = "https://www.ndbc.noaa.gov/data/realtime2/AAMC1.txt"
ALAMEDA_OUTPUT_FILE = "AAMC1.csv"
SF_SOURCE_URL = "https://www.ndbc.noaa.gov/data/realtime2/FTPC1.txt"
SF_OUTPUT_FILE = "FTPC1.csv"
MAX_ROWS = 5


def fetch_text(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def parse_ndbc_text(text: str, max_rows: int = MAX_ROWS) -> tuple[list[str], list[list[str]]]:
    """
    Parse NDBC realtime text format.

    Returns:
        headers: List of column names
        rows: Parsed data rows (limited to max_rows)
    """
    lines = text.strip().splitlines()

    header_line = None
    data_rows = []

    for line in lines:
        if not line.strip():
            continue

        # Column names (first commented line)
        if line.startswith("#") and header_line is None:
            header_line = line.lstrip("#").strip()
            continue

        # Skip other comment lines
        if line.startswith("#"):
            continue

        # Stop once we reach the row limit
        if len(data_rows) >= max_rows:
            break

        data_rows.append(line.split())

    if header_line is None:
        raise ValueError("No header row found in data")

    headers = header_line.split()
    return headers, data_rows


def write_csv(headers: List[str], rows: List[List[str]], output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    # Alameda
    a_raw_text = fetch_text(ALAMEDA_SOURCE_URL)
    a_headers, a_rows = parse_ndbc_text(a_raw_text)
    write_csv(a_headers, a_rows, ALAMEDA_OUTPUT_FILE)

    #SF
    sf_raw_text = fetch_text(SF_SOURCE_URL)
    sf_headers, sf_rows = parse_ndbc_text(sf_raw_text)
    write_csv(sf_headers, sf_rows, SF_OUTPUT_FILE)

if __name__ == "__main__":
    main()
