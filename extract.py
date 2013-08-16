#!/usr/bin/env python


import sys
import bs4
import json
import glob
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import *

out = {}
for f in glob.glob('data.*'):
  soup = bs4.BeautifulSoup(open(f).read())
  shows = soup.find_all('table', class_='new')
  for show in shows:
    title = show.find('b').text
    venue = show.find('a', href='http://www.fringenyc.org/index.php/shows/venue-guide').text
    venue = venue.split(':')[1].strip()
    info = []

    blob = show.find('font', size='2', face='Arial').br
    blob = blob.next_sibling
    while blob is not None:
      if blob.name == 'b' and blob.find_all('a', href='http://www.fringenyc.org/index.php/shows/venue-guide'):
        break

      try:
        if 'Discover' in blob.prettify():
          break

        info.append(blob.prettify())
      except:
        info.append(blob)
        pass

      blob = blob.next_sibling

    times = [a.text for a in show.find_all('a', target='Ticket Window')]
    datetimes = []
    for t in times:
      date, time = t.split('@')
      date = '08/' + date.split()[1].strip() + '/2013'
      time = time.strip()
      
      if time[-1] == '*': time = time[:-1]
      if len(time) == 1: time = time + ':00'
      if time == 'NOON': time = '12:00'

      time = time + 'PM'
      
      try:
        dt = parse(date + ' ' + time + ' EDT' )
        #print dt.utcoffset()
        #print date + ' ' + time, dt
        epoch = datetime.utcfromtimestamp(0)
        epoch = epoch.replace(tzinfo=tzutc())
        #print epoch.utcoffset()
        delta = dt - epoch
        datetimes.append(delta.total_seconds() * 1000.0)
      except:
        raise
        print >>sys.stderr, 'Bad: (%s), (%s)' % (date, time)

    entry = { 'title' : title, 
              'venue' : venue, 
              'info' : ''.join(info),
              'times' : datetimes }

    out[title] = entry

print 'shows = ', json.dumps(out, sort_keys=True, indent=2, separators=(',',':')), ';'
