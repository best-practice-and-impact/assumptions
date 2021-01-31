#!/usr/bin/env bash

set -e

usage() {
    echo ""
    echo "Syntax: git assumptions [-h|f|t] "
    echo "Options:"
    echo "h     show this help."
    echo "f     specify the filename of the output Markdown file"
    echo "      to write the assumptions log to. Defaults to "
    echo "      'assumptions_log.md'."
    echo "t     target is the directory to search for assumptions."
    echo "      Defaults to current dir."
    # echo "  See 'man git-assumptions' for further information"
}


write_md_page()
{
    echo "# Assumptions and Caveats Log

## Assumptions

## Caveats
"
}

# Parse options
while [ "$1" != "" ]; do
    case $1 in
        -f | --file )           shift
                                filename=$1
                                ;;
        -t | --target )         shift
                                target=$1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

# Set defaults
filename=${filename:-"asumptions_log.md"}
target=${target:-"./"}

echo "Searching for assumptions under: $target"

# git grep doesn't work for multiline, so can only get file and first line
assumptions=$(git grep '^# Assumption:(.*)' $target)

# Struggling to get grep to lazy match, even using -P
# grep -Eir '^# Assumption:(.*)((\n#.*)*)'

# grep -rl '# Assumption:' search_here/ | xargs sed -E '/# Assumption:(.*)/,/(\n[^#]*)*/!d'

# Could use sed if end of assumption is indicated
# grep -rl '# Assumption:' search_here/ | xargs sed -E  '/# Assumption:(.*)/,/:end/!d'

echo "Writing assumptions log to: $filename"

write_md_page > $filename
