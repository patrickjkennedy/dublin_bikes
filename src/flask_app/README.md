# Dublin Bikes Flask Web Application

This module contains the application code for the Dublin Bikes Flask Web Application. It consists of a front-end written in HTML, CSS and JavaScript. To launch the web application on your local host:

1. Create a Conda virtual environment as described in the next section below.
2. In the root directory setup the following environment variable by typing them into the console:
`export FLASK_APP=flask_app.py`
3. Add the config.py file to the `flask_app` directory. Consult with a developer on the team for access to this file.
4. To start the application type the `flask run` command from the root module directory. 

## Creating a Conda environment from a requirements.txt
First, create your Conda environment (e.g. flask_app) as follows:

```
conda create -n flask_app python=3.7
```

Activate your new environment with `conda activate flask_app` and install the required Python packages using the command:
```
pip install -r requirements.txt
```
