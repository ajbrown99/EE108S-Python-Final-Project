from ClassInit import ClassGetter
from getpass import getpass
# from flexx import flx
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
            print(clazz[cls])
        print(time.time() - start_time)
        inputs = ""
        while True:
            inputs = input("Enter classes: ")
            inputs_split = inputs.strip().split(" ")
            conflict = False
            classFindError = False
            if inputs == "q":
                break
            for i in range(len(inputs_split)):
                if conflict:
                    continue
                if inputs_split[i] not in clazz:
                    print("Error: One or more class not found.")
                    classFindError = True
                    break
                for j in range(i + 1, len(inputs_split)):
                    if clazz[inputs_split[i]].findConflict(clazz[inputs_split[j]]):
                        print("There is a conflict")
                        conflict = True
                        break
            if not conflict and not classFindError:
                print("There is no conflict")
            print("\n")
    except Exception:
        print("Error logging in")
