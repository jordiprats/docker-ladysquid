#!/usr/local/bin/python

from youtube_api import YouTubeDataAPI

import langdetect
import sys
import re
import os

if os.getenv('DEBUG', False):
    DEBUG = True
else:
    DEBUG = False

def is_evil(code):

    yt = YouTubeDataAPI(os.getenv('YOUTUBE_KEY', '123'))

    response = yt.get_video_metadata(code)

    title = response['video_title']
    description = response['video_description']

    langs = langdetect.detect_langs(title+" "+description)

    for item in langs:
        data = str(item).split(':')
        if DEBUG:
            print(str(item))

        if data[0]=='es':
            if float(data[1])>0.5:
                return True
    
    return False

def get_video_code(url):
    # https://youtu.be/JnlTy3UQ1Js?t=404
    if re.match(r'.*youtu.be/.*', url):
        match = re.search(r'youtu.be/([0-9a-zA-Z_]+)', url)
        if match:
            return match.group(1)

    # https://www.youtube.com/watch?v=msNVGJbfjwA&list=RDMMmsNVGJbfjwA&start_radio=1
    if re.match(r'.*www.youtube.com/.*', url):
        match = re.search(r'www.youtube.com/watch\?.*v=([0-9a-zA-Z_]+).*', url)
        if match:
            return match.group(1)

    return None

while True:
    try:
        line = sys.stdin.readline().strip()
        if line=='quit\n':
            sys.exit('quiting...')
        items=line.split(' ')
        if items[0]=='www.youtube.com' or items[0]=='youtu.be':
            code = get_video_code(items[1])
            if code:
                if DEBUG:
                    print(code)
                if is_evil(code):
                    sys.stdout.write( 'OK\n' )
                    sys.stdout.flush()
                    with open('/code/evil.log', 'a') as logfile:
                        logfile.write(line+' MATCH\n')
                    continue
        with open('/code/evil.log', 'a') as logfile:
            logfile.write(line+' SKIP\n')
    except:
        pass
    sys.stdout.write( 'ERR\n' )
    sys.stdout.flush()