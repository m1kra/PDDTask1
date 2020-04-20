#!/bin/bash
set -euo pipefail

start-dfs.sh
start-yarn.sh

hadoop fs -mkdir -p /user/vagrant
