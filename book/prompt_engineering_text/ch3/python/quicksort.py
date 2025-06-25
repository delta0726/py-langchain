def quicksort(alist):
    if len(alist) <= 1:
        return alist
    
    pivot = alist[len(alist) // 2]  # Choose a pivot element (usually the middle)
    left = [x for x in alist if x < pivot]  # Elements less than the pivot
    middle = [x for x in alist if x == pivot]  # Elements equal to the pivot
    right = [x for x in alist if x > pivot]  # Elements greater than the pivot
    
    return quicksort(left) + middle + quicksort(right)

# Example usage:
my_list = [3, 6, 8, 10, 1, 2, 1]
sorted_list = quicksort(my_list)
print(sorted_list)
