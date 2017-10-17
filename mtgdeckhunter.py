#!/usr/bin/env python
import urllib2, re, argparse, json, operator, random, io, sys

__author__  = "Jeff White [karttoon] @noottrak"
__email__   = "karttoon@gmail.com"
_version_ = "1.0.0"
__date__    = "02JUL017"

#
# JSON struct
#
# deckDB {
#
#         "deckbox": {
#                     deckID: {
#                              "deckCount": 1,
#                              "deckTitle": deckName,
#                              "deckCards": {
#                                            "cardName": 1,
#
#          "goldfish": {
#                       deckID: {
#                                "deckCount": 1,
#                                "deckTitle": deckName,
#                                "deckCards": {
#                                              "cardName": 1,
#
#          "mtgtop8": {
#                      "deckURL": webURL,
#                      deckID: {
#                               "deckCount": 1,
#                               "deckTitle": deckName,
#                               "deckCards": {
#                                             "cardName": 1,
#           "precon": {
#                      deckID: {
#                               "deckURL": webURL,
#                               "deckCount": 1,
#                               "deckTitle": deckName,
#                               "deckCards": {
#                                             "cardName": 1,
#
#

def loadCard(args):

    try:
        cardDB = json.load(open("card.db"))
        print "[+] Loaded existing card data from 'card.db'"

    except:
        print "[!] Failed to load/find existing 'card.db'. Creating a new one."
        cardDB = createCard(cardDB={})

    if args.verbose:
        cardStats(cardDB)

    return cardDB

def createCard(cardDB):

    playerNum = raw_input("\n    [!] Provide DeckBox Inventory number: ")

    print

    # Parse card collection
    response = urllib2.urlopen("https://deckbox.org/sets/%s/export?s=&f=&o=" % playerNum)
    html     = response.read()

    html = html.replace("\n", "")
    html = re.search("\<body\>.+\<\/body\>", html).group()
    html = html.replace("<body>", "").replace("</body>", "")
    html = html.replace("<br/>", "\n")
    html = html.strip().split("\n")

    for line in html:

        cardCount = line.split(" ")[0]
        cardName  = " ".join(line.split(" ")[1:])

        if cardName not in cardDB.values():
            cardDB[cardName] = int(cardCount)
        else:
            cardDB[cardName] += int(cardCount)

    saveCard(cardDB)

    return cardDB

def loadDeck(args):

    try:
        deckDB    = json.load(open("deck.db"))
        deckCount = 0

        for site in deckDB:
            deckCount += len(deckDB[site])

        print "[+] Loaded %s existing deck data from 'deck.db'" % (deckCount - 2)

    except:
        deckDB = {"deckbox"     :{},
                  "goldfish"    :{"deckURL":[]},
                  "mtgtop8"     :{"deckURL":[]},
                  "precon"      :{}
                  }

        print "[!] Failed to load/find existing 'deck.db'. Creating a new one."

    # Takes VERY long as deckDB grows - leave commented unless you really care about it
    #if args.verbose:
    #    deckStats(deckDB)

    # Print deck count per site
    print

    for site in deckDB:

        if site == "goldfish" or site == "mtgtop8":

            deckLen = len(deckDB[site]) - 1

        else:

            deckLen = len(deckDB[site])

        print "        %-10s - %s Decks" % (site, deckLen)

    return deckDB

def saveCard(cardDB):

    json.dump(cardDB, open("card.db", "w"))

    return

def saveDeck(deckDB):

    # Save the deck and keep a successful copy as backup
    # If you cancel / script crashes sometimes JSON will get corrupt so best to keep a backup
    try:
        print "    [*] Saving data..."

        json.dump(deckDB, open("deck.db", "w"))

        print "    [*] Saving backup..."

        json.dump(deckDB, open("backup_deck.db", "w"))

        print "    [*] Saves complete. Resuming..."

    except:
        print "\n[!] Issue with the save! Backup deck can be found at backup_deck.db!"
                
        sys.exit(1)

    return deckDB

