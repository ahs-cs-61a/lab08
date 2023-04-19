# lab07 WWPD?


# IMPORTS

import inspect
import tests.wwpd_storage as s

st = s.wwpd_storage 


# COLORED PRINTS - custom text type to terminal: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal, ANSI colors: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

class bcolors:
    HIGH_MAGENTA = '\u001b[45m'
    HIGH_GREEN = '\u001b[42m'
    HIGH_YELLOW = '\u001b[43;1m'
    MAGENTA = ' \u001b[35m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33;1m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\u001b[0m'
    
def print_error(message):
    print("\n" + bcolors.HIGH_YELLOW + bcolors.BOLD + "ERROR:" + bcolors.RESET + bcolors.YELLOW + bcolors.BOLD + " " + message + bcolors.ENDC)

def print_message(message):
    print("\n" + bcolors.HIGH_MAGENTA + bcolors.BOLD + "MESSAGE:" + bcolors.RESET + bcolors.MAGENTA + bcolors.BOLD + " " + message + bcolors.ENDC)

def print_success(message):
    print("\n" + bcolors.HIGH_GREEN + bcolors.BOLD + "SUCCESS:" + bcolors.RESET + bcolors.GREEN + bcolors.BOLD + " " + message + bcolors.ENDC)


# INCORRECT ANSWER LOOP, INSTRUCTIONS, COMPLETE, OPTIONS

def repeat():
    print("Try again:")
    return input()

def intro(name):
    print("\nWhat Would Python Display?: " + name)
    print("Type the expected output, 'function' if you think the answer is a function object, 'infinite loop' if it loops forever, 'nothing' if nothing is displayed, or 'error' if it errors; use single quotes '' when needed.\n")

def complete():
    print_success("All questions for this question set complete.")

def options():
    print_message("All questions for this question set complete. Restart question set?")
    guess = input("Y/N?\n")
    guess = guess.lower()
    while guess != "y" and guess != "n":
        print_error("Unknown input, please try again.")
        guess = input()
    if guess == "y":
        return "restart"
    return False


# WWPD? ALGORITHM 

def wwpd(name, question_set, stored_list):

    intro(name)

    matched = str([i[:-1] for i in question_set])[1:-1] in str([i[:-1] for i in stored_list])
    restart = matched and options() == "restart"
    done = False

    for q in question_set:
        q[4] = True
        if q not in stored_list or restart:
            done = True 
            if q[1]:
                print(q[1])
            if q[2]:
                print(q[2])
            guess = input()
            while guess != q[3]:
                guess = repeat()
            if not matched:
                op = open("tests/wwpd_storage.py", "w")
                for j in range(len(stored_list)):
                    if q[0] < stored_list[j][0]:
                        stored_list.insert(j, q)
                        break
                if q not in stored_list: 
                    stored_list.append(q)
                op.write("wwpd_storage = " + str(stored_list))
                op.close()
    if done:
        complete()


# REFERENCE FUNCTIONS, CLASSES, METHODS, SEQUENCES, ETC.

class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """

    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()
    
    
# lab07: https://inst.eecs.berkeley.edu/~cs61a/su22/disc/disc07/

t = Tree(1, [Tree(2)])
tr = Tree(2, [Tree(2)])
tr.branches.append(Tree(4, [Tree(8)]))


# QUESTION SET - ELEMENT FORMAT: [<QUESTION NUMBER>, <INITIAL PRINTS> (usually empty), <QUESTION>, <ANSWER>]
# INSPECT MODULE - convert function/class body into String: https://docs.python.org/3/library/inspect.html 

trees_qs = [
    [1, "", ">>> t = Tree(1, Tree(2))", "error"],
    [2, ">>> t = Tree(1, [Tree(2)])", ">>> t.label", str(t.label)]
    [3, "", ">>> t.branches[0]", repr(t.branches[0])],
    [4, "", ">>> t.branches[0].label", str(t.branches[0].label)],
    [5, ">>> t.label = t.branches[0].label", "t", "Tree(2, [Tree(2)])"]
    [6, ">>> t.branches.append(Tree(4, [Tree(8)]))", ">>> len(t.branches)", "2"],
    [7, "", ">>> t.branches[0]", repr(tr.branches[0])],
    [8, "", ">>> t.branches[1]", repr(tr.branches[1])]
]
all_qs = [trees_qs]

for set in all_qs:
    for q in set:
        q.append(False)


# WWPD? QUESTIONS

def wwpd_trees():
    wwpd("Linked Lists", trees_qs, st)
