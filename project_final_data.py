#######################################
#####  SI 507 Final Project       #####
#####   Yuexin Chang  # 67609799  #####
#####  Pokemon team finder        #####
#######################################
import csv
from collections import Counter
from bs4 import BeautifulSoup
import requests
import re
import json

def readcsv(filepath): # OK, return lists in list, list[0] is header
    '''
    read a csv file that contains pokemon data
    reutrn a list of lists that contains one species
    '''
    with open(filepath, 'r', newline='', encoding='utf-8') as file_obj: 
        data = []
        reader = csv.reader(file_obj, delimiter=",")
        for row in reader:
            data.append(row)

        return data

def writecsv(filepath, data, headers=None): # OK
    '''
    write the data (list) into a csv. header (list) is optional 
    '''
    with open(filepath, 'w', newline='', encoding='utf-8') as file_obj:  
        writer = csv.writer(file_obj)  
        if headers:  
            writer.writerow(headers) 
            for row in data:
                writer.writerow(row) 
        else: 
            writer.writerows(data)

def readlist(filepath): # ok
    '''
    read the csv data contains the list of pokemon species, return a list
    '''
    with open(filepath, 'r', newline='', encoding='utf-8') as file_obj: 
        data = []
        reader = csv.reader(file_obj, delimiter=",")
        for row in reader:
            data.append(row[0])

        return data

def writelist(filepath, data,):  # ok
    data1 = []
    for i in data:
        data1.append([i])
    with open(filepath, 'w', newline='', encoding='utf-8') as file_obj:  
        writer = csv.writer(file_obj)  
        writer.writerows(data1)

def match(poke, poke1, pairdict={}):
    '''
    find out whether two pokemon match under my conditions
    '''
    score = 0
    if isspeedmatch(poke, poke1):      # speed
        score += 1
    if isweak4(poke,poke1):            # weak4
        score += 2
    if istypematch(poke, poke1):      # same weakness
        score += 1
    if isdefensematch(poke, poke1):   # weak & against
        score += 2
    if isbeatmatch(poke, poke1):      # against & against
        score += 2
    if isinlist(poke, poke1, pairdict):  # teammate usage rate
        score += 6
    if score >= 7:               # total 14
        return True
    else:
        return False

def isspeedmatch(poke, poke1):
    '''
    poke and poke1 are class Pokemon. 
    If both of them are slow or fast, return True. (for trick room or tail wind)
    '''
    if poke.speed <= 60 and poke1.speed <= 60:
        return True
    elif poke.speed >= 60 and poke1.speed >= 60:
        return True
    else:
        return False

def isweak4(poke,poke1):
    '''
    poke and poke1 are class Pokemon. 
    If poke1 is against one type of poke's weakness4, return true
    If poke1 does not have weak4, return true
    '''
    if not poke.weak4:
        return True
    if poke1.type1 in poke.weak4:
        return True
    elif poke1.type2 in poke.weak4:
        return True
    else:
        return False

def istypematch(poke, poke1):
    '''
    poke and poke1 are class Pokemon. 
    If two species have a same weakness, return false
    '''
    for i in poke.weak:
        if i in poke1.weak:
            return False
    return True

def isdefensematch(poke,poke1):
    '''
    poke and poke1 are class Pokemon. 
    poke1 against at least one of poke's weakness
    '''
    for i in poke.weak:
        if i in poke1.against:
            return True
    return False

def isbeatmatch(poke,poke1):
    '''
    poke and poke1 are class Pokemon. 
    if two speceis against at least two different types, return true
    '''
    num = 0
    for i in poke.against:
        if i not in poke1.against:
            num += 1
    if num >= 2:
        return True
    else:
        return False

def isinlist(poke,poke1,pairdict):
    '''
    poke and poke1 are class Pokemon. usefullist is a teammate of high usage rate
    if poke1 is a widely used teammate of poke, return true
    '''
    if poke1.name in pairdict.get(poke.name):
        return True
    return False


