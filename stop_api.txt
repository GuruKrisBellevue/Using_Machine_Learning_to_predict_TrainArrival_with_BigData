# This script stops the execution of the Python script by killing the background process
#!/bin/bash

export pid=`ps -ef | grep 'python.*[ ]call_cta_api.py' | awk 'NR==1{print $2}' | cut -d' ' -f1`;kill $pid

exit 0
