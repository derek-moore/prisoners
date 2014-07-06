#!/usr/bin/env python

"""
This script runs the prisoner names in boxes problem.  The warden of a prison
offers this deal to 100 prisoners: he will place the name of each prisoner in a
separate box, and then place all 100 boxes in a different room.  Each
prisoner will go into the room, one at a time, and start opening boxes.  The
prisoner can only open up to fifty boxes.  If the prisoner does not find their
name after opening fifty boxes, *all* the prisoners are executed.  But if
every prisoner finds their name, they all go free.  Is there a strategy that
the prisoners can use to improve their chances for survival?

"""

import argparse
import logging
import random
import sys


def main():
    """
    Parses arguments, then runs trial() at least once, or --trials=N number of
    times.
    """
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        epilog='It has been proven that if the warden places the names in the '
               'boxes randomly, the best strategy the prisoners can follow is '
               'the "follow" strategy (with a success rate at '
               '31.1827820689805%).  The method that the prisoners use to '
               'associate themselves with the boxes does not matter. ')
    parser.add_argument('-t', '--trials', nargs=1, type=int,
                        help='The number of trials to run.')
    parser.add_argument('-l', '--logging', nargs=1, type=str,
                        help='Sets the logging level, valid values are info '
                             '(default), or debug.')
    parser.add_argument('-p', '--prisoners', nargs=1, type=int,
                        help='The number of prisoners (default is 100).')
    parser.add_argument('-b', '--boxes', nargs=1, type=int,
                        help='The number of boxes the prisoners are allowed to '
                             'open (default is 50).')
    parser.add_argument(
        '-g', '--labelling', nargs=1, type=str,
        help='The way the prisoners decide to associate themselves with the '
             'boxes.  Allowable values are order, reverse, and random.  Order '
             'is the default (and it is faster).  The labelling scheme they '
             'choose is usually irrelevant anyway.')
    parser.add_argument(
        '-w', '--warden', nargs=1, type=str,
        help='The way the warden decides to place the papers in the boxes.  '
             'Allowable values are order, reverse, random, and long_cycle.  '
             'Random is the default, long_cycle can beat the "follow" '
             'strategy.')
    parser.add_argument(
        '-s', '--strategy', nargs=1, type=str,
        help='The strategy the prisoners use to open the boxes.  Allowable '
             'values are follow, random, and half_and_half.  "Follow" is the '
             'default, and is the provably best strategy if the warden places '
             'the papers in the boxes in a random fashion.')
    args = parser.parse_args()

    log_level = args.logging[0].upper() if args.logging else 'INFO'
    if log_level not in ('INFO', 'DEBUG'):
        parser.print_help()
        return
    else:
        logging.basicConfig(level=getattr(logging, log_level),
                            format='%(levelname)s:%(asctime)s:%(message)s')

    prisoner_labelling = \
        args.labelling[0].lower() if args.labelling else 'order'
    if prisoner_labelling not in ('order', 'random', 'reverse'):
        parser.print_help()
        return

    warden_strategy = args.warden[0].lower() if args.warden else 'random'
    if warden_strategy not in ('order', 'random', 'reverse', 'long_cycle'):
        parser.print_help()
        return

    prisoner_strategy = args.strategy[0].lower() if args.strategy else 'follow'
    if prisoner_strategy not in ('follow', 'random', 'half_and_half'):
        parser.print_help()
        return
    else:
        prisoner_function = \
            getattr(sys.modules[__name__], 'strategy_' + prisoner_strategy)

    num_prisoners = args.prisoners[0] if args.prisoners else 100
    num_boxes_to_open = args.boxes[0] if args.boxes else 50
    num_trials = args.trials[0] if args.trials else 1

    logging.info('The prisoners decide to label themselves using '
                 'the {} method.'.format(prisoner_labelling))
    logging.info('The warden is going to put papers in the boxes according to '
                 'the {} method.'.format(warden_strategy))
    logging.info('The prisoners are going to use the {} '
                 'strategy.'.format(prisoner_strategy))
    logging.info('Starting {} trials with {} prisoners, allowed to '
                 'open {} boxes.'.format(num_trials, num_prisoners,
                                         num_boxes_to_open))

    num_successes = 0
    num_failures = 0
    for trial_num in xrange(1, num_trials + 1):
        logging.debug('Starting trial {}...'.format(trial_num))
        if trial(num_prisoners, num_boxes_to_open, prisoner_labelling,
                 warden_strategy, prisoner_function):
            num_successes += 1
        else:
            num_failures += 1
        logging.debug('Finished trial {}.'.format(trial_num))

    format_msg = {
        'num_successes': num_successes,
        'num_failures': num_failures,
        'num_trials': num_trials,
        'was_were': 'were' if num_successes != 1 else 'was',
        'successes': 'successes' if num_successes != 1 else 'success',
        'failures': 'failures' if num_failures != 1 else 'failure',
        'trials': 'trials' if num_trials != 1 else 'trial',
        'success_rate': (float(num_successes)/float(num_trials))*100.00
    }

    logging.info('The trials are over. There {was_were} {num_successes} '
                 '{successes} and {num_failures} {failures} '
                 'in {num_trials} {trials} for a {success_rate}% '
                 'success rate.'.format(**format_msg))


