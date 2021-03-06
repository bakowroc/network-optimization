CORES=(3 8)
DEMAND_FILES=(
    1000_01.dem
    1000_08.dem
    1300_01.dem
    1300_08.dem
    1600_01.dem
    1600_08.dem
    2000_01.dem
    2000_08.dem
)

for core in "${CORES[@]}"
do
    for file in "${DEMAND_FILES[@]}"
    do
        python main.py -e /e/workspace/roza/network-optimization/entry/ -d $file -c $core -s
    done
done