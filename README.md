# PokeAPI

This API is used to return the statistics values over all the Pokemon's Berries

## How to run

* Download `python =<3.10.4` from: `https://www.python.org/downloads/`
* Clone repository from: `https://github.com/Stijerino/pokeAPI.git`
* Open a terminal from the root repository folder and install the requirements with: `pip install -r requirements.txt`
* Install project dependencies using: `poetry install` && `poetry update`
* To run the project execute: `poetry run python ./main.py` or `poetry run python .\main.py` depending on the OS

## Endpoints

For this API the current available endpoint is `/allBerryStats`, which consumes 
from an external Pokemon API and processes the information into statistics values.