from flask import Flask,render_template,request
from os import sys
import tweepy
#import gmplot
import re
from textblob import TextBlob
import geocoder
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map,icons
#from os import sys
import csv

def do_geocode(address):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        return do_geocode(address)
    
def get_marker_color(magnitude):
    if magnitude < 0:
        return ('ro')
    elif magnitude >0 :
        return ('go')
    else:
        return ('yo')


#=========================================================================
consumer_key = 'GmpTnILRzZMHKQaBlvSZSIVZ3'
consumer_secret = 'noqT3ayytByZvVs6Epd2bSkn6iAA58FsQF7ALPFTZq8Xt7623M'
access_token = '891023187818840064-uu3KXNFEG0FX7dnnhTsAcL1lm3Wrkiz'
access_token_secret = 'Xm1Ws2NJYPv74aGWcCjsN3RTCPZaw9ZJKX0I9XaJrEGPl'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True

#=================================================================================



#=============================Tweet Collection======================================
def collect_tweets(place,query):
    cnt=0
    try:
        print("================================start=========================================")
        for i in range(1):
            avg=0
            g = geocoder.google(place)
            g_string=str(g.lat)+","+str(g.lng)+","+"50mi" 
            #print(g)    
            print("rer")
            saveFile = open('dat2.csv','a')
            print("wer")
            for tweet in tweepy.Cursor(api.search,q=query,lang='en',geocode=g_string).items(50):
                cnt=cnt+1                
                analysis = TextBlob(tweet.text)
                avg=avg + analysis.sentiment.polarity
                saveFile.write(str(tweet.created_at) + ",")
                saveThis = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(u2026)|(https)", " ", tweet.text).split())
                saveFile.write(saveThis + "," + str(analysis.sentiment.polarity ))
                saveFile.write('\n')        
                print(analysis.sentiment.polarity)        
    
    
            print("\n===========================end=========================================")
            saveFile1 = open('dat3.csv','a')
            saveFile1.write(query + "," + place + "," + str(g.lat) + "," + str(g.lng) + "," + str(avg/50))
            saveFile1.write('\n')
            
        saveFile1.close()
        print(cnt)
        '''gmap = gmplot.GoogleMapPlotter(float(g.lat), float(g.lng), 4)
        gmap.plot([float(g.lat)], [float(g.lng)], 'cornflowerblue', edge_width=20)
        gmap.scatter([float(g.lat)], [float(g.lng)], '#3B0B39', size=40, marker=dict(size=8,symbol='square'))
        gmap.scatter([float(g.lat)],[float(g.lng)], 'k', marker=True)
        gmap.heatmap([float(g.lat)], [float(g.lng)])
        gmap.draw("templates\\mymap.html")
        #gmap = gmplot.from_geocode("San Francisco")'''
    except:
        print("Oops!",sys.exc_info()[0],"occured.")
        #cnt=0;
        
    return cnt

#=========================User Interface======================

app = Flask(__name__,static_folder='C:\\Users\\Mnrox\\Documents\\sdl')

@app.route('/')
def dir1():
    return render_template("index.html")

GoogleMaps(app)

@app.route('/map' , methods = ['POST'])
def mapview():
        places = request.form['place']
        queries = request.form['query']
        count = collect_tweets(places,queries)
        
        locs={'color':[],'lats':[],'lons':[]}
        if(count > 0):
            filename = 'dat3.csv'
            #latitude, longitude = [], []   
            #k=0
            with open(filename) as f:
                reader = csv.reader(f)
                for row in reader:
                    if(row[0]==queries):
                        #k=k+1
                        locs['lats'].append(float(row[2]))
                        locs['lons'].append(float(row[3]))
                        if(float(row[4])>0):
                            locs['color'].append(icons.dots.green)
                        elif(float(row[4])==0):
                            locs['color'].append(icons.dots.yellow)
                        else:
                            locs['color'].append(icons.dots.red)
                        
            tup=list(zip(locs['color'],locs['lats'],locs['lons']))        
            print(tup)            
            trdmap = Map(
                identifier="trdmap",
                lat=locs['lats'][0],
                lng=locs['lons'][0],
                #[[i for i in d[x]] for x in d.keys()]
                markers=[{'icon':itr[0],'lat':itr[1],'lng':itr[2]} for itr in tup],
                zoom=3  ,
                style="width:1340px;height:635px;"
            )
                #print(sys.exc_info()[0])        
            return render_template('example.html', trdmap=trdmap)    
        else:
            return render_template("error.html")
        
                
    


'''@app.route('/map' , methods = ['POST'])
def sentiment():
    places = request.form['place']
    queries = request.form['query']
    count = collect_tweets(places,queries)
    if(count > 0):
        return render_template("mymap.html")
    else:
        return render_template("error.html")'''


if __name__ == '__main__':
    app.run()

#==============================================================================