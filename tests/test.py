# lab08 tests


# IMPORTS

import labs.lab08 as lab
import re, inspect, sys, git
from io import StringIO 


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

# concept 1

def test_divisible_by_k():
    print("\n\ndivisible_by_k(10, 2) prints:")
    with Capturing() as divisible_by_k_10_2_output:
        lab.divisible_by_k(10, 2)
    divisible_by_k_10_2 = ["2", "4", "6", "8", "10"]
    if divisible_by_k_10_2 != divisible_by_k_10_2_output:
        print_error("Incorrect prints from divisible_by_k(10, 2)")
        assert divisible_by_k_10_2 == divisible_by_k_10_2_output
    assert lab.divisible_by_k(10, 2) == 5
        

    with Capturing() as divisible_by_k_6_7_output:
        lab.divisible_by_k(6, 7)
    divisible_by_k_6_7 = []
    if divisible_by_k_6_7 != divisible_by_k_6_7_output:
        print_error("Incorrect prints from divisible_by_k(6, 7)")
        assert divisible_by_k_6_7 == divisible_by_k_6_7_output
    assert lab.divisible_by_k(6, 7) == 0


def test_ordered_digits():
    assert lab.ordered_digits(5)
    assert lab.ordered_digits(11)
    assert lab.ordered_digits(127)
    assert lab.ordered_digits(1357)
    result = lab.ordered_digits(21)
    assert not result
    if result is not None:
        print_error("Print, don't return.")
        assert result is None


def test_get_k_run_starter():
    assert lab.get_k_run_starter(123444345, 0) == 3
    assert lab.get_k_run_starter(123444345, 1) == 4
    assert lab.get_k_run_starter(123444345, 2) == 4
    assert lab.get_k_run_starter(123444345, 3) == 1
    assert lab.get_k_run_starter(123412341234, 1) == 1
    assert lab.get_k_run_starter(1234234534564567, 0) == 4
    assert lab.get_k_run_starter(1234234534564567, 1) == 3
    assert lab.get_k_run_starter(1234234534564567, 2) == 2


# concept 2

def test_multiple():
    assert lab.multiple(3, 4) == 12
    assert lab.multiple(14, 21) == 42


def test_mul_by_num():
    x = lab.mul_by_num(5)
    y = lab.mul_by_num(2)
    assert x(3) == 15
    assert y(-4) == -8 


def test_mod_maker():
    mod = lab.mod_maker()
    assert mod(7, 2) == 1
    assert mod(4, 8) == 4
    assert mod(8,4)


def test_add_result():
    identity = lambda x: x      
    square = lambda x: x**2
    a1 = lab.add_results(identity, square)
    assert a1(4) == 20
    a2 = lab.add_results(a1, identity)
    assert a2(4) == 24
    assert a2(5) == 35
    a3 = lab.add_results(a1, a2)
    assert a3(4) == 44    


# reference functions for make_repeater & apply_twice

square, identity, triple, increment = lambda x: x * x, lambda x: x, lambda x: 3 * x, lambda x: x + 1

def test_make_repeater():
    add_three = lab.make_repeater(increment, 3)
    assert add_three(5) == 8    
    assert lab.make_repeater(triple, 5)(1) == 243
    assert lab.make_repeater(square, 2)(5) == 625
    assert lab.make_repeater(square, 4)(5) == 152587890625
    assert lab.make_repeater(square, 0)(5) == 5


def test_apply_twice():
    assert lab.apply_twice(square)(2) == 16


def test_div_by_primes_under():
    assert not lab.div_by_primes_under(10)(11)
    assert not lab.div_by_primes_under(10)(121)
    assert lab.div_by_primes_under(10)(12)
    assert not lab.div_by_primes_under(5)(1)


def test_no_lambda_div_by_primes_under():
    assert not lab.div_by_primes_under(10)(11)
    assert not lab.div_by_primes_under(10)(121)
    assert lab.div_by_primes_under(10)(12)
    assert not lab.div_by_primes_under(5)(1)


