chmod u+x /Users/ziyuewang/Documents/Y4\ project/RunSimulation.command
cd /Users/ziyuewang/Documents/Y4\ project/Simulation/


printf "Progress, please wait"
for ((a = 0; a < 200; a++))
do 
	python main.py $a
	printf $a
done
printf "Done"
