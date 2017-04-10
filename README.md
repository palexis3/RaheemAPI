# ${1:RaheemAPI ReadCSV}

The ReadCSV python script reads a CSV file within the same directory path and gathers the longitude and
latitude from the CSV to generate "good" dummy data up to max 1000 objects to, thereafter post to the staging Raheem API.

## Dependencies
Python 2.7.9

After installing Python 2.7, you can install the libraries posted below using :
`pip install 'LIBRARY'`

Install the following third-party libraries :
`requests`
`pandas`
'jsonurl`
'itertools`
`urllib`

## Requirements

The CSV file to be parsed must be within the same directory as the ReadCSV.py script. 
The script will not post to the Raheem API without internet connection.

## Run
To run the ReadCSV script, simply make sure you're in the same directory of the script and type into your terminal :

python ReadCSV.py -i `YOUR CSV FILE.csv` -count `NUM`

where `YOUR CSV FILE.csv` is the name of the CSV file to be processed and `NUM` is the amount of objects to be produced.
Note: `NUM` can be at maximum 1000.


