#!/bin/sh
cd "$(dirname "$0")" || exit 1
printf '\nOpen http://127.0.0.1:4173 in your browser.\n'
node tools/serve.mjs