def deckStats(deckDB):

    highCard, lowCard, uniqueCards, totalCards = deckCount(deckDB)

    print "\n    [-] Total cards in deck data              - %s" % totalCards
    print "    [-] Unique cards in deck data             - %s" % uniqueCards
    print "    [-] Most common non-basic land card       - %s" % highCard
    print "    [-] Least common non-basic land card      - %s" % lowCard

    return

def deckCount(deckDB):

    totalCards = 0

    cardList = {}

    for site in deckDB:

        for deck in deckDB[site]:

            ignoreDecks = ["deckURL"]

            if deck not in ignoreDecks:

                for card in deckDB[site][deck]["deckCards"]:

                    totalCards += deckDB[site][deck]["deckCards"][card]

                    if card in cardList:

                        cardList[card] += deckDB[site][deck]["deckCards"][card]

                    else:

                        cardList[card] = deckDB[site][deck]["deckCards"][card]

    # Remove lands from list since these will always surpass regular cards
    cardList.pop("Forest",      None)
    cardList.pop("Plains",      None)
    cardList.pop("Swamp",       None)
    cardList.pop("Mountain",    None)
    cardList.pop("Island",      None)

    highCard    = max(cardList.iteritems(), key=operator.itemgetter(1))[0]
    lowCard     = min(cardList.iteritems(), key=operator.itemgetter(1))[0]
    uniqueCards = len(cardList)

    return highCard, lowCard, uniqueCards, totalCards

def deckClean(deckDB):

    deleteDecks = {}
    ignoreList  = ["deckURL"]

    for site in deckDB:

        deleteDecks[site] = []

        for deckID in deckDB[site]:

            if deckID not in ignoreList:

                # Delete decks under 40 cards
                if deckDB[site][deckID]["deckCount"] < 40:

                    deleteDecks[site].append(deckID)

                # Delete decks over 135 cards
                if deckDB[site][deckID]["deckCount"] > 135:

                    deleteDecks[site].append(deckID)

    deletedCount = 0

    for site in deleteDecks:

        for deckID in deleteDecks[site]:

            deckDB[site].pop(deckID)
            deletedCount += 1

    print "\n[+] Pruned %s decks due to size restrictions." % deletedCount

    deckDB = saveDeck(deckDB)

    return deckDB

def cardStats(cardDB):

    highCard, lowCard, uniqueCards, totalCards = cardCount(cardDB)

    print "\n    [-] Total cards in your collection        - %s" % totalCards
    print "    [-] Unique cards in your collection       - %s" % uniqueCards
    print "    [-] Most common non-basic land card       - %s" % highCard
    print "    [-] Least common non-basic land card      - %s\n" % lowCard

    return

def cardCount(cardDB):

    cardList   = {}
    totalCards = 0

    for card in cardDB:

        totalCards += cardDB[card]

    for card in cardDB:

        if card in cardList:

            cardList[card] += cardDB[card]

        else:
            cardList[card] = cardDB[card]

    cardList.pop("Forest",      None)
    cardList.pop("Plains",      None)
    cardList.pop("Swamp",       None)
    cardList.pop("Mountain",    None)
    cardList.pop("Island",      None)

    highCard    = max(cardList.iteritems(), key=operator.itemgetter(1))[0]
    lowCard     = min(cardList.iteritems(), key=operator.itemgetter(1))[0]
    uniqueCards = len(cardList)

    return highCard, lowCard, uniqueCards, totalCards

def checkDecks(deckDB, args):

    # Randomly select order of sites from which to parse for updates
    print "[+] Checking sites for new decks..."

    siteList = ["deckbox", "goldfish", "mtgtop8"]

    random.shuffle(siteList)

    for site in siteList:

        if site == "deckbox":

            deckDB = dbcheckSite(deckDB, args)

        if site == "goldfish":

            deckDB = gfcheckSite(deckDB, args)

        if site == "mtgtop8":

            deckDB = t8checkSite(deckDB, args)

    return deckDB

