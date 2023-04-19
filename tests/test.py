# lab07 tests


# IMPORTS

import labs.lab07 as lab, tests.wwpd_storage as s
import re, inspect, sys, git
from io import StringIO 

st = s.wwpd_storage


# CAPTURING PRINTS (STDOUT) - https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


# COLORED PRINTS - custom text type to terminal: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal, ANSI colors: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

class bcolors:
    HIGH_MAGENTA = '\u001b[45m'
    HIGH_GREEN = '\u001b[42m'
    HIGH_YELLOW = '\u001b[43m'
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


# TESTS

def test_height():
    t = lab.Tree(3, [lab.Tree(5, [lab.Tree(1)]), lab.Tree(2)])
    assert lab.height(t) == 2
    t = lab.Tree(3, [lab.Tree(1), lab.Tree(2, [lab.Tree(5, [lab.Tree(6)]), lab.Tree(1)])])
    assert lab.height(t) == 3


def test_max_path_sum():
    t = lab.Tree(1, [lab.Tree(5, [lab.Tree(1), lab.Tree(3)]), lab.Tree(10)])
    assert lab.max_path_sum(t) == 11


def test_find_path():
    t = lab.Tree(2, [lab.Tree(7, [lab.Tree(3), lab.Tree(6, [lab.Tree(5), lab.Tree(11)])]), lab.Tree(15)])
    assert lab.find_path(t, 5) == [2, 7, 6, 5]
    assert lab.find_path(t, 10) is None
    

def test_prune_small():
    t1 = lab.Tree(6)
    lab.prune_small(t1, 2)
    assert repr(t1) == "Tree(6)"
    t2 = lab.Tree(6, [lab.Tree(3), lab.Tree(4)])
    lab.prune_small(t2, 1)
    assert repr(t2) == "Tree(6, [Tree(3)])"
    t3 = lab.Tree(6, [lab.Tree(1), lab.Tree(3, [lab.Tree(1), lab.Tree(2), lab.Tree(3)]), lab.Tree(5, [lab.Tree(3), lab.Tree(4)])])
    lab.prune_small(t3, 2)
    assert repr(t3) == "Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2)])])"


def test_cumulative_mul():
    t = lab.Tree(1, [lab.Tree(3, [lab.Tree(5)]), lab.Tree(7)])
    lab.cumulative_mul(t)
    assert repr(t) == "Tree(105, [Tree(15, [Tree(5)]), Tree(7)])"
    otherTree = lab.Tree(2, [lab.Tree(1, [lab.Tree(3), lab.Tree(4), lab.Tree(5)]), lab.Tree(6, [lab.Tree(7)])])
    lab.cumulative_mul(otherTree)
    assert repr(otherTree) == "Tree(5040, [Tree(60, [Tree(3), Tree(4), Tree(5)]), Tree(42, [Tree(7)])])"


def test_d_leaves():
    t_one_to_four = lab.Tree(1, [lab.Tree(2), lab.Tree(3, [lab.Tree(4)])])
    lab.d_leaves(t_one_to_four, 5)
    assert repr(t_one_to_four) == "Tree(1, [Tree(2, [Tree(5)]), Tree(3, [Tree(4, [Tree(5), Tree(5)]), Tree(5)])])"
    t1 = lab.Tree(1, [lab.Tree(3)])
    lab.d_leaves(t1, 4)
    assert repr(t1) == "Tree(1, [Tree(3, [Tree(4)])])"
    t2 = lab.Tree(2, [lab.Tree(5), lab.Tree(6)])
    t3 = lab.Tree(3, [t1, lab.Tree(0), t2])
    lab.d_leaves(t3, 10)
    assert repr(t3) == "Tree(3, [Tree(1, [Tree(3, [Tree(4, [Tree(10), Tree(10), Tree(10)]), Tree(10), Tree(10)]), Tree(10)]), Tree(0, [Tree(10)]), Tree(2, [Tree(5, [Tree(10), Tree(10)]), Tree(6, [Tree(10), Tree(10)]), Tree(10)])])"


def test_has_path():
    greetings = lab.Tree('h', [lab.Tree('i'), lab.Tree('e', [lab.Tree('l', [lab.Tree('l', [lab.Tree('o')])]), lab.Tree('y')])])
    assert lab.has_path(greetings, 'h')
    assert not lab.has_path(greetings, 'i')
    assert lab.has_path(greetings, 'hi')
    assert lab.has_path(greetings, 'hello')
    assert lab.has_path(greetings, 'hey')
    assert not lab.has_path(greetings, 'bye')
    assert not lab.has_path(greetings, 'hint')


def test_add_trees():
    numbers = lab.Tree(1, [lab.Tree(2, [lab.Tree(3), lab.Tree(4)]),lab.Tree(5, [lab.Tree(6, [lab.Tree(7)]), lab.Tree(8)])])
    assert repr(lab.add_trees(numbers, numbers)) == "Tree(2, [Tree(4, [Tree(6), Tree(8)]), Tree(10, [Tree(12, [Tree(14)]), Tree(16)])])"
    assert repr(lab.add_trees(lab.Tree(2), lab.Tree(3, [lab.Tree(4), lab.Tree(5)]))) == "Tree(5, [Tree(4), Tree(5)])"
    assert repr(lab.add_trees(lab.Tree(2, [lab.Tree(3)]), lab.Tree(2, [lab.Tree(3), lab.Tree(4)]))) == "Tree(4, [Tree(6), Tree(4)])"
    assert repr(lab.add_trees(lab.Tree(2, [lab.Tree(3, [lab.Tree(4), lab.Tree(5)])]), lab.Tree(2, [lab.Tree(3, [lab.Tree(4)]), lab.Tree(5)]))) == "Tree(4, [Tree(6, [Tree(8), Tree(5)]), Tree(5)])"


# CHECK WWPD? IS ALL COMPLETE

wwpd_complete = True

def test_wwpd():
    if len(st) != 8 or not all([i[4] for i in st]):
        print_error("WWPD? is incomplete.")
        wwpd_complete = False
    assert len(st) == 8
    assert all([i[4] for i in st])


# AUTO-COMMIT WHEN ALL TESTS ARE RAN

user = []

def test_commit():
    try:
        # IF CHANGES ARE MADE, COMMIT TO GITHUB
        user.append(input("\n\nWhat is your GitHub username (exact match, case sensitive)?\n"))
        repo = git.Repo("/workspaces/lab07-" + user[0])
        repo.git.add('--all')
        repo.git.commit('-m', 'update lab')
        origin = repo.remote(name='origin')
        origin.push()
        print_success("Changes successfully committed.")  
    except git.GitCommandError: 
        # IF CHANGES ARE NOT MADE, NO COMMITS TO GITHUB
        print_message("Already up to date. No updates committed.")
    except git.NoSuchPathError:
        # IF GITHUB USERNAME IS NOT FOUND
        print_error("Incorrect GitHub username; try again.")
        raise git.NoSuchPathError("")