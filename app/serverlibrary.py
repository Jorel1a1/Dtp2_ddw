
def merge(array: list, p: int, q: int, r: int, byfunc=None) -> None: # 2 sorted subarrays are merged into larger sorted subarray
    nleft = q - p + 1  # number of elements in left array
    nright = r - q     # number of elements in right array
    left_array = array[p:q + 1]  # copy elements to the left array
    right_array = array[q + 1:r + 1]  # copy elements to the right array
    left = 0  # index for left array
    right = 0  # index for right array
    dest = p  # destination index for the merged array

    while left < nleft and right < nright: # while there are elements  in the left and right array
        if byfunc is None: # if byfunc not provided, compare just on numeric value
            # Compare based on the value itself
            if left_array[left] <= right_array[right]:
                array[dest] = left_array[left]
                left += 1
            else:
                array[dest] = right_array[right]
                right += 1
        else:
            # Compare based on the value returned by the byfunc
            if byfunc(left_array[left]) <= byfunc(right_array[right]): # byfunc(left_array[left]) will be called on a User object in left array
                array[dest] = left_array[left]                         #calling byfunc will return the username of the user object
                left += 1                                              #comparison is based on username e.g "Alice" <= "Bob" alphabetically!
            else:                                                      #left_array[left] (User object) is assigned to parameter item 
                array[dest] = right_array[right]
                right += 1
        dest += 1

    # Handle remaining elements
    while left < nleft:
        array[dest] = left_array[left]
        left += 1
        dest += 1
    while right < nright:
        array[dest] = right_array[right]
        right += 1
        dest += 1



def mergesort(array: list, byfunc=None) -> list: #byfunc is a keyfunction to determine how elements should be compared, used in users route for alphebetical sorting and hall of fame route
    if len(array) <= 1:
        return array  # Base case: an array of 0 or 1 element is already sorted

    # Helper function for recursive sorting
    def sort_helper(array: list, p: int, r: int) -> None:
        if p < r:
            q = (p + r) // 2  # Find the midpoint
            sort_helper(array, p, q)  # Sort the left half
            sort_helper(array, q + 1, r)  # Sort the right half
            merge(array, p, q, r, byfunc)  # Merge the sorted halves after sorting both halves

    sort_helper(array, 0, len(array) - 1) #begins the sorting process by invoking the recursive helper
    return array #returns the sorted array to the caller


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self.items) == 0







