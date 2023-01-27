# BHSEC Schedule Reformatter

## Tool to reformat BHSEC's Round 2 course selection form to the DOE Schedule Software's format

## Usage
1) Create a `config.json` file with the following format.
    ```json
    {
      "School ID": "11X111",
      "School Year": "1",
      "Term ID": "1"
    }
    ```

2) Create an `input.csv` file that is the input spreadsheet. This can be an export 
   of a google spreadsheet.

3) Run the program with:
    ```commandline
    python main.py
    ```

4) The output will be in `output.csv`