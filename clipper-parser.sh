#!/bin/sh
set -e

pdf="$1"
USAGE="$0 [clipper card history pdf file]"

if test -z "$pdf"; then
  echo "$USAGE"
  exit 1
fi

pdf2svg bart-2013-10-11.pdf
