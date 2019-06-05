"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
URL：http://www.codeskulptor.org/#user43_Tl6UdGPLB6_2.py
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    new_hand = list(hand)
    score_dict = {}
    for num in new_hand:
        score_dict[num] = new_hand.count(num)
    temp = []
    for key, value in score_dict.items():
        temp.append(key * value)
        
    return max(temp)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    total_score = 0.0
    free_dice_sequence = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)# a set of tuples
    for seq in free_dice_sequence:        
        hand = list(held_dice) + list(seq) 
        total_score += score(hand)
    expected_score = total_score / len(free_dice_sequence)
    return expected_score


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    holds = [()]
    for num in hand:
        for subset in holds:
            holds = holds + [tuple(subset) + (num,)]
    return set(holds)
                

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hold_value_dic = {}
    value_list = []
    hand_holds = gen_all_holds(hand)
    for hold in hand_holds:
        value = expected_value(hold, num_die_sides, (len(hand) - len(hold))) 
        value_list.append(value)
        hold_value_dic[value] = hold
    
    return (max(value_list), hold_value_dic[max(value_list)])


#def run_example():
#    """
#    Compute the dice to hold and expected score for an example hand
#    """
#    num_die_sides = 6
#    hand1 = ( 2, 3)
#    hand2 = ( 5, 6)
#    hand_score, hold = strategy(hand1, num_die_sides)
#    print "Best strategy for hand", hand1, "is to hold", hold, "with expected score", hand_score
#    print score(hand1)
#    print score(hand2)
##    print score(hand3)
##    print score(hand4)
##    print score(hand5)
#   
#    print gen_all_sequences(range(1, 7), 3 )
#    for roll in gen_all_sequences(range(1, 7), 3 ):
#        print score(roll)
#       
#    print len(gen_all_sequences(range(1, 7), 3 ))
#    print expected_value((1,2), 6, 2)
#    print expected_value((5,), 5, 2)
#    
#    print gen_all_holds([1, 2])
#    print gen_all_holds([1, 2, 3])
#    print strategy((1,2), 6)
#    
#run_example()
    
