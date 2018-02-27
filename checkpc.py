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

## This is the part where we read the PC information from text files
## and populate the dictionary. pc[year][conf] is a list of PC members
## for that conference.

for x in open("sosp17-pc.txt", 'r'):
    xx = x.split(",")
    pc["2017"]["sosp"].append(xx[0])

for x in open("eurosys17-pc.txt", "r"):
    xx = x.split(",")
    pc["2017"]["eurosys"].append(xx[0])

for x in open("fast18-pc.txt", "r"):
    xx = x.split(",")
    pc["2018"]["fast"].append(xx[0])

for x in open("osdi16-pc.txt", "r"):
    xx = x.split(",")
    pc["2016"]["osdi"].append(xx[0])

for x in open("atc17-pc.txt", "r"):
    xx = x.split(",")
    pc["2017"]["usenix"].append(xx[0])

for x in open("popl18-pc.txt", "r"):
    xx = x.split(",")
    pc["2018"]["popl"].append(xx[0])

# - for isca    
for x in open("isca17-pc.txt", "r"):
    xx = x.split("-")
    pc["2017"]["isca"].append(xx[0].strip())
    
# special for popl 17, just use names as is
for x in open("popl17-pc.txt", "r"):
    pc["2017"]["popl"].append(x.strip())

for x in open("pldi17-pc.txt", "r"):
    pc["2017"]["pldi"].append(x.strip())

for x in open("sigcomm17-pc.txt", "r"):
    pc["2017"]["sigcomm"].append(x.strip())

for x in open("sigmod17-pc.txt", "r"):
    pc["2017"]["sigmod"].append(x.strip())

for x in open("vldb17-pc.txt", "r"):
    pc["2017"]["vldb"].append(x.strip())

for x in open("asplos17-pc.txt", "r"):
    xx = x.split(",")
    pc["2017"]["asplos"].append(xx[0])
    
# The main heart of the logic. 'conf', 'conf_short' both need to be
# the values that DBLP sees for this conference. See the many examples
# to identify the values for the conference you are interested in.
#
# pc[year][conf] needs to be setup before check_pc is invoked.
    
def check_pc(conf, year, conf_short):
    total_count = 0
    pc_count = 0
    conf = conf.lower()
    a = dblp.getvenueauthorsbypaper("/conf/" + conf.lower() + "/" + str(year), conf_short)
    for x in a:
        total_count += 1
        for xx in x:
            # Need to put in more hacks like this unfortunately
            if xx == "Yuanyuan Zhou 0001":
                if "Yuanyuan Zhou" in pc[year][conf]:
                    pc_count += 1
                    continue
            if xx in pc[year][conf]:
                pc_count += 1
                # Uncomment if you want to see which papers are PC-authored
                print xx, x, pc_count
                break

    print
    print conf, year
    print "Total Papers:", total_count
    print "PC-Paper Count:", pc_count
    print "Percentage of PC-authored papers: ", format((100.0 * pc_count/total_count if total_count != 0 else 0), '.2f')

#check_pc("sosp", "2017", "SOSP")
#check_pc("eurosys", "2017", "EuroSys")
#check_pc("fast", "2018", "FAST")
#check_pc("osdi", "2016", "OSDI")
#check_pc("usenix", "2017", "USENIX Annual Technical Conference")
#check_pc("popl", "2017", "POPL")
#check_pc("pldi", "2017", "PLDI")
#check_pc("sigcomm", "2017", "SIGCOMM")
#check_pc("sigmod", "2017", "SIGMOD Conference")
#check_pc("asplos", "2017", "ASPLOS")
check_pc("isca", "2017", "ISCA")

