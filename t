sudo apt remove --purge wine wine32 wine64 -y
sudo apt autoremove -y
sudo rm -rf ~/.wine
sudo rm -rf ~/.config/wine

sudo rm /etc/apt/sources.list.d/winehq*
sudo apt update
