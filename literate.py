import sys
import random

class Node(object):
    def __init__(self, letter, probability = 1):
        self.letter = letter
        self.probability = probability
        self.children = {}
        self.numChildren = 0

class RandomTextGenerator(object):
    ###############################################################
    ###############################################################
    ###############################################################
    ###############################################################
    ##############################WALKING FUNCTION*****************
    ###############################################################
    ###############################################################
    ###############################################################
    '''Create a markov tree based on the text and then generate random text'''
    def __init__(self, input_file_name, K, length):
        self.input_file_name = input_file_name
        self.K = K
        self.length = length
        self.input_file = ''.join(open(input_file_name, 'r').readlines()).upper()
        while '\n' in self.input_file:
            self.input_file = self.input_file.replace('\n', '')
        print ('\n' in self.input_file)
        self.counter = 0
        self.markov = Node('', 1)
        print 'Loaded random text generator with file: \n', len(self.input_file)

    # def add_markov_nodes(self, prefix, n_letter):
    def add_markov_nodes(self, string):
        self.counter += 1
        pointer = self.markov
        for letter in string:
            # if pointer == self.markov:
            #     self.counter += 1
            # Increase number of total words that move through this node
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
        if ' ' in self.markov.children:
           del self.markov.children[' ']

    def get_total(self, node):
        total = 0
        for x in node.children:
            total += node.children[x].probability
        return total

    def get_next_from_node(self, node):
        # assert node.numChildren == self.get_total(node)
        print node.numChildren, '-----------------', self.get_total(node), '*', self.markov.letter, '*'
        if node.numChildren > 0:
            random_index = random.randrange(node.numChildren) + 1
            print 'radom:', random_index
            for letter_key in node.children:
                random_index -= node.children[letter_key].probability
                if (random_index <= 0):
                    return node.children[letter_key]
                print 'index:', random_index
        print 'this happenssssss'
        return None

    def get_next_from_prefix(self, prefix):
        pointer = self.markov
        for p_letter in prefix:
            if p_letter in pointer.children:
                pointer = pointer.children[p_letter]
            else:
                print "this happens"
                return None
        return self.get_next_from_node(pointer)

    def generate_random_txt(self):
        self.generate_markov_tree()
        print '--------------####', self.get_total(self.markov), self.markov.letter, '    ', self.markov.probability
        markov_output = ''
        pointer = self.markov
        print self.markov.children
        prefix = self.get_next_from_node(pointer).letter
        print 'No way'
        while (len(markov_output) < self.length):
            s_next = self.get_next_from_prefix(prefix)
            if (s_next):
                pass
                # markov_output += 'a'
                markov_output += s_next.letter
                prefix += s_next.letter
            else:
                prefix = prefix[1:]

            if (len(prefix) > self.K):
                prefix = prefix[1:]




        # while (len(output) < self.length):
        #     for x in range(self.K):
        #         if pointer.numChildren > 0:
        #             rand = random.randrange(pointer.numChildren) + 1
        #             for letter in pointer.children:
        #                 rand -= pointer.children[letter].probability
        #                 if (rand <= 0):
        #                     pointer = pointer.children[letter]
        #                     output += pointer.letter
        #                     break
        #         else:
        #             pointer = self.markov

        return markov_output

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
    print 'Output generated:', output, '--------', rtg.counter