class Pokemon:
    def __init__(self, pokedex, name, status, type1, type2="", points=[], point=0, speed=0, typelist=[], against=[], weak=[], weak4=[], pair=[]):
        self.pokedex = pokedex    #ID of pokedex, 1-890
        self.name = name          #name of the Pokemon
        self.status = status      #normal, sublegendary, legendary, Mythical, only normal and sublegendary Pokemon can be used in normal PVP
        self.type1 = type1        #type of the Pokemon
        self.type2 = type2        #another type of the Pokemon, not all species has type2
        self.points = points      #list of all points
        self.point = point        #total attribution points 
        self.speed = speed        #speed
        self.typelist = typelist  #how it works when beaten by one move
        self.against = against    #stronger than the type
        self.weak = weak          #weaker than the type (include weak4)
        self.weak4 = weak4        #very weaker than the type
        self.pair = pair
    
    def filltypelist(self):   # ok
        '''
        for a Pokemon, use the typelist to fill the against and weak list 
        '''
        self.against = []
        self.weak4 = []
        self.weak = []
        for i in range(len(self.typelist)):
            if self.typelist[i] < 1:
                self.against.append(i)
            if self.typelist[i] == 4:
                self.weak4.append(i)
            if self.typelist[i] > 1:
                self.weak.append(i)
    
    def numbertotype(self):  # ok
        '''
        change the index of type to type name
        '''
        def ntt(numlist):
            for i in range(len(numlist)):
                if numlist[i] == 0:
                    numlist[i] = "Normal"
                if numlist[i] == 1:
                    numlist[i] = "Fire"
                if numlist[i] == 2:
                    numlist[i] = "Water"
                if numlist[i] == 3:
                    numlist[i] = "Electric"
                if numlist[i] == 4:
                    numlist[i] = "Grass"
                if numlist[i] == 5:
                    numlist[i] = "Ice"
                if numlist[i] == 6:
                    numlist[i] = "Fighting"
                if numlist[i] == 7:
                    numlist[i] = "Poison"
                if numlist[i] == 8:
                    numlist[i] = "Ground"
                if numlist[i] == 9:
                    numlist[i] = "Flying"
                if numlist[i] == 10:
                    numlist[i] = "Psychic"
                if numlist[i] == 11:
                    numlist[i] = "Bug"
                if numlist[i] == 12:
                    numlist[i] = "Rock"
                if numlist[i] == 13:
                    numlist[i] = "Ghost"
                if numlist[i] == 14:
                    numlist[i] = "Dragon"
                if numlist[i] == 15:
                    numlist[i] = "Dark"
                if numlist[i] == 16:
                    numlist[i] = "Steel"
                if numlist[i] == 17:
                    numlist[i] = "Fairy"
            return numlist
        self.against = ntt(self.against)
        self.weak = ntt(self.weak)
        self.weak4 = ntt(self.weak4)


    def fillstatus(self, usefullist=[]):  # ok
        '''
        if the pokemon is not useful in normal battle, change the status to "Not useful"
        '''
        if self.status == "Normal":
            if usefullist:
                if self.name not in usefullist:      # not frequently be used in vgc
                    self.status = "Not useful"
            elif self.point < 440:                    # if no usefullist, these are too weak for new player
                self.status = "Not useful"
        if self.name.startswith("Mega ") or self.name.startswith("Primal "):
            self.status = "Mega"

    def fillpair(self, poke, pairdict={}):
        '''
        fill the pair list (edges between nodes)
        '''
        if match(self, poke, pairdict):
            self.pair.append(poke.name)
    
    def sortpair(self, rate):
        '''
        after filling the pairlist, sort it with usage rate and keep the first 20
        '''
        l = []
        for i in rate:
            if i in self.pair:
                l.append(i)
        if len(l) > 20:
            l = l[0:21]
        self.pair = l

    def __str__(self):
        '''
        print the name, pokedex number, type, status and total points
        '''
        return f"No. {self.pokedex}, name: {self.name}, type: {self.type1} {self.type2}, status: {self.status}, total points: {self.point}"
    
    def jsonable(self):
        '''
        write the data into a dict to store in a json file, return a dict
        '''
        return {
            "pokedex": self.pokedex,
            "name": self.name,
            "status": self.status,
            "type1": self.type1,
            "type2": self.type2,
            "points": self.points,
            "point": self.point,
            "speed": self.speed,
            "typelist": self.typelist,
            "against": self.against,
            "weak": self.weak,
            "weak4": self.weak4,
            "pair": self.pair
        }
