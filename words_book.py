#!/usr/bin/python3

import os
import signal

output = os.popen("cat /home/chengs/.bash_history|grep wd")
recite = open("/home/chengs/Desktop/words-book.txt","w+")
review = open("/home/chengs/Desktop/review.txt","w+")
counter = 0
for line in output:
    res = os.popen(line).read()
    if not res.startswith("\033"): # 利用颜色码进行过滤
        continue
    counter += 1
    review.write(str(counter)+"    "+line[3:])
    recite.write(res)
    recite.write(" =========  "+str(counter)+" ========== \n")
    signal.setitimer(signal.ITIMER_REAL, 2)
    
recite.close()
review.close()