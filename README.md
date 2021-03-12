# ebayKleinanzeigenAlert - (ebAlert)
Small CLI program that will send you an a Telegram message for every new posts on the specific links of the Ebay Kleinanzeigen website. 

No API required - Only URL of the query.

## Install
* Download folder or clone
* cd yourself to the main directory
* Hard code your telegram API key and messageID in the telegramclass.py file.
* Install or run straight from directory.
  * install with ````pip install .  ````
  * run with ````python -m ebAlert ````

## Usage & Example
* ```ebAlert links [opts] ``` to show, add, remove links
* ```ebAlert links --help ``` to get list of options for the links
  
* ```ebAlert start``` to start receiving notification


* ```ebAlert links -a "https://www.ebay...k0l9354r20"``` Assuming you just look through the web page while copy no notification will be send. 
* Typically run as a cron job on an hourly basis.

## Requirements
* A telegram bot API token and your personal conversation id
* Python 3
* click, requests, bs4 and sqlalchemy (arguably sqlalchemy is a little overkill for that purpose)

## Future Plans

* add functionality to add link through telegram.