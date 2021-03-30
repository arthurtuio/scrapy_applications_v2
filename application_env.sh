#!/bin/bash

set +e;

ACTION=$1
HOME_DIR=$(eval echo ~$USER) # returns user home folder, Ex: /home/arthur
APP_ENV_BASE_DIR=${APP_ENV_BASE_DIR:-"${HOME_DIR}/application-env"} 


function _help() {
    echo "application-env [ACTION]
Actions:

  install                       - Install cli and create airflow directories
  uninstall                     - Remove airflow enviroment directories
  login                         - Make login on dockerhub
  up                            - Up airflow enviroment
  stop                          - Stop airflow environment
  down                          - Stop and remove airflow environment
Ennvironment variables:
APP_ENV_BASE_DIR            - Airflow enviroment files location
                                    Installed Directory: ${APP_ENV_BASE_DIR}
DOCKER_LOGIN_USERNAME           - DockerHub access username
DOCKER_LOGIN_TOKEN              - DockerHub access token
"
}

function _create_and_set_dir_permissions() {
    directory="${1}/${2}"

    mkdir -p "${directory}";
    sudo chmod 777 "${directory}";
}

function install() {
    PWD=$(eval pwd);

    echo "Installing cli script..."
    sudo cp -f "${PWD}/application-env.sh" /usr/local/bin/application-env
    sudo chmod 755 /usr/local/bin/application-env

    echo "Moving docker-compose file to enviroment..."
    mkdir -p "${APP_ENV_BASE_DIR}"
    cp "${PWD}/docker-compose.yml" "${APP_ENV_BASE_DIR}/"

    echo "Creating airflow directories..."
    _create_and_set_dir_permissions "${APP_ENV_BASE_DIR}" "airflow"
    _create_and_set_dir_permissions "${APP_ENV_BASE_DIR}/airflow" "dags"
    _create_and_set_dir_permissions "${APP_ENV_BASE_DIR}/airflow" "logs"
    _create_and_set_dir_permissions "${APP_ENV_BASE_DIR}/airflow" "plugins"
    echo "Directories successfully created!"
    echo "..."
    echo "application-env CLI is successfully installed!"
}

function login() {
    docker login \
        --username "${DOCKER_LOGIN_USERNAME}" \
        --password "${DOCKER_LOGIN_TOKEN}"
}

function up() {
    APP_ENV_BASE_DIR="${APP_ENV_BASE_DIR}" \
        docker-compose \
        -f "${APP_ENV_BASE_DIR}/docker-compose.yml" \
        up -d
}

function stop() {
    docker-compose -f "${APP_ENV_BASE_DIR}/docker-compose.yml" stop
}

function down() {
    echo "Stop and remove all airflow environment containers? ('y' to confirm)"
    read confirm_down
    [[ "$confirm_down" == "y" ]] && docker-compose -f "${APP_ENV_BASE_DIR}/docker-compose.yml" down
}

function uninstall() {
    echo "Uninstall airflow environment? ('y' to confirm)"
    read confirm_down
    if [ "$confirm_down" == "y" ]; then
        docker-compose -f "${APP_ENV_BASE_DIR}/docker-compose.yml" down

        rm -rf "${APP_ENV_BASE_DIR}"
    fi
}

case $ACTION in
    install)
        install
        ;;
    uninstall)
        uninstall
        ;;
    login)
        login
        ;;
    stop)
        stop
        ;;
    up)
        up
        ;;
    down)
        down
        ;;
    help)
        _help
        ;;
    *)
        _help
esac