#pokedex, name, status, type1, type2="", points=[], point=0, speed=0, typelist=[], against=[], weak=[], weak4=[], pair=[]



########################
####   Start here  #####
########################


# first scrap the page of pokemon showdown usage by Beautifulsoup, and get link of the data of vgc

url = "https://www.smogon.com/stats/2021-11/" # this page stores hundreds of links to data of different battle type

result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
vgc = soup.find_all(text=re.compile(".vgc.*"))     #search by regular expression
#print(vgc) # ['gen8vgc2021series10-0.txt', 'gen8vgc2021series10-1500.txt', 'gen8vgc2021series10-1630.txt', 'gen8vgc2021series10-1760.txt', 'gen8vgc2021series11-0.txt', 'gen8vgc2021series11-1500.txt', 'gen8vgc2021series11-1630.txt', 'gen8vgc2021series11-1760.txt']
#  the fourth and seventh is wanted
# I do not need to use caching here. The historical database (2021 November) is static and I only need to get the name of the dataset once. I store the modified data later.

vgc10 = requests.get('https://www.smogon.com/stats/2021-11/'+vgc[3]).text   # returns a string. 
'''
Total battles: 953
 Avg. weight/team: 0.001
 + ---- + ------------------ + --------- + ------ + ------- + ------ + ------- + 
 | Rank | Pokemon            | Usage %   | Raw    | %       | Real   | %       | 
 + ---- + ------------------ + --------- + ------ + ------- + ------ + ------- + 
 | 1    | Incineroar         | 48.62419% | 768    | 40.294% | 403    | 46.224% | 
 | 2    | Rillaboom          | 44.85093% | 545    | 28.594% | 236    | 27.069% | 
 | 3    | Volcarona          | 43.15309% | 177    |  9.286% | 57     |  6.538% | 
'''

vgc2021_10 = vgc10.split(" | ")                # transform it to a list of pokemons, Gen 8 VGC 2021 Series 10
vgc202110 = []    
for i in range(8,len(vgc2021_10)):
    if i % 8 == 2:
        vgc202110.append(vgc2021_10[i].strip())

vgc11 = requests.get('https://www.smogon.com/stats/2021-11/'+vgc[7]).text     # Gen 8 VGC 2021 Series 11
vgc2021_11 = vgc11.split(" | ")
vgc202111 = []
for i in range(8,len(vgc2021_11)):
    if i % 8 == 2:
        vgc202111.append(vgc2021_11[i].strip())

writelist("F:/si507/project_final/data/vgc202111.csv",vgc202111)   # store it 
writelist("F:/si507/project_final/data/vgc202110.csv",vgc202110)   # store it

# I also find some vgc usage data in kaggle in csv form

vgc7 = readcsv("F:/si507/project_final/data/vgc-series7_2021-01-usage_formatted.csv")   # Gen 8 VGC 2021 Series 7
vgc202107 = []
for i in vgc7[1:]:
    vgc202107.append(i[0])

vgc7 = readcsv("F:/si507/project_final/data/vgc-series7_2021-01-usage_formatted.csv")  # Gen 8 VGC 2020 Series 7
vgc202007 = []
for i in vgc7[1:]:
    vgc202007.append(i[0])

