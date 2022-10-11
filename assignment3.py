import random
import string
import codecs
import gensim 
from nltk.stem.porter import PorterStemmer 

stopwords = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(',')

random.seed(123) 
f = codecs.open("pg3300.txt", "r", "utf-8")
par = f.read()
f.close()
par = par.split(' \r\n')
#\n for unix and \r\n for windows

def gut(p):
    return "gutenberg" not in p.lower()

def tokenize(p):
    s = string.punctuation+"\n\r\t"
    for c in s:
        p = p.replace(c," ").lower()
    return p

# remove paragraphs with Gutenberg
filtered_par = list(filter(gut, par))

# remove string punctuation 
filtered_par = list(map(lambda p: tokenize(p), filtered_par))


# create new list within each paragraph with words
tokens = list(map(lambda p: p.split(" "), filtered_par))

def empty(p):
    if len(p) == 0: 
        return False
    else:
        for s in stopwords:
            if s == p:
                return False
        return True

# remove empty list items
tokens = list(map(lambda p: list(filter(empty, p)), tokens))

#print(tokens[15])

# apply porter stemmer on list of words
stemmer = PorterStemmer()
stemmed = list(map(lambda p: list(map(lambda w: stemmer.stem(w), p)), tokens))
#print(stemmed[14])

dictionary = gensim.corpora.Dictionary(stemmed)
BoW = list(map(lambda p:dictionary.doc2bow(p), stemmed))
#print(BoW)
tfidf_model = gensim.models.TfidfModel(BoW)
tfidf_corpus = tfidf_model[BoW]
tfidf_index = gensim.similarities.MatrixSimilarity(tfidf_corpus) 

lsi_model = gensim.models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=100) 
lsi_corpus = lsi_model[BoW]
lsi_index = gensim.similarities.MatrixSimilarity(lsi_corpus) 
print(dictionary[2])

print(lsi_model.show_topics()[:3])

# stopword_ids = []
# for s in stopwords:
#     stopword_ids.append(dictionary.token2id[stemmer.stem(s)])
# print(stopword_ids)