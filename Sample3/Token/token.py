from queue import Queue

PR = 5  # Total number of processes
token_holder = 0  # Initially process 0 has the token

class Token:
    def __init__(self):
        self.id = 0
        self.token_q = Queue()
        self.ln = [0] * PR

    def update_ln(self, pid, seqno):
        self.ln[pid] = seqno

token = Token()

class Site:
    def __init__(self, pid):
        self.pid = pid
        self.rn = [0] * PR
        self.has_token = False
        self.requesting = False
        self.executing = False

    def request_cs(self):
        global token_holder

        if self.executing or self.requesting:
            print(f"Process {self.pid} is already in CS or has requested.")
            return

        self.requesting = True
        self.rn[self.pid] += 1
        seqno = self.rn[self.pid]

        if token_holder == self.pid:
            print(f"Process {self.pid} already has the token, entering CS.")
            self.enter_cs()
            return

        print(f"Process {self.pid} requested CS with seq {seqno}")
        for i in range(PR):
            if i != self.pid:
                sites[i].receive_request(self.pid, seqno)

        if token_holder == self.pid:
            self.enter_cs()
        else:
            print(f"Process {self.pid} is waiting for the token.")

    def receive_request(self, requester_id, seqno):
        self.rn[requester_id] = max(self.rn[requester_id], seqno)
        if self.has_token and not self.executing and token.ln[requester_id] + 1 == self.rn[requester_id]:
            self.send_token(requester_id)
        elif self.has_token and token.ln[requester_id] + 1 == self.rn[requester_id]:
            token.token_q.put(requester_id)

    def enter_cs(self):
        self.executing = True
        self.has_token = True
        self.requesting = False
        print(f"Process {self.pid} enters CS.")

    def release_cs(self):
        global token_holder

        if not self.executing:
            print(f"Process {self.pid} is not executing CS.")
            return

        print(f"Process {self.pid} releases CS.")
        self.executing = False
        token.update_ln(self.pid, self.rn[self.pid])

        if not token.token_q.empty():
            next_process = token.token_q.get()
            self.send_token(next_process)
        else:
            print(f"Process {self.pid} keeps the token.")

    def send_token(self, next_pid):
        global token_holder
        print(f"Process {self.pid} sends token to Process {next_pid}.")
        self.has_token = False
        token_holder = next_pid
        sites[next_pid].has_token = True
        sites[next_pid].enter_cs()

# Simulation
sites = [Site(i) for i in range(PR)]
sites[0].has_token = True  # Initial token holder

# Requesting and releasing the critical section
sites[0].request_cs()
sites[1].request_cs()
sites[2].request_cs()
sites[0].release_cs()
sites[0].request_cs()
sites[3].request_cs()
sites[1].release_cs()
sites[2].release_cs()
sites[0].release_cs()
sites[3].release_cs()
