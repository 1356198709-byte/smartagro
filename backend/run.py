import uvicorn
uvicorn.run("app.主要:app", host="0.0.0.0", port=8000, reload=False, log_level="warning")
