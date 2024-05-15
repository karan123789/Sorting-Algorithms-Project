from typing import TypeVar, List, Callable


T = TypeVar("T")  # represents generic type


# This is an optional helper function but HIGHLY recommended,  especially for the application problem!
def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
    A helper function that helps do comparison so that it is easier
    when applying it to other functions 

    :param data: List of items to be sorted4
    :param comparator: A function which takes 
    two arguments of type T and returns True 
    when the first argument should be treated as less
    than the second argument.
    :param descending: Perform the sort in descending
    order when this is True. Defaults to False.
    :return: None
    """
    return comparator(first, second) if not descending else comparator(second, first)


def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Given a list of values, sort that 
    list in-place using the selection sort 
    algorithm and the provided comparator

    :param data: List of items to be sorted
    :param comparator: A function which takes 
    two arguments of type T and returns True 
    when the first argument should be treated as less
    than the second argument.
    :param descending: Perform the sort in descending
    order when this is True. Defaults to False.
    :return: None
    """
    for i in range(len(data)):
        index_to_swap = i
        for j in range(i + 1, len(data)):
            if do_comparison(data[j], data[index_to_swap], comparator, descending):
                index_to_swap = j

        data[i], data[index_to_swap] = data[index_to_swap], data[i]


def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Given a list of values, sort that list
    in-place using the bubble sort algorithm
    and the provided comparator

    :param data: List of items to be sorted
    :param comparator: A function which takes 
    two arguments of type T and returns True 
    when the first argument should be treated as less
    than the second argument.
    :param descending: Perform the sort in descending
    order when this is True. Defaults to False.
    :return: None
    """
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if do_comparison(data[j], data[j + 1], comparator, not descending):
                data[j], data[j + 1] = data[j + 1], data[j]
 
def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Given a list of values, sort that list in-place
    using the insertion sort algorithm and the provided
    comparator,and perform the sort in descending order
    if descending is True.
    
    :param data: List of items to be sorted
    :param comparator: A function which takes 
    two arguments of type T and returns True 
    when the first argument should be treated as less
    than the second argument.
    :param descending: Perform the sort in descending
    order when this is True. Defaults to False.
    :return: None
    """
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and do_comparison(key, data[j], comparator, descending):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key


def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Given a list of values, sort that list using a hybrid sort 
    with the merge sort and insertion sort algorithms and the provided
    comparator, and perform the sort in descending order if descending is True.
    The function should use insertion_sort to sort lists once their size is 
    less than or equal to threshold, and
    otherwise perform a merge sort. DO NOT hardcode the threshold 
    check such as if threshold == {any value}. Hint: Think about what
    should happen for lists with only one item.


    :param data: List of items to be sorted
    :param threshold: Maximum size at which insertion sort
    will be used instead of merge sort.
    :param comparator: A function which takes two arguments of
    type T and returns True when the first argument
    should be treated as less than the second argument.
    :param descending: Perform the sort in descending order
    when this is True. Defaults to False.
    :return: None
    """
    if len(data) <= 1:
        return
    elif len(data) <= threshold:
        insertion_sort(data, comparator=comparator, descending=descending)
    else:
        mid = len(data) // 2
        left = data[:mid]
        right = data[mid:]
        
        hybrid_merge_sort(left, threshold=threshold, comparator=comparator, descending=descending)
        hybrid_merge_sort(right, threshold=threshold, comparator=comparator, descending=descending)
        
        i = j = k = 0
        
        while i < len(left) and j < len(right):
            if do_comparison(left[i], right[j], comparator, descending):
                data[k] = left[i]
                i += 1
            else:
                data[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            data[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            data[k] = right[j]
            j += 1
            k += 1 


def quicksort(data: List[T]) -> None:
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first: int, last: int) -> None:
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)


###########################################################
# DO NOT MODIFY
###########################################################

class Score:
    """
    Class that represents SAT scores
    NOTE: While it is possible to implement Python "magic methods" to prevent the need of a key function,
    this is not allowed for this application problems so students can learn how to create comparators of custom objects.
    Additionally, an individual section score can be outside the range [400, 800] and may not be a multiple of 10
    """

    __slots__ = ['english', 'math']

    def __init__(self, english: int, math: int) -> None:
        """
        Constructor for the Score class
        :param english: Score for the english portion of the exam
        :param math: Score for the math portion of the exam
        :return: None
        """
        self.english = english
        self.math = math

    def __repr__(self) -> str:
        """
        Represent the Score as a string
        :return: representation of the score
        """
        return str(self)

    def __str__(self) -> str:
        """
        Convert the Score to a string
        :return: string representation of the score
        """
        return f'<English: {self.english}, Math: {self.math}>'


###########################################################
# MODIFY BELOW
###########################################################

def merge_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of integers using merge sort algorithm
    :param arr: The list of integers to be sorted
    :return: the sorted list of integers
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    return merge(left_half, right_half)

def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Merges two sorted lists into a single sorted list
    :param left: The left half of the list
    :param right: The right half of the list
    :return: the merged and sorted list
    """
    result = []
    left_idx, right_idx = 0, 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1
    result.extend(left[left_idx:])
    result.extend(right[right_idx:])
    return result

def get_median(data: List[int]) -> float:
    """
    Calculates the median of a list of integers
    :param data: The list of integers
    :return: the median value of the list
    """
    data_length = len(data)
    if data_length == 0:
        return 0
    elif data_length == 1:
        return data[0]
    elif data_length % 2 == 1:
        return data[data_length // 2]
    else:
        mid_index = data_length // 2
        return (data[mid_index - 1] + data[mid_index]) / 2

def better_than_most(scores: List[Score], student_score: Score) -> str:
    """
    A list of scores of every student that is broken into ENglish and Math
    that is sorted according to the rules of the median

    :param scores: A list of Score objects representing the SAT score of every student.
    :param student_score: A Score object representing a student’s SAT score broken into
    two values: English and Math.
    :return: None, Both, English, or Math
    """
    english_scores = [score.english for score in scores]
    math_scores = [score.math for score in scores]

    english_scores = merge_sort(english_scores)
    math_scores = merge_sort(math_scores)

    median_english = get_median(english_scores)
    median_math = get_median(math_scores)

    english_better = student_score.english > median_english
    math_better = student_score.math > median_math

    if english_better and math_better:
        return 'Both'
    elif math_better:
        return 'Math'
    elif english_better:
        return 'English'
    else:
        return 'None'