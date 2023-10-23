# optica_fvm_abstracts
Python script to convert abstract submission CSV file into XML files using JOV templates.

## Instructions for generating abstract XML:

1. Add the following columns to the Google Spreadsheet*:

  a. 'Session': this column should contain integer values indicating the session in which the presentation was given. These numbers will determine the order of the abstracts, so use the number 1 for any award lectures, and order the rest of the talk sessions chronologically, and end up with the poster sessions chronologically. To have different headings for the award lectures, you can use, use 0 and 1 to specify Tillyer and Boynton lectures.
  
  b. 'Order': this column should specify the order of talks or posters within each session. If it's a talk session with six talks, they should have values 1-6.
  
  c. 'abstract_number': after sorting the spreadsheet by 'Session' first and 'Order' second, assign numbers 1-N to the sorted abstracts. It's critical that these numbers uniquely identify abstracts from any given meeting (for later DOI assignment) and ideally these will be ordered sensibly. If the 'Session' value for the award lectures are lowest (e.g. 0, and 1), then the award lecture abstracts will appear first, followed by the rest of the sessions, ordered chronologically. In 2023, we put the poster abstracts after all the talks.

2. Edit `config.py` such that:

  a. The session numbers established in #1 above have meaningful session titles.
  
  b. The values for `volume`, `issue`, and `month` accord with instructions from [Debbie Chin](mailto:dchin@arvo.org). 
  
  c. The name of the folder where you want to save the abstract XML files is correct.
  
  d. `max_authors` is set to the maximum number of authors permitted in the Google Form.

3. Download the Google Spreadsheet as a CSV file, and place it in this directory. Assume it's called `abstracts_long_headings_2023.csv`.

4. We need to make a new CSV file with shortened column headers. To do this and create a new CSV with shortened headers called `abstracts_short_headings_2023.csv` run:

    ```python shorten_headers.py abstracts_long_headings_2023.csv abstracts_short_headings_2023.csv```
  
    This will replace the headers using the dictionary in `field_nicknames.py` and output a file called `abstracts_short_headings_2023.csv`
  
5. Run `process_abstracts_csv.py abstracts_short_headings_2023.csv`. This will create a folder (specified in `config.py`) and write your XML files there.

6. Running the Python script will also generate an HTML file (with filename specified in `config.py`) containing HTML versions of the abstracts. These may be useful for generating the online program.

## Instructions for generating YIA ballots:

1. Create a CSV file called `sessions.csv` containing four columns: `number`, `day`, `time`, and `type`. This table is meant to connect the keys for the `sessions` dictionary in `config.py` with the day and time of presentations, so that ballots can contain the latter information. It should look like this:

```
number,day,time,type,
0,Fri,1700,talk,
1,Sat,1545,talk,
2,Fri,815,talk,
.
.
.
```

1. `python csv_to_yia_ballots.py abstracts_2023_shortened_headers.csv > ballots.md`

2. `pandoc --pdf-engine=xelatex -V geometry:margin=1in -o ballots.pdf ballots.md` (or whatever markdown rendering system you prefer.
