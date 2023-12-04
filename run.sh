#! /usr/bin/env bash
set -euxo nounset -o pipefail
#exec 0>&-
(( UID ))
(( ! $# ))

SELF="$(readlink -f "$0")"
[[ -e "$SELF" ]]

if command -v shellcheck ; then
	shellcheck "$SELF"
fi

if [[ -e .env ]] ; then
	set -e
	while read -r line ; do
		line="${line%%#*}"
		[[ "$line" ]] || continue
		export "${line?}"
	done < .env
	set +e
fi

###
# The command uvicorn main:app refers to:
#
# main: the file main.py (the Python "module").
# app: the object created inside of main.py with the line app = FastAPI().
# --reload: make the server restart after code changes. Only use for development.
###
uvicorn asgi:api --reload
