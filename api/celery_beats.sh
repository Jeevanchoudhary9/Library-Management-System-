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
pip install -r requirements.txt


celery -A main.celery beat --loglevel=info