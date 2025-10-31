from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# 配置SQLite数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义联系表单数据模型
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage {self.name}>'

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html', title='Welcome Page', name='John Doe')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # 获取JSON数据
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '没有接收到数据'}), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        # 验证必填字段
        if not name or not email or not message:
            return jsonify({'error': '请填写所有必填字段'}), 400
        
        # 创建新消息记录
        new_message = ContactMessage(
            name=name,
            email=email,
            message=message
        )
        
        # 保存到数据库
        db.session.add(new_message)
        db.session.commit()
        
        print(f"消息已保存 - ID: {new_message.id}, 姓名: {name}")
        
        # 返回成功响应
        return jsonify({
            'status': 'success',
            'message': '消息接收成功，已保存到数据库',
            'message_id': new_message.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"处理请求时出错: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

# 可选：添加一个路由来查看所有消息（仅用于开发）
@app.route('/messages')
def view_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg.id,
            'name': msg.name,
            'email': msg.email,
            'message': msg.message,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(messages_list)

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 简单的验证逻辑
    if username == 'admin' and password == '123':
        return jsonify({'success': True, 'token': 'your_jwt_token_here'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'})

if __name__ == '__main__':
    app.run(debug=True)
