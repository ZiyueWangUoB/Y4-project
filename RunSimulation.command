chmod u+x /home/z/Documents/Y4projects/RunSimulation.command
cd /home/z/Documents/Y4projects/Simulation/


printf "Progress, please wait"
for ((a = 477; a < 1000; a++))
do 
	python3 main.py $a
	printf $a
done
printf "Done"
