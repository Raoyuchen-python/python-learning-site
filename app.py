from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
import subprocess
import sys
import tempfile

app = Flask(__name__)
app.secret_key = 'python-learning-site-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///python_learning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 确保静态文件目录存在
os.makedirs('static/images', exist_ok=True)

# 数据库模型
class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    lesson_id = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    progress = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Favicon路由
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico', 
                               mimetype='image/vnd.microsoft.icon')

# 创建一个简单的favicon
def create_simple_favicon():
    """创建一个简单的favicon文件"""
    favicon_path = 'static/images/favicon.ico'
    if not os.path.exists(favicon_path):
        try:
            try:
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (32, 32), color='#3776ab')
                draw = ImageDraw.Draw(img)
                draw.text((10, 8), "Py", fill=(255, 255, 255))
                img.save(favicon_path, format='ICO')
                print(f"已创建 favicon.ico 在 {favicon_path}")
            except ImportError:
                print("Pillow未安装，创建空favicon文件")
                with open(favicon_path, 'wb') as f:
                    f.write(b'')
        except Exception as e:
            print(f"创建favicon失败: {e}")

create_simple_favicon()

# Python学习数据
PYTHON_DATA = {
    "lessons": [
        {
            "id": 1,
            "title": "Python基础入门",
            "description": "学习Python的基本语法和概念",
            "content": """
            <h3>Python简介</h3>
            <p>Python是一种解释型、面向对象、动态数据类型的高级编程语言。</p>
            
            <h3>第一个Python程序</h3>
            <pre><code>print("Hello, World!")</code></pre>
            
            <h3>变量和数据类型</h3>
            <ul>
                <li>整数：x = 10</li>
                <li>浮点数：y = 3.14</li>
                <li>字符串：name = "Python"</li>
                <li>布尔值：is_true = True</li>
                <li>列表：my_list = [1, 2, 3]</li>
                <li>字典：my_dict = {"name": "John", "age": 25}</li>
            </ul>
            
            <h3>基本运算</h3>
            <pre><code># 算术运算
a = 10 + 5    # 加法
b = 10 - 5    # 减法
c = 10 * 5    # 乘法
d = 10 / 5    # 除法
e = 10 % 3    # 取余
f = 10 ** 2   # 幂运算</code></pre>
            """,
            "difficulty": "入门",
            "duration": "30分钟",
            "prerequisites": []
        },
        {
            "id": 2,
            "title": "控制流程",
            "description": "学习条件判断和循环",
            "content": """
            <h3>条件语句 - if/elif/else</h3>
            <pre><code>age = 18

if age < 18:
    print("未成年人")
elif age >= 18 and age < 60:
    print("成年人")
else:
    print("老年人")</code></pre>
            
            <h3>循环语句 - for循环</h3>
            <pre><code># 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(fruit)

# 使用range函数
for i in range(5):
    print(i)

for i in range(1, 6):
    print(i)</code></pre>
            
            <h3>循环语句 - while循环</h3>
            <pre><code>count = 0
while count < 5:
    print(f"计数: {count}")
    count += 1</code></pre>
            
            <h3>循环控制</h3>
            <pre><code># break - 跳出循环
for i in range(10):
    if i == 5:
        break
    print(i)

# continue - 跳过本次循环
for i in range(5):
    if i == 2:
        continue
    print(i)</code></pre>
            """,
            "difficulty": "入门",
            "duration": "45分钟",
            "prerequisites": ["Python基础入门"]
        },
        {
            "id": 3,
            "title": "函数和模块",
            "description": "学习如何定义函数和使用模块",
            "content": """
            <h3>定义函数</h3>
            <pre><code>def greet(name):
    \"\"\"问候函数\"\"\"
    return f"Hello, {name}!"

# 调用函数
message = greet("Alice")
print(message)</code></pre>
            
            <h3>函数参数</h3>
            <pre><code># 默认参数
def power(base, exponent=2):
    return base ** exponent

print(power(3))      # 9
print(power(3, 3))   # 27

# 关键字参数
def introduce(name, age, city):
    print(f"我叫{name}，今年{age}岁，来自{city}")

introduce(age=25, city="北京", name="张三")</code></pre>
            
            <h3>Lambda函数</h3>
            <pre><code># 匿名函数
square = lambda x: x ** 2
print(square(5))  # 25

# 在列表排序中使用
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]

# 按分数排序
students.sort(key=lambda x: x['score'])
print(students)</code></pre>
            
            <h3>导入模块</h3>
            <pre><code># 导入整个模块
import math
print(math.sqrt(16))  # 4.0

# 导入特定函数
from math import pi, cos
print(pi)
print(cos(0))</code></pre>
            """,
            "difficulty": "初级",
            "duration": "60分钟",
            "prerequisites": ["控制流程"]
        }
    ],
    "exercises": [
        {
            "id": 1,
            "title": "基础练习题",
            "description": "测试基础语法的掌握程度",
            "questions": [
                {
                    "id": 1,
                    "question": "编写一个程序，计算1到100所有偶数的和",
                    "hint": "使用循环和条件判断",
                    "solution": """total = 0
for i in range(1, 101):
    if i % 2 == 0:
        total += i
print(f"1到100的偶数和为: {total}")"""
                },
                {
                    "id": 2,
                    "question": "创建一个函数，接受一个字符串参数，返回该字符串的反转形式",
                    "hint": "使用字符串切片",
                    "solution": """def reverse_string(s):
    return s[::-1]

# 测试
print(reverse_string("hello"))  # olleh"""
                },
                {
                    "id": 3,
                    "question": "编写程序，找出列表中的最大值和最小值",
                    "hint": "使用内置函数或循环遍历",
                    "solution": """numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# 方法1: 使用内置函数
max_value = max(numbers)
min_value = min(numbers)
print(f"最大值: {max_value}, 最小值: {min_value}")

# 方法2: 手动实现
max_val = numbers[0]
min_val = numbers[0]
for num in numbers:
    if num > max_val:
        max_val = num
    if num < min_val:
        min_val = num
print(f"最大值: {max_val}, 最小值: {min_val}")"""
                }
            ]
        },
        {
            "id": 2,
            "title": "中级练习题",
            "description": "挑战更复杂的编程问题",
            "questions": [
                {
                    "id": 1,
                    "question": "编写一个函数，判断一个数是否为素数",
                    "hint": "素数是大于1且只能被1和自身整除的数",
                    "solution": """def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# 测试
print(is_prime(7))   # True
print(is_prime(10))  # False
print(is_prime(17))  # True"""
                },
                {
                    "id": 2,
                    "question": "编写一个函数，计算斐波那契数列的第n项",
                    "hint": "斐波那契数列：0, 1, 1, 2, 3, 5, 8, 13...",
                    "solution": """def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

# 测试
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")"""
                }
            ]
        }
    ],
    "tools": [
        {
            "id": 1,
            "name": "在线Python运行器",
            "description": "在线编写和运行Python代码",
            "url": "/tools/runner"
        },
        {
            "id": 2,
            "name": "代码格式化工具",
            "description": "格式化Python代码，使其符合PEP8规范",
            "url": "/tools/formatter"
        },
        {
            "id": 3,
            "name": "Python速查表",
            "description": "常用Python语法和函数速查",
            "url": "/tools/cheatsheet"
        }
    ]
}

