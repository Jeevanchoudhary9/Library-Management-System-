#! /bin/sh
echo "======================================================================"
echo "Libary Management System"
echo "Modern Application Development-II"
echo "By - Jeevan Ramkrishna Choudhary (22f1001943)"
echo "This file runs celery beats for the application"
echo "----------------------------------------------------------------------"
if [ -d ".venv" ];
then
    echo ".venv folder exists. Runningcelery beats"
else
    echo "creating .venv and install using pip"
    python3 -m venv .venv
fi

# Activate virtual env
. .venv/bin/activate

# Make sure redis server is running
service redis-server restart

# Upgrade the PIP
pip install --upgrade pip
pip install -r requirements.txt

# Now activate the venv and run main.py