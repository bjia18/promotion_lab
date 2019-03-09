import sys
import rev_script

if len(sys.argv)<3 and sys.argv[1]!='accuracy':
    print("<something.csv> <tree/bayes>")
    print("<accuracy>")
    exit(1)

if (sys.argv[1]=='accuracy'):
    rev_script.accuracy()
elif (sys.argv[2]=='tree'):
    rev_script.tree(sys.argv[1])
elif (sys.argv[2]=='bayes'):
    rev_script.pdf(sys.argv[1])
elif (sys.argv[2]=='bootstrap'):
    rev_script.bootstrap(sys.argv[1])

