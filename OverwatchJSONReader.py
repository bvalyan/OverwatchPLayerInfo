import sys
import getopt
import json
from decimal import *
from urllib2 import Request, urlopen, URLError

def getPlayerProfile(profile):
    url ='https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/profile'
    
    request = Request(url);
    
    try:
        response = urlopen(request)
        playerProfileInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No player info. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into 
    playerProfile = json.loads(playerProfileInfo)
    
    profile['Username'] = playerProfile['data']['username']
    profile['Level'] = playerProfile['data']['level']
    profile['Won'] = playerProfile['data']['games']['wins']
    profile['Lost'] = playerProfile['data']['games']['lost']
    profile['Played'] = playerProfile['data']['games']['played']
    profile['WinPct'] = playerProfile['data']['games']['win_percentage']
    profile['Playtime'] = playerProfile['data']['playtime']
    profile['Avatar'] = playerProfile['data']['avatar']

    return profile
    


def getHeroPlaytimeImage(profile):
    url ='https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/heroes'
    
    request = Request(url);
    
    try:
        response = urlopen(request)
        playTimeImageInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No player info. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into 
    playTimeImageList = json.loads(playTimeImageInfo)
    
    #Go through each hero stats for player
    for dict in playTimeImageList:
        #print 'Hero Name Before Replace: '+dict['name']
        #print 'Hero Playtime: '+dict['playtime']
        #print 'Hero Image URL: '+dict['image']
        #print '\n\n'
        name = dict['name']
        
        #Replace problem names
        if name == 'Torbj&#xF6;rn':
            name = 'Torbjoern'
        if name == 'L&#xFA;cio':
            name = 'Lucio'
        if name == 'Soldier: 76':
            name = 'Soldier76'
        if name == 'D.Va':
            name = 'DVa'
        
        
        if dict['playtime'] != '--':  #only get data for heroes the player actually used
            print 'Hero Name After Replace: '+name
            #print 'Hero Playtime: '+dict['playtime']
            
            #initialize nested dictionary
            profile['Heroes'][name] = {}
            
            #assign values to dictionary
            profile['Heroes'][name]['playtime'] = dict['playtime']
            profile['Heroes'][name]['imageURL'] = dict['image']


####################### Stat Check #################
#checks to see if enough stats have been aquired for analysis
def StatCheck(dict,  list):
    for key in list:
        if dict.has_key(key):
            continue
        else:
            print '\tNeeded Stat '+key+' is missing...'
            return False
    
    return True

################################################


