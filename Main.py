import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import timeit
import os

import TestCases
import BubbleSort
import InsertionSort
import SelectionSort
import MergeSort
import QuickSort
import RadixSort
import ShellSort
import TreeSort


def calculate_average_time(array_of_times):
    """Takes a array with times samples and calculates the average of them
    
    Parameters:
    array_of_times (np.array): Array containing the samples

    Returns:
    average_time: Time in average the algorithm took in microseconds
    """
    sum_of_times = 0

    for i in range(array_of_times.size):
        sum_of_times += array_of_times[i]

    average_time = int((sum_of_times / array_of_times.size)*1000000)

    return average_time


def test_timing(test_case, sorter, amount_of_tests):
    """Tests a sorter a given amout of times to get a average time
    
    Parameters:
    test_case (np.array): Array used for the tests
    sorter: Sorter used for the tests
    amount_of_tests (int): How many tests will be made to get a average time

    Returns:
    average_time: Time the sorter took in average to complete the task
    """
    tests_made = 0
    test_times = np.array([])

    while (tests_made < amount_of_tests):
        case = np.copy(test_case)
        startTimer = timeit.default_timer()
        sorter(case)
        stopTimer = timeit.default_timer()

        test_times = np.append(test_times, (stopTimer - startTimer))

        tests_made += 1

    average_time = calculate_average_time(test_times)

    return average_time


def test_sorter(test_case, sorter, amout_of_tests):
    """Tests a given sorter
    
    Parameters:
    test_case (array): Test that will be run
    sorter (array): Sorter that will be tested
    amount_of_tests (int): How many tests will be made to get a average time for sorting

    Returns:
    average_time: Average time of the sorter to complete the task on the given test
    comparisons: How many comparisons the sorter made
    swaps: How many comparisons the sorter swaps
    """
    case = np.copy(test_case)  # Makes a copy so one test doest effect the other
    average_time = test_timing(case, sorter[0], amout_of_tests)
    if sorter[1] != None:
        sortedArray, comparisons, swaps = sorter[1](case)
    else:
        comparisons = 0
        swaps = 0
    return average_time, comparisons, swaps


sorters = np.array([[BubbleSort.bubble2_sort, BubbleSort.bubble2_sort_counting],
                    [InsertionSort.insert_sort, InsertionSort.insert_sort_otimizado_counting],
                    [QuickSort.quick_sort, QuickSort.quick_sort_for_counting],
                    [MergeSort.merge_sort, MergeSort.merge_sort_counting],
                    [ShellSort.shellSort, ShellSort.shellSort_counting],
                    [SelectionSort.selectionSort, SelectionSort.selectionSort_counting],
                    [RadixSort.index_sort, None],
                    [TreeSort.tree_sort, TreeSort.tree_sort_counting]])

test_cases = TestCases.test_cases()  # Gets the test cases
amount_of_tests = 250  # Sets the amount of tests to be made on each case

data = {"sorter": [],
        "average time": [],
        "comparisons": [],
        "swaps": []}
cases = [copy.deepcopy(data) for _ in range(len(test_cases))]

print("-" * 25)
for i, test in enumerate(test_cases):
    print(f"\tCase{i+1}:")
    for sorter in sorters:

        print(f"Testing {sorter[0].__name__}...")

        average_time, comparisons, swaps = test_sorter(test, sorter, amount_of_tests)
        
        cases[i]["sorter"].append(sorter[0].__name__)
        cases[i]["average time"].append(average_time)
        cases[i]["comparisons"].append(comparisons)
        cases[i]["swaps"].append(swaps)

    cases[i] = pd.DataFrame(cases[i])
    print("-" * 25)

# Prints the data frames of each case to the termial
print("-" * 50)
for i in range(len(cases)):
    print(f"Case{i+1}:\
          \n{cases[i]}")
    print("-" * 50)

# Opens a window for each test case with their info
for i, case in enumerate(cases):
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    
    axs[0].bar(case["sorter"], case["average time"], color = "y")
    axs[0].set_title(f"Case Test {i+1}")
    axs[0].set_ylabel("Time (microseconds)")
    
    axs[1].bar(case["sorter"], case["comparisons"], color = "b")
    axs[1].set_ylabel("Quantity of Comparisons")

    axs[2].bar(case["sorter"], case["swaps"], color = "g")
    axs[2].set_xlabel("Sorter")
    axs[2].set_ylabel("Quantity of Swaps")
    
    plt.tight_layout()

plt.show()
