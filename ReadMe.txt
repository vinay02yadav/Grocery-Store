1. Start redis-server and redis-cli in windows.

2. Navigate to the root -> backend folder of the application.
	open three seprate terminal in backend dir:
	-> execute "python main.py" in terminal
	-> celery -A main.celery worker --pool=solo -l info
	-> celery -A main.celery beat --max-interval 600 -l info

3. Navigate to the root -> frontend folder of the application.
	open terminal in frontend dir:
	-> execute "npm run serve" in terminal