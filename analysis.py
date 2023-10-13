import os
import json 
import tqdm


# Get all addresses reverted on deployment
skips = []
for i in os.listdir("logs"):
    if i.startswith("ityfuzz"):
        with open("logs/" + i) as f:
            if "Failed to deploy contract" in f.read():
                skips.append(i.split("-")[1])


# ItyFuzz coverage parsing
def parse_coverage(dir):
    spots = []

    for i in os.listdir(dir):
        if not i.endswith(".json"):
            continue

        cov = json.load(open(os.path.join(dir, i)))
        total_instr_cov = 0
        total_branch_cov = 0
        for (k, v) in cov["coverage"].items():
            total_instr_cov += v["instruction_coverage"]
            total_branch_cov += v["branch_coverage"]
        ts = int(i.split("_")[1].split(".")[0])
        spots.append((ts, total_instr_cov, total_branch_cov))
    return spots

results = {}
for addr in tqdm.tqdm(os.listdir("ityfuzz_outs")):
    if addr in skips:
        continue
    coverage_path = os.path.join("ityfuzz_outs", addr, "coverage")
    cov = parse_coverage(coverage_path)
    results[addr] = cov

def get_starting_time(addr):
    if len(results[addr]) == 0:
        return 0
    return min([i[0] for i in results[addr]])


starting_times = {
    addr: get_starting_time(addr) for addr in results
}

x_ityfuzz = [x for x in range(0, 60)]
y_ityfuzz = [0 for _ in x_ityfuzz]

for i in range(60):
    y_at_i = 0
    for (addr, arr) in results.items():
        addr_y = []
        for (ts, ins, branch) in arr:
            # based on microsecond
            if (ts - starting_times[addr])/ 1000000 <= i:
                addr_y.append(ins)
        if len(addr_y) > 0:
            y_at_i += max(addr_y)
    y_ityfuzz[i] = y_at_i
print("ItyFuzz Data Fully Parsed!")


# Smartian Coverage Parsing

# second => set((addr, pc))
covs = {i: set() for i in range(61)}

for i in os.listdir("smartian_outs"):
    if not i.endswith(".json"):
        continue
    cov = json.load(open(os.path.join("smartian_outs", i)))

    for fn, j in cov.items():
        ts = int(fn.split("_")[1])
        if "0x6b773032d99fb9aad6fc267651c446fa7f9301af" in j:
            for pc in j["0x6b773032d99fb9aad6fc267651c446fa7f9301af"]:
                covs[ts].add((i, pc))

# accumulate
for i in tqdm.tqdm(range(1, 61)):
    covs[i] = covs[i].union(covs[i-1])

x_smartian = []
y_smartian = []

for k, v in covs.items():
    x_smartian.append(k)
    y_smartian.append(len(v))

print("Smartian Data Fully Parsed!")


print("ItyFuzz Final Coverage:", y_ityfuzz[-1])
print("Smartian Final Coverage:", y_smartian[-1])

import matplotlib.pyplot as plt
plt.ylim(y_smartian[1] * 0.9, y_ityfuzz[1] * 1.1)
plt.plot([0]+x_ityfuzz[1:], [0] + y_ityfuzz[1:])
plt.plot([0]+x_smartian[1:], [0] + y_smartian[1:])
plt.legend(["ItyFuzz", "Smartian"])
plt.grid()
plt.savefig("coverage.png")