# Artifact for ItyFuzz

Get the image 
```bash
docker run -ti fuzzland/ityfuzz-artifacts:latest
```
or build it yourself
```bash
docker build . -t ityfuzz-artifacts
docker run -ti ityfuzz-artifacts
```

Run experiment:

```bash
# B1
./run.sh B1

# B2
./run.sh B2

# B3
./run.sh B3
```

### Notes
* Smartian replay over counts the instruction coverage (including instructions executed during deployment). To ensure fair comparisons, we turn the Smartian testcase to ItyFuzz testcase and replay using ItyFuzz.
* In our paper, we filter out checks and assertions inserted by the compiler when calculating the instruction coverage.
