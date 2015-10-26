from re import match, I, search
from random import gauss, randint
import cPickle as pickle, winsound

class animal(object):

    def __init__(self):
        self.turns = 0
        while True:
            self.basestat = gauss(50,20)
            if self.basestat > 0 and self.basestat < 100:
                break

class container(object):

    def __init__(self, id):
        self.animalCount = 0
        self.animalList = []
        self.feedQual = 2
        self.id = id
        if self.id == 'chickencoop':
            self.price = 80
            self.capacity = 12
            self.maintenance = 20
            self.feedCost = 5
        elif self.id == 'sheepsty':
            self.price = 60
            self.capacity = 4
            self.maintenance = 30
            self.feedCost = 10
        elif self.id == 'cowpen':
            self.price = 100
            self.capacity = 2
            self.maintenance = 40
            self.feedCost = 15
        elif self.id == 'empty':
            self.price, self.capacity, self.maintenance = 0, 0, 0

    def changeFeedQual(self):
        self.feedCost += 1
        self.feedQual += 1

    def changeRent(self, newRent):
        self.rentRate = newRent

class chicken(animal):
    id = 'chicken'
    price = 25

    def __init__(self):
        self.layCount = 0
        self.sellPrice = self.price * .5
        super(chicken, self).__init__()

    def layEgg(self, feedQual):
        self.turns += 1
        if (self.basestat * feedQual * gauss(50, 20)) > 5000:
            self.layCount += 1
            return True
        else:
            return False

    def prodPerTurn(self):
        if self.turns == 0:
            print "This chicken is new. Gotta give him a chance first"
            return 0
        else:
            return float(self.layCount) / float(self.turns)

class cow(animal):
    id = 'cow'
    price = 100
    mean = 50
    dev = 20

    def __init__(self):
        super(cow, self).__init__()
        self.sellPrice = self.price * .5
        self.totalMilk = 0

    def giveMilk(self, feedQual):
        milk = self.basestat * feedQual * gauss(self.mean, self.dev)
        self.totalMilk += milk
        self.turns += 1
        return milk

    def prodPerTurn(self):
        if self.turns == 0:
            print "This cow hasn't been milked yet."
            return 0
        else:
            return self.totalMilk / self.turns

class sheep(animal):
    id = 'sheep'
    price = 50
    mean = 20
    dev = 5

    def __init__(self):
        self.wool = randint(0, 100)
        self.sellPrice = self.price * .5
        self.totalWool = 0
        super(sheep, self).__init__()

    def growWool(self, feedQual):
        newWool = self.basestat * feedQual * gauss(self.mean, self.dev)
        self.wool += newWool
        self.totalWool += newWool
        self.turns += 1
        if self.wool > 5000:
            self.wool = 0
            return True
        else:
            return False

    def prodPerTurn(self):
        if self.turns == 0:
            print "C'mon, this little guys just getting started. You're just going to have to wait and see"
            return 0
        else:
            return self.totalWool / self.turns

class farmLand(object):

    def __init__(self):
        self.occupied = False
        self.structure = container('empty')

    def occupy(self, container):
        self.occupied = True
        self.structure = container

    def unoccupy(self):
        self.occupied = False
        self.structure = empty()

    def isOccupied(self):
        return self.occupied

