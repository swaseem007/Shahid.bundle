#!/usr/bin/env python
import re
import base64

HLS_COMPAT = ('iOS', 'Android', 'Roku', 'Safari', 'MacOSX', 'Windows', 'Plex Home Theater', 'Samsung')
shurl = 'http://shahid.mbc.net/ar/shows/content/00~listing~-param-.ptype-.Id-0.sort-latest.pageNumber-%d.html'
msurl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.sort-latest.pageNumber-%d.html'
kurl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7919.sort-latest.pageNumber-%d.html'
durl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.genres-7876.sort-latest.pageNumber-%d.html'
rurl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.genres-7871.sort-latest.pageNumber-%d.html'
turl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7914.sort-latest.pageNumber-%d.html'
curl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.genres-7858.sort-latest.pageNumber-%d.html'
eurl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7915.sort-latest.pageNumber-%d.html'
khurl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7911.sort-latest.pageNumber-%d.html'
syurl = 'http://shahid.mbc.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7918.sort-latest.pageNumber-%d.html'
url_series = 'http://shahid.mbc.net/ar/series/%s'
url_show = 'http://shahid.mbc.net/ar/show/%s'
shahid = 'http://shahid.mbc.net%s'
allcover = 'http://en.kingofsat.net/jpg/mbc-drama.jpg'
urlep = 'http://shahid.mbc.net/ar/series/autoGeneratedContent/relatedEpisodeListingDynamic~listing~-param-.ptype-series.seriesId-%s.showSection-%s.sort-number:DESC.pageNumber-%d.html'
vurl = 'http://l3md.shahid.net/mediaDelivery/media/'
hadurl = 'http://hadynz-shahid.appspot.com/scrape?m=%s'
imgurl = 'http://www.webproxy.net/view?q=%s'
START_MENU = [['TV Shows', 'sh'], ['All Series', 'al'],["Drama","dr"], ['Comedy','co'], ['Romance','ro'], ['Syrian','sr'],['Khaliji','kh'],['Korean','ko'], ['Turkish','tr'] ,['Egyptian','eg']]
PREFIX = "/video/shahid"
NAME = "ShahidMBC"
ART = "art-default3.jpg"
ICON = "icon-default3.png"
key = base64.b64decode('YXBpS2V5PXNoJTQwaGlkMG5saW4zJmhhc2g9YjJ3TUNUSHBTbXl4R3FRakpGT3ljUm1MU2V4JTJCQnBUSy9vb3h5NnZIYXFzJTNE')
search_cover = False
HLSF = False
blocked = False
def contentsxpath(blocked,url):
	if not blocked :
		doc=  HTML.ElementFromURL(url)
	else:
		url= "http://ekkun.com/tower/hack.php?url=%s" %url	
		doc=  HTML.ElementFromURL(url)
	return doc
def contentsjson(n,url):
	if n == 1:	
		dic=  JSON.ObjectFromURL(url)
	else:
		url= "http://ekkun.com/tower/hack.php?url=%s" %url
		dic=  JSON.ObjectFromURL(url)

def videoID(Id, HLSF=False):
	url = 'http://api.shahid.net/api/Content/Episode/'+Id+'/0?'+key
	dic = JSON.ObjectFromURL(url) #contentsjson(2,url)
	m3u8= str(dic['data']['url']).split('/')[-1]
	if HLSF:
		video = vurl+m3u8
		return video
	else:
		dic = JSON.ObjectFromURL(hadurl %m3u8[:-5])
		video=  dic[0]["URL"]
		return video
def episodesId(SID,stype,ss):
	if stype  < 2:
		doc2 =contentsxpath(blocked,url_show %SID)
	else:
		doc2 =contentsxpath(blocked,url_series %SID)	
	urls2 = doc2.xpath('//*[@class="pageSection"]/*')	
	if ss == 4:
		global search_cover
		imgs = doc2.xpath('//*[@id="main"]/*')
		search_cover = imgs[2][0][0].get('src')
	show = urls2[0][0][3][0][0][0].get('onclick').split('showSection-')[1].split("'")[0]
	i= 0
	check =True
	episodes= []
	while check:
		try:
			url = urlep %(SID, show,i)
			doc = contentsxpath(blocked,url)
			urls = doc.xpath('//*[@class="subitem"]/div/@id')[1:][::2]

			if len(urls)>0:
				episodes.extend(urls)
				i+=1
			else:
				check = False
		except:
			check = False
	return episodes	

