from gensim.models import Word2Vec

# First ConfigA will be converted into binary format.
modelA = Word2Vec.load("output_configA/word2vec_model")
modelA.wv.save_word2vec_format("output_configA/vectors.txt", binary=False)
modelA.wv.save_word2vec_format("output_configA/vectors.bin", binary=True)

# And then ConfigB will be converted into binary format.
modelB = Word2Vec.load("output_configB/word2vec_model")
modelB.wv.save_word2vec_format("output_configB/vectors.txt", binary=False)
modelB.wv.save_word2vec_format("output_configB/vectors.bin", binary=True)

print(" Vectors exported in both formats for Config A and Config B.")
