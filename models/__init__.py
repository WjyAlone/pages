from flask_sqlalchemy import SQLAlchemy

# 创建 db 实例
db = SQLAlchemy()

from .recorder import Recorder
from .message import Message

__all__ = ['Recorder', 'Message', 'db']

