# The Prisoners and the Boxes, or "Names and Boxes"

-----------------------

This script will run trials of the "Names and Boxes" problem listed here on Peter Winkler's website in his article "Seven Puzzles You Think You Must Not Have Heard Correctly":  [https://www.math.dartmouth.edu/~pw/solutions.pdf](https://www.math.dartmouth.edu/~pw/solutions.pdf)

There are some additional options that you can pass to the script, maybe one or two are interesting but most are not really helpful.  Use --help to get a full list of options available.


## The Puzzle

The Warden has offered a deal to 100 prisoners.  He has placed their names in 100 separate boxes, and he has placed the boxes in a separate room.  The prisoners will be let into the room, one at a time, and will be permitted to open up to fifty boxes each.  If the prisoner does not find his name in any of those fifty boxes, *all* of the prisoners are executed.  But if each prisoner find his name in a box, they all go free!

The prisoners may not communicate after entering the room.  The only thing they may do is come up with a strategy beforehand.

Some warden, huh?  There is a 50% chance that a prisoner will find his name in one of the fifty boxes that he opens.  And for 100 prisoners to do this in a row... it would be like flipping a coin 100 times and getting 100 heads.  The chances of that happening are 1/2^100, which unbelievably unlikely.

The Warden has already decided he is going to place the names in the boxes randomly.  And he *will* allow the prisoners to come up with a strategy beforehand.  After all, he is pretty confident that he is going to execute 100 prisoners tonight, regardless of what happens!

Some strategy may be necessary, I suppose... why not? For example, if all prisoners open the same fifty boxes each time they go into the room, there is a 0% chance that they will all survive, since they will miss some of the boxes, and each box has a prisoner's name in it.  So if they at least make sure as a group to open all of the boxes, there will be a tiny chance that they will survive, right?

So the prisoners go off to an adjoining room to discuss their strategy.  The Warden looks at his Junior Wardens and they all share an ugly laugh.

Eventually, the prisoners come back and enter the room, one by one.  There are no tricks, no strange interpretations of the rules, no games.  They just stick to their strategy.

The next day, the warden is found in his car, sobbing into a Big Mac, and questioning all of his life choices.  Every prisoner found their name.

How?  Does a strategy exist to dramatically improve the prisoners' chances?


## The Script

I wrote this script to prove the solution to myself... I didn't think I heard it correctly!  If you haven't heard of this puzzle before, please stop and enjoy the puzzle first.

When you think how much the prisoner's chances can be improved by using a simple strategy, one which can defeat The Warden's random placement of names in the boxes, you will be amazed.

-----------------------

When I ran the program for 1000000 trials, this was the response:

    INFO:2014-07-05 01:22:12,346:The trials are over. There were 311418 successes and 688582 failures in 1000000 trials for a 31.1418% success rate.

-----------------------
Just run ./prisonser.py to run one trial.  Use --help to see all the options.  If the warden knew what the prisoners were up to, he could have used --warden=long_cycle