# concept 3

def test_count_stair_ways():
    assert lab.count_stair_ways(4) == 5


def test_count_k():
    assert lab.count_k(3, 3) == 4
    assert lab.count_k(4, 4) == 8
    assert lab.count_k(10, 3) == 274
    assert lab.count_k(300, 1) == 1


def test_insert_into_all():
    nl = [[], [1, 2], [3]]
    assert lab.insert_into_all(0, nl) == [[0], [0, 1, 2], [0, 3]]


def test_subseqs():
    seqs = lab.subseqs([1, 2, 3])
    assert sorted(seqs) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    assert lab.subseqs([]) == [[]]


def test_non_decrease_subseqs():
    seqs = lab.non_decrease_subseqs([1, 3, 2])
    assert sorted(seqs) == [[], [1], [1, 2], [1, 3], [2], [3]]
    assert lab.non_decrease_subseqs([]) == [[]]
    seqs2 = lab.non_decrease_subseqs([1, 1, 2])
    assert sorted(seqs2) == [[], [1], [1], [1, 1], [1, 1, 2], [1, 2], [1, 2], [2]]


def test_num_trees():
    assert lab.num_trees(1) == 1
    assert lab.num_trees(2) == 1
    assert lab.num_trees(3) == 2
    assert lab.num_trees(8) == 429  


# concept 4

def test_add_this_many():
    s = [1, 2, 4, 2, 1]
    lab.add_this_many(1, 5, s)
    assert s == [1, 2, 4, 2, 1, 5, 5]
    lab.dd_this_many(2, 2, s)
    assert s == [1, 2, 4, 2, 1, 5, 5, 2, 2] 


def test_partial_reverse():
    a = [1, 2, 3, 4, 5, 6, 7]
    lab.partial_reverse(a, 2)
    assert a == [1, 2, 7, 6, 5, 4, 3]
    lab.partial_reverse(a, 5)
    assert a == [1, 2, 7, 6, 5, 3, 4]


def test_index_largest():
    assert lab.index_largest([8, 5, 7, 3 ,1]) == 0
    assert lab.index_largest((4, 3, 7, 2, 1)) == 2


def test_pizza_sort():
    a = [8, 5, 7, 3, 1, 9, 2]
    lab.pizza_sort(a)
    assert a == [9, 8, 7, 5, 3, 2, 1]


def test_trade():
    a = [1, 1, 3, 2, 1, 1, 4]
    b = [4, 3, 2, 7]
    with Capturing() as trade_1_output:
        lab.trade(a, b)
    if trade_1_output != "Deal!":
        print_error("Incorrect prints from trade([1, 1, 3, 2, 1, 1, 4], [4, 3, 2, 7])")
        assert trade_1_output == "Deal!"
    assert a == [4, 3, 1, 1, 4]
    assert b == [1, 1, 3, 2, 2, 7]

    c = [3, 3, 2, 4, 1]
    with Capturing() as trade_2_output:
        lab.trade(b, c)
    if trade_2_output != "No deal!":
        print_error("Incorrect prints from trade([1, 1, 3, 2, 2, 7], [3, 3, 2, 4, 1])")
        assert trade_1_output == "No deal!"
    assert b == [1, 1, 3, 2, 2, 7]
    assert c == [3, 3, 2, 4, 1]

    with Capturing() as trade_3_output:
        lab.trade(a, c)
    if trade_3_output != "Deal!":
        print_error("Incorrect prints from trade([4, 3, 1, 1, 4], [3, 3, 2, 4, 1])")
        assert trade_3_output == "Deal!"
    assert a == [3, 3, 2, 1, 4]
    assert b == [1, 1, 3, 2, 2, 7]
    assert c == [4, 3, 1, 4, 1]
    
    d = [1, 1]
    e = [2]
    with Capturing() as trade_4_output:
        lab.trade(d, e)
    if trade_4_output != "Deal!":
        print_error("Incorrect prints from trade([1, 1], [2])")
        assert trade_4_output == "Deal!"
    assert d == [2]
    assert e == [1, 1]


