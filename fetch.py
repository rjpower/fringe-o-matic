#!/usr/bin/env python

import os, time

for i in range(26): 
  x = chr(ord('A') + i)
  os.system('wget -O data.%s http://www.fringenyc.org/basic_page.php?ltr=%s' % (x, x))
  time.sleep(1)

  
os.system('wget -O data.num http://www.fringenyc.org/basic_page.php?ltr=num')
