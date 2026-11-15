@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "$b=@{client_id='capstone-client';grant_type='password';username='candidate1';password='Candidate@12345'}; (Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/realms/capstone/protocol/openid-connect/token' -Body $b).access_token | Set-Clipboard; 'user token copied'"
