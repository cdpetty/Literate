import sys
import random

class Node(object):
    def __init__(self, letter, probability = 1):
        self.letter = letter
        self.probability = probability
        self.children = {}
        self.numChildren = 0

class RandomTextGenerator(object):
    '''Create a markov tree based on the text and then generate random text'''
    def __init__(self, input_file_name, K, length):
        self.input_file_name = input_file_name
        self.K = K
        self.length = length
        self.input_file = ''.join(open(input_file_name, 'r').readlines()).upper()
        self.markov = Node('', 1)
        # print 'Loaded random text generator with file: \n', self.input_file

    # def add_markov_nodes(self, prefix, n_letter):
    def add_markov_nodes(self, string):
        pointer = self.markov
        for letter in string:
            # Increase number of total words that move through this node
            if letter == '\n':
                break
            else:
                pointer.numChildren += 1
                if letter in pointer.children:
                    # print 'Letter:', letter, 'in children dict'
                    # Move to next node and update its probabilty
                    pointer = pointer.children[letter]
                    pointer.probability += 1
                else:
                    # print 'Letter:', letter, 'not in children dict'
                    pointer.children[letter] = Node(letter, 1)
                    pointer = pointer.children[letter]

        # print 'Ended on letter: ', pointer.letter, 'prob = ', pointer.probability
        self.print_path_for_string(string)

    def generate_markov_tree(self):
        prefix = suffix = ''
        for n_letter_loc in range(len(self.input_file)):
            max_length = n_letter_loc + self.K + 1
            self.add_markov_nodes(self.input_file[n_letter_loc: max_length if max_length < len(self.input_file) else len(self.input_file)])
            # for level in range (1, self.K):

    def generate_random_txt(self):
        self.generate_markov_tree()
        output = ''
        pointer = self.markov
        while (len(output) < self.length):
            for x in range(self.K):
                if pointer.numChildren > 0:
                    rand = random.randrange(pointer.numChildren) + 1
                    for letter in pointer.children:
                        rand -= pointer.children[letter].probability
                        if (rand <= 0):
                            pointer = pointer.children[letter]
                            output += pointer.letter
                            break
                else:
                    pointer = self.markov

        return output

    def print_path_for_string(self, string):
        # print self.markov.numChildren
        pointer = self.markov
        for letter in string:
            if letter == '\n':
                break
            else:
                pointer = pointer.children[letter]

        # print '----------------'
        # print self.markov.children

if __name__=='__main__':
    input_file_name = sys.argv[1]
    K = int(sys.argv[2])
    length = int(sys.argv[3])
    rtg = RandomTextGenerator(input_file_name, K, length)
    output = rtg.generate_random_txt()
    print 'Output generated:', output
