#!/bin/bash

leds_per_m="${1:-60 74}"
tiling="${2:-penta}"

if [ "$tiling" == "penta" ];
then
	n_segments=30;
elif [ "$tiling" == "quad" ];
then
	n_segments=12;
elif [ "$tiling" == "tri" ];
then
	n_segments=6;
else
	exit 1;
fi

for leds in $leds_per_m;
do
	for subdiv in 1 2 3 4 5;
	do
		for x in 3 5 7 9;
		do
			echo "$(./tube.py -info -tiling "${tiling}" -segment-floor "$((x*1000/leds))" -subdivisions "$subdiv" -thickness 3 -width 17.5 -height 19 | grep diameter | cut -d' ' -f2) leds: $((n_segments*((3*subdiv*x)-1))) leds/m: $leds leds/segment: $x subdiv: $subdiv"
		done
	done
done | sort -n
