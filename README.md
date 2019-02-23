# Dublin Bikes

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

## How do I make contributions?
To make contributions to this project::

1) Clone the repository and create a feature branch from 'develop'.
2) When you're happy for others to see and review your changes, create a pull request with develop as the base (it should default to that anyway).
3) Once it's reviewed by another developer, you can merge your changes to 'develop'.

Towards the end of the sprint, or other production milestones, a release version is merged from 'develop' to 'master' with a suitable versioned tag.
