#!/bin/sh

palette="./palette.png"
filters="fps=15,scale=320:-1:flags=lanczos"
filename=$(basename -- "$fullfile")

for i in ./*.gif;
do
    echo "Processing $i file...";
    filename=$(basename -- "$i")
    filename="${filename%.*}"
    ffmpeg -v warning -i "$i" -vf "$filters,palettegen=stats_mode=diff" -y $palette
    ffmpeg -i "$i" -i $palette -lavfi "$filters,paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" -y "$filename'.gif"
done