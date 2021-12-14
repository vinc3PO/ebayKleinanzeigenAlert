# ebayKleinanzeigenAlert - (ebAlert)
Small CLI program that will send you a Telegram message for every new posts on the specific links of the Ebay Kleinanzeigen website. 

No API required - Only URL of the query.

## Install
* Download folder or clone
* cd yourself to the main directory
* create a telegram bot -> https://core.telegram.org/bots
* Hard code your telegram API key and messageID in the telegramclass.py file.
* Install or run straight from the directory.
  * install with ````pip install .  ````
  * run with ````python -m ebAlert ````

## Usage & Example
* ```ebAlert links [opts] ``` to show, add, remove links
* ```ebAlert links --help ``` to get list of options for the links
  
* ```ebAlert start``` to start receiving notification


* ```ebAlert links -a "https://www.ebay...k0l9354r20"```  This assumes that you just had a look through the web page already, so no notification will be send. 
* Typically, this would be run as a cron job on an hourly basis.

## Requirements
* A telegram bot API token and your personal conversation id
* Python 3
* click, requests, bs4 and sqlalchemy (arguably sqlalchemy is a little overkill for that purpose)

## ChangeLog
 0.6 -> 1.0
* Refactoring.
* Add TOKEN and CHAT_ID taken from environment variable. 
* Fix title and city and distance if so.
* Update telegram message.  

## Future Plans

* add functionality to add links directly via telegram.

## Development Branch

** dev_telegram **
* Bot data stored in the database
* Multibot allowed
* Possibilite to choice towards which bot goes which notification
* Docker