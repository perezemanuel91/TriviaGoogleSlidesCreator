# TriviaGoogleSlidesCreator 
*Updated 12/05/2020

## Prequisites:
- Google Sheets with all trivia information (optional, since you can use the sample sheet) 
- virtualenv (optional)
- python, pip

## Steps (Overview):
- Install all dependencies 
- Get credentials
- Run playground.py

## 0. Installing dependencies
Install python3 and virtualenv (if using a virtual environment).

Run the following commands to download the packages in the root directory. 

python3 -m venv venv/

source venv/bin/activate (if using Unix or MacOS)

source venv/Scripts/activate (if using Windows)

pip3 install -r requirements.txt

## 1. Getting credentials
Follow Step 1 of Python Quickstart for both [Google Slides](https://developers.google.com/slides/quickstart/python) and [Google Sheets](https://developers.google.com/sheets/api/quickstart/python). When downloading the 'credentials.json' files, rename them 'credentials_slides.json' and 'credentials_sheets.json' respectively and place into the root directory of this repo.

## 2. Running playground.py: Create the presentation!
Run "python3 playground.py {presentation id} {name of tab}" eg. python3 playground.py "12nghSvz4o_SzHWEF-XykQ4sAzZ1ofR8vR6RArQhV_M0" "Sheet1"

Both the presentation id and name of first tab are optional. Running without any parameters uses the default '12nghSvz4o_SzHWEF-XykQ4sAzZ1ofR8vR6RArQhV_M0'and 'Sheet1' respectively. 

(If the URL is https://docs.google.com/spreadsheets/d/12nghSvz4o_SzHWEF-XykQ4sAzZ1ofR8vR6RArQhV_M0/, then the id is 12nghSvz4o_SzHWEF-XykQ4sAzZ1ofR8vR6RArQhV_M0)

You will be prompted to give access to your gmail to read/write Google Slides and Sheets. Once you give permission successfully, token_sheets.pickle and token_slides.pickle should appear in your repo. The presentation should then appear in your Google Drive folder!

You can manage your credentials at https://console.developers.google.com/apis/dashboard

## Trivia Google Sheets Formatting
See https://docs.google.com/spreadsheets/d/12nghSvz4o_SzHWEF-XykQ4sAzZ1ofR8vR6RArQhV_M0/ for a sample spreadsheet

The first line contains at least two elements, the title and author (in that order). Anything after that will be ignored. 

The second line is optional. It contains headers to clarify the content of the columns. If not using, line should be left blank. 

The rest of the lines are either Round rows or Question rows. 

Round rows require at least 2 elements: the round type and number joined together and the round title. You can add an optional (and only) 3rd element: a description of the round. The round type and number are represented as {Round Type}{Round Number} eg. R1

Currently, there are 2 Round Types: R(egular) and B(ullet). R is a straightforward slide with a title and a body. This is the most common format. B is a special case where the body only contains bulleted items. 

Question rows include 4 elements: the question number, the question, the answer, and the number of points. 

## Trivia Google Slides Output Produced

See https://docs.google.com/presentation/d/1IsrE0cdgh3ikepu1sitMZYHiZ1CxBLObz0ZS_xdSydM/ for the sample output. 

Right now, the first slide is unforunately an empty slide (but you can easily delete it :D)

What follows is the following:

- Title/Author Slide
- Summary of all the rounds Slide (with point totals)
- Rounds and Questions 
    - Rounds start with a Round Number + Name / Summary (if applicable) slide
    - Each question maps to 3 slides with different bodies that share a Round Title
        - The Round Title includes the round number, round name, question number, and the number of points the question is worth
        - The bodies of the 3 slides contain the question, a filler body ("AND THE ANSWER IS..."), and the answer. 

