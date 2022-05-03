from data_loader_test import loader_test
from data_reader_test import reader_test


def main():
    import sys
    filename = sys.argv[1]
    batch = int(sys.argv[2])
    test_size = int(sys.argv[3])
    test_size_reader = int(sys.argv[4])
    loader_test(batch, filename, test_size)
    reader_test(filename, test_size_reader)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
