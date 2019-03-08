from ClassInit import ClassGetter
from getpass import getpass
import time

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = getpass(prompt="Enter your password: ")
    start_time = time.time()
    print("Loading Classes...\n")

    initClass = ClassGetter()

    try:
        initClass.login(username, password)
        clazz = initClass.createClasses()
        for cls in clazz:
            for sec in cls:
                print(str(sec))
        print(time.time() - start_time)
    except Exception:
        print("Error logging in")
