from main import main as test_car_problem
import time

def main():
    for test_size in range(2,7):
        start = time.time()
        test_car_problem(test_size)
        end = time.time()
        print(end-start,'\n')

if __name__ == "__main__":
    main()
