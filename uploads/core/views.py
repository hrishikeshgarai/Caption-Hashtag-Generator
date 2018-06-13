from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from core.models import Document
from core.forms import DocumentForm
from elasticsearch import Elasticsearch, RequestsHttpConnection
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from random import *
import sqlite3
import geocoder
from urllib2 import urlopen
import boto3, requests, json
from requests_aws4auth import AWS4Auth

aws_access_key_id = 'aws_access_key_id'
aws_secret_access_key = 'aws_secret_access_key'

host = 'elasticsearchlink'
awsauth = AWS4Auth(aws_access_key_id,aws_secret_access_key,'us-east-1', 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
es.info()

uploaded_file_url=None
keyword = set()
logged =False

def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents})

def home1(request):
    if request.method == 'POST':
        a=request.POST['text4'] 
        context = RequestContext(request, {'request': request, 'user': request.user})
        return render(request, 'core/home1.html', {'text4':a, 'cotext': context, 'logged': logged , 'uploaded_file_url':uploaded_file_url})
    return render(request, 'core/simple_upload.html', {'logged': logged})


def generate_hashtag(request):
    if request.method == 'GET':
        hashtag = []
        keyword3 = list(keyword)
        url = "https://ritekit.com/oauth/token"
        payload = "grant_type=client_credentials&client_id=******&client_secret=*******"
        headers = {
          'cache-control': "no-cache",
          'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        res =  json.loads(response.content)
        access_token = res['access_token']
        for keys in keyword3:
            print keys
            url1 = "https://api.ritekit.com/v1/stats/basic/"+keys+"?access_token="+access_token
            response = requests.request("GET", url1)
            hashtag_response = json.loads(response.content)
            associated_hashtag = hashtag_response['associatedHashtags']
            try:
                length = len(hashtag_response['associatedHashtags'])
                print length
            except:
                continue
            for i in range(0,length):
                hashtag_value = '#'+hashtag_response['associatedHashtags'][i]['hashtag']
                hashtag.append(hashtag_value)
        hashes=set(hashtag)
        hashtag = list(hashes)
        hashtag_json = json.dumps(hashtag)
        print hashtag_json
        print len(hashtag)
        return HttpResponse(hashtag_json, content_type="application/json")
    return render(request, 'core/simple_upload.html',{'logged': logged})

def upload_press(request):
    
    cap = []
    keyword2 = list(keyword)
    print keyword2
    for keys in keyword2:
        count = 1
        allquotes = es.search(index='quotes1', doc_type="'"+keys+"'", size=4000, body={"query": {"match":{"keyword" : keys }}})
        length = len(allquotes['hits']['hits'])
        print "length : ", length
        if(length>=1):
            for i in range(0,count):
                if(length == 1):
                    random_number = 0
                else:
                    random_number =  randint(0,length-1)
                print random_number
                allquotes_final = allquotes['hits']['hits'][random_number]
                try:
                    cap.append(allquotes_final['_source']['quote'])
                except:
                    continue
        else:
            continue
    del keyword2[:]
    quotes_json = json.dumps(cap)
    print quotes_json
    return HttpResponse(quotes_json, content_type="application/json")

def generate_location(request):
    send_url = "http://freegeoip.net/json"
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "administrative_area_level_1" in c['types']:
            town = c['long_name']
    loc=[town+", "+country]
    loc_json=json.dumps(loc)
    return HttpResponse(loc_json, content_type="application/json")

def generate_activity(request):
    
    act = ['accomplished','aggravated','alive','alone','amazed','amazing','amused','angry','annoyed','anxious','awesome','awful','bad','beautiful','better','blah','blessed','bored','broken','chill','cold','comfortable','confident','confused','content','cool','crappy','crazy','curious','depressed','determined','disappointed','down','drained','drunk','ecstatic','emotional','energized','excited','exhausted','fantastic','fat','free','fresh','frustrated','full','funny','good','grateful','great','guilty','happy','heartbroken','helpless','hopeful','hopeless','horrible','hot','hungry','hurt','impatient','in love','incomplete','inspired','irritated','lazy','lonely','lost','loved','lovely','lucky','mad','meh','miserable','motivated','nervous','nostalgic','OK','old','optimistic','overwhelmed','pained','pissed','pissed off','positive','pretty','proud','pumped','ready','refreshed','relaxed','relieved','rough','sad','safe','satisfied','scared','sexy','shocked','sick','silly','sleepy','sore','sorry','special','stressed','strong','stupid','super','surprised','terrible','thankful','tired','uncomfortable','upset','weak','weird','well','wonderful','worried']
    act_json=json.dumps(act)
    return HttpResponse(act_json, content_type="application/json")

def call_caption(request):
    if request.method == 'POST':
        return render(request, 'core/caption.html',{'logged': logged})
    return render(request, 'core/simple_upload.html', {'logged': logged})

def call_hashtag(request):
    if request.method == 'POST':
        a=request.POST['text1']
        return render(request, 'core/hashtag.html',{'logged': logged, 'text1':a})
    return render(request, 'core/simple_upload.html', {'logged': logged})

def call_activity(request):
    if request.method == 'POST':
        b=request.POST['text2']
        return render(request, 'core/activity.html',{'logged': logged, 'text2':b})
    return render(request, 'core/simple_upload.html', {'logged': logged})

def call_location(request):
    if request.method == 'POST':
        c=request.POST['text3']
        return render(request, 'core/location.html',{'logged': logged, 'text3':c})
    return render(request, 'core/simple_upload.html', {'logged': logged})

def login1(request):
    # if request.method == 'POST':
    #     return render(request, 'core/login.html')
    return render(request, 'core/login.html', {'logged': logged})

def logout1(request):
    # if request.method == 'POST':
    #     return render(request, 'core/login.html')
    global logged  
    logged=False
    return render(request, 'core/home.html', {'logged': logged})

def sign_up(request):
    # if request.method == 'POST':
    #     return render(request, 'core/sign_up.html')
    return render(request, 'core/sign_up.html')

def simple_upload(request):
    global uploaded_file_url
    if request.method == 'POST' and request.FILES['myfile']:
        print logged 
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #return render(request, 'core/simple_upload.html', {
         #   'uploaded_file_url': uploaded_file_url
        #})
        
        fileName=str(myfile)
        print "Filename : ", file
        bucket='gcr253'
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(fileName, bucket, fileName)

        client=boto3.client('rekognition')

        response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},MinConfidence=80)
        print('Detected labels for ' + fileName)
        res=[]
        s = 0;
        #keyword = []
        for label in response['Labels']:
            print label['Name']
            keyword.add(label['Name'])
        response1 = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},Attributes=["ALL", "DEFAULT"])
        for person in response1['FaceDetails']:
            for emotion in person['Emotions']:
                print emotion['Type']
                keyword.add(emotion['Type'])
        keyword1 = list(keyword)
        for key in keyword1:      
            r = requests.get("http://quotes.rest/quote/search.json?api_key=**********&minlength=100&maxlength=200&category="+key)
            response = json.loads(r.content)
            #s += 1;
            try:
                x = response['contents']['quote']
                print x
                es.index(index='quotes1', doc_type="'"+key+"'", body={'quote': x, 'keyword' : key}, ignore = [400, 404])
                #quotes.append(s)
                #quotes.append(response['contents']['quote'])
                #res.append(quotes)
            except:
                continue  
                 
        
        return render(request, 'core/simple_upload.html', {'uploaded_file_url': uploaded_file_url,'logged': logged})
        #return render(request, 'core/simple_upload.html')
        #quotes_json = json.dumps(cap)
        #print quotes_json
        #return quotes_json
        #return HttpResponse(quotes_json, content_type="application/json")

    return render(request, 'core/simple_upload.html', {'logged': logged})
    #return HttpResponse(None)

