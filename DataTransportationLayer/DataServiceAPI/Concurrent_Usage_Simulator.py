#By: Tejas Kumar
#This script is used to simulate conncurrent usage using multiprocessing.
#The idea is to test DataService to see if successfully allows concurrent usage for data retrieval.

import asyncio
import sys
from multiprocessing import Pool
import DataService
import random
import time


#A Taskmap => User selects a task they want to test for concurrency. 
TaskMap = {
    "1": (DataService.RequestLatestKPIForProgram, (3,)),
    "2": (DataService.RequestKPIForProgramAndUniversity, (4, 5)),
    "3": (DataService.RequestProgramCategories, ()),
    "4": (DataService.RequestNOCGroupingOptions, ()),
    "5": (DataService.RequestProgramNOCLinks, (3,)), 
    "6": (DataService.RequestNOCGroupLaborStatistics, ("DGUID123", 5)),  
    "7": (DataService.RequestEROptions, (1,)),  
    "8": (DataService.RequestEconomicRegionEmploymentEstimate, (5, 1)),  
    "9": (DataService.RequestProvince, ()), 
}

#Runs the asychronous function 
def Run_Function(func, *args):
    return asyncio.run(func(*args))

#Main Working Function given the argument tuple. 
def worker(args_tuple):
    """Worker for multiprocessing: runs the async function"""
    func, args = args_tuple
    time.sleep(random.uniform(0.05, 0.2)) #This helps simulate time flucuations. 
    result = Run_Function(func, *args)
    try:
        print(f"Task {func.__name__} completed, got {len(result)} rows")
        print(result.head())
    except TypeError:
        print(f"Task {func.__name__} completed, result has no length")
    return result

def main():

    if len(sys.argv) < 3:
        print("Usage: python Concurrent_Usage_Simulator.py <task_id> <num_processes>")
        sys.exit(1)

    task_id = sys.argv[1]
    num_processes = int(sys.argv[2])

    if num_processes > 10:
        print(f"Too Many Workers - Range is between 1 to 10")
        sys.exit(1)

    print(f"Testing Task: {task_id} => with {num_processes} Users")

    if task_id not in TaskMap:
        print(f"Invalid task_id '{task_id}'. Valid IDs: {list(TaskMap.keys())}")
        sys.exit(1)

    func, args = TaskMap[task_id]

    # Prepare identical tasks for each process
    tasks = [(func, args) for _ in range(num_processes)]

    # Spawn multiple processes to run the same async function concurrently
    with Pool(processes=num_processes) as pool:
        results = pool.map(worker, tasks)

    ct = 0
    for r in results:
        if len(r) > 0:
            ct += 1
    
    if ct == num_processes:
        print(f"\nAll {num_processes} processes successfully completed.")
    else:
        print(f"\nOnly {ct} processes sucessfully completed.")

if __name__ == "__main__":
    main()
