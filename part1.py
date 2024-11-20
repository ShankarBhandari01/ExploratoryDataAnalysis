
def calculate_efficiency(task_a, task_b, allocation):
   
    try:
        print('<------Initialisation-------->')
        #  number of resources
        number = len(allocation) 
        print(f'lenght of allocation is {number}')
        if number == 0:
            raise ValueError("allocation list is empty !")  # check if allocation list is empty
        
        primary_time = [0] * number
        secondary_time = [0] * number
        print(f'primarty_time: {primary_time}')
        print(f'secondary_time: {secondary_time}')
        print('\n')
        
        for i in range(number):
            idx = allocation[i]
            print(f'Step: {i+1},idx: {idx}')
            if i == 0:
                print(f'i is 0 than: ')
                print(f'primary_time[{i}] = task_a[{idx}] = {task_a[idx]}')
                primary_time[i] = task_a[idx] # get the value in idx index  of task_a
                print(f'secondary_time[{i}]= (primary_time[{i}]={primary_time[i]}) + (task_b[{idx}] = {task_b[idx]}) = {primary_time[i] + task_b[idx]}')
                secondary_time[i] = primary_time[i] + task_b[idx]  # get the value in idx index  of task_b and do sum  with primary_time[i]
            else:
                print(f'{i} is greater than 0]')
                print(f'primary_time[{i}] = primary_time[{i}-{1}] = {primary_time[i-1]} + task_a = {task_a[idx]}')
                print(f'max value of (secondary_time[{i}-{1}], primary_time[{i}-{1}])= {max( secondary_time[i-1], primary_time[i])}')
                print(f'secondary_time[{i}] = max value + task_b[{idx}] = {max(secondary_time[i-1], primary_time[i]) + task_b[idx]}')
                primary_time[i] = primary_time[i-1] + task_a[idx]
                secondary_time[i] = max(secondary_time[i-1], primary_time[i]) + task_b[idx]
            print('\n')
            print(f'primary_time: {primary_time}')
            print(f'seconday_time: {secondary_time}')
            print('\n')
        print(f'final primary_time: {primary_time}')
        print(f'final secondary_time: {secondary_time}')
        return primary_time, secondary_time
    
    except  ValueError as e: 
        print(e)   # print the error message
        return None, None 


def select_min(tasks, available):
    """
    Select minimun value based on task provided and available value.
    this fucntion will raised  error task list values lengths is equal to  0. 
    it is designed to selected heighest priority task with
    minimum value present in the task list. 
    
    Parameter:
    tasks (list): list of tasks with their values
    available (int): available value to select task
    
    Return:
        int: selected task value
        init:  index of selected task
        
    Raises:
        ValueError: if task list values engths is equal to  0
        
    Behavior:
       - Check if task is available and less than min_value
       - If available, return the task value and index
       - If not available, return None and None
       
    Example:
        >>> task = [4, 9, 3, 8, 7]
        >>> available = [True,True,True,True]
        >>> select_min(task, available)
        (2,2)
    """
    
    try:
        if len(tasks) == 0:
            raise ValueError("Task list is empty !")  # check if task list is empty

        min_value = float('inf')  # Initialize min_value as infinity
        min_index = -1  # Initialize min_index as -1
        for i in range(len(tasks)):
            # Check if task is available and less than min_value
            if available[i] and tasks[i] < min_value:
                min_value = tasks[i]   # Update min_value
                min_index = i   # Update min_index
        return (min_value, min_index)
    except ValueError as e:
        print(e)   # print the error message
        return None, None 


def allocate_resources(priority_task_a, priority_task_b):
    """
    Allocate resources based on two priority lists for a set of tasks.

    This function takes two lists of priorities for the same set of tasks and
    creates a single allocation order that balances both priority schemes.
    It alternates between selecting tasks from each priority list, always
    choosing the highest priority (lowest number) available task.

    Parameters:
    priority_task_a (list of int): The first list of priorities for the tasks.
                              Lower numbers indicate higher priority.
    priority_task_b (list of int): The second list of priorities for the tasks.
                              Lower numbers indicate higher priority.

    Returns:
    list of int: A list of task indices representing the order in which
                 resources should be allocated. The length of this list
                 is equal to the length of the input priority lists.

    Raises:
    ValueError: If the input priority lists have different lengths.

    Behavior:
    - Tasks selected based on priority_task_a are added to the beginning of the result.
    - Tasks selected based on priority_task_b are added to the end of the result.
    - In case of a tie (same priority in both lists), priority_task_a is given precedence.
    - The function prints detailed steps of its execution, showing comparisons
      and decisions made at each step.

    Example:
    >>> priority_task_a = [4, 9, 3, 8, 7]
    >>> priority_task_b = [2, 1, 6, 5, 10]
    >>> allocate_resources(priority_task_a, priority_task_b)
    [2, 0, 1, 4, 3]
    """
    try:
        # Check if the input lists have the same length
        if len(priority_task_a) != len(priority_task_b):
            raise ValueError("Priority lists must have the same length")

        lenght = len(priority_task_a)  # Initialize the result list
        available = [True] * lenght  # Assume all tasks are available initially
        primary_allocation = []  # Store the primary allocation order
        secondary_allocation = []  # Store the secondary allocation order

        print("<--------Initial state:--------->")
        print(f"Priority List A: {priority_task_a}")
        print(f"Priority List B: {priority_task_b}")
        print(f"Available: {available} \n ")

        for step in range(lenght):
            print(f"Step {step + 1}:")

            # Find the task with the lowest priority in priority_task_a
            min_value_a, min_idx_a = select_min(priority_task_a, available)
            # Find the task with the lowest priority in priority_task_b
            min_value_b, min_idx_b = select_min(priority_task_b, available)

            print(f"Minimum value in A: {min_value_a} at index {min_idx_a}")
            print(f"Minimum value in B: {min_value_b} at index {min_idx_b}")

            if min_value_a <= min_value_b:
                print(f"A ({min_value_a}) is smaller than B ({min_value_b})")
                # Add the task with the lowest priority in priority_task_a to the primary allocation
                primary_allocation.append(min_idx_a)
                available[min_idx_a] = False  # Mark the task as unavailable
                print(f"Task {min_idx_a} added to primary allocation")
            else:
                print(f"B ({min_value_b}) is smaller than A ({min_value_a})")
                # Add the task with the lowest priority in priority_task_b to the secondary allocation
                secondary_allocation.insert(0, min_idx_b)
                available[min_idx_b] = False
                print(f"Task {min_idx_b} added to secondary allocation")

            print(f"Updated available: {available}")
            print(f"Current primary allocation: {primary_allocation}")
            print(f"Current secondary allocation: {secondary_allocation}\n")
        # merges the primary and secondary allocations
        final_allocation = primary_allocation + secondary_allocation

        print(f"Final allocation: {final_allocation}")
        print("<---------------End-------------->")
        return final_allocation
    except ValueError as e:
        print(e)   # Print the error message
        return None  # Return None if an error occurs
        

# input priorities list 
priority_task_a = [4, 9, 3, 8, 7]
priority_task_b = [5, 2, 6, 10, 1]
# output of the allication function 
final_allication = allocate_resources(priority_task_a, priority_task_b)
final_allication =[0, 1, 2, 3, 4]
print(f"final_allication:  {final_allication}")  
# output of calculate efficienvy fucntion. 
calculated_efficiency = calculate_efficiency(priority_task_a, priority_task_b, final_allication)  
print(f"efficiency : primary time: {calculated_efficiency[0]} and secondary time {calculated_efficiency[1]}") 

 
