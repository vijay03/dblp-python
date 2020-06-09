## Counting PC-Authored Papers ##

This script relies on DBLP to pull the papers related to a given
conference and year. There are three things the user needs to set for
each conference. Let me use USENIX ATC as an example.

1. The conference name as seen by DBLP. For example, for ATC this is
`usenix`.

2. The `venue` as seen by DBLP. Each paper belonging to
this conference will have this venue set. For example, for ATC this is
`USENIX Annual Technical Conference`.

3. The year of the conference.

You might need to poke around DBLP a bit to get these values. For
example, if you go to
[http://dblp.uni-trier.de/search/publ/api?q=/conf/eurosys/2017](http://dblp.uni-trier.de/search/publ/api?q=/conf/eurosys/2017),
you can see what the `venue` and conference name parameters are for Eurosys.

### PC Information ###

Unfortunately, there is no automated way to get the program committee
information.  You need to manually get the list of PC members and put
them in a text file. You then process the list of PC members and add
them to the `pc[year][conf]` list in `checkpc.py`.

An effort must be made to make the names of the PC members identical
to how they appear on DBLP. For example, if an author is called "A
B. C" on DBLP, their PC entry must be changed to reflect that (often
it will be just "A C" in the PC list).

For authors with common names, their DBLP name might have a
number. For example, "A B 001". The PC entry will have to changed to
reflect the correct author.
        
### Checking PC Authorship ###

After parsing the PC list and populating `pc[year][conf]` you must
call `check_pc(conf, year, DBLP-conf-venue)`. `conf` and
`DBLP-conf-venue` must match what DBLP sees for the conference as
mentioned above. The `conf` used in `pc` and `check_pc` must match.

`check_pc` will then print out the total number of papers, the number
of papers with at least one PC member as author, and the percentage of
total papers authored by PC members.

### Sample Output ###

``
PC Paper # 1
Title:  ABC
PC Member who is author: DEF

ConfConf 2019
Total papers:  62
PC Papers:  18
Percentage:  29.0
```      
    
### Caveats ###

This scripts works to the extent the names of the program committee
match their DBLP name for their papers. As such, it is likely it does
not work well for authors with unicode characters in their names, and
authors with common names. Thus, the results of this script are a
lower bound on the number of PC-authored papers in the conference.

### Results ###

Results for a number of recent conferences, sorted by % of
PC-Papers. Each PC-Authored paper is only counted once.
    
| Conference | Year | Total Papers | PC-Papers | % of PC-Papers |
|-------------|:-------------:| -----:|----:|----:|
POPL    | 2017 |   64 |    6   |  9.4  |
ASPLOS  | 2017 |   56 |    7   |  12.5 |
CoNEXT		| 2015 |	40	|	5	|	12.50
PLDI    | 2018 |   55 |    8   |  14.5 |  
ATC     | 2017 |   63 |   10   |  15.9 |
PLDI    | 2017 |   47 |    8   |  17.0 |
Eurosys | 2017 |   41 |    7   |  17.1 |
CoNEXT		| 2017 |	39	|	7	|	17.95
NSDI    | 2015 |   42 |    8   |  19.1 |
CoNEXT		| 2014 |	36	|	7	|	19.44
CoNEXT		| 2013 | 	30	|	6	|	20.00 |
NSDI    | 2016 |   44 |    9   |  20.4 |
OSDI    | 2016 |   47 |   10   |  21.3 |
NSDI    | 2017 |   46 |   10   |  21.7 |
SOSP    | 2015 |   30 |    7   |  23.3 |
CoNEXT	| 2012 |   32 |	  9    | 28.12 |
ISCA    | 2019 |   62 |   18   |  29.0 |
CoNEXT		| 2016 |	35	|	11	|	31.43
ISCA    | 2017 |   54 |   17   |  31.5 |
FAST    | 2018 |   24 |    8   |  33.3 |
SIGMOD  | 2017 |  102 |   35   |  34.3 |          
Mobicom | 2014 |   37 |   13   |  35.1 |
SOSP    | 2017 |   39 |   14   |  35.9 | 
SOSP    | 2013 |   30 |   11   |  36.7 |
Mobicom | 2017 |   35 |   13   |  37.1 |            
SIGCOMM | 2017 |   36 |   14   |  38.9 |            
SIGCOMM | 2014 |   46 |   18   |  39.1 | 
Mobicom | 2015 |   38 |   15   |  39.5 |            
SIGCOMM | 2015 |   40 |   18   |  45.0 | 
Mobicom | 2016 |   31 |   17   |  54.8 |            
SIGCOMM | 2016 |   39 |   22   |  56.4 |            

Seperately showing different conferences, sorted by year.

| Conference | Year | Total Papers | PC-Papers | % of PC-Papers |
|-------------|:-------------:| -----:|----:|----:|
NSDI    | 2015 |   42 |    8   |  19.1 |
NSDI    | 2016 |   44 |    9   |  20.4 |
NSDI    | 2017 |   46 |   10   |  21.7 |

| Conference | Year | Total Papers | PC-Papers | % of PC-Papers |
|-------------|:-------------:| -----:|----:|----:| 
PLDI    | 2017 |   47 |    8   |  17.0 |
PLDI    | 2018 |   55 |    8   |  14.5 | 

| Conference | Year | Total Papers | PC-Papers | % of PC-Papers |
|-------------|:-------------:| -----:|----:|----:|
SIGCOMM | 2014 |   46 |   18   |  39.1 | 
SIGCOMM | 2015 |   40 |   18   |  45.0 |            
SIGCOMM | 2016 |   39 |   22   |  56.4 | 
SIGCOMM | 2017 |   36 |   14   |  38.9 |            
     
| Conference | Year | Total Papers | PC-Papers | % of PC-Papers |
|-------------|:-------------:| -----:|----:|----:|
Mobicom | 2014 |   37 |   13   |  35.1 |            
Mobicom | 2015 |   38 |   15   |  39.5 |            
Mobicom | 2016 |   31 |   17   |  54.8 |            
Mobicom | 2017 |   35 |   13   |  37.1 |            

| Conference | Year | Total Papers | PC-Papers | % of PC-Papers |
|-------------|:-------------:| -----:|----:|----:|
SOSP    | 2013 |   30 |   11   |  36.7 |
SOSP    | 2015 |   30 |    7   |  23.3 |
SOSP    | 2017 |   39 |   14   |  35.9 |

 Conference | Year | Total Papers | PC-Papers | % of PC-Papers |
|-------------|:-------------:| -----:|----:|----:|
CoNEXT		| 2012 |	32	|	9	|	28.12
CoNEXT		| 2013 | 	30	|	6	|	20.00
CoNEXT		| 2014 |	36	|	7	|	19.44
CoNEXT		| 2015 |	40	|	5	|	12.50
CoNEXT		| 2016 |	35	|	11	|	31.43
CoNEXT		| 2017 |	39	|	7	|	17.95


PLDI 2018 information contributed by the PC Chair, Dan Grossman.
CoNEXT information contributed by Marco Mellia and Roberto Marturano.
