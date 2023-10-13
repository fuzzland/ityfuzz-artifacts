import multiprocessing
import os
import sys

TEST = sys.argv[1]

def run(addr, cpu):
    cmd = f"taskset -c {cpu} ./Smartian/build/Smartian fuzz -v 1 --timelimit 60 --program ./Smartian-Artifact/benchmarks/{TEST}/bin/{addr}.bin --abifile ./Smartian-Artifact/benchmarks/{TEST}/abi/{addr}.abi -o smartian_outs/{addr}  --useothersoracle > logs/{addr} 2>&1"
    os.system(cmd)

targets = [x.split(".")[0] for x in os.listdir(f"./Smartian-Artifact/benchmarks/{TEST}/bin") if x.endswith(".bin")]


CPU_AMOUNT = os.cpu_count() - 2

while len(targets) > 0:
    all_ps = []
    for i in range(CPU_AMOUNT):
        if len(targets) == 0:
            break

        print("Running on", targets[0], "on CPU", i)
        all_ps.append(multiprocessing.Process(target=run, args=(targets[0], i)))

        targets = targets[1:]
    for i in all_ps:
        i.start()
    
    for i in all_ps:
        i.join()
    print("Finished one batch!")