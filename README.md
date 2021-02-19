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


## Installing
**Python 3.8 or higher is required**


````
# Linux
git clone https://github.com/Gliger13/three_microservices.git
cd three_microservices
python setup.py install
````


## Author

Made by Andrei Zaneuski (@Gliger13), Belarus, Minsk as task
