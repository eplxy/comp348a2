import textwrap


def show_menu():
    print(textwrap.dedent("""
        1. Display Global Statistics
        2. Display Base Station Statistics
        3. Check Coverage
        4. Exit
          """))
    return input("Enter choice: ")


def show_global_statistics():
    print("Global Statistics")
    return


def option_check_coverage():
    print("Check Coverage")
    return


while True:
    choice = show_menu()
    match choice:
        case "1":
            show_global_statistics()
            print("Global Statistics")
        case "2":
            print("Base Station Statistics")
        case "3":
            print("Check Coverage")
        case "4":
            print("Exiting")
            break
        case _:
            print("Invalid choice")

print("test")
