import threading
import time

def my_function(name, number):
    """This function does some work and prints a message."""
    print(f"Thread {name} is doing work for {number} seconds.")
    time.sleep(number)
    print(f"Thread {name} finished its work.")

# Create and start two threads
thread1 = threading.Thread(target=my_function, args=("Thread 1", 3))
thread2 = threading.Thread(target=my_function, args=("Thread 2", 2))

thread1.start()
thread2.start()

# Wait for both threads to finish (optional)
thread1.join()
thread2.join()

print("Main thread finished execution.")
