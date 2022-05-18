#!/bin/bash

function usage {
	echo -e '\nScript to automate folder creation for thm/hack the box ctfs. \nMakes a readme.md downloads, enum, scripts and bin directories. \n\nUSAGE:'
	echo -e '\t-d:\tDIRECTORY \n\t\tpath to save new folder in'
	echo -e '\t-n:\tNAME \n\t\tName of new folder'
	exit 0
}

argparse=d:n:h

while getopts ${argparse} options

do
	case "${options}" in

	d) DIRECTORY=${OPTARG};;

    n) NAME=${OPTARG};;

    h) usage
    
    esac
done

 
cd $DIRECTORY 

set -e 
mkdir $NAME 
set +e

cd $NAME

mkdir enum bin scripts downloads

mkdir enum/web enum/nmap

touch readme.md

echo '#' $NAME >> readme.md

echo -e '\n\n## enum \n\n\n\n## exploit \n\n\n\n## Privesc' >> readme.md

echo "Created folder ${NAME} in ${DIRECTORY}"