# ========== 主要页面路由 ==========

@app.route('/')
def index():
    return render_template('index.html', data=PYTHON_DATA)

@app.route('/lessons')
def lessons():
    return render_template('lessons.html', lessons=PYTHON_DATA['lessons'])

@app.route('/lesson/<int:lesson_id>')
def lesson_detail(lesson_id):
    lesson = next((l for l in PYTHON_DATA['lessons'] if l['id'] == lesson_id), None)
    if lesson:
        return render_template('lesson_detail.html', lesson=lesson)
    return "课程不存在", 404

@app.route('/exercises')
def exercises():
    return render_template('exercises.html', exercises=PYTHON_DATA['exercises'])

@app.route('/exercise/<int:exercise_id>')
def exercise_detail(exercise_id):
    exercise = next((e for e in PYTHON_DATA['exercises'] if e['id'] == exercise_id), None)
    if exercise:
        return render_template('exercise_detail.html', exercise=exercise)
    return "练习不存在", 404

@app.route('/tools')
def tools():
    return render_template('tools.html', tools=PYTHON_DATA['tools'])

# ========== 工具页面路由 ==========

@app.route('/tools/runner')
def tool_runner():
    """在线Python运行器工具"""
    return render_template('tool_runner.html')

@app.route('/tools/formatter')
def tool_formatter():
    """代码格式化工具"""
    return render_template('tool_formatter.html') if os.path.exists('templates/tool_formatter.html') else "代码格式化工具正在开发中"

