@echo off
REM Activate the Flask venv
venv\Scripts\activate
REM Run Flask server
python app.py
REM Deactivate the Flask venv
venv\Scripts\deactivate
REM Run npm commands
cd C:\Users\JackBegley\source\repos\FantasyPremierLeague\client\src
npm start