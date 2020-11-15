import math
import random
import time

# Implementation of binary search algorithm!

# Essence of binary search:
# If you have a sorted list and you want to search this array for something,
# You could go through each item in the list and ask, is this equal to what we're looking for?
# But we can make this *faster* by leveraging the fact that our array is sorted!
# Binary search ~ O(log(n)), naive search ~ O(n)

# In these two examples, l is a list in ascending order, and target is something that we're looking for
# Return -1 if not found

def naive_search(l, target):
    # in the naive method, we'll scan the entire list and ask if it's equal to target
    # if so, let's return the index
    # if target not in list l, then return None
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1

def binary_search(l, target, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1

    if high < low:
        return -1
    # use divide and conquer to leverage the fact that our list is sorted!
    midpoint = (low + high) // 2

    # we'll check if l[midpoint] == target, and if not, we can find out if
    # target will be to the left or right of midpoint
    # we know everything to the left of midpoint is smaller than the midpoint
    # and everything to the right is larger
    if l[midpoint] == target:
        return midpoint
    elif target < l[midpoint]:
        return binary_search(l, target, low, midpoint - 1)
    else:
        return binary_search(l, target, midpoint + 1, high)

if __name__ == '__main__':
    # l = [1, 3, 7, 10, 235, 236, 11643, 239509234]
    # for target in l:
    #     print(binary_search(l, target))

    length = 10000
    # length = 5
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3*length, 3*length))
    sorted_list = sorted(list(sorted_list))
    print("Got list!")

    start = time.time()
    for target in sorted_list:
        naive_search(sorted_list, target)
    end = time.time()
    print("Naive search time: ", end-start)

    start = time.time()
    for target in sorted_list:
        binary_search(sorted_list, target)
    end = time.time()
    print("Binary search time: ", end-start)


