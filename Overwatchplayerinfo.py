'''
Created on Jun 9, 2016

@author: Brandon
'''
from urllib2 import Request, urlopen, URLError
import csv
import sys
import re


print('input your Battle.net ID');
name = raw_input();

print('Platform?');
platform = raw_input();
    

editedpcname = re.sub('\#', '-', name,0);
#print editedpcname;

#print(platform);
request = Request('https://api.lootbox.eu/'+platform+'/us/'+ editedpcname+'/heroes');



try:
    response = urlopen(request)
    playerInfo = response.read()
    #print playerInfo;
except URLError, e:
    print 'No player info. Got an error code:', e

print('Top Hero:');
heroUsed = re.search('name":"(\w+)', playerInfo, 0); 
name = heroUsed.group(1);
if name == 'L':
    heroUsed = re.search('name":"(.{10})', playerInfo, 0); 
    name = heroUsed.group(1);
hoursPlayed = re.search('playtime":"(\d+\s\w+)', playerInfo, 0);
hours = hoursPlayed.group(1);
if name == 'L&#xFA;cio':
    print('Lucio');
else: print(name);
print(hours+ '\n');
print('Total Stats');
print("----------------------------");

    
request = Request('https://api.lootbox.eu/pc/us/'+ editedpcname+'/profile')

try:
    response = urlopen(request)
    playerInfo = response.read()
    #print playerInfo;
except URLError, e:
    print 'No player info. Got an error code:', e 
    
#print playerInfo;   

matchesPlayed = re.search('played":"(\d+,\d+|\d+)', playerInfo, 0);
currentLevel = re.search('level":(\d+)', playerInfo, 0);
winPercentage = re.search('percentage":"(\d+\w)', playerInfo, 0)
print "Matches played: " +  matchesPlayed.group(1);
print('Current Level: ' + currentLevel.group(1));
name = 'Mercy'; #TEST

request = Request('https://api.lootbox.eu/pc/us/'+editedpcname+'/hero/' + name + '/');
try:
    response = urlopen(request)
    playerInfo = response.read()
    #print playerInfo;
except URLError, e:
    print 'No player info. Got an error code:', e 
 
print(name);

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
    toprezthreshold = 6;
    midrezthreshold = 3.4;
    topsavedthreshold = 7.51;
    midsavedthreshold = 4.51;
    topmostplayersavethreshold = 29;
    midmostplayersavethreshold = 14;
    
    
    
    
    if float(averageHealing) >= tophealingthreshold:
        calcResult+= 10.0;
    elif float(averageHealing) >= midhighhealingthreshold:
        calcResult += 8.0;
    elif float(averageHealing) >= midhealingthreshold:
        calcResult += 5.0;
    else: calcResult += 3.0;
    
    #print(float(averageHealing));
    
    if float(heroWins) >= topwinthreshold:
        calcResult += 5.0
    elif float(heroWins) >= midwinthreshold:
        calcResult += 3.5;
    else: calcResult += 2
    
    if float(playersrezzed) >= toprezthreshold:
        calcResult += 5.0;
    elif float(playersrezzed) >= midrezthreshold:
        calcResult += 3.0;
    else: calcResult += 1.0;
    
    #print(calcResult);
    #print(playersrezzed);
    
    if float(playerssaved) >= topsavedthreshold:
        calcResult += 10;
    elif float(playerssaved) >= midsavedthreshold:
        calcResult += 7;
    else: calcResult += 5;
    
    #print(calcResult);
    
    if float(mostplayerssaved) >= topmostplayersavethreshold:
        calcResult += 5;
    elif float(mostplayerssaved) >= midmostplayersavethreshold:
        calcResult += 3;
    else: calcResult += 1;
    
    #print('players saved'+mostplayerssaved);
   
    
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
    
    print('Your battle class is ' + battleClass);
    
        
    
    
   
#print(playerInfo);

    