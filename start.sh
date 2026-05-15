#!/bin/bash

# Jalankan Tor di background
echo "Starting Tor..."
sudo service tor start

# Jalankan Privoxy di background
echo "Starting Privoxy..."
sudo service privoxy start

# Tunggu agar Tor membangun sirkuit (IP baru)
echo "Waiting for Tor to stabilize..."
sleep 20

# Jalankan bot Python kamu
echo "Launching the bot..."
python bot.py