# Now we have 6 lists of pokemon usage rate. Select the first 300 species (make up 99% of total usage) and remove the duplicate
usefullist = list(set(vgc202007[0:299] + vgc202107[0:299] + vgc202110[0:299] + vgc202111[0:299]))   #get 365 species/forms
writelist("F:/si507/project_final/data/usefullist.csv",usefullist)


# here is the teammate usage rate in vgc 2021 sereis 11 in json file

with open("F:/si507/project_final/data/gen8vgc2021series11-1760.json", 'r', encoding='utf-8') as file_obj: 
    pok = json.load(file_obj)
data = pok["data"]              # read the json file and find the useful part. got 291 species
datateam = {}                  
datamatch = {}                   

for k,v in data.items():              # store teammates data into a dict 
    datateam[k] = v['Teammates']
for k,v in datateam.items():          # sort the teammates by the usage rate
    l = []
    e = v
    f = zip(e.values(), e.keys())
    c = sorted(f,reverse=True)
    for i in range(len(c)):
        if c[i][0] > 1:               # only store rate > 1
            l.append(c[i][1])
    datamatch[k] = l                  # store the data in a dict with species name as key and teammates list as value

with open("F:/si507/project_final/data/vgc202111.json", 'w', encoding='utf-8') as file_obj:
    json.dump(datamatch, file_obj, ensure_ascii=False, indent=2)         # write into a json and store it on my computer



# now change the pokedex csv into pokemon class
pokedex = readcsv("F:/si507/project_final/data/pokedex.csv")

pokeclass = {}
for j in range(len(pokedex)-1):
    b = pokedex[j+1]
    bp = b[6:12]
    bpp=[]
    for i in bp:
        bpp.append(float(i))
    bt = b[12:30]
    btt=[]
    for i in bt:
        btt.append(float(i))
    bul = Pokemon(int(b[0]),b[1],b[2],b[3],b[4],bpp,int(b[5]),int(b[11]),btt)

    bul.filltypelist()
    bul.numbertotype()

    pokeclass[bul.name] = bul.jsonable()

with open("F:/si507/project_final/data/pokedex.json", 'w', encoding='utf-8') as file_obj:
    json.dump(pokeclass, file_obj, ensure_ascii=False, indent=2)         # write into a json and store it on my computer


# Now fill the pair list of each species
with open("F:/si507/project_final/data/pokedex.json", 'r', encoding='utf-8') as file_obj:
    pokedex = json.load(file_obj)

usefullist = readlist("F:/si507/project_final/data/usefullist.csv")

with open("F:/si507/project_final/data/vgc202111.json", 'r', encoding='utf-8') as file_obj:
    pairdict = json.load(file_obj)

pokelist = []
for v in pokedex.values():
    pokelist.append(Pokemon(v["pokedex"],v["name"],v["status"],v["type1"],v["type2"],v["points"],v["point"],v["speed"],v["typelist"],v["against"],v["weak"],v["weak4"],v["pair"]))
#pokedex, name, status, type1, type2="", points=[], point=0, speed=0, typelist=[], against=[], weak=[], weak4=[], pair=[]
for i in pokelist:
    i.fillstatus(usefullist)

rate = readlist("F:/si507/project_final/data/vgc202111.csv")

for j in range(len(pokelist)):
    for i in pokelist:
        if i.status not in ["Not useful","Mega","Mythical"]:
            pokelist[j].fillpair(i, pairdict)
            pokelist[j].sortpair(rate)

pokedict = {}
for i in pokelist:
    pokedict[i.name] = i.jsonable()

print(pokedict["Pikachu"], pokedict["Venusaur"])
with open("F:/si507/project_final/data/pokepair.json", 'w', encoding='utf-8') as file_obj:
    json.dump(pokedict, file_obj, ensure_ascii=False, indent=2)

# this pokepair.json contains the information I need to build my graph. each species is a node, and if one node is linked to another node, the name of species is added to the pair list




