import random
import nltk

''' Just a simple class for constructing a bigram-based
    Markov Chain sentence model '''

class WordChain:
    def __init__(self, words):
        print "Building Markov Chain"
        self.tokens = [w for w in (words)
                            if w.isalpha() 
                            or w == "." 
                            or w == "!" 
                            or w == "?"]

        # Do a bigram-based frequency analysis to begin constructing
        # the chain
        self.mapping = {}
        for i in xrange(len(self.tokens)-1):
            w1 = self.tokens[i];
            w2 = self.tokens[i+1]; 
            
            # Lowercase words that aren't starting sentences
            # E.g. "I", "Russia", "Smith", etc.
            if w2[0].isupper() and w1 != '.':
                self.tokens[i+1] = w2 = self.tokens[i+1].lower() 

            if w1 in self.mapping:
                if w2 in self.mapping[w1]:
                    self.mapping[w1][w2] += 1
                else:
                    self.mapping[w1][w2] = 1
            else:
                self.mapping[w1] = {w2: 1}
        self.normalize_chain()

    # Go through our graph and assign edges a probability
    def normalize_chain(self):
        for word in self.mapping:
            # get the total number of times each bigram starting with 
            # 'word' occurs
            total = 0
            for word2 in self.mapping[word].keys():
                total += self.mapping[word][word2]

            # calculate how frequently the 2nd word follows the first
            for word2 in self.mapping[word].keys():
                self.mapping[word][word2] = self.mapping[word][word2]/float(total);


    # Generate psuedo-random numbers to create a new sentence based on our chain
    # Returns a list of words
    def build_sentence(self):
        """ 
        Get a starting word -- i.e one that's capitalized and is also not
        punctuation
       
        e.g. to force a sentence to start with a particular word:
            first_word = "The" 
        """
        first_word = "."
        while (first_word.islower() or first_word == "." or first_word == "?" or first_word == "!"):
            first_word = self.tokens[random.randint(0, len(self.tokens)-1)]
        
        # Add it to our sentence
        chain = first_word

        # Keep adding words until we reach a terminator
        # Note: for better efficency, use a running total 
        # and binary search to find which word was rolled
        while True:
            rand_num = random.random()
            target = 0
            for word2 in self.mapping[chain[-1]].keys():
                target += self.mapping[chain[-1]][word2]
                if target >= rand_num:
                    # This is the word we "rolled"
                    chain += " "+word2

                    # If the sentence terminated, or no words 
                    # have followed this one, return
                    if (word2 == "." or word2 == "?" or word2 == "!" or
                                                    not word2 in self.mapping.keys()):
                        return chain[:-2]+chain[-1];

                    # Go on to the next word
                    break

def main():
    """ 
    Replace the brown corpus with other corpora
    or use your own textfile like so:
        f = open(filename)
        t = f.read()
    """
    from nltk.corpus import twitter_samples 
    words = []
    for sentence in twitter_samples.strings():
        words += nltk.word_tokenize(sentence) + ["."]
    chain = WordChain(words)
    print chain.build_sentence()

if __name__ == "__main__":
    main()
    
    

