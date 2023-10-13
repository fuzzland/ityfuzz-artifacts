rm -rf logs && mkdir logs
echo "Running Smartian Tests"
rm -rf smartian_outs && mkdir smartian_outs
python3 run_smartian.py $1
python3 convert_to_ityfuzz_replayable.py $1

echo "Running ItyFuzz Tests"
rm -rf ityfuzz_outs && mkdir ityfuzz_outs
python3 run_ityfuzz.py $1

echo "Calculating Real Smartian Coverage"
# the errors can be safely ignored as they represent calls that are no longer supported
# to be fair, ItyFuzz is also not touching them
python3 run_smartian_cov.py $1


echo "Accounting for Coverage!"
python3 analysis.py $1

echo "Coverage plot is in coverage.png"