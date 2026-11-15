@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "$b=@{client_id='capstone-client';grant_type='password';username='admin1';password='Admin@12345'}; (Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/realms/capstone/protocol/openid-connect/token' -Body $b).access_token | Set-Clipboard; 'admin token copied'"
