# JCDecaux API Scraper Prototype

This repository contains a script that queries the JCDecaux Dublin Bikes API and writes the response to a MySQL database. 
Please note that the database needs to be created in advance of running the script, with the column names specified in the
script. For further discussion around the database and the reasoning of it's column types etc., please see this
Google Doc.

## API Key
I've removed my personal API key, as well as other sensitive credentials from the script. Before running the script yourself,
please insert the correct credentials, your own API key, and the names for your database and table.

## How do we get it to run every 5 minutes?
To get the script to run every 5 minutes, we use the crontab Unix program. To create a job, type the following in your terminal:
```
crontab -e 
```
You can then insert the following line of code:
```
*/5 * * * * /anaconda3/envs/scraper_prototype/bin/python /Users/patrick/hdip/comp30830_software_engineering/scraper_prototype/scraper.py
```

Where `*/5 * * * * ` specifies that the program is to be ran every 5 minutes,
`/anaconda3/envs/scraper_prototype/bin/python` is the Python interpreter from the Conda environment we want to use,
And `/Users/patrick/hdip/comp30830_software_engineering/scraper_prototype/scraper.py` is the full path to the script.