@app.route('/tools/cheatsheet')
def tool_cheatsheet():
    """Python速查表"""
    return render_template('tool_cheatsheet.html') if os.path.exists('templates/tool_cheatsheet.html') else "Python速查表正在开发中"

# ========== API接口 - 完全修复版 ==========

@app.route('/run_code', methods=['POST'])
def run_code():
    """
    执行Python代码 - Windows完全兼容版
    修复所有编码和变量错误
    """
    try:
        code = request.json.get('code', '')
        
        # 安全检查
        dangerous_keywords = ['__import__', 'eval', 'exec', 'open', 'os.', 'sys.', 'subprocess']
        for keyword in dangerous_keywords:
            if keyword in code:
                return jsonify({
                    "success": False,
                    "output": None,
                    "error": f"安全限制：禁止使用 {keyword}"
                })
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("import sys\n")
            f.write("import io\n")
            f.write("sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')\n")
            f.write("sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')\n\n")
            f.write(code)
            temp_file = f.name
        
        try:
            # 执行代码 - 使用binary模式
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                timeout=5,
                env={**os.environ, 'PYTHONUTF8': '1'}
            )
            
            # 清理临时文件
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            
            # 手动解码输出
            output_text = result.stdout.decode('utf-8', errors='replace') if result.stdout else ''
            error_text = result.stderr.decode('utf-8', errors='replace') if result.stderr else ''
            
            # 如果没有输出，添加提示
            if not output_text and not error_text:
                # 检测代码特征
                has_print = 'print(' in code
                has_variable = '=' in code and not any(x in code for x in ['==', '!=', '>=', '<='])
                
                if not has_print:
                    output_text = "✅ 代码执行成功！\n"
                    output_text += "=" * 40 + "\n"
                    output_text += "📌 提示：你的代码没有包含 print() 语句\n"
                    output_text += "💡 建议：添加 print() 来查看结果\n"
                    output_text += "=" * 40 + "\n"
                    output_text += "例如：\n"
                    output_text += '  print("Hello World")\n'
                    if has_variable:
                        output_text += "  x = 100\n"
                        output_text += "  print(x)  # 输出变量值\n"
                else:
                    output_text = "✅ 代码执行成功！\n"
            
            return jsonify({
                "success": True,
                "output": output_text,
                "error": error_text if error_text else None
            })
                
        except subprocess.TimeoutExpired:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            return jsonify({
                "success": False,
                "output": None,
                "error": "代码执行超时（超过5秒）"
            })
        except Exception as e:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            return jsonify({
                "success": False,
                "output": None,
                "error": str(e)
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "output": None,
            "error": str(e)
        })

@app.route('/api/progress', methods=['POST'])
def update_progress():
    data = request.json
    lesson_id = data.get('lesson_id')
    progress = data.get('progress', 0)
    
    if 'progress' not in session:
        session['progress'] = {}
    
    session['progress'][str(lesson_id)] = progress
    session.modified = True
    
    return jsonify({
        "success": True,
        "message": "进度已更新",
        "progress": progress
    })

@app.route('/api/get_progress')
def get_progress():
    progress = session.get('progress', {})
    return jsonify({
        "success": True,
        "progress": progress
    })

@app.route('/about')
def about():
    return render_template('about.html')

# ========== 静态文件路由 ==========

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# ========== 错误处理 ==========

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') if os.path.exists('templates/404.html') else "404 - 页面未找到", 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html') if os.path.exists('templates/500.html') else "500 - 服务器内部错误", 500

# ========== 数据库初始化 ==========

def init_db():
    with app.app_context():
        db.create_all()
        print("数据库已初始化")

# ========== 主程序入口 ==========

if __name__ == '__main__':
    init_db()
    print("=" * 50)
    print("Python学习网站已启动！")
    print("访问地址: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)