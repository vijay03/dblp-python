import datetime
import dblp
import operator
import pickle
from collections import defaultdict

pc = {}
pc["2015"] = defaultdict(list)
pc["2016"] = defaultdict(list)
pc["2017"] = defaultdict(list)
pc["2018"] = defaultdict(list)
pc["2019"] = defaultdict(list)

sosp = {}
sosp_pc = defaultdict(list) 
#pc["2017"]["sosp"] = sosp_pc
eurosys_pc = defaultdict(list)

def clean_author_name(x):
    x = x.encode('ascii', 'ignore') # ignore problems due to unicode
    # middle names and initials often cause problems, so get rid of those
    s = x.split(' ')
    # ignore the DBLP number at the end if there is one
    if s[-1].isdigit(): 
        x = s[0] + " " + s[-2]
    else:
        x = s[0] + " " + s[-1]
    return x

for x in open("isca19-pc.txt", 'r'):
    xx = x.split(",")
    #print xx[0]
    pc["2019"]["isca"].append(xx[0])

for x in open("sosp17-pc.txt", 'r'):
    xx = x.split(",")
    #print xx[0]
    sosp_pc[2017].append(xx[0])
    pc["2017"]["sosp"].append(xx[0])

for x in open("eurosys17-pc.txt", "r"):
    xx = x.split(",")
    #print xx[0]
    eurosys_pc[2017].append(xx[0])
    pc["2017"]["eurosys"].append(xx[0])

for x in open("fast18-pc.txt", "r"):
    xx = x.split(",")
    #print xx[0]
    pc["2018"]["fast"].append(xx[0])

for x in open("osdi16-pc.txt", "r"):
    xx = x.split(",")
    #print xx[0]
    pc["2016"]["osdi"].append(xx[0])

for x in open("atc17-pc.txt", "r"):
    xx = x.split(",")
    #print xx[0]
    pc["2017"]["usenix"].append(xx[0])

for x in open("popl18-pc.txt", "r"):
    xx = x.split(",")
    #print xx[0]
    pc["2018"]["popl"].append(xx[0])

# special for popl 17, just use names as is
for x in open("popl17-pc.txt", "r"):
    pc["2017"]["popl"].append(x.strip())

for x in open("pldi17-pc.txt", "r"):
    pc["2017"]["pldi"].append(x.strip())

for x in open("sigcomm17-pc.txt", "r"):
    pc["2017"]["sigcomm"].append(x.strip())

for x in open("sigcomm18-pc.txt", "r"):
    pc["2018"]["sigcomm"].append(x.strip())
    
total_count = 0
pc_count = 0

def check_pc(conf, year, conf_short):
    total_count = 0
    pc_count = 0
    conf = conf.lower()
    a = dblp.getvenueauthorsbypaper("/conf/" + conf.lower() + "/" + str(year), conf_short)
    for x in a:
        total_count += 1
        for xxx in x:
            for xx in xxx:
                if xx == "Yuanyuan Zhou 0001":
                    if "Yuanyuan Zhou" in pc[year][conf]:
                        pc_count += 1
                        print "YY Zhou", x
                        continue
                if clean_author_name(xx) in pc[year][conf]:
                    pc_count += 1
                    #print xx, x, pc_count
                    print "PC Paper #", pc_count
                    print "Title: ", x[0][0]
                    print "PC Member who is author:", clean_author_name(xx)
                    print
                    break
            
    print conf_short, year
    print "Total papers: ", total_count
    print "PC Papers: ", pc_count
    print "Percentage: ", round(100 * pc_count/total_count, 1)

#check_pc("sosp", "2017", "SOSP")
#check_pc("eurosys", "2017", "EuroSys")
#check_pc("fast", "2018", "FAST")
#check_pc("osdi", "2016", "OSDI")
#check_pc("usenix", "2017", "USENIX Annual Technical Conference")
#check_pc("popl", "2017", "POPL")
#check_pc("pldi", "2017", "PLDI")
#check_pc("sigcomm", "2018", "SIGCOMM")
#check_pc("osdi", "2018", "OSDI")
check_pc("isca", "2019", "ISCA")
