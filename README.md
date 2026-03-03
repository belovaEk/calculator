Для запуска системы необходимо открыть отдельно папки 
calculator-app и calculator-backend

Чтоб поднять frontend:
1. Откройте папку calculator-app
2. npm install
3. npm install -g serve
4. serve -s build -l 8081


 - Local:    http://localhost:8081
 - Network:  http://172.22.112.1:8081

   Чтобы поднять backend:
1. Откройте папку calculator-backend
2. python -m venv venv
3. .\venv\Scripts\Activate.ps1   
4.  pip install -r requirements.txt
5.  python main.py
  
   Верися python 3.11.14
   Версия Node 20.18.0
