class RoundRobinLoadBalancer:
    def __init__(self, numServers):
        self.numServers = numServers
        self.servers = [[] for _ in range(numServers)]

    def addProcesses(self, processes):
        currentIndex = 0
        for process in processes:
            self.servers[currentIndex].append(process)
            currentIndex = (currentIndex + 1) % self.numServers  # Round robin distribution

    def printProcesses(self):
        for i, server in enumerate(self.servers):
            print(f"Server {i + 1} Processes: {server}")

def main():
    # Initial processes in the servers
    initialProcesses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # Number of servers
    numServers = 4
    loadBalancer = RoundRobinLoadBalancer(numServers)

    print("Processes before balancing:")
    print(*initialProcesses)

    loadBalancer.addProcesses(initialProcesses)

    print("\nProcesses after balancing:")
    loadBalancer.printProcesses()

if __name__ == "__main__":
    main()
