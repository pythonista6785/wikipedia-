import wikipedia as wiki
import os.path
import nltk as nl
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
from nltk.util import ngrams
import exceptions

presentpath=os.getcwd()
save_path = str(presentpath)+'/txtfiles'

if not os.path.exists(save_path):
    os.makedirs(save_path)
mnswrd=[]
fileames=[]
def writingtextfiles(typ,links):
    typ1=typ
    for link in links:
        try:
            page = wiki.WikipediaPage(link)
            content = page.content
            stemmer = SnowballStemmer("english")
            tokenizer = RegexpTokenizer(r'\w+')
            stem_data = tokenizer.tokenize(stemmer.stem(content))
            stop_data = stopwords.words('english')
            words = [word for word in stem_data if word not in stop_data]
            completeName = os.path.join(save_path, str(typ1)+str(link)+".txt")
            f=open(completeName,'w')
            fileames.append(str(typ1)+str(link)+".txt")
            fa=open(presentpath+'/montster_word.txt','a')
            mnswrd.extend(words)
            fa.write(", ".join(words).encode('utf-8'))
            print ".",
            f.write("Total words in the file:{}".format(len(words)))
            f.write("\r\n")
            f.write(", ".join(words).encode('utf-8'))
            f.close()
            fa.close()

        except:
            print "This is an error message!"

f = open(presentpath+'/f.txt','r')
lis =f.read().replace("\xc5\x8d" ,' ')
lis1 = lis.replace("\xc4\xb1",' ')
lis2 = lis.replace(" ",'_')
nf = lis2.split('\n')
nfl = nf[:-3]

writingtextfiles('nonfeatured.',nfl)
# opened page using WikipediaPage
f = open(presentpath+'/u.txt','r')
lis =f.read().replace("\xc2\xa0" ,' ')
lis1 = lis.replace("\xc3\xa0" ,' ')
links = lis1.split('\n')
writingtextfiles('featured.',links)


def writeArff(fname,di):
    dictionary=di
    f=open(fname,'w')
    f.write("% token -datagrams")
    f.write('\r\n')
    f.write("@RELATION wordcounts")
    f.write('\r\n')
    f.write('\r\n')

    for i in dictionary['attribute']:
        wr="@ATTRIBUTE "+", ".join(i)
        f.write("@ATTRIBUTE "+", ".join(i).encode('utf-8')+' numeric')
        f.write('\r\n')
    f.write('\r\n')
    f.write('\r\n')
    f.write("@DATA")
    f.write('\r\n')
    f.write('\r\n')
    for fil1 in fileames:
        re=open(save_path+'/'+fil1,'r')
        find=re.read().split(', ')
        m=''
        for mon in mnswrd:
            m=m+str(find.count(mon))+', '
        m=m+' '+str(fil1.split('.')[1])+' '+str(fil1.split('.')[0])
        f.write(m)
        f.write('\r\n')
    f.close()

for gram in range(1,4):
    dictionary={}
    attribute=[]
    data=[]
    va=str(gram)+'gram'
    filename=va+'.arff'
    va=nl.BigramCollocationFinder.from_words(mnswrd)._ngram_freqdist(mnswrd,gram).items()
    for spl in va:
        attribute.append(spl[0])
        data.append(spl[1])
    dictionary['attribute']=attribute
    dictionary['data']=data
    writeArff(filename,dictionary)
