# JCDecaux & OpenWeatherMap API Scraper

This directory contains scripts that query both the JCDecaux Dublin Bikes and OpenWeatherMap APIs and writes the response to a MySQL database. 
Please note that the database needs to be created in advance of running the script, with the column names specified in the
script. For further discussion around the database and the reasoning of it's column types etc., please see this
Google Document:
https://docs.google.com/document/d/1S93vuhNOTOamthBR9mcUg1IaO3tfUsxxOa3TP0FvkL4/edit?usp=sharing

## API Key
Before running the script yourself, please insert the correct credentials, your own API keys, and the names for your database and table.

To request a JCDecaux API key head to https://developer.jcdecaux.com.

For an OpenWeatherAPI key, head to https://openweathermap.org/api.

## How do we get it to run every 5 minutes?
To get the script to run every 5 minutes, you can set it to run as a cronjob on the server. To create a job, type the following in your terminal:
```
crontab -e 
```
You can then insert the following line of code:
```
*/5 * * * * /anaconda3/envs/scraper/bin/python /Users/patrick/dublin_bikes/scraper/scraper.py
```

Where `*/5 * * * * ` specifies that the program is to be ran every 5 minutes,
`/anaconda3/envs/scraper/bin/python` is the Python interpreter from the Conda environment we want to use,
And `/Users/patrick/dublin_bikes/scraper/scraper.py` is the full path to the script.

## Creating a Conda environment from a requirements.txt
First, create your Conda environment (e.g. scraper_prototype) as follows:

```
conda create -n scraper python=3.7
```

Activate your new environment with `conda activate scraper` and install the required Python packages using the command:
```
pip install -r requirements.txt
```
