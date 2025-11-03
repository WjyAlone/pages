# gunicorn_conf.py
import multiprocessing

bind = "127.0.0.1:5000"
workers = 3
worker_class = "sync"
timeout = 30
preload_app = True

# 日志配置
accesslog = "/www/wwwroot/repiece.top/logs/access.log"
errorlog = "/www/wwwroot/repiece.top/logs/error.log"
loglevel = "info"