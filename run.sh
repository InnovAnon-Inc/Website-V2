#! /usr/bin/env bash
set -euxo nounset -o pipefail
exec 0>&-
(( UID ))
(( ! $# ))
[[ -e .env ]]
export $(cat .env)

python -m whatever
