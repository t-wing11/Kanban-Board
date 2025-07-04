# start.ps1

# Start new window for kanban board FE
Start-Process powershell -ArgumentList "cd kanban-board-fe; npm run dev"

# Run backend in this window
cd kanban-board-BE
.\venv\Scripts\activate
python app.py