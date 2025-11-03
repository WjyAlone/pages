from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import Message, Recorder, db
from services.message_service import MessageService
from services.recorder_service import RecorderService
from datetime import datetime

app = Flask(__name__)
# 配置SQLite数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
static_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJpYXQiOjE2ODAwMDAwMDAsImV4cCI6MTY4MDAwMzYwMH0.signature'

with app.app_context():
    db.create_all()

def get_client_ip():
    """获取客户端真实IP地址"""
    # 检查常见的代理头
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_REAL_IP'].split(',')[0]
    elif request.environ.get('HTTP_X_REAL_IP'):
        ip = request.environ['HTTP_X_REAL_IP']
    elif request.environ.get('HTTP_CLIENT_IP'):
        ip = request.environ['HTTP_CLIENT_IP']
    else:
        ip = request.environ.get('REMOTE_ADDR')
    return ip

@app.route('/')
def home():
    client_ip = get_client_ip()
    try:
        platform = request.headers['User-Agent'].split()[1][1:]
    except:
        platform = 'None'
    try:
        browser = request.headers['User-Agent'].split()[4][:-1]
    except:
        browser = 'None'
    print(client_ip, request.headers['User-Agent'].split())
    RecorderService.create_record(client_ip, platform, browser)
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
        
        MessageService.create_message(name, email, message)

        print(f"消息已保存 - 姓名: {name}")
        
        # 返回成功响应
        return jsonify({
            'status': 'success',
            'message': '消息接收成功，已保存到数据库'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"处理请求时出错: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

@app.route('/login', methods=['GET'])
def login_page():
    """显示登录页面"""
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """处理AJAX登录请求"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 简单的验证逻辑
    if username == 'admin' and password == '123':
        return jsonify({'success': True, 'token': static_token})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'})

@app.route('/api/messages')
def view_messages():
    if 'Authorization' in request.headers:
        try:
            token = request.headers['Authorization'].split()[1]
            if token != static_token:
                return jsonify({
                    'success': False,
                    'message': 'Wrong'
                }), 401
            elif token == static_token:
                messages = MessageService.get_messages()
                messages_list = []
                for msg in messages:
                    messages_list.append({
                        'id': msg.id,
                        'name': msg.name,
                        'email': msg.email,
                        'message': msg.message,
                        'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'pending'
                    })
                return jsonify(messages_list)

        except IndexError:
            return jsonify({
                'success': False,
                'message': 'WrongToken'
            }), 401
    else:
        return 'BadRequest'

@app.route('/api/status')
def view_status():
    if 'Authorization' in request.headers:
        try:
            token = request.headers['Authorization'].split()[1]
            if token != static_token:
                return jsonify({
                    'success': False,
                    'message': 'Wrong'
                }), 401
            elif token == static_token:
                records = RecorderService().get_records()
                records_list = []
                for msg in records:
                    records_list.append({
                        'id': msg.id,
                        'ip': msg.client_ip,
                        'platform': msg.platform,
                        'browser': msg.browser,
                        'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'pending'
                    })
                return jsonify(records_list)

        except IndexError:
            return jsonify({
                'success': False,
                'message': 'WrongToken'
            }), 401
    else:
        return 'BadRequest'

@app.route('/api/message/action', methods=['POST'])
def messageAction():
    data = request.get_json()
    act = data.get('action')
    ID = data.get('ID')
    if act == 'delete':
        try:
            MessageService.delete_message(ID)
            return jsonify({
                'success': True
            })
        except:
            return jsonify({
                'success': False
            })

@app.route('/api/ipconfig/action', methods=['POST'])
def ipAction():
    data = request.get_json()
    act = data.get('action')
    ID = data.get('ID')
    if act == 'delete':
        try:
            RecorderService.delete_record(ID)
            return jsonify({
                'success': True
            })
        except:
            return jsonify({
                'success': False
            })
    elif act == 'delete_all':
        try:
            for record in RecorderService.get_records():
                RecorderService.delete_record(record.id)
            return jsonify({
                'success': True
            })
        except Exception as e:
            return jsonify({
                'success': False
            })
@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)