# SI507
final project of si507, Pokemon teammate finder

## Files
### project_final_data.py
This file contains the code of data processing. I used Beautifulsoup to scrap a page from https://www.smogon.com/ and requests package. 
csv files are all downloaded from https://www.kaggle.com/, json files are downloaded from https://www.smogon.com/.
No api key is needed. 
I process the data source seperately and store them into my computer, so there may be some duplicate code. You can find the raw data and modified data in this repo.

### project_final_play.py
Thsi file contains the code of using my modified data. Just run it and follow the instructions.
You have 6 options. It may be not useful for Pokemon specialists. Just have fun!

### raw data
pokedex.csv: data of 898 species and all forms (mega and regional form)
vgc202110.csv, vgc202111.csv, vgc-series7_2021-01-usage_formatted.csv : Pokemon usage rate in VGC battle in Pokemon showdown
gen8vgc2021series11-1760.json : 291 Pokemon data in VGC battle in Pokemon showdown

### final modified data
pokename.json: a list of all Pokemon species
pokepair.json: a dictionary of Pokemon data and the recommend teammates