def trial(num_prisoners, num_boxes_to_open, mapping_type, warden_strategy,
          prisoner_function):
    """
    Runs a single trial... num_prisoners open num_boxes_to_open using
    prisoner_function to chose their next box to hopefully beat warden_strategy.

    """
    logging.debug('Starting trial, {} prisoner(s) will each open {} '
                  'box(es).'.format(num_prisoners, num_boxes_to_open))
    prisoners = create_mapping(mapping_type, num_prisoners)
    boxes = create_mapping(warden_strategy, num_prisoners)

    logging.debug('The prisoners have labelled themselves '
                  'this way: {}'.format(prisoners))
    logging.debug('The warden has placed the papers in the boxes '
                  'this way: {}'.format(boxes))

    for prisoner in prisoners:
        box_number = prisoners[prisoner]
        logging.debug('Prisoner {} is enters the room, and starts with their '
                      'box number: {}.'.format(prisoner, box_number))
        attempts = 0
        boxes_attempted = [box_number]
        while True:
            attempts += 1
            logging.debug('On attempt #{}, prisoner #{} opens box #{} and sees '
                          'a slip of paper with {} on '
                          'it.'.format(attempts, prisoner, box_number,
                                       boxes[box_number]))
            paper = boxes[box_number]
            if prisoner == paper:
                logging.debug('On attempt #{} prisoner #{} found their number '
                              'in box number {}!'.format(attempts, prisoner,
                                                         box_number))
                break
            else:
                logging.debug('Prisoner #{} did not find their number on '
                              'attempt {}.'.format(prisoner, attempts))
                if attempts == num_boxes_to_open:
                    logging.debug('Prisoner {} ran out of chances... '
                                  'All the prisoners are '
                                  'executed!'.format(prisoner))
                    return False
                box_number = prisoner_function(
                    prisoners=prisoners, boxes=boxes, paper=paper,
                    boxes_attempted=boxes_attempted, prisoner=prisoner)
                boxes_attempted.append(box_number)
    return True


def strategy_follow(**kwargs):
    """
    It has been proven that this strategy cannot be improved if the names are
    placed in the boxes in a random way.  In this case, the prisoners look at
    the paper in the box, and then open the box that is associated with the
    prisoner on the paper.

    """
    prisoners = kwargs.get('prisoners')
    paper = kwargs.get('paper')

    return prisoners[paper]


def strategy_random(**kwargs):
    """
    A bad strategy, a prisoner will open boxes randomly, but at least skipping
    boxes they have already opened.

    """
    boxes = kwargs.get('boxes')
    boxes_attempted = kwargs.get('boxes_attempted')
    possible_boxes = set(boxes.keys()).difference(set(boxes_attempted))

    return random.choice(list(possible_boxes))


def strategy_half_and_half(**kwargs):
    """
    A bad strategy, depending on your prisoner number, only open boxes randomly
    in the top or bottom half.

    """
    box_numbers = kwargs.get("boxes").keys()
    prisoner = kwargs.get("prisoner")
    boxes_attempted = kwargs.get("boxes_attempted")
    max_box = max(box_numbers)
    middle = max_box/2
    if prisoner >= middle:
        possible_boxes = [box for box in range(middle, max_box + 1)
                          if box not in boxes_attempted]
    else:
        possible_boxes = [box for box in range(1, middle + 1)
                          if box not in boxes_attempted]

    return random.choice(possible_boxes)


def create_mapping(mapping_type, size):
    """
    Returns a dictionary of 1..N items -> numbers.  This could be
    boxes -> papers, or prisoners -> boxes.  The mapping of items to numbers
    is 1:1.

    long_cycle can defeat the "follow" strategy, since it ensures that there is
    a cycle that is longer than the number of boxes the prisoners are allowed
    to open.

    """

    if mapping_type == 'order':
        return dict(zip(range(1, size + 1), range(1, size + 1)))
    elif mapping_type == 'reverse':
        return dict(zip(range(1, size + 1), range(size, 0, -1)))
    elif mapping_type == 'random':
        random_permutation = range(1, size + 1)
        random.shuffle(random_permutation)
        return dict(zip(range(1, size + 1), random_permutation))
    elif mapping_type == 'long_cycle':
        return dict(zip(range(1, size + 1), range(2, size + 1) + [1]))
    else:
        raise NotImplementedError(
            'Unimplemented mapping: {}'.format(mapping_type))


if __name__ == '__main__':
    main()
