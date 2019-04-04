# Dublin Bikes

[![Build Status](https://travis-ci.com/patrickjkennedy/dublin_bikes.svg?token=AMDCQxDUHNS5cqZyzh6o&branch=develop)](https://travis-ci.com/patrickjkennedy/dublin_bikes)

## Introduction
Welcome to the repository for Dublin Bikes - a software engineering group project developed by
[Kieran Curtin](https://github.com/curtinkieran), [Moriah Fiebiger](https://github.com/mofiebiger)
and [Patrick Kennedy](https://github.com/patrickjkennedy) as part of COMP30830 Software Engineering at University
College Dublin. This document outlines what the project is, what this repository contains, and how to navigate through it.

## What is it?
The goal of our project was to develop a web application to display occupancy and weather information for Dublin Bikes.

## What's in this repository?
It comprises a Flask application for the web application, as well as a data analysis component of a web scraper and
machine learning model.

## How do I navigate through this repository and make contributions?
This project uses a monolithic repository structure, with the following branching strategy. The 'master' branch consists of production-ready, deployable code. These are tagged using semantic versioning (e.g. MAJOR.MINOR.PATCH). The 'develop' branch is the 'work-in-progress' branch, that all feature branches are taken from and merged back into. Feature branches are signified with a 'feature-' prefix.

# Running the Dublin Bikes Flask Web Application Locally

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

## How do I make contributions?
To make contributions to this project::

1) Clone the repository and create a feature branch from 'develop'.
2) When you're happy for others to see and review your changes, create a pull request with develop as the base (it should default to that anyway).
3) Once it's reviewed by another developer, you can merge your changes to 'develop'.

Towards the end of the sprint, or other production milestones, a release version is merged from 'develop' to 'master' with a suitable versioned tag.