def t8checkSite(deckDB, args):

    print """\n###########
# MtGTop8 #
###########
"""

    response = urllib2.urlopen("http://mtgtop8.com/index")
    html     = response.read()

    # Parse eventID's out
    urlList = [x.replace("event?e=","").replace("&","") for x in re.findall("event\?e=[0-9]+&", html)]

    if urlList[-1] not in deckDB["mtgtop8"]["deckURL"] or args.update != False:

        print "[!] Press CTRL+C to stop updating a section at any time\n"

        try:
            deckDB = t8updateDecks(deckDB, urlList, args)

        except KeyboardInterrupt:
            deckDB = saveDeck(deckDB)
            return deckDB

    else:

        print "    [!] MtGTop8 up-to-date"

    return deckDB

def t8updateDecks(deckDB, urlList, args):

    deckCount = 0
    noName = ["W.png",
              "B.png",
              "R.png",
              "G.png",
              "U.png",
              "C.png"]

    if urlList[0] not in deckDB["mtgtop8"]["deckURL"]:

        print "[+] Performing incremental deck update\n"

        try:

            # Check if this is the first run and adjust accordingly to correctly download some
            if deckDB["mtgtop8"]["deckURL"] == []:

                deckDB["mtgtop8"]["deckURL"] = urlList

                highID = int(urlList[0])

            for event in range(highID, int(urlList[-1]), -1):

                response = urllib2.urlopen("http://mtgtop8.com/event?e=%s" % event)

                # Site uses Windows-1252 so we'll convert as necessary
                try:
                    html = response.read().decode("Windows-1252").encode("utf-8")
                except:
                    html = response.read()

                # Remove newline as their HTML sometimes splits titles
                html     = html.replace("\n", "")

                if "data[Deck][cards]" not in html:

                    pass

                else:

                    # Parse deckID's from each event
                    deckList   = re.findall("\?e=[0-9]+\&d=[0-9]+\&f=[A-Z]{2,3}", html)
                    eventTitle = str(re.search("class=S18 align=center\>.+?\</td\>", html).group().replace("class=S18 align=center>","").replace("</td>", ""))

                    if event not in deckDB["mtgtop8"]["deckURL"]:

                        # Need to keep events separate from deck data
                        deckDB["mtgtop8"]["deckURL"].append(event)

                        print "    [#] Downloading decks from event %s - %s" % (event, eventTitle)

                        for deckID in deckList:

                            deckID      = deckID.split("=")[2].replace("&f", "")
                            titleSearch = r"d=" + deckID + "&f=[A-Z].+?\>.+?\<\/a\>"
                            deckTitle   = str(re.search(titleSearch, html).group().split(">")[1].replace("</a", ""))

                            #Rename decks that are just colored (sealed)
                            for image in noName:

                                if image in deckTitle:

                                    deckTitle = "NoName Sealed"

                            try:
                                deckDB = t8scrapeDeck(deckDB, deckID, deckTitle)

                            except:
                                pass

                            deckCount += 1

                            # Save after every 100 decks
                            if deckCount == 100:

                                deckDB = saveDeck(deckDB)

                                deckCount = 0

        except KeyboardInterrupt:
            deckDB = saveDeck(deckDB)
            return deckDB

    # Full update
    if args.update == True:

        print "[+] Performing full deck update\n"

        try:

            deckDB["mtgtop8"]["deckURL"].sort()

            lowID     = int(deckDB["mtgtop8"]["deckURL"][0])
            highID    = int(deckDB["mtgtop8"]["deckURL"][-1])

            if args.verbose:
                print "    [-] Most recent saved event ID - %s" % highID
                print "    [-] Oldest saved event ID      - %s" % lowID

            for event in range(lowID, 0, -1):

                response = urllib2.urlopen("http://mtgtop8.com/event?e=%s" % event)

                # Site uses Windows-1252 so we'll convert as necessary
                try:
                    html = response.read().decode("Windows-1252").encode("utf-8")
                except:
                    html = response.read()

                # Remove newline as their HTML sometimes splits titles
                html     = html.replace("\n", "")

                if "data[Deck][cards]" not in html:

                    pass

                else:

                    # Parse deckID's from each event
                    deckList   = re.findall("\?e=[0-9]+\&d=[0-9]+\&f=[A-Z]{2,3}", html)
                    eventTitle = str(re.search("class=S18 align=center\>.+?\</td\>", html).group().replace("class=S18 align=center>", "").replace("</td>", ""))

                    if event not in deckDB["mtgtop8"]["deckURL"]:

                        # Need to keep events separate from deck data
                        deckDB["mtgtop8"]["deckURL"].append(event)

                        print "    [#] Downloading decks from event %s - %s" % (event, eventTitle)

                        for deckID in deckList:

                            deckID      = deckID.split("=")[2].replace("&f", "")
                            titleSearch = r"d=" + deckID + "&f=[A-Z].+?\>.+?\<\/a\>"
                            deckTitle   = str(re.search(titleSearch, html).group().split(">")[1].replace("</a", ""))

                            #Rename decks that are just colored (sealed)
                            for image in noName:

                                if image in deckTitle:

                                    deckTitle = "NoName Sealed"

                            try:
                                deckDB = t8scrapeDeck(deckDB, deckID, deckTitle)

                            except:
                                pass

                            deckCount += 1

                            # Save after every 100 decks
                            if deckCount == 100:

                                deckDB = saveDeck(deckDB)

                                deckCount = 0

        except KeyboardInterrupt:

            print "\n[!] Caught exception. Saving deck and exiting.\n"

            deckDB = saveDeck(deckDB)

            return deckDB

    return deckDB

