#!/bin/bash

NAME="remote_control"
FLASKDIR=/home/pi/remote_control
VENVDIR=/home/pi/venv
SOCKFILE=/home/pi/remote_control/sock
USER=pi
GROUP=pi
NUM_WORKERS=3

echo "Starting $NAME"

# activate the virtualenv
cd $VENVDIR
source bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your unicorn
exec gunicorn RaspApp:app -b 0.0.0.0:5000 \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE
