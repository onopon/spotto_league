#!/bin/sh
while [ `curl -I 0.0.0.0:8080 -o /dev/null -w '%{http_code}\n' -s` -eq 000 ]
do
  echo "waiting..."
  sleep 1
done
echo "app is ready!"