def t8scrapeDeck(deckDB, deckID, deckTitle):

    # Validate deck hasn't been seen before
    if deckID not in deckDB["mtgtop8"]:

        deckDB["mtgtop8"][deckID] = {"deckCards": {}, "deckCount": 0}

        response = urllib2.urlopen("http://mtgtop8.com/dec?d=%s" % deckID)
        html     = response.read()

        # Parse deck for cards
        cardList = re.findall("[0-9]{1,2} \[.+?\] .+?\n", html)

        deckDB["mtgtop8"][deckID]["deckTitle"] = deckTitle

        print "    [-] Adding deck %s - %s" % (deckID, deckTitle)

        for cardInfo in cardList:

            cardCount = int(cardInfo.split(" ")[0])
            # Slash replace to keep inline with other two sites for dual split cards
            cardName  = u" ".join(cardInfo.split(" ")[2:]).replace("/", "//").strip()

            if cardName in deckDB["mtgtop8"][deckID]["deckCards"]:

                deckDB["mtgtop8"][deckID]["deckCards"][cardName] += cardCount

            else:

                deckDB["mtgtop8"][deckID]["deckCards"][cardName] = cardCount

            deckDB["mtgtop8"][deckID]["deckCount"] += cardCount

    return deckDB

def gfcheckSite(deckDB, args):

    print """\n###############
# MtGGoldfish #
###############
"""

    # These can be tuned if necessary
    formatList = ["standard",
                  "modern",
                  "pauper",
                  "legacy",
                  "vintage",
                  "frontier",
                  "commander_1v1",
                  "commander",
                  "tiny_leaders"
                  ]

    print "[!] Press CTRL+C to stop updating a section at any time\n"

    try:
        for format in formatList:

            urlList = []

            # Parse "full" ($$$) deckURL's
            response = urllib2.urlopen("https://www.mtggoldfish.com/metagame/%s/full#paper" % format)
            html     = response.read()

            for urlEntry in [x for x in re.findall("\/archetype\/.+?'\>\<", html)]:

                urlList.append(urlEntry)

            # Parse "budget" ($) deckURL's
            response = urllib2.urlopen("https://www.mtggoldfish.com/decks/budget/%s#paper" % format)
            html     = response.read()

            for urlEntry in [x for x in re.findall("\/deck\/[0-9]{1,7}'\>\<", html)]:

                urlList.append(urlEntry)

            if all(x in deckDB["goldfish"]["deckURL"] for x in urlList):

                print "    [!] %s format decks up-to-date" % format

            else:

                print "    [#] Downloading %s format new decks..." % format

                deckDB = gfupdateDecks(deckDB, urlList, args)

    except KeyboardInterrupt:
        deckDB = saveDeck(deckDB)
        return deckDB

    return deckDB

