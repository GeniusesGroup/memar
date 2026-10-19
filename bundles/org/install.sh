#!/bin/bash
# title:         install.sh
# description:   Clone|build|run apps
# author:        Omid Hekayati
# created:       Oct 22 2016
# updated:       Aug 09 2020
# version:       0.4
# usage:         ./install.sh || bash install.sh
# comment:
#       in linux use if occur any problem       dos2unix install.sh
#       for more log details in linux use       journalctl -u sabz.city.service -e
#==============================================================================

# var's
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
NC='\033[0m'
repo_Dir="${HOME}/sabz.city"

# Welcoming message
printf "${CYAN}
                                                        *************
                                                        Welcome back!
                                                        *************
       ${NC}\n"

# Get admin need that run this scripts
printf "${GREEN}Select one option
        ${BLUE}0)Exit
        ${BLUE}1)Install Ubuntu dependency ppa
        ${BLUE}2)Update Ubuntu pakages & Install dependencies
        ${BLUE}3)Clone || Update repo
        ${BLUE}4)Enable systemd services
        ${BLUE}5)Build
        ${BLUE}6)Start
        ${BLUE}7)
        ${BLUE}8)Get or renew LetsEncrypt 
        ${BLUE}9)
        ${BLUE}10) ${NC}\n"
read option

# exit from script
if [[ $option == 0 ]]; then
    exit

# Install Ubuntu dependency ppa
elif [[ $option == 1 ]]; then
    printf "\n${GREEN}Install Ubuntu dependency ppa${NC}\n"
    apt-get -y install software-properties-common || true
    add-apt-repository ppa:longsleep/golang-backports || true
    add-apt-repository ppa:certbot/certbot || true

# Update Ubuntu pakages & Install dependencies
elif [[ $option == 2 ]]; then
    printf "\n${GREEN}Update Ubuntu pakages & Install dependencies${NC}\n"
    apt-get update
    apt-get -y upgrade
    apt-get -y install git golang-go certbot

# Clone || Update repo
elif [[ $option == 3 ]]; then
    # Get|Update git repo
    printf "\n${GREEN}Clone||Pull repo to ${GREEN} $repo_Dir/ ${NC}\n"
    git clone https://github.com/GeniusesGroup/sabz.city.git $repo_Dir --recursive --shallow-submodules || true
    git -C $repo_Dir/ checkout -f || true
    git -C $repo_Dir/ pull --recurse-submodules || true
    cd $repo_Dir
    go get -u

# Enable systemd services
elif [[ $option == 4 ]]; then
    # Install||Update systemd .service files
    printf "\n${GREEN}Update sabz.city.service Systemd ${NC}\n"
    systemctl enable $repo_Dir/sabz.city.service
    # update systemd daemon
    printf "\n${GREEN}Update systemd daemon ${NC}\n"
    systemctl daemon-reload

# Build
elif [[ $option == 5 ]]; then
    # Get repo dependecies & Build app
    printf "\n${GREEN}build sabz.city main and development phase app ${NC}\n"
    go build

# Start||Restart main version app
elif [[ $option == 6 ]]; then
    # Restart||Start app
    printf "\n${GREEN}Start||Restart app ${NC}\n"
    service sabz.city restart

# Start||Restart dev version app
elif [[ $option == 7 ]]; then
    printf "\n${GREEN}--- ${NC}\n"
    cd "/root/sabz.city/"
    zip -9 -r -q datastore-files-v4.zip ./datastore-files/

# Get||Renew letsencrypt certificate
elif [[ $option == 8 ]]; then
    printf "\n${GREEN}Get||Update letsencrypt certificate ${NC}\n"
    certbot certonly --manual --preferred-challenges dns --domain sabz.city \
    --csr $repo_Dir/secret/sabz.city.csr --cert-path $repo_Dir/secret/sabz.city.crt --key-path $repo_Dir/secret/sabz.city.key \
    --fullchain-path $repo_Dir/secret/sabz.city-fullchain.crt --chain-path $repo_Dir/secret/sabz.city-chain.crt

#
elif [[ $option == 9 ]]; then
    printf "\n${GREEN}--- ${NC}\n"

#
elif [[ $option == 10 ]]; then
    printf "\n${GREEN}--- ${NC}\n"

else
    printf "${YELLOW}Invalid choose, try again from beginning ${NC}\n" exec bash "$0"
fi

# loop script until select exit!
exec bash "$0"
