# Application Pages

This directory contains the individual Python scripts that serve as the pages for the multi-page Streamlit application.

## Naming Convention

The files are named using a `NUMBER_NAME.py` convention. Streamlit uses this naming scheme to automatically create a sidebar for navigation, ordering the pages based on the number and using the file name (with underscores replaced by spaces) as the display title.

For example, `1_Overview.py` becomes the first link in the sidebar, displayed as "Overview".

## Pages

-   `1_Overview.py`: The main dashboard for the financial portfolio, showing top-level metrics and visualizations.
-   `2_Cash.py`: A detailed deep-dive into cash assets.
-   `3_Investments.py`: A detailed deep-dive into investment assets.
-   `4_Pensions.py`: A detailed deep-dive into pension assets.
-   `5_All_Assets.py`: A consolidated view that combines all financial assets into a single table.
-   `6_Cars.py`: The dashboard for the Car Equity Tracker, featuring detailed financial analysis for vehicles. 