def gfupdateDecks(deckDB, urlList, args):

    deckCount = 0
    deckList  = {}

    for urlEntry in urlList:

        if urlEntry not in deckDB["goldfish"]["deckURL"]:

            # Parse deck for card
            response = urllib2.urlopen("https://www.mtggoldfish.com/%s#paper" % urlEntry.replace("'><", ""))
            html     = response.read()

            deckDB["goldfish"]["deckURL"].append(urlEntry)

            try:
                deckTitle = str(re.search("\<title\>.+?\<\/title\>", html).group().replace("<title>", "").replace("</title>",""))

                if "/deck/download/" not in html:
                    #print "    [!] No download link for deck - %s" % deckTitle
                    break

                deckID           = str(re.search("\/deck\/download\/[0-9]{1,7}\"\>", html).group().replace("/deck/download/","").replace("\">", ""))
                deckList[deckID] = deckTitle

                try:
                    gfscrapeDeck(deckDB, deckID, deckList)

                except:
                    pass

                deckCount += 1

                # Save after every 100 decks
                if deckCount == 100:

                    deckDB = saveDeck(deckDB)

                    deckCount = 0

            except:
                pass

    return deckDB

def gfscrapeDeck(deckDB, deckID, deckList):

    deckTitle                               = deckList[deckID].replace("for Magic: the Gathering", "")
    deckDB["goldfish"][deckID]              = {"deckCards": {}, "deckCount": 0}
    deckDB["goldfish"][deckID]["deckTitle"] = deckTitle

    print "    [-] Adding Deck %s - %s" % (deckID, deckTitle)

    # Parse cards from deck
    response = urllib2.urlopen("https://www.mtggoldfish.com/deck/download/%s" % deckID)
    html     = response.read()

    cardList = re.findall("[0-9]{1,2} .+?\r\n", html)

    for card in cardList:

        cardCount = int(card.split(" ")[0])
        cardName  = str(" ".join(card.replace("\r\n", "").split(" ")[1:]))

        if cardName in deckDB["goldfish"][deckID]["deckCards"]:

            deckDB["goldfish"][deckID]["deckCards"][cardName] += cardCount

        else:

            deckDB["goldfish"][deckID]["deckCards"][cardName] = cardCount

        deckDB["goldfish"][deckID]["deckCount"] += cardCount

    return deckDB

def dbcheckSite(deckDB, args):

    print """\n###########
# Deckbox #
###########
"""

    # Parse deckID's
    response = urllib2.urlopen("https://deckbox.org/decks/mtg")
    html     = response.read()

    latestID = re.search("\/sets\/[0-9]+\"\>", html).group().replace("/sets/", "").replace("\">", "")

    if latestID not in deckDB["deckbox"] or args.update == True:

        try:
            deckDB = dbupdateDecks(deckDB, html, args)

        except KeyboardInterrupt:
            deckDB = saveDeck(deckDB)
            return deckDB

    else:
        print "    [!] Deckbox up-to-date"

    return deckDB

def dbupdateDecks(deckDB, html, args):

    deckList   = []
    ignoreList = ["deckURL"]

    for deckID in deckDB["deckbox"]:

        if deckID not in ignoreList:

            deckList.append(deckID)

    deckList.sort()

    latestID    = int(re.search("\/sets\/[0-9]+\"\>", html).group().replace("/sets/", "").replace("\">", ""))

    # First run
    if deckList == []:

        lowID  = latestID - 50
        highID = latestID - 50

    else:

        lowID  = int(deckList[0])
        highID = int(deckList[-1])

    deckCount   = 0

    if args.verbose:
        print "\n    [-] Latest ID on Deckbox - %s" % latestID
        print "    [-] Most recent saved ID - %s" % highID
        print "    [-] Oldest saved ID      - %s" % lowID

    print "[!] Press CTRL+C to stop updating at any time\n"

    if latestID > highID:

        print "[+] Performing incremental deck update\n"

        for deckID in range(latestID, highID, -1):

            try:
                deckDB = dbscrapeDeck(deckDB, deckID)

            except KeyboardInterrupt:
                deckDB = saveDeck(deckDB)
                return deckDB

            except:
                pass

            deckCount += 1

            # Save after every 100 decks
            if deckCount == 100:

                deckDB = saveDeck(deckDB)

                deckCount = 0

    # Full update will likely be canceled
    if args.update != False and lowID > 0:

        print "[+] Performing full deck update\n"

        for deckID in range(lowID, 0, -1):

            try:
                deckDB = dbscrapeDeck(deckDB, deckID)

            except KeyboardInterrupt:
                deckDB = saveDeck(deckDB)
                return deckDB

            except:
                pass

            deckCount += 1

            # Save after every 100 decks
            if deckCount == 100:

                deckDB = saveDeck(deckDB)

                deckCount = 0

    return deckDB

