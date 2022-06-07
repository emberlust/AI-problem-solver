from search import *
from utils import *
import time

from car_problem import CarProblem

def main(num = 0):

    if num == 0:
        num = input("Enter parking lot size: ")
    problem = CarProblem(int(num))
    path = astar_search(problem).solution()
    print(path)
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()