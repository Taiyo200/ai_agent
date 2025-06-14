from functions.write_file import write_file

def main():
    print('Test 1: write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum")')
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print()

    print('Test 2: write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")')
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print()

    print('Test 3: write_file("calculator", "/tmp/temp.txt", "this should not be allowed")')
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    print()

if __name__ == "__main__":
    main()
