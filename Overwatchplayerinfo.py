'''
Created on Jun 9, 2016

@author: Brandon
'''
from urllib2 import Request, urlopen, URLError
import csv
import sys
import re
from Tkinter import *



print('Input your Battle.net ID');
name = raw_input();

print('Platform?');
platform = raw_input();
    
print('Scrubbing username...')
editedpcname = re.sub('\#', '-', name,0);
#print editedpcname;
print('Requesting Data...')
print('\n');
#print(platform);
if platform == 'pc':
    request = Request('https://api.lootbox.eu/'+platform+'/us/'+ editedpcname+'/heroes');
else:
    request = Request('https://api.lootbox.eu/'+platform+'/global/'+ editedpcname+'/heroes');



try:
    response = urlopen(request)
    playerInfo = response.read()
    #print playerInfo;
except URLError, e:
    print 'No player info. Got an error code:', e

print('Top Hero:');
heroUsed = re.search('name":"(\w+.{1}\s\d+|\w+)', playerInfo, 0); 
name = heroUsed.group(1);
if name == 'L':
    heroUsed = re.search('name":"(.{10})', playerInfo, 0); 
    name = heroUsed.group(1);
hoursPlayed = re.search('playtime":"(\d+\s\w+)', playerInfo, 0);
hours = hoursPlayed.group(1);
if name == 'L&#xFA;cio':
    print('Lucio');
else: print(name);
if name == 'Soldier: 76': #Adjust for API naming conventions
    name = 'Soldier76';
print(hours+ '\n');

    
if platform == 'pc':
    request = Request('https://api.lootbox.eu/'+platform+'/us/'+ editedpcname+'/profile');
else:
    request = Request('https://api.lootbox.eu/'+platform+'/global/'+ editedpcname+'/profile');

try:
    response = urlopen(request)
    playerInfo = response.read()
    #print playerInfo;
except URLError, e:
    print 'No player info. Got an error code:', e 
    
#print playerInfo;   

print('Total Stats');
print("----------------------------");


matchesPlayed = re.search('played":"(\d+,\d+|\d+)', playerInfo, 0);
currentLevel = re.search('level":(\d+)', playerInfo, 0);
winPercentage = re.search('percentage":"(\d+\w)', playerInfo, 0)
print "Matches played: " +  matchesPlayed.group(1);
print('Current Level: ' + currentLevel.group(1));
name = 'Soldier76'; #TEST

if platform == 'pc':
    request = Request('https://api.lootbox.eu/pc/us/'+editedpcname+'/hero/' + name + '/');
else:
    request = Request('https://api.lootbox.eu/xbl/global/'+editedpcname+'/hero/' + name + '/');

#requestText = 'https://api.lootbox.eu/xbl/global/'+editedpcname+'/hero/' + name + '/';

#print(requestText);

try:
    response = urlopen(request)
    playerInfo = response.read()
    #print playerInfo;
except URLError, e:
    print 'No player info. Got an error code:', e 
 
print(name);
gamesPlayed = re.search('GamesPlayed":"(\d+,\d+|\d+)', playerInfo, 0);
try: gamesPlayed = gamesPlayed.group(1);
except AttributeError:
    gamesPlayed = 0;

gamesPlayed = re.sub(',', '', gamesPlayed, 0);

