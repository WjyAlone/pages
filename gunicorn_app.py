# gunicorn_app.py
import multiprocessing

# 基础配置
bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"

# 性能调优
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30

# 内存优化
preload_app = True

# 日志配置
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# 进程管理
daemon = False
pidfile = "/var/run/gunicorn/flask.pid"
umask = 0o022

# 安全设置
tmp_upload_dir = None

# 环境变量
raw_env = [
    "FLASK_ENV=production",
    "DATABASE_URL=sqlite:///portfolio.db"
]