def dbscrapeDeck(deckDB, deckID):

    deckDB["deckbox"][deckID] = {"deckCards": {}, "deckCount": 0}

    # Parse cards from deck
    response = urllib2.urlopen("https://deckbox.org/sets/%s" % deckID)
    html     = response.read()

    html = html.replace("\n", "")

    cardEntries = re.findall("\<tr id='[0-9]+_main'\>.+?\<\/tr\>", html)

    deckTitle = re.search("\"name\":\".+?\",\"", html).group()
    deckTitle = str(deckTitle.replace("\"name\":\"", "").replace("\",\"", ""))

    if deckTitle == "Wishlist" or deckTitle == "Tradelist" or deckTitle == "Inventory":

        return deckDB

    else:

        print "    [-] Adding Deck %s - %s" % (deckID, deckTitle)

    deckDB["deckbox"][deckID]["deckTitle"] = deckTitle

    for entry in cardEntries:

        entry = entry.replace("<", "\n")
        entry = entry.strip().split("\n")

        cardName  = str(entry[4].split(">")[1])
        cardCount = int(entry[1].replace("td class='card_count'>", "").replace("</td", ""))

        if cardName in deckDB["deckbox"][deckID]["deckCards"]:

            deckDB["deckbox"][deckID]["deckCards"][cardName] += cardCount

        else:

            deckDB["deckbox"][deckID]["deckCards"][cardName] = cardCount

        deckDB["deckbox"][deckID]["deckCount"] += cardCount

    return deckDB

def searchDecks(cardDB, deckDB, args):

    deckList = {}

    print "\n[+] Searching for playable decks with %s%% match\n" % args.commonality

    lowSize  = int(args.size.split("-")[0])
    highSize = int(args.size.split("-")[1])

    for site in deckDB:

        deckList[site] = {}

        for deckID in deckDB[site]:

            # Filter out so only decks come through + correct size
            if deckID != "deckURL" and deckDB[site][deckID]["deckCount"] >= lowSize and deckDB[site][deckID]["deckCount"] <= highSize:

                matchState, matchDelta, matchCount = matchDecks(cardDB, deckDB, deckID, site, args)

                if matchState == True:

                    deckList[site][deckID] = {"matchDelta": matchDelta, "matchCount": matchCount}

    return deckList

def matchDecks(cardDB, deckDB, deckID, site, args):

    commonality = float(args.commonality) / float(100)
    matchCount  = 0
    deckCount   = 0
    deckDelta   = []

    for card in deckDB[site][deckID]["deckCards"]:

        deckCount += deckDB[site][deckID]["deckCards"][card]

    for card in deckDB[site][deckID]["deckCards"]:

        if card not in cardDB and commonality == 1.0:

            return False, None, None

        if card in cardDB:

            if deckDB[site][deckID]["deckCards"][card] > cardDB[card] and commonality == 1.0:

                return False, None, None

            if deckDB[site][deckID]["deckCards"][card] <= cardDB[card]:

                matchCount += deckDB[site][deckID]["deckCards"][card]

            else:

                # Capture cards in collection but missing count
                matchCount += cardDB[card]
                deckDelta.append("%s - %s" % (deckDB[site][deckID]["deckCards"][card] - cardDB[card],card))

        # Capture cards not in collection
        if card not in cardDB:

            deckDelta.append("%s - %s" % (deckDB[site][deckID]["deckCards"][card], card))

    # Check for 100% (default) or specified match %
    try:
        if float(matchCount)/float(deckCount) >= commonality:

            return True, deckDelta, str("%s%% (%-3s/%-3s)" % (int(float(matchCount)/float(deckCount) * 100.0), matchCount, deckCount))

        else:

            return False, None, None

    except:
        return False, None, None

