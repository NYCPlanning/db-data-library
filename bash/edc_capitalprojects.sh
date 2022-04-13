#!/bin/bash
source bash/config.sh

function import_data {
    import edc_capitalprojects "20211124"
}

function all {
    import_data
}

# Execution of All commands:
case $1 in 
    import_data) $@;;
    *) all;;
esac