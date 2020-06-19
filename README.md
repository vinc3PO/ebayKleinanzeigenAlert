# ebayKleinanzeigenAlert - (ebAlert)
Small CLI program that will send you an a Telegram message for every new posts on the specific links of the Ebay Kleinanzeigen website. 

## Install
* Hard code you telegram API and messageID on the the telegramclass.py file. 
* Download and unzip
* run ````pip install .  ````

## Usage
* ```ebAlert links [opts] ``` to show, add, remove links
* ```ebAlert alert``` to start the program

## Requirements
* telegram bot API
* python 3
* works on linux and windows
* click, bs4 and sqlalchemy 