if name == 'Mercy':
    averageHealing = re.search('HealingDone-Average":"(\d+,\d+|\d+)', playerInfo, 0);
    averageHealing = averageHealing.group(1);
    averageHealing = re.sub(',', '', averageHealing, 0);
    heroWins = re.search('WinPercentage":"(\d+)', playerInfo, 0);
    playersrezzed = re.search('PlayersResurrected-Average":"(\d+)', playerInfo, 0);
    playersrezzed = playersrezzed.group(1);

    playerssaved = re.search('PlayersSaved-Average":"(\d+)', playerInfo, 0);
    playerssaved = playerssaved.group(1);
    mostplayerssaved = re.search('MostPlayersSavedinaGame":"(\d+)', playerInfo, 0);
    mostplayerssaved = mostplayerssaved.group(1);
    try:
        heroWins = heroWins.group(1);
    except AttributeError:
        heroWins = 0;
        
    #averageHealing = averageHealing.group(1);
    #print(averageHealing);
    averageHealing = re.sub(',', '', averageHealing, 0);
    calcResult = 0;
    tophealingthreshold = 3500;
    midhighhealingthreshold = 2500;
    midhealingthreshold = 1500;
    lowhealingthreshold = 750;
    topwinthreshold = 50;
    midwinthreshold = 48;
    toprezthreshold = 5;
    midrezthreshold = 3.4;
    topsavedthreshold = 7.51;
    midsavedthreshold = 4.51;
    topmostplayersavethreshold = 29;
    midmostplayersavethreshold = 14;

    if float(averageHealing) >= tophealingthreshold:
        calcResult+= 15.0;
    elif float(averageHealing) >= midhighhealingthreshold:
        calcResult += 10.0;
    elif float(averageHealing) >= midhealingthreshold:
        calcResult += 6.0;
    else: calcResult += 3.0;
    
    print(calcResult);
    
    #print(float(averageHealing));
    
    if float(heroWins) >= topwinthreshold:
        calcResult += 5.0
    elif float(heroWins) >= midwinthreshold:
        calcResult += 3.5;
    else: calcResult += 2
    
    print(calcResult);
    
    if float(playersrezzed) >= toprezthreshold:
        calcResult += 5.0;
    elif float(playersrezzed) >= midrezthreshold:
        calcResult += 3.0;
    else: calcResult += 1.0;
    
  
    print(calcResult);
    #print(playersrezzed);
    
    if float(playerssaved) >= topsavedthreshold:
        calcResult += 10;
    elif float(playerssaved) >= midsavedthreshold:
        calcResult += 7;
    else: calcResult += 5;
    
    print(calcResult);
    
    if float(mostplayerssaved) >= topmostplayersavethreshold:
        calcResult += 5;
    elif float(mostplayerssaved) >= midmostplayersavethreshold:
        calcResult += 3;
    else: calcResult += 1;
    
    #print('players saved'+mostplayerssaved);
   
if name == 'Soldier76':
    calcResult = 0;
    elimsPerLife = re.search('EliminationsperLife":"(\d+.\d+|\d+)', playerInfo, 0);
    try: elimsPerLife = elimsPerLife.group(1);
    except AttributeError:
        elimsPerLife = 0;
    #elimsPerLife = re.sub(',', '', averageHealing, 0);
    averageSoloKills = re.search('SoloKills-Average":"(\d+.\d+|\d+)', playerInfo, 0);
    try: averageSoloKills = averageSoloKills.group(1);
    except AttributeError:
        averageSoloKills = 0;
    averageElims = re.search('Eliminations-Average":"(\d+.\d+|\d+)', playerInfo, 0);
    try: averageElims = averageElims.group(1);
    except AttributeError:
        averageElims = 0;
    averageDamage = re.search('DamageDone-Average":"(\d+,\d+|\d+)', playerInfo, 0);
    try: averageDamage = averageDamage.group(1);
    except AttributeError:
        averageDamage = 0;
    try: averageDamage = re.sub(',', '', averageDamage, 0);
    except TypeError: averageDamage = 0;
    winPercentage = re.search('WinPercentage":"(\d+,\d+|\d+)', playerInfo, 0); 
    try: winPercentage = winPercentage.group(1);
    except AttributeError:
        winPercentage = 0;
    weaponAccuracy = re.search('WeaponAccuracy":"(\d+)', playerInfo, 0);
    try: weaponAccuracy = weaponAccuracy.group(1);
    except AttributeError:
        weaponAccuracy = 0;
    helixKills = re.search('HelixRocketsKills-Average": "(\d+.\d+|\d+)', playerInfo, 0);
    try: helixKills = helixKills.group(1);
    except AttributeError:
        helixKills = 0;
    
    topElimThreshold = 3;
    medElimThreshold = 2;
    averageSoloKillsTopThreshold = 3.5;
    averageSoloKillsMedThreshold = 2.8;
    averageElimsTopThreshold = 18;
    averageElimsMedThreshold = 14;
    averageDamageTopThreshold = 7800;
    averageDamageMedThreshold = 5500;
    winPercentageTopThreshold = 90;
    winPercentageMedThreshold = 50;
    winPercentageMedLowThreshold = 40;
    accuracyTopThreshold = 40;
    accuracyMedThreshold = 30;
    helixKillsTopThreshold = 4;
    helixKillsMidThreshold = 2;
    
    if float(elimsPerLife) >= topElimThreshold:
        calcResult += 5
    elif float(elimsPerLife) >= medElimThreshold:
        calcResult += 3
    elif float(elimsPerLife) == 0:
        calcResult += 0
    
    else: calcResult += 1.5
    
    print(calcResult);
    
    if float(averageSoloKills) >= averageSoloKillsTopThreshold:
        calcResult += 2
    elif float(averageSoloKills) >= averageSoloKillsMedThreshold:
        calcResult += 0.5
    elif float(averageSoloKills) == 0:
        calcResult += 0
    
    else: calcResult += 0
    
    print(calcResult);
    
    if float(averageElims) >= averageElimsTopThreshold:
        calcResult += 9
    elif float(averageElims) >= averageElimsMedThreshold:
        calcResult += 4.5
    elif float(averageElims) == 0:
        calcResult = 0    
    else: calcResult += 2
    
    print(calcResult);
    
    if float(averageDamage) >= averageDamageTopThreshold:
        calcResult += 13
    elif float(averageDamage) >= averageDamageMedThreshold:
        calcResult += 8
    elif float(averageDamage) == 0:
        calcResult += 0
    else: calcResult += 4
    
    print(calcResult);
    
    if float(winPercentage) >= winPercentageTopThreshold:
        calcResult += 3
    elif float(winPercentage) >= winPercentageMedThreshold:
        calcResult += 1
    elif float(winPercentage) >= winPercentageMedLowThreshold:
        calcResult += .5
    elif float(winPercentage) == 0:
        calcResult += 0
    else: calcResult += 0
    
    print(calcResult);
    
    if float(weaponAccuracy) >= accuracyTopThreshold:
        calcResult += 5
    elif float(weaponAccuracy) >= accuracyMedThreshold:
        calcResult += 3
    elif float(weaponAccuracy) == 0:
        calcResult += 0
    else: calcResult += 1.5
    
    print(calcResult);
    
    if float(helixKills) >= helixKillsTopThreshold:
        calcResult += 3
    elif float(helixKills) >= helixKillsMidThreshold:
        calcResult += 2
    elif float(helixKills) == 0:
        calcResult += 0
    else: calcResult += 1
 
