#!/bin/bash

for leds in 60 74;
do
	for subdiv in 1 2 3 4 5;
	do
		for x in 3 5 7 9;
		do
			echo "$(./tube.py -info -tiling penta -segment-floor "$((x*1000/leds))" -subdivisions "$subdiv" -thickness 3 -width 17.5 -height 19 | grep diameter | cut -d' ' -f2) leds/m: $leds leds/segment: $x subdiv: $subdiv"
		done
	done
done | sort -n
