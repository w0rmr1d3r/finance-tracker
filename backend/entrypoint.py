import uvicorn

uvicorn.run("finance_tracker.__main__:app", host="0.0.0.0", port=8000)
