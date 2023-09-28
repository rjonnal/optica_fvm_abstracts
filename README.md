# optica_fvm_abstracts
Python script to convert abstract submission CSV file into XML files using JOV templates.

## Instructions:

1. Add a column called 'Session' to the Google Spreadsheet. This column should contain integer values indicating the session in which the presentation was given. These numbers will determine the order of the abstracts, so use the number 1 for any award lectures, and order the rest of the sessions chronologically.

2. Edit `config.py` such that the session numbers established in #1 above have meaningful session titles. Also edit the values for `volume`, `issue`, and `month` according to instructions from [Debbie Chin](mailto:dchin@arvo.org). Also edit the name of the folder where you want to save the abstract XML files.

3. Download the Google Spreadsheet as a CSV file, and place it in this directory. Assume it's called `google_sheets_abstracts_2023.csv`.

4. We need to make a new CSV file with shortened column headers. To do this and create a new CSV with shortened headers called `abstracts_for_processing.csv` run:

    ```python shorten_headers.py google_sheets_abstracts_2023.csv abstracts_for_processing.csv```
  
    This will replace the headers using the dictionary in `field_nicknames.py` and output a file called `abstracts_for_processing.csv`
  
5. Run `process_abstracts_csv.py abstracts_for_processing.csv`. This will create a folder (specified in `config.py`) and write your XML files there.
