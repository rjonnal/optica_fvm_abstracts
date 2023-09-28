# optica_fvm_abstracts
Python script to convert abstract submission CSV file into XML files using JOV templates.

## Instructions for generating abstract XML:

1. Add a column called 'Session' to the Google Spreadsheet. This column should contain integer values indicating the session in which the presentation was given. These numbers will determine the order of the abstracts, so use the number 1 for any award lectures, and order the rest of the sessions chronologically. Alternatively, use 0 and 1 to specify Tillyer and Boynton lectures.

2. Edit `config.py` such that:

  a. The session numbers established in #1 above have meaningful session titles.
  
  b. The values for `volume`, `issue`, and `month` accord with instructions from [Debbie Chin](mailto:dchin@arvo.org). 
  
  c. The name of the folder where you want to save the abstract XML files is correct.
  
  d. `max_authors` is set to the maximum number of authors permitted in the Google Form.

3. Download the Google Spreadsheet as a CSV file, and place it in this directory. Assume it's called `google_sheets_abstracts_2023.csv`.

4. We need to make a new CSV file with shortened column headers. To do this and create a new CSV with shortened headers called `abstracts_for_processing.csv` run:

    ```python shorten_headers.py google_sheets_abstracts_2023.csv abstracts_for_processing.csv```
  
    This will replace the headers using the dictionary in `field_nicknames.py` and output a file called `abstracts_for_processing.csv`
  
5. Run `process_abstracts_csv.py abstracts_for_processing.csv`. This will create a folder (specified in `config.py`) and write your XML files there.


## Instructions for generating YIA ballots:

1. `python csv_to_yia_ballots.py abstracts_2023_shortened_headers.csv > ballots.md`

2. `pandoc --pdf-engine=xelatex -V geometry:margin=1in -o ballots.pdf ballots.md`
