import time
from multiprocessing import cpu_count, Pool


def factorize_synch(*numbers):
    start_time = time.time()
    result = []
    for num in numbers:
        result.append([x for x in range(1, num + 1) if x % 2 == 0])
    print(f'Synch process finished by {time.time() - start_time} sec.')
    return result


def factorize_parallel(*numbers):
    cpu_num = cpu_count()
    start_time = time.time()
    pool = Pool(cpu_num)
    result = pool.map(factorize_number, numbers)
    print(f'Parallel {cpu_num} process finished by {time.time() - start_time} sec.')
    return result


def factorize_number(num):
    return [x for x in range(1, num + 1) if x % 2 == 0]


def main() -> None:
    factorize_synch(128, 255, 99999, 10651060)
    factorize_parallel(128, 255, 99999, 10651060)


if __name__ == '__main__':
    main()
