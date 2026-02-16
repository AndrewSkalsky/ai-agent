from functions.write_file import write_file

def test_get_files_info():
    
    print("Result for 'lorem.txt' directory:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    #-------------------------------------
    
    print("Result for 'pkg/morelorem.txt' directory:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    #-------------------------------------
    
    print("Result for '/tmp/temp.txt' directory:")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

test_get_files_info()