def card(n): # used in test_shuffle
    """Return the playing card numeral as a string for a positive n <= 13."""
    assert type(n) == int and n > 0 and n <= 13, "Bad card n"
    specials = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    return specials.get(n, str(n))


def test_shuffle():
    assert lab.shuffle(range(6)) == [0, 3, 1, 4, 2, 5]
    suits = ['H', 'D', 'S', 'C']
    cards = [card(n) + suit for n in range(1,14) for suit in suits]
    assert cards[:12] == ['AH', 'AD', 'AS', 'AC', '2H', '2D', '2S', '2C', '3H', '3D', '3S', '3C']
    assert cards[26:30] == ['7S', '7C', '8H', '8D']
    assert lab.shuffle(cards)[:12] == ['AH', '7S', 'AD', '7C', 'AS', '8H', 'AC', '8D', '2H', '8S', '2D', '8C']
    assert lab.shuffle(lab.shuffle(cards))[:12] == ['AH', '4D', '7S', '10C', 'AD', '4S', '7C', 'JH', 'AS', '4C', '8H', 'JD']
    assert lab.cards[:12] == ['AH', 'AD', 'AS', 'AC', '2H', '2D', '2S', '2C', '3H', '3D', '3S', '3C']


# concept 5

def test_player():
    p1 = lab.Player('Hill')
    p2 = lab.Player('Don')
    assert p1.popularity == 100
    p1.debate(p2)  
    assert p1.popularity == 150
    assert p2.popularity == 100
    assert p2.votes == 0
    p2.speech(p1)
    assert p2.votes == 10
    assert p2.popularity == 110
    assert p1.popularity == 135 
    p1.speech(p2)
    assert p1.votes ==13
    assert p1.popularity == 148
    assert p2.votes == 10
    assert p2.popularity == 99
    for _ in range(4):
        p1.debate(p2)
    p2.debate(p1)
    assert p2.popularity == 49
    p2.debate(p1)
    assert p2.popularity == 0


def test_game():
    p1, p2 = lab.Player('Hill'), lab.Player('Don')
    g = lab.Game(p1, p2)
    winner = g.play()
    assert p1 is winner
    assert winner is g.winner()
    assert g.turn == 10
    p1.votes = p2.votes
    assert g.winner is None


def test_aggresive_player():
    p1, p2 = lab.AggressivePlayer('Don'), lab.Player('Hill')
    g = lab.Game(p1, p2)
    winner = g.play()
    assert p1 is winner
    p1.popularity = p2.popularity
    assert p1.choose(p2) == p1.debate
    p1.popularity += 1
    assert not p1.choose(p2) == p1.debate
    assert p2.choose(p1) == p2.speech


def test_cautious_player():
    p1, p2 = lab.CautiousPlayer('Hill'), lab.AggressivePlayer('Don')
    p1.popularity = 0
    assert p1.choose(p2) == p1.debate
    p1.popularity = 1
    assert not p1.choose(p2) == p1.debate
    assert p2.choose(p1) == p2.speech


def test_person():
    steven = lab.Person("Steven")
    assert steven.repeat() == 'I squirreled it away before it could catch on fire.'
    assert steven.say("Hello") == 'Hello'
    assert steven.repeat() == 'Hello'
    assert steven.greet() == 'Hello, my name is Steven'
    assert steven.repeat() == 'Hello, my name is Steven'
    assert steven.ask("preserve abstraction barriers") == 'Would you please preserve abstraction barriers'
    assert steven.repeat() == 'Would you please preserve abstraction barriers'


