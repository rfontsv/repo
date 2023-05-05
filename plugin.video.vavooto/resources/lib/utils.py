# -*- coding: utf-8 -*-
import xbmcgui, xbmcaddon, sys, xbmc, os, time, json, xbmcplugin
PY2 = sys.version_info[0] == 2
if PY2:
	from urlparse import urlparse, parse_qsl, quote_plus
	from urllib import urlencode
	translatePath = xbmc.translatePath
else:
	from urllib.parse import urlencode, urlparse, parse_qsl, quote_plus
	import xbmcvfs
	translatePath = xbmcvfs.translatePath

def py2dec(msg):
	if PY2:
		return msg.decode("utf-8")
	return msg

addon = xbmcaddon.Addon()
addonInfo = addon.getAddonInfo
addonID = addonInfo('id')
addonprofile = py2dec(translatePath(addonInfo('profile')))
addonpath = py2dec(translatePath(addonInfo('path')))
if not os.path.exists(addonprofile):
	os.makedirs(addonprofile)

def selectDialog(list, heading=None, multiselect = False):
	if heading == 'default' or heading is None: heading = addonInfo('name')
	if multiselect:
		return xbmcgui.Dialog().multiselect(str(heading), list)
	return xbmcgui.Dialog().select(str(heading), list)

home = xbmcgui.Window(10000)

def set_cache(key, value, timeout=300):
	data={"sigValidUntil": int(time.time()) +timeout,"value": value}
	home.setProperty(key, json.dumps(data))
	
def get_cache(key):
	keyfile = home.getProperty(key)
	if keyfile:
		r = json.loads(keyfile)
		if r.get('sigValidUntil', 0) > int(time.time()):
			return r.get('value')
		home.clearProperty(key)
	return

def getAuthSignature():
	signfile = get_cache('signfile')
	if signfile: return signfile
	vec = {"vec": "9frjpxPjxSNilxJPCJ0XGYs6scej3dW/h/VWlnKUiLSG8IP7mfyDU7NirOlld+VtCKGj03XjetfliDMhIev7wcARo+YTU8KPFuVQP9E2DVXzY2BFo1NhE6qEmPfNDnm74eyl/7iFJ0EETm6XbYyz8IKBkAqPN/Spp3PZ2ulKg3QBSDxcVN4R5zRn7OsgLJ2CNTuWkd/h451lDCp+TtTuvnAEhcQckdsydFhTZCK5IiWrrTIC/d4qDXEd+GtOP4hPdoIuCaNzYfX3lLCwFENC6RZoTBYLrcKVVgbqyQZ7DnLqfLqvf3z0FVUWx9H21liGFpByzdnoxyFkue3NzrFtkRL37xkx9ITucepSYKzUVEfyBh+/3mtzKY26VIRkJFkpf8KVcCRNrTRQn47Wuq4gC7sSwT7eHCAydKSACcUMMdpPSvbvfOmIqeBNA83osX8FPFYUMZsjvYNEE3arbFiGsQlggBKgg1V3oN+5ni3Vjc5InHg/xv476LHDFnNdAJx448ph3DoAiJjr2g4ZTNynfSxdzA68qSuJY8UjyzgDjG0RIMv2h7DlQNjkAXv4k1BrPpfOiOqH67yIarNmkPIwrIV+W9TTV/yRyE1LEgOr4DK8uW2AUtHOPA2gn6P5sgFyi68w55MZBPepddfYTQ+E1N6R/hWnMYPt/i0xSUeMPekX47iucfpFBEv9Uh9zdGiEB+0P3LVMP+q+pbBU4o1NkKyY1V8wH1Wilr0a+q87kEnQ1LWYMMBhaP9yFseGSbYwdeLsX9uR1uPaN+u4woO2g8sw9Y5ze5XMgOVpFCZaut02I5k0U4WPyN5adQjG8sAzxsI3KsV04DEVymj224iqg2Lzz53Xz9yEy+7/85ILQpJ6llCyqpHLFyHq/kJxYPhDUF755WaHJEaFRPxUqbparNX+mCE9Xzy7Q/KTgAPiRS41FHXXv+7XSPp4cy9jli0BVnYf13Xsp28OGs/D8Nl3NgEn3/eUcMN80JRdsOrV62fnBVMBNf36+LbISdvsFAFr0xyuPGmlIETcFyxJkrGZnhHAxwzsvZ+Uwf8lffBfZFPRrNv+tgeeLpatVcHLHZGeTgWWml6tIHwWUqv2TVJeMkAEL5PPS4Gtbscau5HM+FEjtGS+KClfX1CNKvgYJl7mLDEf5ZYQv5kHaoQ6RcPaR6vUNn02zpq5/X3EPIgUKF0r/0ctmoT84B2J1BKfCbctdFY9br7JSJ6DvUxyde68jB+Il6qNcQwTFj4cNErk4x719Y42NoAnnQYC2/qfL/gAhJl8TKMvBt3Bno+va8ve8E0z8yEuMLUqe8OXLce6nCa+L5LYK1aBdb60BYbMeWk1qmG6Nk9OnYLhzDyrd9iHDd7X95OM6X5wiMVZRn5ebw4askTTc50xmrg4eic2U1w1JpSEjdH/u/hXrWKSMWAxaj34uQnMuWxPZEXoVxzGyuUbroXRfkhzpqmqqqOcypjsWPdq5BOUGL/Riwjm6yMI0x9kbO8+VoQ6RYfjAbxNriZ1cQ+AW1fqEgnRWXmjt4Z1M0ygUBi8w71bDML1YG6UHeC2cJ2CCCxSrfycKQhpSdI1QIuwd2eyIpd4LgwrMiY3xNWreAF+qobNxvE7ypKTISNrz0iYIhU0aKNlcGwYd0FXIRfKVBzSBe4MRK2pGLDNO6ytoHxvJweZ8h1XG8RWc4aB5gTnB7Tjiqym4b64lRdj1DPHJnzD4aqRixpXhzYzWVDN2kONCR5i2quYbnVFN4sSfLiKeOwKX4JdmzpYixNZXjLkG14seS6KR0Wl8Itp5IMIWFpnNokjRH76RYRZAcx0jP0V5/GfNNTi5QsEU98en0SiXHQGXnROiHpRUDXTl8FmJORjwXc0AjrEMuQ2FDJDmAIlKUSLhjbIiKw3iaqp5TVyXuz0ZMYBhnqhcwqULqtFSuIKpaW8FgF8QJfP2frADf4kKZG1bQ99MrRrb2A="}
	url = 'https://www.vavoo.tv/api/box/ping2'
	import requests
	req = requests.post(url, data=vec).json()
	signed = req['response'].get('signed')
	set_cache('signfile', signed)
	return signed 

