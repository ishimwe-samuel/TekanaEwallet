
# Tekana e-Wallet
Tekana e-Wallet is an e-Wallet platform that helps users transfer money to their fellow friends on the same platform
## Tech Stack

**Server:** Python - Django \
**Database Engine:** PostgreSQL \
**Background Worker :** Celery
**Caching Engine:** Redis



## Installation

Install 

```bash
  sudo apt install redis
  cd TekanaEwallet
  pip install virtualenv 
  virtualenv venv 
  source /venv/bin/activate
```
    
## Running Tests
You will need to run both the backend and celery on different terminal instances  
\
To run , run the following command

```bash
    python manage.py runserver
```
To run celery, run the following command

```bash
    celery -A TekanaEwallet worker -l INFO   
```
## Demo
please access this link for a quick demo \
https://www.samueldev.com

