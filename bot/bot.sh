#!/usr/bin/env bash

# bot.sh: kick off bot.py with an appropriate environment

set -eo pipefail

here=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

source "${here}/twitter.env"
source "${here}/env/bin/activate"

python3 "${here}/bot.py"
