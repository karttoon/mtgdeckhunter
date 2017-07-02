# mtgdeckhunter
Uses your Magic the Gathering (MtG) library of cards to search within decks downloaded from [Deckbox](https://deckbox.org/), [MtG Goldfish](https://www.mtggoldfish.com/), and [MtG Top 8](http://mtgtop8.com/index) for ones you can build.

Create your library of cards on the Deckbox inventory page and enter your ID when you run the script for the first time. My collection is listed [here](https://deckbox.org/sets/1721702) and in file "card.db" that I've included for testing purposes. Additionally, you can download a "deck.db" file I've uploaded with contains 16 official pre-constructed decks. You're on your own for actually downloading the decks from the sites as it takes long time and fairly temporal in context (current format/sets).

Blog post - [02JUL2017 - MtG Deck Hunting](http://ropgadget.com/posts/mtg_deck_hunting.html)

I've included a number of features to make searching the downloaded decks slightly easier and I'll cover these flags towards the end.

Each deck will have a corresponding URL that links back to the source of the deck where you can get additional information on the respective site. This is purely meant as a quick way to hone in on potential decks you can build with your current library and is not meant to suggest any particular deck or style.

*NOTE: I will not be actively maintaining this script and just created it to suit a specific need of mine, which turned out to be rather fruitless, so you're on your own for fixes and updates.

Before getting into it, below is the usage for the script.

```
usage: mtgdeckhunter.py [-h] [-u] [-c <num>] [-n] [-v] [-f FILTER]
                        [-s <lownum>,<highnum>]

Find playable decks from DeckBox, MTGTOP8, MTGGoldFish, and Official PreCons

optional arguments:
  -h, --help            show this help message and exit
  -u, --update          Perform full deck update.
  -c <num>, --commonality <num>
                        Match above specified percentage, default is 100%.
  -n, --noupdate        Perform just deck matches on existing data.
  -v, --verbose         Print additional meta data. Can take a LONG time to
                        process.
  -f FILTER, --filter FILTER
                        Comma separated list of words to filter from matched
                        decks.
  -s <lownum>,<highnum>, --size <lownum>,<highnum>
                        Limit returned decks to a certain deck size, default
                        is 40-80.
```                        

Running the script for the first time will look similar to the below output (truncated for space).

```
$ python mtgdeckhunter.py

    __  __,  _   __,__, __,        _
    / \_( \ /_\ //~_) |//~'     _ (_) _
   / %  : '<_v_\\\~/|_(\\__, _ (_)   (_)
  / /\  C\  \ ~  ~~ ~ ~ ~~~~~    _   _
 / /  \  \ \ \  The Gathering   (_) (_)
~~~    ~~`  ~~`

[!] Failed to load/find existing 'card.db'. Creating a new one.

    [!] Provide DeckBox Inventory number: 1721702

[+] Loaded 16 existing deck data from 'deck.db'

        goldfish   - 0 Decks
        mtgtop8    - 0 Decks
        precon     - 16 Decks
        deckbox    - 0 Decks

[+] Checking sites for new decks...

###############
# MtGGoldfish #
###############

[!] Press CTRL+C to stop updating a section at any time

    [#] Downloading standard format new decks...
    [-] Adding Deck 688877 - Temur Energy Deck 
    [-] Adding Deck 688879 - Mardu Vehicles Deck 
    [-] Adding Deck 679204 - GB Energy Deck 
<TRUNCATED>
    [-] Adding Deck 487606 - GU Emerge — Kaladesh Update  Deck
    [-] Adding Deck 487411 - GW Bloodbriar — Kaladesh Update  Deck
    [-] Adding Deck 487602 - Evolutionary Dredge — Kaladesh Update  Deck
    [#] Downloading modern format new decks...
    [-] Adding Deck 686965 - Grixis Death&#39;s Shadow Deck 
    [-] Adding Deck 680198 - Eldrazi Tron Deck 
<TRUNCATED>
    [-] Adding Deck 677706 - Mardu Burn Deck 
    [-] Adding Deck 689488 - UR Deck 
    [-] Adding Deck 675310 - BR Deck 
<TRUNCATED>
    [-] Adding Deck 673466 - WR Deck 
    [-] Adding Deck 686989 - Jund Ramp Deck 
    [-] Adding Deck 686967 - Mono-Black Devotion Deck 
    [*] Saving data...
    [*] Saving backup...
    [*] Saves complete. Resuming...
    [-] Adding Deck 686973 - R/G Through the Breach Deck 
    [-] Adding Deck 686974 - Four-Color Saheeli Deck 
<TRUNCATED>
    [#] Downloading pauper format new decks...
<TRUNCATED>
    [#] Downloading legacy format new decks...
<TRUNCATED>
    [#] Downloading vintage format new decks...
<TRUNCATED>
    [#] Downloading frontier format new decks...
<TRUNCATED>
    [#] Downloading commander_1v1 format new decks...
<TRUNCATED>
    [#] Downloading commander format new decks...
<TRUNCATED>
    [#] Downloading tiny_leaders format new decks...
    [-] Adding Deck 660642 - Shu Yun, the Silent Tempest Deck 
    [-] Adding Deck 686100 - Alesha, Who Smiles at Death Deck 

###########
# Deckbox #
###########

[!] Press CTRL+C to stop updating at any time

[+] Performing incremental deck update

    [-] Adding Deck 1742911 - Copy of HOU Mono U Fray
    [-] Adding Deck 1742910 - insect tribal v2 devour
    [-] Adding Deck 1742909 - Death and Taxes Brian Coval
<TRUNCATED>
    [-] Adding Deck 1742864 - nekuar
    [-] Adding Deck 1742863 - M - Grixis Death\u0026#39;s Shadow 1
    [-] Adding Deck 1742862 - BoslanKek

###########
# MtGTop8 #
###########

[!] Press CTRL+C to stop updating a section at any time

[+] Performing incremental deck update

    [#] Downloading decks from event 16039 - Environmental Master - Amonkhet
    [-] Adding deck 298748 - Emerge
    [-] Adding deck 298749 - Golgari Constrictor
    [-] Adding deck 298751 - Mardu Vehicle
    [-] Adding deck 298750 - Temur Energy
    [-] Adding deck 298754 - Emerge
    [-] Adding deck 298747 - Golgari Constrictor
    [-] Adding deck 298752 - Golgari Constrictor
    [-] Adding deck 298753 - Jund
    [#] Downloading decks from event 16038 - MTGO Pauper League
    [-] Adding deck 298743 - Deep Hours Aggro
<TRUNCATED>
    [#] Downloading decks from event 15778 - MTGO Competitive Standard League
    [-] Adding deck 296787 - Mono Black Zombies
    [-] Adding deck 296788 - Jund
    [-] Adding deck 296789 - Red Deck Wins
    [-] Adding deck 296786 - Golgari Constrictor
    [-] Adding deck 296785 - Golgari Constrictor
    [-] Adding deck 296784 - Jund
    [-] Adding deck 296783 - Marvelous Energy

[+] Pruned 24 decks due to size restrictions.
    [*] Saving data...
    [*] Saving backup...
    [*] Saves complete. Resuming downloads...

[+] Searching for playable decks with 100% match

    [-] Deck 298009 - NoName Sealed (40 cards - 100%)
            http://mtgtop8.com/event?d=298009

    [-] Deck 298008 - NoName Sealed (40 cards - 100%)
            http://mtgtop8.com/event?d=298008

    [-] Deck 298579 - NoName Sealed (61 cards - 100%)
            http://mtgtop8.com/event?d=298579

    [-] Deck 296929 - NoName Sealed (61 cards - 100%)
            http://mtgtop8.com/event?d=296929
```

Basically it will iterate over each site and try to download the latest decks from when you last ran the script. For MtG Top 8 and Deckbox you can use the "-u" flag for full update which will cause it to just keep downloading decks from those sites. For MtG Top 8 it's feasible to download all of the decks in a night but for Deckbox, which is primarily creative deck ideas versus actual decks used like on Top 8, you'll be downloading until the end of enternity and most will be garbage. Alternatively, you can use the "-n" flag to not do any updates and just focus on the deck hunting.

Alright, so let's say I don't care about sealed draft decks, test decks, or X decks because they are most likely not theorycrafted enough and people were just dealt what they were dealt. You can  use the "-f" flag to filter out certain decks.

```
$ python mtgdeckhunter.py -n -f sealed,draft,test

    __  __,  _   __,__, __,        _
    / \_( \ /_\ //~_) |//~'     _ (_) _
   / %  : '<_v_\\\~/|_(\\__, _ (_)   (_)
  / /\  C\  \ ~  ~~ ~ ~ ~~~~~    _   _
 / /  \  \ \ \  The Gathering   (_) (_)
~~~    ~~`  ~~`

[+] Loaded existing card data from 'card.db'
[+] Loaded 94593 existing deck data from 'deck.db'

        goldfish   - 1294 Decks
        mtgtop8    - 78463 Decks
        precon     - 16 Decks
        deckbox    - 14820 Decks

[+] Searching for playable decks with 100% match

    [-] Deck 1703378 - Amonkhet League (42 cards - 100%)
            https://deckbox.org/sets/1703378

    [-] Deck 1740542 - Bant Control AKHx6 (40 cards - 100%)
            https://deckbox.org/sets/1740542

    [-] Deck 1742059 - Missing AKH C (62 cards - 100%)
            https://deckbox.org/sets/1742059

    [-] Deck 1741945 - 2017/06/30 (40 cards - 100%)
            https://deckbox.org/sets/1741945

    [-] Deck 1697612 - Day 2 Chaff (52 cards - 100%)
            https://deckbox.org/sets/1697612
```

Cool, but what if I want to search for decks where I have most of the cards and only decks between 60-70 cards? You can use the "-c" commonality flag to specify what percentage the deck needs to match and the "-s" flag to specify the low/high numbers for the deck size.

```
$ python mtgdeckhunter.py -n -f sealed,draft,test -c 80 -s 60-70

    __  __,  _   __,__, __,        _
    / \_( \ /_\ //~_) |//~'     _ (_) _
   / %  : '<_v_\\\~/|_(\\__, _ (_)   (_)
  / /\  C\  \ ~  ~~ ~ ~ ~~~~~    _   _
 / /  \  \ \ \  The Gathering   (_) (_)
~~~    ~~`  ~~`

[+] Loaded existing card data from 'card.db'
[+] Loaded 94593 existing deck data from 'deck.db'

        goldfish   - 1294 Decks
        mtgtop8    - 78463 Decks
        precon     - 16 Decks
        deckbox    - 14820 Decks

[+] Searching for playable decks with 80% match

    [-] Deck 223629 - Unknown Scapeshift (60 cards - 80%)
            http://mtgtop8.com/event?d=223629

    [-] Official - Amonkhet - Gideon, Martial Paragon (60 cards - 81%)
            http://magic.wizards.com/en/articles/archive/news/amonkhet-planeswalker-deck-lists-2017-04-19#gideon_martial_paragon

    [-] Deck 1741853 - GR (60 cards - 91%)
            https://deckbox.org/sets/1741853

    [-] Deck 1742059 - Missing AKH C (62 cards - 100%)
            https://deckbox.org/sets/1742059

    [-] Deck 1740177 - Zombies (67 cards - 86%)
            https://deckbox.org/sets/1740177

    [-] Deck 1740194 - Embalm (Standard) (60 cards - 95%)
            https://deckbox.org/sets/1740194

    [-] Deck 1692181 - Amonkhet League SPEC (63 cards - 93%)
            https://deckbox.org/sets/1692181

    [-] Deck 1739950 - 20170621 - BG - -1/-1 - AKH (60 cards - 90%)
            https://deckbox.org/sets/1739950

    [-] Deck 1707170 - Deck Deck1 (61 cards - 96%)
            https://deckbox.org/sets/1707170

    [-] Deck 1740700 - Gideon (60 cards - 90%)
            https://deckbox.org/sets/1740700

    [-] Deck 1740712 - Copy of Zombie (Tournament 1) (60 cards - 88%)
            https://deckbox.org/sets/1740712

    [-] Deck 1740325 - Decimator Beetle \u0026amp; Hepatra (60 cards - 90%)
            https://deckbox.org/sets/1740325

    [-] Deck 1729593 - Mazo Eche (70 cards - 87%)
            https://deckbox.org/sets/1729593

    [-] Deck 1710712 - Deck 1 (60 cards - 88%)
            https://deckbox.org/sets/1710712

    [-] Deck 1742528 - Blue \u0026amp; White Tokens (63 cards - 92%)
            https://deckbox.org/sets/1742528

    [-] Deck 1742026 - Emily Amonkhet 1 red (60 cards - 85%)
            https://deckbox.org/sets/1742026

    [-] Deck 1740111 - w - trial of solidarity (60 cards - 81%)
            https://deckbox.org/sets/1740111

    [-] Deck 1742735 - White Zombie/Token (60 cards - 85%)
            https://deckbox.org/sets/1742735

    [-] Deck 1741227 - Attempt at Control (60 cards - 93%)
            https://deckbox.org/sets/1741227

    [-] Deck 1740340 - Crocodiles (63 cards - 87%)
            https://deckbox.org/sets/1740340

    [-] Deck 1742757 - Gideon Preconstructed Amonkhet (60 cards - 81%)
            https://deckbox.org/sets/1742757
```

Now I can check out the titles, see if anything stands out and hit the respective URL's to read more about the deck.

The "-v" verbose flag will give you some additional information about what you're missing, if that's interesting for knowing whether you might have a quick substitute.

```
$ python mtgdeckhunter.py -n -f sealed,draft,test -c 95 -v

    __  __,  _   __,__, __,        _
    / \_( \ /_\ //~_) |//~'     _ (_) _
   / %  : '<_v_\\\~/|_(\\__, _ (_)   (_)
  / /\  C\  \ ~  ~~ ~ ~ ~~~~~    _   _
 / /  \  \ \ \  The Gathering   (_) (_)
~~~    ~~`  ~~`

[+] Loaded existing card data from 'card.db'

    [-] Total cards in your collection        - 1094
    [-] Unique cards in your collection       - 321
    [-] Most common non-basic land card       - Evolving Wilds
    [-] Least common non-basic land card      - Open into Wonder

[+] Loaded 94593 existing deck data from 'deck.db'

        goldfish   - 1294 Decks
        mtgtop8    - 78463 Decks
        precon     - 16 Decks
        deckbox    - 14820 Decks

[+] Searching for playable decks with 95% match

    [-] Deck 298214 - TBD (45 cards - 97%)
            http://mtgtop8.com/event?d=298214

        [!] 97% (44 /45 ) - Missing Cards: 1 - Bontu's Monument

    [-] Deck 298211 - TBD (45 cards - 95%)
            http://mtgtop8.com/event?d=298211

        [!] 95% (43 /45 ) - Missing Cards: 1 - Ruthless Sniper, 1 - Mouth // Feed

    [-] Deck 1733716 - TSMTG Summer 2017 (45 cards - 95%)
            https://deckbox.org/sets/1733716

        [!] 95% (43 /45 ) - Missing Cards: 1 - Gravedigger, 1 - Regal Caracal

    [-] Deck 1740194 - Embalm (Standard) (60 cards - 95%)
            https://deckbox.org/sets/1740194

        [!] 95% (57 /60 ) - Missing Cards: 2 - Open into Wonder, 1 - Temmet, Vizier of Naktamun

    [-] Deck 1729729 - Amonkhet Pool (55 cards - 96%)
            https://deckbox.org/sets/1729729

        [!] 96% (53 /55 ) - Missing Cards: 1 - Sweltering Suns, 1 - Grasping Dunes

    [-] Deck 1739960 - W/R (50 cards - 96%)
            https://deckbox.org/sets/1739960

        [!] 96% (48 /50 ) - Missing Cards: 1 - Standing Troops, 1 - Wrangle

    [-] Deck 1707170 - Deck Deck1 (61 cards - 96%)
            https://deckbox.org/sets/1707170

        [!] 96% (59 /61 ) - Missing Cards: 1 - Throne of the God-Pharaoh, 1 - Regal Caracal

    [-] Deck 1697612 - Day 2 Chaff (52 cards - 100%)
            https://deckbox.org/sets/1697612

        [!] 100% (52 /52 ) - Missing Cards:

    [-] Deck 1739498 - Amonkhet- Gideon \u0026amp; Friends (40 cards - 97%)
            https://deckbox.org/sets/1739498

        [!] 97% (39 /40 ) - Missing Cards: 1 - Gideon of the Trials

    [-] Deck 1703378 - Amonkhet League (42 cards - 100%)
            https://deckbox.org/sets/1703378

        [!] 100% (42 /42 ) - Missing Cards:

    [-] Deck 1701266 - Work League (59 cards - 98%)
            https://deckbox.org/sets/1701266

        [!] 98% (58 /59 ) - Missing Cards: 1 - Sweltering Suns

    [-] Deck 1742059 - Missing AKH C (62 cards - 100%)
            https://deckbox.org/sets/1742059

        [!] 100% (62 /62 ) - Missing Cards:

    [-] Deck 1741945 - 2017/06/30 (40 cards - 100%)
            https://deckbox.org/sets/1741945

        [!] 100% (40 /40 ) - Missing Cards:

    [-] Deck 1741948 - 3 X AKH 6/30/17 (40 cards - 95%)
            https://deckbox.org/sets/1741948

        [!] 95% (38 /40 ) - Missing Cards: 1 - Sweltering Suns, 1 - Regal Caracal

    [-] Deck 1740542 - Bant Control AKHx6 (40 cards - 100%)
            https://deckbox.org/sets/1740542

        [!] 100% (40 /40 ) - Missing Cards:

    [-] Deck 1690805 - Magic League 1 all cards (46 cards - 97%)
            https://deckbox.org/sets/1690805

        [!] 97% (45 /46 ) - Missing Cards: 1 - Hippo

    [-] Deck 1742238 - White-Blue 7-1-17 (40 cards - 97%)
            https://deckbox.org/sets/1742238

        [!] 97% (39 /40 ) - Missing Cards: 1 - Galestrike
```

Enjoy.