def log_me_in(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:
            global logged  
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            x=request.POST['username']
            c.execute("select password from USER where uname=:uname", {'uname':x})
            y=c.fetchone()
            conn.close()
            if y==None:
                return render(request, 'core/sign_up.html', {'alert1': "You are not yet signed up!"})
            if y[0]!=request.POST['password']:
                return render(request, 'core/login.html', {'alert1': "Username and Password doesnt match!"})
            if y[0]==request.POST['password']:
                print "abc"
                logged=True
                print logged
                return render(request, 'core/simple_upload.html' , {'logged': logged})
    return render(request, 'core/login.html')


def sign_me_up(request):
    if request.method == 'POST' and request.POST['username']:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        a=request.POST['username']
        b=request.POST['fname']
        d=request.POST['lname']
        e=request.POST['email']
        f=request.POST['password']
        g=request.POST['re_password']
        c.execute("select * from USER where uname=:uname", {'uname':a})
        y=c.fetchone()
        if y!=None:
            conn.close()
            return render(request, 'core/sign_up.html', {'alert1': "username already exist , please use different username!"})
        if f!=g:
            conn.close()
            return render(request, 'core/sign_up.html', {'alert1': "Password doesnt match!"})
        else:
            c.execute("INSERT INTO USER VALUES(:uname, :fname, :lname, :email, :password)",{'uname':a,'fname':b,'lname':d,'email':e,'password':f})
            conn.commit()
            conn.close()
            return render(request, 'core/login.html', {'alert1': "Successfully signed_up!"})
    return render(request, 'core/login.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })