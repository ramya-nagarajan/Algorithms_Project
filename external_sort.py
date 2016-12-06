#!/usr/bin/python
import random
import struct
import time

def parent_(i):
    return i / 2


def left_(i):
    return 2 * i


def right_(i):
    return 2 * i + 1


def heapify(A, parent, last):
    left = left_(parent)
    right = right_(parent)
    if left <= last and A[left] < A[parent]:
        smallest = left
    else:
        smallest = parent
    if right <= last and A[right] < A[smallest]:
        smallest = right
    if smallest != parent:
        A[parent], A[smallest] = A[smallest], A[parent]
        heapify(A, smallest, last)
    return A


def heap_length(A):
    return len(A) - 1


def build_heap(A):  # build a heap A from an unsorted array
    n = heap_length(A)
    for i in range(n / 2, -1, -1):
        heapify(A, i, n)
    return A


def mergeSort(list):
    if len(list) > 1:
        mid = len(list)//2
        left = list[:mid]
        right = list[mid:]
        mergeSort(left)
        mergeSort(right)
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                list[k] = left[i]
                i += 1
            else:
                list[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            list[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            list[k] = right[j]
            j += 1
            k += 1
    return list


def create_initial_runs(ip, run_size, num_ways):
    op_list = []
    output_file_prefix = "output"
    for i in range(1, num_ways + 1):
        op_list.append(output_file_prefix + str(i) + ".txt")
    for i in range(1, num_ways + 1):
        with open(op_list[i-1], "wb") as f:
            y = ip[((i-1) * run_size):(run_size * i)]
            result = mergeSort(y)
            for j in result:
                f.write(struct.pack('<i', j))
            f.close()
    return op_list


def initial_compute_dict(num_ways, op_list):
    return {op_list[i]: {'VALUE': None, 'FILE_NAME': op_list[i], 'BYTES_READ':
        0} for i in range(0, num_ways)}


def get_next_data(compute_dict,values):
    for i in compute_dict:
        if compute_dict[i]['BYTES_READ'] == -1:
            continue
        with open(i, 'r') as f:
            if compute_dict[i]['VALUE'] is None:
                f.seek(compute_dict[i]['BYTES_READ'])
                y = f.read(4)
                if y == '':
                    compute_dict[i]['BYTES_READ'] = -1
                    continue
                value = struct.unpack('<i', y)[0]
                compute_dict[i]['VALUE'] = value
                compute_dict[i]['BYTES_READ'] += 4
    return compute_dict


def get_file(compute_dict, min_elem):
    for i in compute_dict:
        if compute_dict[i]['VALUE'] == min_elem:
            return i


def get_list(compute_dict):
    return [compute_dict[i]['VALUE'] for i in compute_dict]


def external_sort(ip, op, num_ways, run_size):
    op_list = create_initial_runs(ip, run_size, num_ways)
    compute_dict = initial_compute_dict(num_ways, op_list)
    output_file = open(op, 'wb')
    compute_dict = get_next_data(compute_dict, [])
    values = build_heap(get_list(compute_dict))
    for i in range(0, num_ways * run_size):
        min_elem = values[0]
        output_file.write(str(min_elem) + " ")
        m_file = get_file(compute_dict, min_elem)
        compute_dict[m_file]['VALUE'] = None
        compute_dict = get_next_data(compute_dict, values)
        if compute_dict[m_file]['VALUE'] is not None:
            values[0] = compute_dict[m_file]['VALUE']
        else:
            values.pop(0)
        if len(values) == 0:
            break
        heapify(values, 0, heap_length(values))
    output_file.close()


def main():
    num_ways = 10
    run_size = 200
    list1 = []
    input_file = "input.txt"
    output_file = "output.txt"
    for i in range(num_ways * run_size):
        list1.append(random.randint(0, 10000))
    infile = open(input_file, "w")
    infile.write(" ".join(str(i) for i in list1))
    infile.close()
    start = time.time()
    external_sort(list1, output_file, num_ways, run_size)
    end = time.time()
    time_taken = end-start
    print "time taken =",time_taken

if __name__ == "__main__":
    main()

