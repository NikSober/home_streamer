#!/bin/env bash
bash -xu <<< "$(curl -fsSL https://raw.githubusercontent.com/filebot/plugins/master/installer/rpm.sh)"
sudo dnf5 -y config-manager addrepo --from-repofile='https://raw.githubusercontent.com/filebot/plugins/master/yum/main.repo'
sudo dnf5 -y config-manager setopt filebot.enabled=1
sudo dnf5 -y install zenity mediainfo
sudo dnf5 -y install filebot

filebot -script fn:sysinfo