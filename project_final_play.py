#######################################
#####  SI 507 Final Project       #####
#####   Yuexin Chang  # 67609799  #####
#####  Pokemon team finder ui     #####
#######################################


from collections import Counter
import json
import time

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
        return f"No. {self.pokedex}, name: {self.name}, type: {self.type1} {self.type2}, status: {self.status}, total points: {self.point}\nteammate recommendation: {self.pair}"
    
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

def testteam(team):
    '''
    evaluate the team(a list of at most 6 pokemon)
    '''
    m = 0
    n = 0
    print()
    for i in team:       # test speed
        if i.speed <= 60:
            m += 1
        elif i.speed >= 100:
            n += 1
    if n >= len(team) - 1:
        print("Please be aware of trick room.")
    if m >= len(team) - 1:
        print("The speed of your team is low")

    t = []                    # test weakness
    for i in team:
        t += i.weak

    mt = Counter(t).most_common(2)[0][0]
    mt1 = Counter(t).most_common(2)[1][0]
    print(f"Please be aware of type {mt} and {mt1}.")

def findteammate(team):
    '''find more team mates fot the team(a list of at most 6 pokemon)'''
    m = []
    for i in team:
        m += i.pair
    n = Counter(m).most_common(6)
    nn = []
    for i in n:
        nn.append(i[0])
    print("\nYou may want: ",nn)

########################
####   Start here  #####
########################


# first read the json files of our data: pokedex = pokepair.json = pokemon data graph, 
# pairdict = vgc202111.json = modified teammate usage rate of some species, pokename = a list of all species names
pokedex = {}
with open("F:/si507/project_final/data/pokepair.json", 'r', encoding='utf-8') as file_obj:
    pokedict = json.load(file_obj)

for k,v in pokedict.items():
    pokedex[k] = Pokemon(v["pokedex"],v["name"],v["status"],v["type1"],v["type2"],v["points"],v["point"],v["speed"],v["typelist"],v["against"],v["weak"],v["weak4"],v["pair"])

with open("F:/si507/project_final/data/vgc202111.json", 'r', encoding='utf-8') as file_obj:
    pairdict = json.load(file_obj)

with open("F:/si507/project_final/data/pokename.json", 'r', encoding='utf-8') as file_obj:
    pokename = json.load(file_obj)


# function 1: find teammates for a Pokemon
def func1():
    poke = input("Please input the name of the Pokemon species: ")
    while True:
        if poke in pokename:
            print()
            print(pokedex[poke])
            break
        else:
            poke = input("Please input a correct name: ")

# function 2: find out whether two species are good to be teammates
def func2():
    poke = input("Please input the name of the Pokemon species: ")
    while True:
        if poke in pokename:
            break
        else:
            poke = input("Please input a correct name: ")
    poke1 = input("Please input the name of the other Pokemon species: ")
    while True:
        if poke1 in pokename:
            break
        else:
            poke1 = input("Please input a correct name: ")
    if match(pokedex[poke], pokedex[poke1],pairdict):
        print(f"\n{poke1} can be a nice teammate of {poke}.")
    else: 
        print(f"\n{poke1} may not be a nice teammate of {poke}.")

# function 3: test a team
def func3():
    names = input("Please input the names of species in yout team, seperate them by commas: ")
    while True:
        team = names.split(",")
        test = 0
        for i in range(len(team)):
            team[i] = team[i].strip()
            if team[i] not in pokename:
                test += 1
        if test == 0:
            break
        else:
            names = input("Please input correct names, seperate them by commas: ")
    teams = []
    for t in team:
        teams.append(pokedex[t])
    testteam(teams)

# function 4: find teammates for a team
def func4():
    names = input("Please input the names of species in yout team, seperate them by commas: ")
    while True:
        team = names.split(",")
        test = 0
        for i in range(len(team)):
            team[i] = team[i].strip()
            if team[i] not in pokename:
                test += 1
        if test == 0:
            break
        else:
            names = input("Please input correct names, seperate them by commas: ")
    teams = []
    for t in team:
        teams.append(pokedex[t])
    findteammate(teams)

def func6():
    '''
    test a pokemon is useful or not
    '''
    poke = input("Please input the name of the Pokemon species: ")
    while True:
        if poke in pokename:
            break
        else:
            poke = input("Please input a correct name: ")
    status = pokedex[poke].status
    if status in ["Mega","Mythical"]:
        print(f"\n{poke} is mega or mythical Pokemon and can not be used in VGC battles now.")
    elif status == "Legendary":
        print(f"\n{poke} is legendary Pokemon.\nYou can only have one legendary Pokemon in yout team in VGC 2021.")
    else:
        print(f"\n{poke} can be used in VGC battles if you have it in Galar")

########################
####   Start here  #####
########################

print("\nHello, this is a helper for Pokemon teammate.")
time.sleep(1)
while True:
    print("\nPlease select what you want:")
    print("1. Check the information and find a teammate for one species.")
    print("2. Find out whether two species are good to be teammates.")
    print("3. Test your team's weakness")
    print("4. Find teammates for your team")
    print("5. See all species names")
    print("6. Test a pokemon is useful or not")
    time.sleep(1)
    print("\nName example: Tapu Fini, Mega Charizard X, Zacian-Crowned, Nidoran M, Raichu-Alola")
    print("If you want to quit, please input 'quit'")
    time.sleep(1)
    s = input("\nPlease input the number of your selection: ")
    if s == "quit":
        break
    try:
        s = int(s)
    except:
        print("\nPlease input a number from 1 to 6. ")
        time.sleep(2)
        continue
    
    if s == 1:
        print()
        func1()
    if s == 2:
        print()
        func2()
    if s == 3:
        print()
        func3()
    if s == 4:
        print()
        func4()
    if s == 5:
        print()
        count = 0
        for i in pokename:
            print(i ,end = ", ")
            count += 1
            if count % 10 == 0:
                print(end = "\n")
    if s == 6:
        print()
        func6()
    time.sleep(5)

print("\nThank you, goodbye!")