if name == 'Lucio':
    calcResult = 0;
    averageHealing = re.search('HealingDone-Average":"(\d+,\d+|\d+)', playerInfo, 0);
    averageHealing = averageHealing.group(1);
    averageHealing = re.sub(',', '', averageHealing, 0);
    heroWins = re.search('WinPercentage":"(\d+)', playerInfo, 0);
    heroWins = heroWins.group(1);
    soundBarriers = re.search('SoundBarriersProvided-Average": "(\d+.\d+|\d+)', playerInfo, 0);
    soundBarriers = soundBarriers.group(1);
    defAssists = re.search('"DefensiveAssists-Average": "(\d+.\d+|\d+)', playerInfo, 0)
    defAssists = defAssists.group(1);
    objTime = re.search('ObjectiveTime-Average": "(\d+.\d+|\d+)', playerInfo, 0)
    objTime = objTime.group(1);
    
    topaveragehealingthreshold = 7000;
    midaveragehealingthreshold = 5500;
    topwinratethreshold = 61;
    midwinratethreshold = 57;
    topSBThreshold = 8;
    midSBThreshold = 5;
    topDefThreshold = 5;
    midDefThreshold = 3;
    topTimeThreshold = 75;
    midTimeThreshold = 70;
    
    if float(averageHealing > topaveragehealingthreshold):
        calcResult += 10;
    elif float(averageHealing > midaveragehealingthreshold):
        calcResult += 7;
        
    
    
        
print('Hero Score: ' + str(calcResult));


if calcResult >= 30:
    battleClass = 'Alpha';
elif calcResult >= 20:
    battleClass = 'Beta';
elif calcResult >= 10:
    battleClass = 'Gamma';
elif calcResult >= 5:
    battleClass = 'Delta';
else: battleClass = 'Epsilon';

if int(gamesPlayed) < 50:
    print('NOTE: Player has not played enough games for a confident representation and therefore has not been definitively placed in a battle class.')
    print('Your battle pre-class is ' + battleClass);

else:        
    print('Their battle class is ' + battleClass);     
    
    
   
#print(playerInfo);

    