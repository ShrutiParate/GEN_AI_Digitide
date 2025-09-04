def main():
    tasks = []

    while True:
        print("\n======== To Do List App 😊 =========")
        print("1. Add Task")
        print("2. Show Tasks")
        print("3. Mark Task as Done")
        print("4. Delete All Done Tasks")   
        print("5. Exit from the App")       

        choice = input("Enter your choice: ")

        if choice == '1':
            n_tasks = int(input("How many tasks you want to add: "))
            for i in range(n_tasks):
                task = input("Enter the task: ")
                tasks.append({"task": task, "done": False})
                print("Task", task, "is added")

        elif choice == '2':
            print("\nYour Tasks:")
            if not tasks:
                print("No tasks added yet.")
            else:
                for index, task in enumerate(tasks):
                    status = "✅ Done" if task["done"] else "❌ Not Done"
                    print(f"{index + 1}. {task['task']} - {status}")

        elif choice == '3':
            task_index = int(input("Enter the task number to mark as done: "))
            if 0 < task_index <= len(tasks):
               tasks[task_index - 1]["done"] = True
               print("Task has been marked as done.")
            else:
               print("Invalid task number.")


        elif choice == '4':
            before_count = len(tasks)
            tasks = [task for task in tasks if not task["done"]]
            after_count = len(tasks)
            print(f"{before_count - after_count} done task(s) deleted.")

        elif choice == '5':
            print("Exiting fron the To-Do List App. \nGoodbye😊😊! Have a great day ahead😊😊😊😊😊😊")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
