#!/bin/bash
# Act setup guide in the notion page
set -e

DIRECTORY=$(dirname $0)

cd $DIRECTORY/.. && act workflow_dispatch