# ebayKleinanzeigenAlert - (ebAlert)
Small CLI program that will send you an a Telegram message for every new posts on the specific links of the Ebay Kleinanzeigen website. 

No API required - Only URL of the query.

## Install
* Hard code your telegram API key and messageID in the telegramclass.py file. 
* Download and unzip
* run ````pip install .  ````

## Usage & Example
* ```ebAlert links [opts] ``` to show, add, remove links
* ```ebAlert start``` to start receiving notification


* ```ebAlert links add "https://www.ebay...k0l9354r20"``` Assuming you just look through the web page while copy no notification will be send. 

## Requirements
* telegram bot API
* python 3
* works on linux and windows
* click, requests,bs4 and sqlalchemy 

## Future Plans

* add functionality to add link through telegram.