#!/bin/bash

mkdir -p ffmpeg
cd ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz --strip-components=1

echo $(pwd)/ffmpeg > ../ffmpeg_path.txt

export PATH=$PATH:$(pwd)

cd ..
python bot/bot.py
