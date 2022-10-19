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

def gut(p):
    return "gutenberg" not in p.lower()
    
def preprocessing(data):
    par = data.split(' \r\n')
    #\n for unix and \r\n for windows

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

    # apply porter stemmer on list of words
    stemmer = PorterStemmer()
    stemmed = list(map(lambda p: list(map(lambda w: stemmer.stem(w), p)), tokens))

    return stemmed

stemmed_book = preprocessing(par)

dictionary = gensim.corpora.Dictionary(stemmed_book)
Book_BoW = list(map(lambda p:dictionary.doc2bow(p), stemmed_book))  
    
book_tfidf_model = gensim.models.TfidfModel(Book_BoW)
book_tfidf_corpus = book_tfidf_model[Book_BoW]
book_tfidf_index = gensim.similarities.MatrixSimilarity(book_tfidf_corpus) 



full_paragraphs =list(filter(gut, par.split(" \r\n")))
full_paragraphs = list(map(lambda p: p.replace("\r\n", ""), full_paragraphs))

def findRelevantDocuments(query, dictionary, book_tfidf_model):
    processed_query = preprocessing(query)
    query_BoW = dictionary.doc2bow(processed_query[0])
    query_tfidf_corpus = book_tfidf_model[query_BoW]
    doc2similarity = enumerate(book_tfidf_index[query_tfidf_corpus]) 
    tfidf_sim = sorted(doc2similarity, key=lambda kv: -kv[1])[:3]
    for i in tfidf_sim:
        print(str(i[1]) + ": " + full_paragraphs[i[0]][:400])


#query_tfidf_model = gensim.models.TfidfModel(Book_BoW)

findRelevantDocuments("What is the function of money?", dictionary, book_tfidf_model)

# ----- (OUTPUT) TASK 4.3 --------
# 0.44443128: The general stock of any country or society is the same with that of all its inhabitants 
# or members; and, therefore, naturally divides itself into the same three portions, each of which has a 
# distinct function or office.
# 
# 0.28487432: That wealth consists in money, or in gold and silver, is a popular notion which naturally 
# arises from the double function of money, as the instrument of commerce, and as the measure 
# of value. In consequence of its being the instrument of commerce, when we have money we can more readily      
# obtain whatever else we have occasion for, than by means of any other commodity. The great affair, we 
# always find, is to get money. When that is obtained, there is no difficulty in making any subsequent 
# 
# 0.27443162: Whatever part of his stock a man employs as a capital, he always expects it to be 
# replaced to him with a profit. He employs it, therefore, in maintaining productive hands only; and a
# fter having served in the function of a capital to him, it constitutes a revenue to them. Whenever h
# e employs any part of it in maintaining unproductive hands of any kind, that part is from that 
# moment withdrawn from his capital, and placed in his stock reserved for immediate consumption.  




# query_lsi_corpus = book_lsi_model[query_tfidf_corpus]

# doc2similarity = enumerate(book_lsi_index[query_lsi_corpus])


# for i in sorted(query_lsi_corpus):
#     print(i)
#print(sorted(doc2similarity, key=lambda kv: -kv[1])[:3] ) 

#lsi_query = lsi_model[tfidf_query]

# print( sorted(query_lsi_corpus, key=lambda kv: -abs(kv[1]))[:3] )
#print( query_lsi_model.show_topics() )
#print( book_lsi_model.show_topics()[:3] )

#print( sorted(doc2similarity, key=lambda kv: -kv[1])[:3] ) 

# stopword_ids = []
# for s in stopwords:
#     stopword_ids.append(dictionary.token2id[stemmer.stem(s)])
# print(stopword_ids)

book_lsi_model = gensim.models.LsiModel(book_tfidf_corpus, id2word=dictionary, num_topics=100) 
book_lsi_corpus = book_lsi_model[Book_BoW]
book_lsi_index = gensim.similarities.MatrixSimilarity(book_lsi_corpus) 

# query_tfidf_index = gensim.similarities.MatrixSimilarity(query_tfidf_corpus) 
# query_lsi_model = gensim.models.LsiModel(query_tfidf_corpus, id2word=dictionary, num_topics=100) 
# query_lsi_index = gensim.similarities.MatrixSimilarity(query_lsi_corpus) 
processed_query = preprocessing("What is the function of money?")
query_BoW = dictionary.doc2bow(processed_query[0])