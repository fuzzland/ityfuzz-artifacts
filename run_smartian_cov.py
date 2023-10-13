import multiprocessing
import os
import subprocess
import json
import sys

TEST = sys.argv[1]

def run(addr):
    results = {}
    for replay in os.listdir(f"./smartian_outs/{addr}/testcase/"):
        if replay.endswith("_replayable"):
            try:
                cmd = f"timeout 60s ./ityfuzz/target/release/ityfuzz evm -t \"deployment/{addr}/*\" --replay-file ./smartian_outs/{addr}/testcase/{replay} --run-forever"
                out = subprocess.check_output(cmd, shell=True)
                out = out.decode("utf-8")
                out = out.split("\n")
                last_line = out[-2]
                results[replay] = json.loads(last_line)
            except Exception as e:
                print("Error", addr, replay)

    with open(f"smartian_outs/{addr}.json", "w+") as fp:
        json.dump(results, fp)

targets = [x.split(".")[0] for x in os.listdir(f"./Smartian-Artifact/benchmarks/{TEST}/bin") if x.endswith(".bin")]

with multiprocessing.Pool(42) as p:
    p.map(run, targets)