class farmer(object):

    def __init__(self, name):
        self.name = name
        self.farm = [[farmLand() for i in range(0,2)]for i in range(0,2)]
        self.vertLimit, self.horLimit = 3, 3
        self.cash = 1000
        self.rentRate = 10
        self.cowCount, self.chickenCount, self.sheepCount, self.turns = 0, 0, 0, 1
        self.nextFlag = False
        self.quitFlag = False
        self.winFlag = False

    def upgradeRent(self, newRent):
        self.rentRate = newRent

    def infoOut(self):
        if self.cash >= 10000:
            print "Congratulations! You won! Your memory will now forever live on in the leaderboard."
            winsound.PlaySound('cheering.wav', winsound.SND_FILENAME)
            self.winFlag = True
            self.nextFlag = True
            return True
        print "Cows:", self.cowCount, "Sheep:", self.sheepCount, "Chickens:", self.chickenCount, "\n"
        print "Your farm looks like: \n"
        farmDrawing = []
        for y in xrange(0,len(self.farm)):
            farmRow = ""
            for x in xrange(0,len(self.farm[y])):
                if self.farm[y][x].isOccupied():
                    if self.farm[y][x].structure.id == 'cowpen':
                        farmRow += ('C')
                    if self.farm[y][x].structure.id == 'sheepsty':
                        farmRow += ('S')
                    if self.farm[y][x].structure.id == 'chickencoop':
                        farmRow += ('c')
                else:
                    farmRow += ('O')
                farmRow += " "
            farmDrawing.append(farmRow)
        while len(farmDrawing) > 0:
            print farmDrawing.pop()
        print ''
        return False

    def hasMatchStructure(self, structure, numOrdered):
        hasMatch = []
        for y in range(0, len(self.farm)):
            for x in range(0, len(self.farm[y])):
                if self.farm[y][x].structure.id == structure.id and self.farm[y][x].structure.capacity >= (len(self.farm[y][x].structure.animalList) + numOrdered):
                    hasMatch.append((x,y))
        if len(hasMatch) > 0:
            print "The following locations can be used:"
            for el in hasMatch:
                print el
            return True
        else:
            raw_input("No containers with the capacity required were found.")
            return False

    def canSell(self, id, sellNum, prodName, animalName):
        hasMatch = []
        for y in xrange(0, len(self.farm)):
            for x in xrange(0, len(self.farm[y])):
                if self.farm[y][x].isOccupied() and self.farm[y][x].structure.id == id and self.farm[y][x].structure.animalCount >= sellNum:
                    hasMatch.append((x,y))
        if len(hasMatch) > 0:
            print "The following locations can be chosen."
            for el in hasMatch:
                count = 1
                for el1 in self.farm[el[1]][el[0]].structure.animalList:
                    print "%s number %d at location %shas produced %d %s per turn and can be sold for %d" %(animalName, count, el, el1.prodPerTurn(), prodName, el1.sellPrice)
                    count += 1
            return True
        else:
            print "There aren't any locations where that many animals can be sold"
            return False

    def chooseCoordinates(self, prompt, boundsPrompt, coordPrompt):
        print prompt
        while True:
            x = (raw_input("x > "))
            y = (raw_input("y > "))
            if x.isdigit() and y.isdigit():
                x = int(x)
                y = int(y)
                if y < len(self.farm) and x < len(self.farm[y]):
                    return x, y
                else:
                    print boundsPrompt
            else:
                print coordPrompt

    def buyMultAnimal(self):
        while True:
            num = raw_input("How many animals do you want to buy?\n> ")
            if num.isdigit():
                num = int(num)
                break
            else:
                print"Num has to be an int.. let's try this again."
        selection = raw_input("And what species are we buying today? Cow: %d$ Sheep: %d$ Chicken: %d$\n> "%(cow.price, sheep.price, chicken.price))
        names = ['cow', 'sheep', 'chicken']
        for species in names:
            match = search(species, selection, I)
            if match:
                totalPrice = 0
                if species == 'cow':
                    if self.cash < cow.price * num:
                        raw_input("Haha, you are too poor for that many cows. You are short %d$" %(cow.price*num - self.cash))
                        return
                    if num > 2:
                        print "Are you crazy?!? No cow pen in the world could pen that many cows!"
                        return
                    print "Let's see if there are any available cow barns"
                    if self.hasMatchStructure(container('cowpen'), num):
                        x, y = self.chooseCoordinates('What location will we use?', "That's not your land you dirty thief", "Coordinates must be integers.. try again and focus this time.")
                        for el in range(0, num):
                            newCow = cow()
                            self.farm[y][x].structure.animalList.append(newCow)
                            self.cash -= newCow.price
                            totalPrice += newCow.price
                            self.farm[y][x].structure.animalCount += 1
                            self.cowCount += 1
                elif species == 'sheep':
                    if self.cash < sheep.price * num:
                        raw_input("Haha, you are too poor for that many sheep. You are short %d$" %(sheep.price*num - self.cash))
                        return
                    if num > 4:
                        print "Sheep are introverts and don't enjoy being in pens with more than 4 sheep."
                        return
                    print "Let's see if there are any available sheep pens"
                    if self.hasMatchStructure(container('sheepsty'), num):
                        x, y = self.chooseCoordinates('What location will we use?', "That's not your land you dirty thief", "Coordinates must be integers.. try again and focus this time.")
                        for el in range(0, num):
                            newsheep = sheep()
                            self.farm[y][x].structure.animalList.append(newsheep)
                            self.cash -= newsheep.price
                            totalPrice += newsheep.price
                            self.farm[y][x].structure.animalCount += 1
                            self.sheepCount += 1
                elif species == 'chicken':
                    if self.cash < chicken.price * num:
                        raw_input("Haha, you are too poor for that many chickens. You are short %d$" %(sheep.price*num - self.cash))
                        return
                    if num > 12:
                        print "Too many chickens."
                        return
                    print "Let's see if there are any available chicken coops"
                    if self.hasMatchStructure(container('chickencoop'), num):
                        x, y = self.chooseCoordinates('What location will we use?', "That's not your land you dirty thief", "Coordinates must be integers.. try again and focus this time.")
                        for el in range(0, num):
                            newChick = chicken()
                            self.farm[y][x].structure.animalList.append(newChick)
                            self.cash -= newChick.price
                            totalPrice += newChick.price
                            self.farm[y][x].structure.animalCount += 1
                            self.chickenCount += 1
                winsound.PlaySound('coin.wav', winsound.SND_FILENAME)
                raw_input("%d$ spent. Bank: %d /n" %(totalPrice, self.cash))
                break

    def sellFn(self, id, sellNum, prodName, animalName):
        if not self.canSell(id, sellNum, prodName, animalName):
            return
        else:
            x, y = self.chooseCoordinates('Which coordinates do you want to use?', "You can't sell animals that aren't yours, try choosing land that you own", "Do you even know what an integer is?")
            print "The pen at (%d, %d) holds %d %ss" %(x, y, self.farm[y][x].structure.animalCount, animalName)
            for el1 in xrange(0, sellNum):
                count = 1
                for el2 in self.farm[y][x].structure.animalList:
                    print "%s number %d has produced %d %s per turn and can be sold for %d" %(animalName, count, el2.prodPerTurn(), prodName, el2.sellPrice)
                    count += 1
                while True:
                    selectNum = raw_input("Which %s do you want to sell? Press 'c' to cancel.\n> " %animalName)
                    if selectNum.isdigit():
                        selectNum = int(selectNum)
                        if 0 < selectNum <= self.farm[y][x].structure.animalCount:
                            selectNum -= 1
                            break
                        else:
                            print "I'm afraid I can't let you do that, Dave."
                    elif selectNum == 'c' or selectNum == 'C':
                        return
                    else:
                        print "The number must be a number. Let's try that again."
                print "Gained %d from the sale of %s number %d." %(self.farm[y][x].structure.animalList[selectNum].sellPrice,animalName , selectNum + 1)
                winsound.PlaySound('cash_register_x.wav', winsound.SND_FILENAME)
                self.cash += self.farm[y][x].structure.animalList[selectNum].sellPrice
                del self.farm[y][x].structure.animalList[selectNum]
                self.farm[y][x].structure.animalCount -= 1
                if animalName == 'cow':
                    self.cowCount -=1
                elif animalName == 'chicken':
                    self.chickenCount -=1
                else:
                    self.sheepCount -= 1
            print "Bank: %d" %self.cash

    def sellAnimal(self):
        animalId = raw_input("What type of animal do you want to sell?\n> ")
        names = ["cow", "sheep", "chicken"]
        for animal in names:
            match = search(animal, animalId, I)
            if match:
                print "I think you said %ss!" %animal
                while True:
                    sellNum = raw_input("And how many do you want to sell?\n> ")
                    if sellNum.isdigit():
                        sellNum = int(sellNum)
                        break
                    else:
                        print "Good effort! Try using a number this time."
                if animal == "cow":
                    self.sellFn('cowpen', sellNum, 'mLs of milk', 'cow')
                    break
                elif animal == 'sheep':
                    self.sellFn('sheepsty',sellNum, 'official wool units', 'sheep')
                    break
                elif animal == 'chicken':
                    self.sellFn('chickencoop', sellNum, 'eggs', 'chicken')
                    break

    def buyContainer(self):
        while True:
            x, y = self.chooseCoordinates("Where should the container go?", "You don't own that land you greedy goober!", "Generally, coordinates work better if number are used. Shall we try doing that?")
            if self.farm[y][x].isOccupied():
                print "Occupied, try another square"
            else: break
        selection = raw_input("Which type of container?\nCow %d$ chicken %d$ sheep %d$?\n> " %(container('cowpen').price, container('chickencoop').price, container('sheepsty').price))
        names = ["cow", "sheep", "chicken"]
        for animal in names:
            match = search(animal, selection, I)
            if match:
                print "I think you said %s!" %animal
                if animal == "cow":
                    newC = container('cowpen')
                    if self.cash < newC.price:
                        print "Need %d more $ for that purchase" %(newC.price - self.cash)
                        break
                    self.farm[y][x].occupy(newC)
                    self.cash -= newC.price
                    winsound.PlaySound('coin.wav', winsound.SND_FILENAME)
                elif animal == "sheep":
                    newC = container('sheepsty')
                    if self.cash < newC.price:
                        print "Need %d more $ for that purchase" %(newC.price - self.cash)
                        break
                    self.farm[y][x].occupy(newC)
                    self.cash -= newC.price
                    winsound.PlaySound('coin.wav', winsound.SND_FILENAME)
                else:
                    newC = container('chickencoop')
                    if self.cash < newC.price:
                        print "Need %d more $ for that purchase" %(newC.price - self.cash)
                        break
                    self.farm[y][x].occupy(newC)
                    self.cash -= newC.price
                    winsound.PlaySound('coin.wav', winsound.SND_FILENAME)

    def buyLand(self):
        print "(For now) the farm must be a rectangle."
        while True:
            selection1 = raw_input("Do you want to expand horizontally or vertically? (v, h)\n> ")
            if selection1 == 'v':
                self.vertExpand()
            elif selection1 == 'h':
                self.horExpand()
            else:
                print "Command not recognized.. Is it really so difficult to choose one of two letters?"
                continue
            break

    def vertExpand(self):
        if len(self.farm) == self.vertLimit:
            raw_input("You need to upgrade before you can expand vertically.")
            return
        num = len(self.farm[0])
        price = num * 50
        if self.cash < price:
            raw_input("You don't have enough money for this, you need %d more to take this action." %(price-self.cash))
            return
        while True:
            selection2 = raw_input("The expansion will cost %d, are you sure you want to proceed (y, n)\n> " %(price))
            match2 = match('[yn]', selection2, I)
            if match2:
                if selection2 == 'y':
                    newRow = []
                    for el in range(0,num):
                        newRow.append(farmLand())
                    self.farm.append(newRow)
                    self.cash -= (price)
            elif selection2 == 'n':
                pass
            else:
                print "Holy crap it's a yes or no question... May as well try again I suppose."
                continue
            break

    def horExpand(self):
        if len(self.farm[0]) == self.horLimit:
            raw_input("You're gonna have to upgrade before expanding horizontally")
            return
        print "Let's expand horizontally."
        num = len(self.farm)
        price = num * 50
        if self.cash < price:
            raw_input("You don't have enough money for this, you need %d more to take this action." %(price-self.cash))
            return
        while True:
            selection2 = raw_input("The expansion will cost %d, are you sure you want to proceed (y, n)\n> " %price)
            match2 = match('[yn]', selection2, I)
            if match2:
                if selection2 == 'y':
                    for row in self.farm:
                        row.append(farmLand())
                    self.cash -= price
                elif selection2 == 'n':
                    pass
            else:
                print "Holy crap it's a yes or now question... May as well try again I suppose."
                continue
            break

    def upgrades(self):
        print"""Here are the upgrades currently available:

r = Upgrade Rent Rate
f = Upgrade Feed
c = Upgrade Container
h = Upgrade Horizontal Limit
v = Upgrade Vertical Limit"""

        selection = raw_input('> ')
        foo = match('[rfchv]', selection, I)
        if foo:
            if selection == 'r':
                if self.rentRate == 10:
                    price = 700
                    newRate = 7
                elif self.rentRate == 7:
                    price = 1000
                    newRate = 5
                else:
                    print "You can't upgrade your rent anymore"
                    return
                if price > self.cash:
                    raw_input("You are too poor for this upgrade.")
                    return
                while True:
                    choice = raw_input("Current Rent is %d/square, upgraded rent is %d/square. Upgrade will cost %d$. Proceed? (y/n) \n> " %(self.rentRate, newRate, price))
                    if choice == 'y' or choice == 'Y':
                        self.rentRate = newRate
                        self.cash -= price
                        raw_input('Upgrade complete. Bank is now %d' % self.cash)
                        break
                    elif choice == 'n' or choice == 'N':
                        raw_input("I see you are a very discerning customer... perhaps another time.")
                        break
                    else:
                        print "Sorry? Didn't quite catch that there old boy."

            if selection == 'f':
                while True:
                    print"Which feed should we upgrade?"
                    x = raw_input('x >')
                    y = raw_input('y >')
                    if x.isdigit() and y.isdigit():
                        x = int(x)
                        y = int(y)
                        if y < len(self.farm) and x < len(self.farm[y]):
                            if self.farm[y][x].isOccupied():
                                self.farm[y][x].structure.changeFeedQual()
                                self.cash -= 20
                                print "That'll be 20$. Bank is now %d" %self.cash
                                break
                        else:
                            print "You don't own that land you greedy bugger!"
                    else:
                        print "x and y must be integers, x and y were NOT integers, try again using INTEGERS for X and Y"
            if selection == 'c':
                x, y = self.chooseCoordinates('Which container do you want to upgrade?', "I don't know about you but around here we only upgrade containers on our land", "Good god man! Integers I say! Is that so hard!")
                price = 100
                if self.cash < price:
                    raw_input("You can't afford this upgrade.. I'm afraid I'm going to have to ask you to leave")
                    return
                while True:
                    choice = raw_input('The current rate is %d, the upgraded rate is %d, the price of the upgrade is %d. Proceed? (y/n)\n> ' %(self.farm[y][x].structure.maintenance, self.farm[y][x].structure.maintenance * 3 / 5, price))
                    if choice == 'y' or choice == 'Y':
                        self.cash -= price
                        self.farm[y][x].structure.maintenance = self.farm[y][x].structure.maintenance * 3 / 5
                        break
                    elif choice == 'n' or choice == 'N':
                        break
                    else:
                        print 'Wat?'

            if selection == 'v':
                price = self.vertLimit * 100
                choice = raw_input('It will cost %d for this upgrade, proceed? (y/n)' %price)
                if choice == 'y' or choice == 'Y':
                    self.cash -= price
                    self.vertLimit += 1
                    raw_input("Congrats! The vertical limit is now %d" %self.vertLimit)
            if selection == 'h':
                price = self.horLimit * 100
                choice = raw_input('It will cost %d for this upgrade, proceed? (y/n)' %price)
                if choice == 'y' or choice == 'Y':
                    self.cash -= price
                    self.horLimit += 1
                    raw_input("Congrats! The horizontal limit is now %d" %self.horLimit)

    def saveGame(self):
        sv = pickle.load(open("saves.p", "rb"))
        sv.append(self)
        pickle.dump(sv, open('saves.p', 'wb'))
        raw_input('Game saved!')

    def takeTurn(self):
        self.nextFlag = False
        print "You have %d$. What do you want to do?" %self.cash
        playerChoice = raw_input("a = Buy Animals\nl = Buy Land\nc = Buy Container\ns = Sell Animals\nu = Buy Upgrades\nn = Next Turn\nsv = Save Game\nq = Quit Game\n> ")
        foo = match('[aclnusq]', playerChoice, I)
        if foo:
            if playerChoice == 'a' or playerChoice == 'A':
                self.buyMultAnimal()
            elif playerChoice == 'c' or playerChoice == 'C':
                self.buyContainer()
            elif playerChoice == 'l' or playerChoice == 'L':
                self.buyLand()
            elif playerChoice == 's' or playerChoice == 'S':
                self.sellAnimal()
            elif playerChoice == 'u' or playerChoice == 'U':
                self.upgrades()
            elif playerChoice == 'n' or playerChoice == 'N':
                self.nextFlag = True
            elif playerChoice == 'sv' or playerChoice == 'SV':
                self.saveGame()
            elif playerChoice == 'q' or playerChoice == 'Q':
                self.nextFlag = True
                self.quitFlag = True

    def endTurn(self):
        expenses = self.expenses()
        cowSum, sheepum, chickSum = 0, 0, 0
        for y in xrange(0,len(self.farm)):
            for x in xrange(0,len(self.farm[y])):
                if self.farm[y][x].isOccupied():
                    if self.farm[y][x].structure.id == 'cowpen':
                        cowtotal = 0
                        cowCount = 0
                        for cowEl in self.farm[y][x].structure.animalList:
                            cowCount += 1
                            milk = cowEl.giveMilk(self.farm[y][x].structure.feedQual)
                            print "Cow number %d in the pen at (%d, %d) has produced %d mLs of milk!" %(cowCount, x, y, milk)
                            cowtotal += milk / 200
                        print "You made %d$ off the cows in cowpen %d, %d" %(cowtotal, x, y)
                        cowSum += cowtotal
                    elif self.farm[y][x].structure.id == 'sheepsty':
                        sheeptotal = 0
                        sheepCount = 0
                        for sheepEl in self.farm[y][x].structure.animalList:
                            sheepCount += 1
                            if sheepEl.growWool(self.farm[y][x].structure.feedQual):
                                print "Sheep shorn! Sheep number %d in pen %d, %d has grown out of his coat" %(sheepCount, x, y)
                                sheeptotal += 70
                        print "You made %d$ off the sheep in sheepsty %d, %d" %(sheeptotal, x, y)
                        sheepum += sheeptotal
                    elif self.farm[y][x].structure.id == 'chickencoop':
                        chickentotal = 0
                        chickCount = 0
                        for chickEl in self.farm[y][x].structure.animalList:
                            chickCount += 1
                            if chickEl.layEgg(self.farm[y][x].structure.feedQual):
                                print "Egg successfully laid by chicken number %d in coop %d, %d" %(chickCount, x, y)
                                chickentotal += 5
                        print "You made %d$ off the chickens in coop %d, %d" %(chickentotal, x, y)
                        chickSum += chickentotal
        print "Your profit from your cows was %d$" %cowSum
        print "Your profit from your sheep was %d$" %sheepum
        print "Your profit from your chickens was %d$" %chickSum
        totalSum = sum([cowSum, sheepum, chickSum])
        self.cash += totalSum
        if expenses < totalSum:
            winsound.PlaySound('cash_register_x.wav', winsound.SND_FILENAME)
        raw_input("Your total cash gained was %d$. Bank: %d" %(totalSum, self.cash))
        if self.cash < 0:
            print "You're officially broke! You lose the game! Don't worry, not everyone has what it takes to be a farmer."
            winsound.PlaySound('boo.wav', winsound.SND_FILENAME)
            quit()

    def expenses(self):
        self.turns += 1
        totalRent = 0
        if self.turns % 5 == 0:
            raw_input("Taxman is here! Time for rent collection!")
            for y in xrange(0,len(self.farm)):
                for x in xrange(0,len(self.farm[y])):
                    totalRent += self.rentRate
            self.cash -= totalRent
            print "Your land rent for this period is %d$, your bank is now %d$" %(totalRent, self.cash)
        rentCost = 0
        for y in xrange(0,len(self.farm)):
            for x in xrange(0, len(self.farm[y])):
                if self.farm[y][x].isOccupied():
                    rentCost += self.farm[y][x].structure.maintenance
        self.cash -= rentCost
        feedCost = 0
        for y in xrange(0,len(self.farm)):
            for x in xrange(0, len(self.farm[y])):
                if self.farm[y][x].isOccupied():
                    feedCost += self.farm[y][x].structure.feedCost
        self.cash -= feedCost
        print "Feed Cost: %d$ Maintenance Cost: %d$ Bank: %d$" %(feedCost, rentCost, self.cash)
        return totalRent + feedCost + rentCost