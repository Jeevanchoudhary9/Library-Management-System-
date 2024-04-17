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
    virtualenv .venv
fi

# Activate virtual env
. .env/bin/activate


celery -A main.celery worker --loglevel=info