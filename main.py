from ClassInit import ClassGetter
from getpass import getpass

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = getpass(prompt="Enter your password: ")
    print("Loading Classes...\n")

    initClass = ClassGetter()

    initClass.login(username, password)
    # print(createClasses())
    clazz = initClass.createClasses()
    for cls in clazz:
        for sec in cls:
            print(str(sec))
