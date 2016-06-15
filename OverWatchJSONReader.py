import sys
import getopt
import json
from urllib2 import Request, urlopen, URLError



def getHeroPlaytimeImage(profile):
    
    request = Request('https://api.lootbox.eu/'+profile['Platform']+'/'+profile['Region']+'/'+profile['GamerTag']+'/heroes');
    
    try:
        response = urlopen(request)
        playTimeImageInfo = response.read()
        #print playerInfo;
    except URLError, e:
        print 'No player info. Got an error code:', e
    
    #Load JSON string into 
    playTimeImageList = json.loads(playTimeImageInfo)
    
    #Go through each hero stats for player
    for dict in playTimeImageList:
        print 'Hero Name: '+dict['name']
        print 'Hero Playtime: '+dict['playtime']
        print 'Hero Image URL: '+dict['image']
        print '\n\n'



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
                print '"'+arg+'" is an invalid platform. Choices are "eu","us","global"'
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
        'WinPct': 0 , 
        'Heroes': {}
    }

    #call Playtime and Image function to start building the player profile
    getHeroPlaytimeImage(playerProfile)

if __name__ == "__main__":
    main()
