# SF Bay Swim

**[SF Bay Swim](https://sfbayswim.info)** is a lightweight Python Flask web application that helps swimmers and open-water enthusiasts understand recent water quality conditions in the San Francisco Bay.

The site aggregates public testing data, highlights elevated bacteria levels, and provides environmental context (tides and weather) to support safer decision-making when recreating in open-water.

<img src="static/swimbug_blank.png" height=349px width=160px/>

## Water Quality 

SF Bay Swim presents **historical and recent water quality data** in a simple, visual format.

The application currently provides:

- Recent bacterial water quality test results
- Historical trends for bacteria counts
- Visual flags for samples with elevated bacteria levels
- Embedded tide and local weather data for additional context


### California Water Quality Data

Water quality data is pulled from a **[public California water quality testing database](https://data.ca.gov/dataset/surface-water-fecal-indicator-bacteria-results)**. This dataset includes laboratory results for bacterial indicators commonly used to assess recreational water safety.

The application:
- Retrieves new test results from the public source daily
- Normalizes and stores relevant fields locally
- Preserves historical test records for trend analysis


## Data Processing & Storage

To support fast queries and historical comparisons, the application:

1. Pulls raw test data from the public database
2. Extracts and normalizes select fields needed for display
3. Stores the processed data in a small, local database
4. Uses this database as the primary source for charts and summaries

This approach keeps the front-end responsive while preserving a clear lineage back to the original public data.


## Bacteria Level Flags

Test results from local agencies around the bay are **manually flagged** when bacteria levels exceed thresholds of concern.

These flags:
- Help draw attention to potentially unsafe conditions
- Are visually highlighted in charts and summaries
- Are intended as an informational signal, not a guarantee of safety



## Charts & Visualizations

The front end includes charts that show:

- Historical bacteria counts over time
- Recent trends at specific testing locations

These visualizations are designed to provide **context**, rather than point-in-time judgments.


## Environmental Context

To complement water quality data, the site includes embedded third-party visualizations:

- **Tide information** via iframe
- **Local weather conditions** via iframe

These elements help swimmers understand broader conditions that may affect water movement, exposure, and comfort.


## Important Disclaimer

SF Bay Swim is an **informational resource only**.

- Data may be delayed, incomplete, or subject to change
- Flagged or unflagged results do not guarantee safety
- Always use personal judgment and local guidance before entering the water


## Project Status

This project is actively evolving. Any input or interest in helping is welcome!


## Feedback

I welcome input and would love to hear from you if you have questions, feedback, or suggestions.
