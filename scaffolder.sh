#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'

install_dependency() {

    local package_name="$1"

    # Check if the package is installed
    if ! command -v "$package_name" &>/dev/null; then
        echo "$package_name is not installed. Attempting to install..."

        # Install the package based on the package manager (adjust as needed for your system)
        if command -v apt-get &>/dev/null; then
            sudo apt-get install "$package_name"
        elif command -v brew &>/dev/null; then
            brew install "$package_name"
        else
            echo "Error: Unable to determine the package manager. Please install $package_name manually."
            return 1
        fi
    fi

}

gh_authenticate() {
    echo -e "${BLUE}Retrieving gh auth status...${BLUE}"
    if ! gh auth status >/dev/null 2>&1; then
        read -p "You need to login to gh. Would you like to login (y/n)? " login

        if [[ $login == 'y' ]]; then
            gh auth login
        else
            echo "Authentication was not successful. Git repository creation will not be possible."
        fi
    else
        echo "Authentication successful."
    fi

}

main() {
    read -p "$(echo -e "${GREEN}scaffolder > ${GREEN}")" OPTION
    OPTIONS=($OPTION)
    history -s "$OPTION"

    base_command=$(echo "$OPTION" | awk '{print $1}')
    arguments="${OPTION#$base_command}"

    commands=("scaffold" "templates" "licenses" "settings" "languages")

    if [[ " ${commands[@]} " =~ " ${base_command} " ]]; then
        python3 "$base_command.py" $arguments
    else
        case $base_command in
        clear)
            clear
            ;;
        exit)
            loop=0
            ;;
        history)
            history
            ;;
        *)
            echo -e "${RED}Unrecognized command: $base_command \n"
            ;;
        esac
    fi
}

loop=1
OPTIONS=""

install_dependency "gh"
install_dependency "jq"

cwd=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
path="$cwd/data/scaffolder.json"
gh_check=$(jq -r '.gh_check' $path)
venv_dir="$cwd/venv"

if [ -d "$venv_dir" ]; then
    echo "Activating existing virtual environment..."
    source "$venv_dir/bin/activate"
else
    read -p "Virtual environment not found. Would you like to create one and install all dependencies? (y/n)" v
    if [[ $v == 'y' ]]; then
        python3 -m venv "$venv_dir"
        source "$venv_dir/bin/activate"
        pip install -r "$cwd/requirements.txt"
    fi
fi

cd "$cwd/src"
HISTSIZE=100

history -r script_history

if [ $gh_check == 'true' ]; then
    gh_authenticate
fi

while :; do
    main
    [[ loop -eq 1 ]] || break
done

deactivate
