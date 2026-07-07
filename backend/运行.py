# 运行.py — 启动入口（主要代码）
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout.reconfigure(line_buffering=True)

import os
import webbrowser
import threading
import uvicorn

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print()
    print("  ======================================")
    print("       智慧农业管理系统")
    print("  ======================================")
    print()
    print("  http://localhost:8008")
    print()

    threading.Timer(1.5, lambda: webbrowser.open("http://localhost:8008")).start()

    uvicorn.run(
        "app.主要:app",
        host="0.0.0.0",
        port=8008,
        reload=False,
        log_level="warning",
    )
