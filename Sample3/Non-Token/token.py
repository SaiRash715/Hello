ns = int(input("Enter number of sites: "))
ncs = int(input("Enter number of sites which want to enter critical section: "))

ts = [0] * ns  # Timestamps for each site
request = []   # List of sites requesting CS
mp = {}        # Map timestamp -> site

for _ in range(ncs):
    timestamp = int(input("\nEnter timestamp: "))
    site = int(input("Enter site number: "))
    ts[site - 1] = timestamp
    request.append(site)
    mp[timestamp] = site

print("\nSites and Timestamps:")
for i in range(len(ts)):
    print(f"Site {i + 1}: Timestamp {ts[i]}")

for site in request:
    print(f"\nRequest from site: {site}")
    for j in range(len(ts)):
        if site != (j + 1):
            if ts[j] > ts[site - 1] or ts[j] == 0:
                print(f"Site {j + 1} Replied")
            else:
                print(f"Site {j + 1} Deferred")
    print("\n")

print("Order of entering Critical Section:")
c = 0
for timestamp, site in sorted(mp.items()):
    print(f"Site {site} entered Critical Section")
    if c == 0:
        print("\nSimilarly,\n")
    c += 1