def test_round():
    g = lab.CucumberGame()
    g.play_round(3, [(3, 4), (0, 8), (1, 8), (2, 5)])
    assert g.winners == [1]

    with Capturing() as play_round_1_output:
        g.play_round(1, [(3, 5), (1, 4), (2, 5), (0, 8), (3, 7), (0, 6), (1, 7)])
    play_round_1 = ["It is not your turn, player 3", "It is not your turn, player 0", "The round is over, player 1"]
    if play_round_1 != play_round_1_output:
        print_error("Incorrect prints from g.play_round(1, [(3, 5), (1, 4), (2, 5), (0, 8), (3, 7), (0, 6), (1, 7)]).")
        assert play_round_1 == play_round_1_output
    assert g.winners == [1, 3]

    with Capturing() as play_round_2_output:
        g.play_round(3, [(3, 7), (2, 5), (0, 9)])
    play_round_2 = "It is not your turn, player 2"
    if play_round_2 != play_round_2_output:
        print_error("Inccorect prints from g.play_round(3, [(3, 7), (2, 5), (0, 9)]).")
        assert play_round_2 == play_round_2_output
    assert g.winners == [1, 3]


# concept 6

def test_two_list():
    a = [1, 3]
    b = [1, 1]
    c = lab.two_list(a, b)
    assert repr(c) == "Link(1, Link(3))"
    a = [1, 3, 2]
    b = [2, 2, 1]
    c = lab.two_list(a, b)
    assert repr(c) == "Link(1, Link(1, Link(3, Link(3, Link(2)))))"


def test_convert_link():
    link = lab.Link(1, lab.Link(2, lab.Link(3, lab.Link(4))))
    assert lab.convert_link(link) == [1, 2, 3, 4]
    assert lab.convert_link(lab.Link.empty) == []


def test_multiply_lnks():
    a = lab.Link(2, lab.Link(3, lab.Link(5)))
    b = lab.Link(6, lab.Link(4, lab.Link(2)))
    c = lab.Link(4, lab.Link(1, lab.Link(0, lab.Link(2))))
    p = lab.multiply_lnks([a, b, c])
    assert p.first == 48
    assert p.rest.first == 12
    assert p.rest.rest.rest is lab.Link.empty


def test_flip_two():
    one_lnk = lab.Link(1)
    lab.flip_two(one_lnk)
    assert repr(one_lnk) = "Link(1)"
    lnk = lab.Link(1, lab.Link(2, lab.Link(3, lab.Link(4, lab.Link(5)))))
    lab.flip_two(lnk)
    assert repr(lnk) = "Link(2, Link(1, Link(4, Link(3, Link(5)))))"


def test_deep_len():
    assert lab.deep_len(lab.Link(1, lab.Link(2, lab.Link(3)))) == 3
    assert lab.deep_len(lab.Link(lab.Link(1, lab.Link(2)), lab.Link(3, lab.Link(4)))) == 4
    levels = lab.Link(lab.Link(lab.Link(1, lab.Link(2)), lab.Link(3)), lab.Link(lab.Link(4), lab.Link(5)))
    assert str(levels) == "<<<1 2> 3> <4> 5>"
    assert lab.deep_len(levels) == 5


def test_make_to_string():
    kevins_to_string = lab.make_to_string("[", "|-]-->", "", "[]")
    jerrys_to_string = lab.make_to_string("(", " . ", ")", "()")
    lst = lab.Link(1, lab.Link(2, lab.Link(3, lab.Link(4))))
    assert kevins_to_string(lst) == '[1|-]-->[2|-]-->[3|-]-->[4|-]-->[]'
    assert kevins_to_string(lab.Link.empty) == '[]'
    assert jerrys_to_string(lst) == '(1 . (2 . (3 . (4 . ()))))'
    assert jerrys_to_string(lab.Link.empty) == '()' 


# concept 7

def test_sum_tree():
    t = lab.Tree(4, [lab.Tree(2, [lab.Tree(3)]), lab.Tree(6)])
    assert lab.sum_tree(t) == 15


