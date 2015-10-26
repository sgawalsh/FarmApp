from farmclasses import *

print """Welcome to Stephen's Super Fun Farm Game!
Win by getting 10 000$! Lose by going broke!
Buy animals to make $$$!
A world of adventure awaits so let's goooooo!"""

loopBool = True
while loopBool:
    choice = raw_input("New game, Load Game, Delete file, or View Leaderboard? (n/l/d/v)\n> ")
    if choice == 'n' or choice == 'N':

        player = farmer(raw_input("First off, please enter your name.\n> "))
        break
    elif choice == 'l' or choice == 'L':
        sv = pickle.load(open("saves.p", "rb"))
        if len(sv) == 0:
            print "Ain't nuthin here."
            continue
        print "The saved files are:"
        count = 1
        for el in sv:
            print "%d. Name: %s Cash: %d Turn: %d Cows %d Chickens %d Sheep %d" %(count, el.name, el.cash, el.turns, el.cowCount, el.chickenCount, el.sheepCount)
            count += 1
        while True:
            try:
                playerselect = raw_input("Which file do you want to load? Or 'q' to quit\n> ")
                playerselect = int(playerselect)
                playerselect = int(playerselect) - 1
                if 0 <= playerselect < len(sv):
                    player = sv[playerselect]
                    loopBool = False
                    break
                else:
                    print "Try choosing a save file that exists."
                    continue
            except ValueError:
                if playerselect == 'q':
                    break
                else:
                    print "That's not a number."
                    continue


    elif choice == 'd' or choice == 'D':
        sv = pickle.load(open("saves.p", "rb"))
        if len(sv) == 0:
            print "Ain't nuthin here."
            continue
        print "The saved files are:"
        count = 1
        for el in sv:
            print "%d. Name: %s Cash: %d Turn: %d Cows %d Chickens %d Sheep %d" %(count, el.name, el.cash, el.turns, el.cowCount, el.chickenCount, el.sheepCount)
            count += 1
        while True:
            playerselect = raw_input("Which file do you want to delete? or 'q' to quit.\n> ")
            if playerselect.isdigit():
                playerselect = int(playerselect) - 1
                if 0 <= playerselect < len(sv):
                    del sv[playerselect]
                    pickle.dump(sv, open('saves.p', 'wb'))
                    break
                else:
                    print "Try a better number."
            elif playerselect == 'q':
                break
            else:
                print "Choose a number!"
        continue
    elif choice == 'v' or choice == 'V':
        lb1 = pickle.load(open('leaderboard.p', 'rb'))
        if len(lb1) == 0:
            print "No winners yet."
            continue
        else:
            print "Leaderboard:"
            count = 1
            for el in lb1:
                print " %d: Name: %s Cash: %d Turns %d" %(count, el[0], el[1], el[2])
                count += 1
            del lb1, count
    else:
        raw_input("Hmmm, not a great start.. Try again!")

while True:
    while not player.nextFlag:
        print "\nTurn Number %d" %player.turns
        if player.infoOut():
            break
        player.takeTurn()
    if player.winFlag == True:
        break
    if player.quitFlag == True:
        quit()
    raw_input("End turn %d" %player.turns)
    player.nextFlag = False
    player.endTurn()

playerTup = (player.name, player.cash, player.turns)
lb = pickle.load(open("leaderboard.p", "rb"))
lb.append(playerTup)
lb.sort(key = lambda tup: tup[1], reverse = True)
lb.sort(key = lambda tup: tup[2])
if len(lb) > 10:
    for el in xrange(10, len(lb)):
        del lb[el]
pickle.dump(lb, open("leaderboard.p", "wb"))
print "The new leaderboard looks like:"
count = 1
for el in lb:
    print " %d: Name: '%s' Cash: %d$ Turns %d" %(count, el[0], el[1], el[2])
    count += 1