def Start():
	ObjectContainer.art = R(ART)
	HTTP.CacheTime = 180



@handler(PREFIX, NAME, thumb=ICON)
def MainMenu():
	global HLSF
	global blocked
	oc = ObjectContainer()
	if Client.Platform in HLS_COMPAT:
		HLSF = True
	doc=  HTML.ElementFromURL(shahid %'')
	if 'Blocked' in doc.xpath('//title/text()')[0]:
		blocked = True

	for menu in sorted(START_MENU):
		oc.add(DirectoryObject(key = Callback(ShahidList, category = menu[1]), title = menu[0]))
	oc.add(InputDirectoryObject(key = Callback(SearchShahidList), title = "Search by ID", prompt = "Search"))
	return oc

@route(PREFIX + "/list")
def ShahidList(category = None):
	if category == None:
		Log.Info("[No category has been set.")
	elif category == "sh":
		return CreateShahidList(shurl, 'TV Shows')			
	elif category == "al":
		return CreateShahidList(msurl, 'All')
	elif category == "dr":
		return CreateShahidList(durl, 'Drama')
	elif category == "co":
		return CreateShahidList(curl, 'Comedy')
	elif category == "ro":
		return CreateShahidList(rurl,'Romance')
	elif category == "sr":
		return CreateShahidList(syurl,'Syrian')
	elif category == "kh":
		return CreateShahidList(khurl,'Khaliji')
	elif category == "eg":
		return CreateShahidList(eurl, 'Egyptian')
	elif category == "tr":
		return CreateShahidList(turl,'Turkish')
	else:
		Log.Error("No defined category.")

@route(PREFIX + "/search")
def SearchShahidList(query):
	if query:
		return ShahidWatch('se_'+query,allcover, query,2)

def CreateShahidList(sel, title = "Sports", page=0):
	doc2 = contentsxpath(blocked,sel %page)
	urls3 =  doc2.xpath('//*[@class="subitem"]/div/@id')[1:][::2]
	imgs2 = doc2.xpath('//*[@class="subitem"]/*/a/*/img/@src')
	oc = ObjectContainer(title1 = title)
	for i in range(len(urls3)):
		
		if '/show' in sel:
			SID2 = urls3[i]
			stype = 1
		else:
			SID2 =urls3[i]
			stype  = 2
		if not blocked:
			cover = imgs2[i]
		else:
			cover = 'http://ekkun.com/tower/hack.php?url='+imgs2[i]
		
		name2  = SID2
		oc.add(DirectoryObject(
			key = Callback(ShahidWatch, url = str(SID2), cover = cover, title = name2, stype=stype),
			title = name2,
			thumb = Resource.ContentsOfURLWithFallback(url = cover, fallback='icon-cover.png')
			))
	if len(urls3) == 30:
		oc.add(NextPageObject(
					key = Callback(CreateShahidList,sel=sel, title=title, page=page+1),
					title = "More..."
			))						

	return oc
def ShahidWatch(url,cover, title,stype):
	if 'se' in url:
		url=url.split('_')[1]
		episodes = episodesId(url,stype,4)
		cover =  search_cover
	else:    	
		episodes = episodesId(url,stype,5)
	if len(episodes)>0:
		Ids=[]
		oc = ObjectContainer(title1 = title)
		k=1
		for ep in episodes[::-1]:
			Ids.append(ep)
			k+=1
		for n in range(0,len(Ids)):
			name= str(n+1)
			oc.add(CreateVideoClipObject(url=Ids[n], title=' Episode '+name, thumb=cover))
	else:
		Log.Error("Failed loading the page")
	return oc

def CreateVideoClipObject(url, title, thumb, container = False):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, container = True),
        url = url,
        title = title,
        thumb = thumb,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = HTTPLiveStreamURL(url = videoID(url,HLSF))
                    )
                ],
                optimized_for_streaming = True
            )
        ]
    )

    if container:
        return ObjectContainer(objects = [vco])
    else:
        return vco
    return vco
