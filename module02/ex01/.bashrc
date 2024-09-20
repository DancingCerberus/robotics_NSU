#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

[ -f "/home/cerberus/.ghcup/env" ] && source "/home/cerberus/.ghcup/env" # ghcup-env
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

ros2_on(){
     export ROS_DOMAIN_ID=42
     export ROS_VERSION=2
     export ROS_PYTHON_VERSION=3
     export ROS_DISTRO=humble
     source /opt/ros/humble-base/setup.bash
}
source /opt/ros/humble-base/setup.bash
source ~/ros2_ws/install/setup.bash
