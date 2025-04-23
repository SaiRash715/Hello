import threading
import time

shared_resource = 0
lock = threading.Lock()

def modify_resource(thread_name):
    global shared_resource
    print(f"{thread_name} is trying to access the shared resource.")
    
    # Acquire the lock to modify the shared resource safely
    with lock:
        print(f"{thread_name} has acquired the lock.")
        
        # Read the current value of the shared resource
        current_value = shared_resource
        
        # Simulate some delay
        time.sleep(1)
        
        # Update the shared resource
        shared_resource = current_value + 1
        print(f"{thread_name} updated the shared resource to {shared_resource}.")
    
    # Lock is released automatically when exiting the 'with' block
    print(f"{thread_name} released the lock.")

# List to store all threads
threads = []

# Create and start 5 threads
for i in range(5):
    thread_name = f"Thread-{i+1}"
    thread = threading.Thread(target=modify_resource, args=(thread_name,))
    threads.append(thread)
    thread.start()

# Ensure all threads complete execution
for thread in threads:
    thread.join()

# Final value of the shared resource
print(f"Final value of shared_resource: {shared_resource}")