################  Hero Get Data Functions ################
#https://api.lootbox.eu/<platform>/<region>/<tag>/hero/<HeroName>/
def getDataBastion(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Bastion/'
    request = Request(url);
    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Bastion. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'TankKills', 'SentryKills', 'ReconKills', 'SelfHealing', 'Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Bastion']['DisplayName'] = 'Bastion' 
    profile['Heroes']['Bastion']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Bastion']['WinPercentage'] = 0
    else:
        profile['Heroes']['Bastion']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Bastion']['TankKills-Average'] = float(heroStats['TankKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Bastion']['SentryKills-Average'] = float(heroStats['SentryKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Bastion']['ReconKills-Average'] = float(heroStats['ReconKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Bastion']['SelfHealing-Average'] = float(heroStats['SelfHealing'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Bastion']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataDVa(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/DVa/'
    request = Request(url);
    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for D.Va. Got an error code:', e
        print 'URL: '+url
        
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'Self-DestructKills', 'DamageBlocked', 'Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['DVa']['DisplayName'] = 'D.Va' 
    profile['Heroes']['DVa']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['DVa']['WinPercentage'] = 0
    else:
        profile['Heroes']['DVa']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['DVa']['Self-DestructKills-Average'] = float(heroStats['Self-DestructKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['DVa']['DamageBlocked-Average'] = float(heroStats['DamageBlocked'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['DVa']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataGenji(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Genji/'
    request = Request(url);
    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Genji. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'DragonbladeKills', 'DamageReflected', 'Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Genji']['DisplayName'] = 'Genji'
    profile['Heroes']['Genji']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Genji']['WinPercentage'] = 0
    else:
        profile['Heroes']['Genji']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Genji']['DragonbladeKills-Average'] = float(heroStats['DragonbladeKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Genji']['DamageReflected-Average'] = float(heroStats['DamageReflected'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Genji']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',',''))  / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataHanzo(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Hanzo/'
    request = Request(url);
    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Hanzo. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'DragonstrikeKills', 'ScatterArrowKills', 'Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Hanzo']['DisplayName'] = 'Hanzo'
    profile['Heroes']['Hanzo']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Hanzo']['WinPercentage'] = 0
    else:
        profile['Heroes']['Hanzo']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Hanzo']['DragonstrikeKills-Average'] = float(heroStats['DragonstrikeKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Hanzo']['ScatterArrowKills-Average'] = float(heroStats['ScatterArrowKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Hanzo']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataJunkrat(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Junkrat/'
    request = Request(url);
    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Junkrat. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'EnemiesTrapped', 'RIP-TireKills', 'Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Junkrat']['DisplayName'] = 'Junkrat'
    profile['Heroes']['Junkrat']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Junkrat']['WinPercentage'] = 0
    else:
        profile['Heroes']['Junkrat']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Junkrat']['EnemiesTrapped-Average'] = float(heroStats['EnemiesTrapped'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Junkrat']['RIP-TireKills-Average'] = float(heroStats['RIP-TireKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Junkrat']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataLucio(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Lucio/'
    request = Request(url);
    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Lucio. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'SoundBarriersProvided', 'HealingDone','OffensiveAssists','DefensiveAssists','Eliminations', 'SoundBarriersProvided-MostinGame', 'ObjectiveTime-Average']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Lucio']['DisplayName'] = 'Lucio'
    profile['Heroes']['Lucio']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Lucio']['WinPercentage'] = 0
    else:
        profile['Heroes']['Lucio']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Lucio']['SoundBarriersProvided-Average'] = float(heroStats['SoundBarriersProvided'].replace(',', '')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Lucio']['HealingDone-Average'] = float(heroStats['HealingDone'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Lucio']['OffensiveAssists-Average'] = float(heroStats['OffensiveAssists'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Lucio']['DefensiveAssists-Average'] = float(heroStats['DefensiveAssists'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Lucio']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Lucio']['SoundBarriersProvided-MostinGame'] = float(heroStats['SoundBarriersProvided-MostinGame'])
    profile['Heroes']['Lucio']['ObjectiveTime-Average'] = float(heroStats['ObjectiveTime-Average'])
    
    return profile

def getDataMcCree(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/McCree/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for McCree. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'DeadeyeKills', 'FantheHammerKills','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['McCree']['DisplayName'] = 'McCree'
    profile['Heroes']['McCree']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['McCree']['WinPercentage'] = 0
    else:
        profile['Heroes']['McCree']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['McCree']['DeadeyeKills-Average'] = float(heroStats['DeadeyeKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['McCree']['FantheHammerKills-Average'] = float(heroStats['FantheHammerKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['McCree']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataMei(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Mei/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Mei. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'EnemiesFrozen', 'BlizzardKills','DamageBlocked','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Mei']['DisplayName'] = 'Mei'
    profile['Heroes']['Mei']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Mei']['WinPercentage'] = 0
    else:
        profile['Heroes']['Mei']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mei']['EnemiesFrozen-Average'] = float(heroStats['EnemiesFrozen'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mei']['BlizzardKills-Average'] = float(heroStats['BlizzardKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mei']['DamageBlocked-Average'] = float(heroStats['DamageBlocked'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mei']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataMercy(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Mercy/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Mercy. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'PlayersResurrected', 'HealingDone','BlasterKills','OffensiveAssists', 'DefensiveAssists','Eliminations','PlayersSaved']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Mercy']['DisplayName'] = 'Mercy'
    profile['Heroes']['Mercy']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Mercy']['WinPercentage'] = 0
    else:
        profile['Heroes']['Mercy']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mercy']['PlayersResurrected-Average'] = float(heroStats['PlayersResurrected'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mercy']['HealingDone-Average'] = float(heroStats['HealingDone'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mercy']['BlasterKills-Average'] = float(heroStats['BlasterKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mercy']['OffensiveAssists-Average'] = float(heroStats['OffensiveAssists'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mercy']['DefensiveAssists-Average'] = float(heroStats['DefensiveAssists'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mercy']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Mercy']['PlayersSaved-Average'] = float(heroStats['PlayersSaved'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))

    return profile

def getDataPharah(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Pharah/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Pharah. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'BarrageKills', 'RocketDirectHits','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Pharah']['DisplayName'] = 'Pharah'
    profile['Heroes']['Pharah']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Pharah']['WinPercentage'] = 0
    else:
        profile['Heroes']['Pharah']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Pharah']['BarrageKills-Average'] = float(heroStats['BarrageKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Pharah']['RocketDirectHits-Average'] = float(heroStats['RocketDirectHits'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Pharah']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataReaper(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Reaper/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Reaper. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'SoulsConsumed', 'DeathBlossomKills','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Reaper']['DisplayName'] = 'Reaper'
    profile['Heroes']['Reaper']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Reaper']['WinPercentage'] = 0
    else:
        profile['Heroes']['Reaper']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Reaper']['SoulsConsumed-Average'] = float(heroStats['SoulsConsumed'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Reaper']['DeathBlossomKills-Average'] = float(heroStats['DeathBlossomKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Reaper']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataReinhardt(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Reinhardt/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Reinhardt. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'DamageBlocked', 'ChargeKills','FireStrikeKills', 'EarthshatterKills','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Reinhardt']['DisplayName'] = 'Reinhardt'
    profile['Heroes']['Reinhardt']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Reinhardt']['WinPercentage'] = 0
    else:
        profile['Heroes']['Reinhardt']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Reinhardt']['DamageBlocked-Average'] = float(heroStats['DamageBlocked'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Reinhardt']['ChargeKills-Average'] = float(heroStats['ChargeKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Reinhardt']['FireStrikeKills-Average'] = float(heroStats['FireStrikeKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Reinhardt']['EarthshatterKills-Average'] = float(heroStats['EarthshatterKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Reinhardt']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataRoadhog(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Roadhog/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Roadhog. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'EnemiesHooked', 'WholeHogKills','SelfHealing','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    
    profile['Heroes']['Roadhog']['DisplayName'] = 'Roadhog'
    profile['Heroes']['Roadhog']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Roadhog']['WinPercentage'] = 0
    else:
        profile['Heroes']['Roadhog']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Roadhog']['EnemiesHooked-Average'] = float(heroStats['EnemiesHooked'].replace(',','')) / float(heroStats['HooksAttempted'].replace(',', ''))
    profile['Heroes']['Roadhog']['WholeHogKills-Average'] = float(heroStats['WholeHogKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Roadhog']['SelfHealing-Average'] = float(heroStats['SelfHealing'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Roadhog']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataSoldier76(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Soldier76/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Soldier: 76. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'HelixRocketsKills', 'TacticalVisorKills','HealingDone','Eliminations','WeaponAccuracy','SoloKills-Average','EliminationsperLife','DamageDone-Average']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    
    profile['Heroes']['Soldier76']['DisplayName'] = 'Soldier: 76'
    profile['Heroes']['Soldier76']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Soldier76']['WinPercentage'] = 0
    else:
        profile['Heroes']['Soldier76']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Soldier76']['HelixRocketsKills-Average'] = float(heroStats['HelixRocketsKills'].replace(',', '')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Soldier76']['TacticalVisorKills-Average'] = float(heroStats['TacticalVisorKills'].replace(',', '')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Soldier76']['HealingDone-Average'] = float(heroStats['HealingDone'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Soldier76']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Soldier76']['WeaponAccuracy'] = float(heroStats['WeaponAccuracy'].replace('%',''))
    profile['Heroes']['Soldier76']['SoloKills-Average'] = float(heroStats['SoloKills-Average'])
    profile['Heroes']['Soldier76']['EliminationsperLife'] = float(heroStats['EliminationsperLife'])
    profile['Heroes']['Soldier76']['DamageDone-Average'] = float(heroStats['DamageDone-Average'].replace(',',''))
    
    return profile

def getDataSymmetra(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Symmetra/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Symmetra. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'SentryTurretKills', 'PlayersTeleported','ShieldsProvided','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    
    profile['Heroes']['Symmetra']['DisplayName'] = 'Symmetra'
    profile['Heroes']['Symmetra']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Symmetra']['WinPercentage'] = 0
    else:
        profile['Heroes']['Symmetra']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Symmetra']['SentryTurretKills-Average'] =float(heroStats['SentryTurretKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Symmetra']['PlayersTeleported-Average'] = float(heroStats['PlayersTeleported'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Symmetra']['ShieldsProvided-Average'] = float(heroStats['ShieldsProvided'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Symmetra']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataTorborn(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Torbjoern/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Torbjorn. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'ArmorPacksCreated', 'TurretKills','MoltenCoreKills','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Torbjoern']['DisplayName'] = 'Torbjorn'
    profile['Heroes']['Torbjoern']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Torbjoern']['WinPercentage'] = 0
    else:
        profile['Heroes']['Torbjoern']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Torbjoern']['ArmorPacksCreated-Average'] = float(heroStats['ArmorPacksCreated'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Torbjoern']['TurretKills-Average'] = float(heroStats['TurretKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Torbjoern']['MoltenCoreKills-Average'] = float(heroStats['MoltenCoreKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Torbjoern']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataTracer(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Tracer/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Tracer. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'PulseBombKills', 'SelfHealing','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Tracer']['DisplayName'] = 'Tracer'
    profile['Heroes']['Tracer']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Tracer']['WinPercentage'] = 0
    else:
        profile['Heroes']['Tracer']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Tracer']['PulseBombKills-Average'] = float(heroStats['PulseBombKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Tracer']['SelfHealing-Average'] = float(heroStats['SelfHealing'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Tracer']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataWidowmaker(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Widowmaker/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Widowmaker. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'VenomMineKills', 'ScopedHits','ScopedCriticalHits','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Widowmaker']['DisplayName'] = 'Widowmaker'
    profile['Heroes']['Widowmaker']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Widowmaker']['WinPercentage'] = 0
    else:
        profile['Heroes']['Widowmaker']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Widowmaker']['VenomMineKills-Average'] = float(heroStats['VenomMineKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Widowmaker']['ScopedAccuracy'] = float(heroStats['ScopedHits'].replace(',','')) / float(heroStats['ScopedShots'].replace(',',''))
    profile['Heroes']['Widowmaker']['ScopedCritialRate'] = float(heroStats['ScopedCriticalHits'].replace(',','')) / float(heroStats['ScopedHits'].replace(',',''))
    profile['Heroes']['Widowmaker']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataWinston(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Winston/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Winston. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'DamageBlocked', 'PrimalRageKills','JumpPackKills','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Winston']['DisplayName'] = 'Winston'
    profile['Heroes']['Winston']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Winston']['WinPercentage'] = 0
    else:
        profile['Heroes']['Winston']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Winston']['DamageBlocked-Average'] = float(heroStats['DamageBlocked'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Winston']['PrimalRageKills-Average'] = float(heroStats['PrimalRageKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Winston']['JumpPackKills-Average'] = float(heroStats['JumpPackKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Winston']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataZarya(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Zarya/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Zarya. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'DamageBlocked', 'LifetimeGravitonSurgeKills','HighEnergyKills','ProjectedBarriersApplied','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    
    profile['Heroes']['Zarya']['DisplayName'] = 'Zarya'
    profile['Heroes']['Zarya']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Zarya']['WinPercentage'] = 0
    else:
        profile['Heroes']['Zarya']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Zarya']['DamageBlocked-Average'] = float(heroStats['DamageBlocked'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Zarya']['GravitonSurgeKills-Average'] = float(heroStats['LifetimeGravitonSurgeKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Zarya']['FullEnergyKills-Average'] = float(heroStats['HighEnergyKills'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',','')) #Kills at 100% charge ??? Need more investigation
    profile['Heroes']['Zarya']['ProjectedBarriersApplied-Average'] = float(heroStats['ProjectedBarriersApplied'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Zarya']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

def getDataZenyatta(profile):
    url = 'https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/hero/Zenyatta/'
    request = Request(url);

    
    try:
        response = urlopen(request)
        heroInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No hero info for Zenyatta. Got an error code:', e
        print 'URL: '+url
    
    #Load JSON string into dictionary 
    heroStats = json.loads(heroInfo)
    
    statList = ['GamesWon', 'HealingDone', 'TranscendenceHealing','OffensiveAssists','DefensiveAssists','Eliminations']
    if not StatCheck(heroStats, statList):
        print '\tNot Enough Data to Generate Stats...'
        return
    
    profile['Heroes']['Zenyatta']['DisplayName'] = 'Zenyatta'
    profile['Heroes']['Zenyatta']['GamesPlayed'] =  float(heroStats['GamesPlayed'].replace(',',''))
    if not heroStats.has_key('GamesWon'):
        profile['Heroes']['Zenyatta']['WinPercentage'] = 0
    else:
        profile['Heroes']['Zenyatta']['WinPercentage'] = float(heroStats['GamesWon'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Zenyatta']['HealingDone-Average'] = float(heroStats['HealingDone'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Zenyatta']['TranscendenceHealing-Average'] = float(heroStats['TranscendenceHealing'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Zenyatta']['OffensiveAssists-Average'] = float(heroStats['OffensiveAssists'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',','')) #Kills at 100% charge ??? Need more investigation
    profile['Heroes']['Zenyatta']['DefensiveAssists-Average'] = float(heroStats['DefensiveAssists'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    profile['Heroes']['Zenyatta']['Eliminations-Average'] = float(heroStats['Eliminations'].replace(',','')) / float(heroStats['GamesPlayed'].replace(',',''))
    
    return profile

##################################################
## Algorithm Computation

def computeScore(heroName, profile):

    if heroName == 'Mercy':
        calcResult = 0;
        preFlag = 0;
        heroDict = getDataMercy(profile);
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
        topdefassistthreshold = 10;
        middefassistthreshold = 8;

        if heroDict['Heroes']['Mercy']['HealingDone-Average'] >= tophealingthreshold:
            calcResult+= 15.0;
        elif heroDict['Heroes']['Mercy']['HealingDone-Average'] >= midhighhealingthreshold:
            calcResult += midHighPercentage(15.0);
        elif heroDict['Heroes']['Mercy']['HealingDone-Average'] >= midhealingthreshold:
            calcResult += midPercentage(15.0);
        else: calcResult += lowPercentage(15.0);
        
        print(calcResult);
        
        #print(float(averageHealing));
        
        if heroDict['Heroes']['Mercy']['WinPercentage'] >= topwinthreshold:
            calcResult += 5.0
        elif heroDict['Heroes']['Mercy']['WinPercentage'] >= midwinthreshold:
            calcResult += midPercentage(5.0);
        else: calcResult += lowPercentage(5.0);
        
        print(calcResult);
        
        if heroDict['Heroes']['Mercy']['PlayersResurrected-Average'] >= toprezthreshold:
            calcResult += 5.0;
        elif heroDict['Heroes']['Mercy']['PlayersResurrected-Average'] >= midrezthreshold:
            calcResult += midPercentage(5.0);
        else: calcResult += lowPercentage(5.0);
        
    
        print(calcResult);
        #print(playersrezzed);
        
        if heroDict['Heroes']['Mercy']['PlayersSaved-Average'] >= topsavedthreshold:
            calcResult += 10;
        elif heroDict['Heroes']['Mercy']['PlayersSaved-Average'] >= midsavedthreshold:
            calcResult += midPercentage(10.0);
        else: calcResult += lowPercentage(10.0);
        
        print(calcResult);
        
        if heroDict['Heroes']['Mercy']['DefensiveAssists-Average'] >= topdefassistthreshold:
            calcResult += 5;
        elif heroDict['Heroes']['Mercy']['DefensiveAssists-Average'] >= middefassistthreshold:
            calcResult += midPercentage(5.0);
        else: calcResult += lowPercentage(5.0);

        if heroDict['Heroes']['Mercy']['GamesPlayed'] < 50:
            preFlag = 1;

    if heroName == 'Soldier76':
        calcResult = 0;
        preFlag = 0;
        topElimThreshold = 3;
        medElimThreshold = 2;
        heroDict = getDataSoldier76(profile);
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

        print(heroDict['Heroes']['Soldier76'])
        
        if float(heroDict['Heroes']['Soldier76']['EliminationsperLife']) >= float(topElimThreshold):
            calcResult += 5
        elif float(heroDict['Heroes']['Soldier76']['EliminationsperLife']) >= float(medElimThreshold):
            calcResult += midPercentage(5.0);
        elif float(heroDict['Heroes']['Soldier76']['EliminationsperLife']) == 0:
            print('true');
            calcResult += 0;
        
        else: calcResult += lowPercentage(5.0);
        
        
        if heroDict['Heroes']['Soldier76']['SoloKills-Average'] >= averageSoloKillsTopThreshold:
            calcResult += 2
        elif heroDict['Heroes']['Soldier76']['SoloKills-Average'] >= averageSoloKillsMedThreshold:
            calcResult += midPercentage(2.0)
        elif heroDict['Heroes']['Soldier76']['SoloKills-Average'] == 0:
            calcResult += 0;
        
        else: calcResult += lowPercentage(2.0)
        
        print(calcResult);
        
        if  heroDict['Heroes']['Soldier76']['Eliminations-Average'] >= averageElimsTopThreshold:
            calcResult += 9
        elif heroDict['Heroes']['Soldier76']['Eliminations-Average'] >= averageElimsMedThreshold:
            calcResult += midPercentage(9.0)
        elif heroDict['Heroes']['Soldier76']['Eliminations-Average'] == 0:
            calcResult += 0    
        else: calcResult += lowPercentage(9.0)
        
        print(calcResult);
        
        if heroDict['Heroes']['Soldier76']['DamageDone-Average']  >= averageDamageTopThreshold:
            calcResult += 13
        elif heroDict['Heroes']['Soldier76']['DamageDone-Average']  >= averageDamageMedThreshold:
            calcResult += midPercentage(13.0);
        elif heroDict['Heroes']['Soldier76']['DamageDone-Average']  == 0:
            calcResult += 0
        else: calcResult += lowPercentage(13.0);
        
        print(calcResult);
        
        if heroDict['Heroes']['Soldier76']['WinPercentage'] >= winPercentageTopThreshold:
            calcResult += 3
        elif heroDict['Heroes']['Soldier76']['WinPercentage'] >= winPercentageMedThreshold:
            calcResult += midHighPercentage(3.0)
        elif heroDict['Heroes']['Soldier76']['WinPercentage'] >= winPercentageMedLowThreshold:
            calcResult += midPercentage(3.0)
        elif heroDict['Heroes']['Soldier76']['WinPercentage'] == 0:
            calcResult += 0
        else: calcResult += lowPercentage(3.0)
    
        print(calcResult);
        
        if heroDict['Heroes']['Soldier76']['WeaponAccuracy'] >= accuracyTopThreshold:
            calcResult += 5
        elif heroDict['Heroes']['Soldier76']['WeaponAccuracy'] >= accuracyMedThreshold:
            calcResult += midPercentage(5.0)
        elif heroDict['Heroes']['Soldier76']['WeaponAccuracy'] == 0:
            calcResult += 0
        else: calcResult += lowPercentage(5.0)
        
        print(calcResult);
        
        if heroDict['Heroes']['Soldier76']['HelixRocketsKills-Average'] >= helixKillsTopThreshold:
            calcResult += 3
        elif heroDict['Heroes']['Soldier76']['HelixRocketsKills-Average'] >= helixKillsMidThreshold:
            calcResult += midPercentage(3.0)
        elif heroDict['Heroes']['Soldier76']['HelixRocketsKills-Average'] == 0:
            calcResult += 0
        else: calcResult += lowPercentage(3.0)

        if heroDict['Heroes']['Soldier76']['GamesPlayed'] < 50:
            preFlag = 1;


    if heroName == "Lucio":
        calcResult = 0;
        preFlag = 0;
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
        topElimThreshold =  7;
        midElimThreshold =  5;
        heroDict = getDataLucio(profile);

        if heroDict['Heroes']['Lucio']['HealingDone-Average'] >= topaveragehealingthreshold:
            calcResult += 10;
        elif heroDict['Heroes']['Lucio']['HealingDone-Average'] >= midaveragehealingthreshold:
            calcResult += midPercentage(10);
        else: calcResult = lowPercentage(10);

        print(calcResult);

        if heroDict['Heroes']['Lucio']['WinPercentage'] >= topwinratethreshold:
            calcResult += 5;
        elif profile['Heroes']['Lucio']['WinPercentage']  >= midwinratethreshold:
            calcResult += midPercentage(5);
        else: calcResult += lowPercentage(5);

        print(calcResult);


        if heroDict['Heroes']['Lucio']['SoundBarriersProvided-Average'] >= topSBThreshold:
            calcResult +=7;
        elif heroDict['Heroes']['Lucio']['SoundBarriersProvided-Average'] >= midSBThreshold:
            calcResult += midPercentage(7);
        else:
            calcResult += lowPercentage(7);

        print(calcResult);

        if heroDict['Heroes']['Lucio']['DefensiveAssists-Average'] >= topDefThreshold:
            calcResult += 8;
        elif heroDict['Heroes']['Lucio']['DefensiveAssists-Average'] >= midDefThreshold:
            calcResult += midPercentage(8);
        else:
            calcResult += lowPercentage(8);

        print(calcResult);

        if heroDict['Heroes']['Lucio']['ObjectiveTime-Average'] >= topTimeThreshold:
            calcResult += 5;
        elif heroDict['Heroes']['Lucio']['ObjectiveTime-Average'] >= midTimeThreshold:
            calcResult += midPercentage(5);
        else:
            calcResult += lowPercentage(5);

        print(calcResult);

        if heroDict['Heroes']['Lucio']['Eliminations-Average'] >= topElimThreshold:
            calcResult += 5;
        elif heroDict['Heroes']['Lucio']['Eliminations-Average'] >= midElimThreshold:
            calcResult += midPercentage(5);
        else:
            calcResult += lowPercentage(5);


        if heroDict['Heroes']['Lucio']['GamesPlayed'] < 50:
            preFlag = 1;

    if heroName == "Junkrat":
        calcResult = 0;
        preFlag = 0;
        heroDict = getDataJunkrat(profile);
        topElimThreshold = 12;
        midElimThreshold = 9;
        topdamagetheshold = 6500;
        middamagethreshold = 5000;
        



    return (calcResult, preFlag)

##################################################

def midHighPercentage(topScore):
    newpercentage = float(topScore) * (85.0/100.0);
    return newpercentage;

def midPercentage(topScore):
    newpercentage = float(topScore) * (75.0/100.0);
    return newpercentage;

def lowPercentage(topScore):
    newpercentage = float(topScore) * (50.0/100.0);
    return newpercentage;


##################################################

def main():
    platform = ""       # options: pc,xbl,psn
    region = ""         #options: eu,us,global
    tag = ""            #api requirement replace '#' with '-'

    if len(sys.argv) == 1:
        print 'Usage: OverWatchJSONReader.py -t <gamerTag> -r <region> -p <platform>' 
        sys.exit(2)

    #collect the values from the command line
    try:
        opts,  args = getopt.getopt(sys.argv[1:],  'h:p:r:t:') 
    except getopt.GetoptError:
        print 'Usage: OverWatchJSONReader.py -t <gamerTag> -r <region> -p <platform>' 
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: OverWatchJSONReader.py -t <gamerTag> -r <region> -p <platform>'
            sys.exit()
        elif opt == '-p':
            if arg in ("pc", "xbl", "psn"):
                platform = arg
            else:
                print '"'+arg+'" is an invalid platform. Choices are "pc","xbl","psn"'
                sys.exit(2)
        elif opt == '-r':
            if arg in ("eu","us","global"):
                region = arg
            else:
                print '"'+arg+'" is an invalid region. Choices are "eu","us","global"'
                sys.exit(2)
        elif opt =='-t':
            tag = arg.replace("#","-")

    
    #Check to see if the required parameters are given
    if platform == '':
        print 'Platform parameter "-p" must be given. Choices are "pc","xbl","psn"'
        sys.exit(2)
    
    if region == '':
        print 'Region parameter "-r" must be given. Choices are "eu","us","global"'
        sys.exit(2)
    
    if tag == '':
        print 'Gamer Tag parameter "-t" must be given.'
        sys.exit(2)
    
    #print the collected inputs
    print 'Platform: '+platform
    print 'Region: '+region
    print 'Game Tag: '+tag


    playerProfile = {
        'GamerTag': tag , 
        'Region': region,
        'Platform': platform, 
        'Username':  '', 
        'Level': '', 
        'Won': '', 
        'Lost': '', 
        'Played': '', 
        'WinPct': '' ,
        'Playtime': '', 
        'Avatar': '', 
        'Heroes': {} #Double Dictionary [Hero][Stat]
    }
    
    #call get profile
    profile = getPlayerProfile(playerProfile)
    
    #call Playtime and Image function to start building the player profile
    getHeroPlaytimeImage(playerProfile)
    
    #Loop through the heroes the player has played with calling the "getData" for each
    heroes = playerProfile['Heroes'].keys()

    print("Please input the hero you wish to obtain a rating for.")
    inputHero = raw_input();
    heroScore, flag = computeScore(inputHero, profile);
    if heroScore >= 30:
        battleClass = 'Alpha';
    elif heroScore >= 20:
        battleClass = 'Beta';
    elif heroScore >= 10:
        battleClass = 'Gamma';
    elif heroScore >= 5:
        battleClass = 'Delta';
    else: battleClass = 'Epsilon';
    
    if flag == 1: #Flag indicates amount of games won
        print('NOTE: Player has not played enough games for a confident representation and therefore has not been definitively placed in a battle class.');
        print('Your battle pre-class is ' + battleClass);
    else:
        print('Their battle class is ' + battleClass);

    print('Hero Score: ' + str(heroScore));

    '''
    print "Loading data for "+str( len(heroes) )+" heroes..."
    
    for hero in heroes:
        print "Loading Data For Hero: "+hero+"..."
        if hero == 'Bastion':
            getDataBastion(playerProfile)
        elif hero == 'DVa':
            getDataDVa(playerProfile)
        elif hero == 'Genji':
            getDataGenji(playerProfile)
        elif hero == 'Hanzo':
            getDataHanzo(playerProfile)
        elif hero == 'Junkrat':
            getDataJunkrat(playerProfile)
        elif hero == 'Lucio':
            getDataLucio(playerProfile)
        elif hero == 'McCree':
            getDataMcCree(playerProfile)
        elif hero == 'Mei':
            getDataMei(playerProfile)
        elif hero == 'Mercy':
            getDataMercy(playerProfile)
        elif hero == 'Pharah':
            getDataPharah(playerProfile)
        elif hero == 'Reaper':
            getDataReaper(playerProfile)
        elif hero == 'Reinhardt':
            getDataReinhardt(playerProfile)
        elif hero == 'Roadhog':
            getDataRoadhog(playerProfile)
        elif hero == 'Soldier76':
            getDataSoldier76(playerProfile)
        elif hero == 'Symmetra':
            getDataSymmetra(playerProfile)
        elif hero == 'Torbjoern':
            getDataTorborn(playerProfile)
        elif hero == 'Tracer':
            getDataTracer(playerProfile)
        elif hero == 'Widowmaker':
            getDataWidowmaker(playerProfile)
        elif hero == 'Winston':
            getDataWinston(playerProfile)
        elif hero == 'Zarya':
            getDataZarya(playerProfile)
        elif hero == 'Zenyatta':
            getDataZenyatta(playerProfile)
            '''


    #print all gathered data
    #print json.dumps(playerProfile,  indent=4)

if __name__ == "__main__":
    main()
