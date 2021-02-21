# Three microservices
![Generic badge](https://img.shields.io/badge/version-0.0.0-green.svg) ![Generic badge](https://img.shields.io/badge/python-3.8-blue.svg) 

A project about the networking of three microservices: Reaper, Keeper, Master.
Also, microservices are deployed using Docker / docker-compose


### Reaper
 - scrapes data from websites
 - parses data
 - stores date using Keeper
 - provides API to Master to start scraping


### Keeper
 - manages a DB that stores date provided by Reaper
 - provides the interface for Master in order to retrieve data


### Master
 - gets data from Keeper
 - provides API to get the data
 - forces Reaper to run web scrapper

## API
All microservices provide API
##### GET
Any get request will return a list of available microservice commands.
##### POST
Through the post, you can give commands to the microservice, the json template of POST is:
````
json_data = {
    "command_name": ""
    "data": {}
}
````
### Available commands:
#### Reaper

 - start_scraping - starts scraping the website according to the specified parameters.

#### Keeper

 - save_data - save any json data contained in the request.
 - get_data - get data using piece of information.

#### Master

 - run_web_parser - sends a request to Reaper to start scraping.
 - get_data - sends a request to Keeper for get information.

## Installing and run
**Python 3.8 or higher is required**

Using docker:
````
# Linux
git clone https://github.com/Gliger13/three_microservices.git
cd three_microservices/
docker-compose build && docker-compose up -d
````

If you want to install the microservice, for example master, separately then:
````
# Linux
git clone https://github.com/Gliger13/three_microservices.git
cd three_microservices/master/
python setup.py install
python master/app.py
````

## Author

Made by Andrei Zaneuski (@Gliger13), Belarus, Minsk as task