def getWatchedSig():
	watchedsignfile = get_cache('watchedsignfile')
	if watchedsignfile: return watchedsignfile
	import requests
	_data='{"x": "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"}'
	_headers={"user-agent": "WATCHED/1.8.3 (android)", "accept": "application/json", "content-type": "application/json; charset=utf-8", "content-length": "2624", "accept-encoding": "gzip", "cookie": "lng="}
	r = requests.post('https://www.watched.com/api/box/ping', data=_data, headers=_headers).json()['response']
	signed = r['signed']
	set_cache('watchedsignfile', signed)
	return signed

def log(*args):
	msg=""
	for arg in args:
		msg += repr(arg)
	xbmc.log(msg, xbmc.LOGINFO)

def yesno(heading, line1, line2='', line3='', nolabel='', yeslabel=''):
	if PY2: return xbmcgui.Dialog().yesno(heading, line1,line2,line3, nolabel, yeslabel)
	else: return xbmcgui.Dialog().yesno(heading, line1+"\n"+line2+"\n"+line3, nolabel, yeslabel)
	
def ok(heading, line1, line2='', line3=''):
	if PY2: return xbmcgui.Dialog().ok(heading, line1,line2,line3)
	else: return xbmcgui.Dialog().ok(heading, line1+"\n"+line2+"\n"+line3)

def getIcon(name):
	if os.path.exists("%s/resources/art/%s.png" % (addonpath ,name)):return "%s/resources/art/%s.png" % (addonpath ,name)
	else: return  name

def end(succeeded=True, cacheToDisc=True):
	return xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=succeeded, cacheToDisc=cacheToDisc)
	
def add(params, o, isFolder=False):
	return xbmcplugin.addDirectoryItem(int(sys.argv[1]), url_for(params), o, isFolder)

def set_category(cat):
	xbmcplugin.setPluginCategory(int(sys.argv[1]), cat)


def set_content(cont):
	xbmcplugin.setContent(int(sys.argv[1]), cont)
	
def set_resolved(item):
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def sort_method():
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)

def url_for(params):
	return "%s?%s" % (sys.argv[0], urlencode(params))
	