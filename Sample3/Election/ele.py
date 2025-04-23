# Ring Election Algorithm with user input

# Get user input
total_processes = int(input("Enter total number of processes: "))
failed_process = int(input("Enter the process number that fails: "))
initiator = int(input("Enter the process number initiating the election: "))

# Initialize process list
processes = [{'id': i, 'active': True} for i in range(total_processes)]

# Mark the failed process as inactive
processes[failed_process]['active'] = False

print(f"\n[INFO] Total processes: {total_processes}")
print(f"[INFO] Process {failed_process} has failed.")
print(f"[INFO] Election initiated by Process {initiator}\n")

# Election Phase
old = initiator
new = (old + 1) % total_processes

while True:
    if processes[new]['active']:
        print(f"Process {old} passes Election({old}) to Process {new}")
        old = new
    new = (new + 1) % total_processes
    if new == initiator:
        break

# Find the new coordinator (highest active ID)
coordinator = max(
    (i for i in range(total_processes) if processes[i]['active']),
    key=lambda i: processes[i]
)
print(f"\n[RESULT] Process {coordinator} becomes the new Coordinator.\n")

# Coordinator Announcement Phase
old = coordinator
new = (old + 1) % total_processes

while True:
    if processes[new]['active']:
        print(f"Process {old} passes Coordinator({coordinator}) message to Process {new}")
        old = new
    new = (new + 1) % total_processes
    if new == coordinator:
        print("\n[INFO] End of Election.\n")
        break
