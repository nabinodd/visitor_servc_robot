import requests
import json
from requests.auth import HTTPDigestAuth
import re

regex = r"<currTemperature>(\d*)<\/currTemperature>"
url = 'http://192.168.10.222:80/ISAPI/Event/notification/alertStream'
username = 'admin'
password = 'ingnepal123'
boundry  = '--MIME_boundary'

def connect():
    session = requests.Session()
    response = session.get( url, stream=True, auth=HTTPDigestAuth( username, password) )
    if 404 == response.status_code :
        return
    for chunk in response.iter_content(128) :
        try:
            data = chunk.decode( 'utf-8')
            matches = re.finditer(regex, data, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                tmpr=match.groups()[0]
                yield tmpr
        except:
            pass

if __name__ == "__main__":
    for tmper in connect():
        temperature=tmper
        print('Current temperature is : ',temperature)