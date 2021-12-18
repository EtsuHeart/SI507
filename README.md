# SI507
final project of si507, Pokemon teammate finder

## Files
### project_final_data.py
This file contains the code of data processing. 
I used Beautifulsoup to scrap a page from https://www.smogon.com/ and requests package. No api key is needed. 
csv files are all downloaded from https://www.kaggle.com/, json files are downloaded from https://www.smogon.com/.
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

## Data structure
My data are in a graph. Each Pokémon species is a node. If this species is not frequently used in battles, or not suitable for a new battle player, I will not put it into my graph. 
Then if two species are suitable to be put in one team (judged by some conditions), these two nodes will be connected. 
The final modified data is pokepair.json which stores the pokemon data and recommended teammates.

## Interaction
Interaction is in **command line prompts**
user has 6 selections at first
1. Check the information and find a teammate for one species."
2. Find out whether two species are good to be teammates."
3. Test your team's weakness"
4. Find teammates for your team"
5. See all species names"
6. test a Pokémon is useful or not
and an input example
Name example: Tapu Fini, Mega Charizard X, Zacian-Crowned, Nidoran M, Raichu-Alola

User input the number of selection and go to the next step.
Each selection is in a function (except 5, a print statement)

For **function 1**, user need to input the name of one species and got the data and recommended teammates like this
Please input the name of the Pokemon species: Pikachu
No. 25, name: Pikachu, type: Electric , status: Normal, total points: 320
teammate recommendation: ['Landorus-Therian', 'Thundurus', 'Rillaboom', 'Kyogre', 'Whimsicott', 'Urshifu-Rapid-Strike', 'Charizard', 'Indeedee-F', 'Tornadus', 'Calyrex-Shadow', 'Coalossal', 'Yveltal', 'Weezing', 'Togekiss', 'Tsareena', 'Landorus', 'Araquanid', 'Dragonite', 'Talonflame', 'Rayquaza', 'Gyarados']
I print this using the __str__()method of class Pokemon

**Function** 2 helps testing whether two pokemon can be teammates
Please input the name of the Pokemon species: Charizard
Please input the name of the other Pokemon species: Venusaur
Venusaur can be a nice teammate of Charizard.

**Function 3 and 4** helps testing a team or finding more teammates
Please input the names of species in yout team, seperate them by commas: Tapu Fini, Mega Charizard X, Zacian-Crowned, Nidoran M, Raichu-Alola
Please be aware of type Ground and Electric.
You may want:  ['Landorus-Therian', 'Rillaboom', 'Whimsicott', 'Grimmsnarl', 'Thundurus', 'Urshifu-Rapid-Strike']

**Function 5** returns the name of all species and forms so that user can select one from it

**Function 6** tests a species’ status and return whether it can be used in VGC battle
Mega Charizard X is mega or mythical Pokemon and can not be used in VGC battles now.


