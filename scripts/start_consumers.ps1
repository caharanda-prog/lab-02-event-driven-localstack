Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m consumers.orders_worker"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m consumers.payments_worker"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m consumers.notifications_worker"