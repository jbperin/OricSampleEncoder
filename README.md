# Sample Tweaker 
A small utility app to convert audio file for Oric replaying

## Overview
SampleTweaker is a utility application to help converting audio files from various audio format into C and/or ASM buffer for inclusion into Oric application.

## Setup
To run the script as a Python script:
1. Clone the repository to your local computer
2. Change to repository directory: `cd SampleTweaker`
3. Create a Python Virtual Environment: `python -m venv env`
4. Activate the Virtual Environment: `source env/bin/activate` or
   `env\Scripts\activate.bat`
5. Install dependencies: `python -m pip install -r requirements.txt`
6. Run the app: `python ./app.py`

## Usage

pyinstaller -F SampleTweaker.py

