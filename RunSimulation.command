chmod u+x /Users/ziyuewang/Documents/Y4\ project/RunSimulation.command
cd /Users/ziyuewang/Documents/Y4\ project/Simulation/

for ((a = 0; a < 50; a++))
do 
	python main.py $a
	printf $a "/50"
done
printf "Done"