def printDecks(deckDB, deckID, site, args, filterWords, matchCount, matchDelta):

    # Deck structure for pre-cons slightly different since no ID
    if site == "precon":

        deckTitle = deckID

    else:

        deckTitle = deckDB[site][deckID]["deckTitle"]

    if any(x.lower() in deckTitle.lower() for x in filterWords):

        return

    if site == "deckbox":

        print "    [-] Deck %s - %s (%s cards - %s)\n            https://deckbox.org/sets/%s\n" % (deckID,
                                                                                                 deckTitle,
                                                                                                 deckDB[site][deckID]["deckCount"],
                                                                                                 matchCount.split(" ")[0],
                                                                                                 deckID)
        if args.verbose:

            print "        [!] %-5s - Missing Cards: %s\n" % (matchCount, ", ".join(matchDelta))

    if site == "goldfish":

        print "    [-] Deck %s - %s (%s cards - %s)\n            https://www.mtggoldfish.com/deck/%s\n" % (deckID,
                                                                                                         deckTitle,
                                                                                                         deckDB[site][deckID]["deckCount"],
                                                                                                         matchCount.split(" ")[0],
                                                                                                         deckID)
        if args.verbose:

            print "        [!] %-5s - Missing Cards: %s\n" % (matchCount, ", ".join(matchDelta))

    if site == "mtgtop8":

        print "    [-] Deck %s - %s (%s cards - %s)\n            http://mtgtop8.com/event?d=%s\n" % (deckID,
                                                                                                   deckTitle,
                                                                                                   deckDB[site][deckID]["deckCount"],
                                                                                                   matchCount.split(" ")[0],
                                                                                                   deckID)
        if args.verbose:

            print "        [!] %-5s - Missing Cards: %s\n" % (matchCount, ", ".join(matchDelta))

    if site == "precon":

        print "    [-] Official - %s (%s cards - %s)\n            %s\n" % (deckTitle,
                                                                         deckDB[site][deckID]["deckCount"],
                                                                         matchCount.split(" ")[0],
                                                                         deckDB["precon"][deckID]["deckURL"])

def main():

    parser = argparse.ArgumentParser(description="Find playable decks from DeckBox, MTGTOP8, MTGGoldFish, and Official PreCons")
    parser.add_argument("-u", "--update", help="Perform full deck update.", action="store_true")
    parser.add_argument("-c", "--commonality", help="Match above specified percentage, default is 100%%.", metavar="<num>", type=int, default=100)
    parser.add_argument("-n", "--noupdate", help="Perform just deck matches on existing data.", action="store_true")
    parser.add_argument("-v", "--verbose", help="Print additional meta data. Can take a LONG time to process.", action="store_true")
    parser.add_argument("-f", "--filter", help="Comma separated list of words to filter from matched decks.")
    parser.add_argument("-s", "--size", help="Limit returned decks to a certain deck size, default is 40-80.", metavar="<lownum>,<highnum>", default="40-80")
    args = parser.parse_args()

    print """
    __  __,  _   __,__, __,        _
    / \_( \ /_\ //~_) |//~'     _ (_) _
   / %  : '<_v_\\\\\\~/|_(\\\\__, _ (_)   (_)
  / /\  C\  \ ~  ~~ ~ ~ ~~~~~    _   _
 / /  \  \ \ \  The Gathering   (_) (_)
~~~    ~~`  ~~`
    """

    cardDB = loadCard(args)
    deckDB = loadDeck(args)

    filterWords = []

    if args.filter:

        filterWords = args.filter.split(",")

    if not args.noupdate:

        checkDecks(deckDB, args)

        deckDB = deckClean(deckDB)

    deckList = searchDecks(cardDB, deckDB, args)

    if len(deckList) > 0:

        for site in deckList:

            for deckID in deckList[site]:

                printDecks(deckDB,
                           deckID,
                           site,
                           args,
                           filterWords,
                           deckList[site][deckID]["matchCount"],
                           deckList[site][deckID]["matchDelta"])

    else:

        print "[!] No playable decks with current cards\n"

if __name__ == "__main__":

    main()
