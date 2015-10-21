import random
import nltk
import sys
global mapping

mapping = {}
tokens = []

# Go through our graph and assign edges a probability
def normalize_chain():
    for word in mapping:
        # find the total number of times that the word occurs in the text
        total = 0
        for word2 in mapping[word].keys():
            total += mapping[word][word2]

        # get the percent the 2nd word follows the first
        for word2 in mapping[word].keys():
            mapping[word][word2] = mapping[word][word2]/float(total);


# Generate psuedo-random numbers to create a new sentence based on our chain
# Note, returns a list of words
def build_sentence():
    global tokens

    """ 
    Get a starting word that's capitalized (we've lowercased all words
    that don't start sentences) and is also not punctuation
    
    Forcing the first word to be "The" yields some intersting results
    i.e:
        first_word = "The" 
    """
    first_word = "."
    while (first_word.islower() or first_word == "." or first_word == "?" or first_word == "!"):
        first_word = tokens[random.randint(0, len(tokens)-1)]
    
    # Add it to our sentence
    chain = [first_word]

    # Keep adding words until we reach a terminator
    while True:
        rand_num = random.random()
        target = 0
        for word2 in mapping[chain[-1]].keys():
            target += mapping[chain[-1]][word2]
            if target >= rand_num:
                # This is the word we "rolled"
                chain.append(word2)

                # If the sentence terminated, or no words 
                # have followed this one, return
                if (word2 == "." or word2 == "?" or word2 == "!" or
                                                not word2 in mapping.keys()):
                    return chain;

                # Go on to the next word
                break

def main():
    print "Building Markov Chain"
    
    """ 
    Replace the brown corpus with other corpora
    or use your own textfile like so:
        f = open(filename)
        t = f.read()
    """

    from nltk.corpus import brown
    t = brown.words()
    global tokens
    tokens = [w for w in (t)
                        if w.isalpha() 
                        or w == "." 
                        or w == "!" 
                        or w == "?"]

    # Do a bigram-based frequency analysis to begin constructing a Markov Chain
    for i in xrange(len(tokens)-1):
        w1 = tokens[i];
        w2 = tokens[i+1]; 
        
        # Lowercase words that aren't starting sentences
        # E.g. "I", "Russia", "Smith", etc.
        if w2[0].isupper() and w1 != '.':
            tokens[i+1] = w2 = tokens[i+1].lower() 

        if w1 in mapping:
            if w2 in mapping[w1]:
                mapping[w1][w2] += 1
            else:
                mapping[w1][w2] = 1
        else:
            mapping[w1] = {w2: 1}
    normalize_chain()

    print "Press <return> to generate a new sentence, or 'q' to quit"
    while (raw_input() != 'q'):
        # Build our sentence from the Markov Chain
        sentence = "".join([word+" " for word in build_sentence()])
        # Get rid of the whitespace surrounding the ending punctuation mark
        sentence = (sentence[:-3] + sentence[-2])
        print sentence

if __name__ == "__main__":
    main()

