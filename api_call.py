import requests
import json

API_KEY = ""

def get_iframe_src(div):
    return [x for x in div.split() if 'src' in x][0].split('src')[-1].strip('=').strip("'")

def getHighlights():
    url = "https://free-football-soccer-videos.p.rapidapi.com/"

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "free-football-soccer-videos.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    v = json.loads(response.content)

    comps = {}
    for i in v:
        c = i['competition']['name']
        if c in comps:
            l = comps[c]
            e = i['title'], i['embed'], get_iframe_src(i['embed'])
            l.append(e)
            comps[c] = l
        else:
            l = []
            e = i['title'], i['embed'], get_iframe_src(i['embed'])
            l.append(e)
            comps[c] = l

    return comps