def test_sprout_leaves():
    t1 = lab.Tree(1, [lab.Tree(2), lab.Tree(3)])
    new1 = lab.sprout_leaves(t1, [4, 5])
    assert repr(new1) == "Tree(1, [Tree(2, [Tree(4), Tree(5)]), Tree(3, [Tree(4), Tree(5)])])"
    t2 = lab.Tree(1, [lab.Tree(2, [lab.Tree(3)])])
    new2 = lab.sprout_leaves(t2, [6, 1, 2])
    assert repr(new2) == "Tree(1, [Tree(2, [Tree(3, [Tree(6), Tree(1), Tree(2)])])])"


def test_hailstone_tree():
    assert repr(lab.hailstone_tree(1, 0)) == "Tree(1)"
    assert repr(lab.hailstone_tree(1, 4)) == "Tree(1, [Tree(2, [Tree(4, [Tree(8, [Tree(16)])])])])"
    assert repr(lab.hailstone_tree(8, 3)) == "Tree(8, [Tree(16, [Tree(32, [Tree(64)]), Tree(5, [Tree(10)])])])"


def test_find_paths():
    tree_ex = lab.Tree(2, [lab.Tree(7, [lab.Tree(3), lab.Tree(6, [lab.Tree(5), lab.Tree(11)])]), lab.Tree(1, [lab.Tree(5)])])
    assert lab.find_paths(tree_ex, 5) == [[2, 7, 6, 5], [2, 1, 5]]
    assert lab.find_paths(tree_ex, 12) == []


def test_make_even():
    t = lab.Tree(1, [lab.Tree(2, [lab.Tree(3)]), lab.Tree(4), lab.Tree(5)])
    lab.make_even(t)
    assert t.label == 2
    assert t.branches[0].branches[0].label == 4  


def test_is_bst():
    t1 = lab.Tree(6, [lab.Tree(2, [lab.Tree(1), lab.Tree(4)]), lab.Tree(7, [lab.Tree(7), lab.Tree(8)])])
    assert lab.is_bst(t1)
    t2 = lab.Tree(8, [lab.Tree(2, [lab.Tree(9), lab.Tree(1)]), lab.Tree(3, [lab.Tree(6)]), lab.Tree(5)])
    assert not lab.is_bst(t2)
    t3 = lab.Tree(6, [lab.Tree(2, [lab.Tree(4), lab.Tree(1)]), lab.Tree(7, [lab.Tree(7), lab.Tree(8)])])
    assert not lab.is_bst(t3)
    t4 = lab.Tree(1, [lab.Tree(2, [lab.Tree(3, [lab.Tree(4)])])])
    assert lab.is_bst(t4)
    t5 = lab.Tree(1, [lab.Tree(0, [lab.Tree(-1, [lab.Tree(-2)])])])
    assert lab.is_bst(t5)
    t6 = lab.Tree(1, [lab.Tree(4, [lab.Tree(2, [lab.Tree(3)])])])
    assert lab.is_bst(t6)
    t7 = lab.Tree(2, [lab.Tree(1, [lab.Tree(5)]), lab.Tree(4)])
    assert not lab.is_bst(t7)


def test_reverse_other():
    t = lab.Tree(1, [lab.Tree(2), lab.Tree(3), lab.Tree(4)])
    lab.reverse_other(t)
    assert repr(t) == "Tree(1, [Tree(4), Tree(3), Tree(2)])"
    t = lab.Tree(1, [lab.Tree(2, [lab.Tree(3, [lab.Tree(4), lab.Tree(5)]), lab.Tree(6, [lab.Tree(7)])]), lab.Tree(8)])
    lab.reverse_other(t)
    assert repr(t) == "Tree(1, [Tree(8, [Tree(3, [Tree(5), Tree(4)]), Tree(6, [Tree(7)])]), Tree(2)])"


user = []

def test_commit():
    try:
        # IF CHANGES ARE MADE, COMMIT TO GITHUB
        user.append(input("\n\nWhat is your GitHub username (exact match, case sensitive)?\n"))
        repo = git.Repo("/workspaces/lab08-" + user[0])
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