document.addEventListener('DOMContentLoaded', function() {
    // 初始化粒子背景
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 } },
            color: { value: "#ffffff" },
            shape: { type: "circle" },
            opacity: { value: 0.5, random: true },
            size: { value: 3, random: true },
            line_linked: {
                enable: true,
                distance: 150,
                color: "#ffffff",
                opacity: 0.2,
                width: 1
            },
            move: {
                enable: true,
                speed: 2,
                direction: "none",
                random: true,
                straight: false,
                out_mode: "out",
                bounce: false
            }
        },
        interactivity: {
            detect_on: "canvas",
            events: {
                onhover: { enable: true, mode: "repulse" },
                onclick: { enable: true, mode: "push" },
                resize: true
            }
        }
    });

    const loginForm = document.getElementById('loginForm');
    const loginPage = document.getElementById('loginPage');
    const adminDashboard = document.getElementById('adminDashboard');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const togglePassword = document.getElementById('togglePassword');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const logoutBtn = document.getElementById('logoutBtn');
    const refreshBtn = document.getElementById('refreshBtn');
    const exportBtn = document.getElementById('exportBtn');
    const ordersTableBody = document.getElementById('ordersTableBody');
    const loginBtn = document.querySelector('.login-btn');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.querySelector('.btn-loader');

    // 检查是否已登录
    if(localStorage.getItem('isLoggedIn') === 'true') {
        showAdminDashboard();
        loadOrdersData();
    }

    // 切换密码可见性
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // 切换图标
        const icon = this.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });

    // 表单提交处理
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 显示加载状态
        btnText.style.display = 'none';
        btnLoader.style.display = 'flex';
        loginBtn.disabled = true;
        
        // 简单验证
        setTimeout(() => {
                        
            function login(username, password) {
                fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        localStorage.setItem('isLoggedIn', 'true');
                        showAdminDashboard();
                        loadOrdersData();
                        localStorage.setItem('token', data.token);
                    } else {
                        // 登录失败
                        usernameError.textContent = '账号或密码错误';
                        passwordInput.parentElement.classList.add('error');
                        
                        // 重置按钮状态
                        btnText.style.display = 'block';
                        btnLoader.style.display = 'none';
                        loginBtn.disabled = false;
                    }
                })
                .catch(error => {
                    console.error('错误:', error);
                    alert('网络错误');
                });
            }
            login(usernameInput.value, passwordInput.value)
        }, 1500);
    });

    // 显示管理员后台
    function showAdminDashboard() {
        loginPage.style.display = 'none';
        adminDashboard.style.display = 'block';
    }

    // 加载订单数据
    function loadOrdersData() {
        // 模拟订单数据
        const orders = [
            { id: 'ORD-7842', customer: '山田太郎', product: '动漫手办 - 初音未来', date: '2023-06-15', amount: '¥ 12,400', status: 'completed' },
            { id: 'ORD-7841', customer: '佐藤花子', product: '限定画集 - 你的名字', date: '2023-06-15', amount: '¥ 8,900', status: 'pending' },
            { id: 'ORD-7840', customer: '铃木一郎', product: '蓝光碟 - 鬼灭之刃', date: '2023-06-14', amount: '¥ 21,500', status: 'completed' },
            { id: 'ORD-7839', customer: '高桥美咲', product: '周边T恤 - 咒术回战', date: '2023-06-14', amount: '¥ 5,600', status: 'cancelled' },
            { id: 'ORD-7838', customer: '田中健太', product: '漫画全集 - 海贼王', date: '2023-06-13', amount: '¥ 15,800', status: 'processing' },
            { id: 'ORD-7837', customer: '伊藤由美', product: '海报套装 - 进击的巨人', date: '2023-06-13', amount: '¥ 3,200', status: 'completed' },
            { id: 'ORD-7836', customer: '渡边直树', product: '模型工具套装', date: '2023-06-12', amount: '¥ 7,500', status: 'processing' },
            { id: 'ORD-7835', customer: '中村优子', product: '限定版CD - 动漫原声', date: '2023-06-12', amount: '¥ 4,300', status: 'completed' }
        ];

        // 清空表格
        ordersTableBody.innerHTML = '';

        // 添加订单行
        orders.forEach((order, index) => {
            const row = document.createElement('tr');
            row.style.animationDelay = `${index * 0.1}s`;
            row.classList.add('fade-in-row');
            
            // 状态标签
            let statusBadge = '';
            switch(order.status) {
                case 'completed':
                    statusBadge = '<span class="badge badge-completed">已完成</span>';
                    break;
                case 'pending':
                    statusBadge = '<span class="badge badge-pending">待处理</span>';
                    break;
                case 'cancelled':
                    statusBadge = '<span class="badge badge-cancelled">已取消</span>';
                    break;
                case 'processing':
                    statusBadge = '<span class="badge badge-processing">处理中</span>';
                    break;
            }
            
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.customer}</td>
                <td>${order.product}</td>
                <td>${order.date}</td>
                <td>${order.amount}</td>
                <td>${statusBadge}</td>
                <td class="action-cell">
                    <button class="table-btn btn-view" data-id="${order.id}">查看</button>
                    <button class="table-btn btn-edit" data-id="${order.id}">编辑</button>
                    <button class="table-btn btn-delete" data-id="${order.id}">删除</button>
                </td>
            `;
            
            ordersTableBody.appendChild(row);
        });

        // 添加行动画
        const rows = document.querySelectorAll('.fade-in-row');
        rows.forEach(row => {
            row.style.opacity = '0';
            row.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                row.style.transition = 'all 0.5s ease-out';
                row.style.opacity = '1';
                row.style.transform = 'translateX(0)';
            }, 100);
        });
    }

    // 退出登录
    logoutBtn.addEventListener('click', function() {
        localStorage.setItem('isLoggedIn', 'false');
        adminDashboard.style.display = 'none';
        loginPage.style.display = 'flex';
        loginForm.reset();
        
        // 重置按钮状态
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
        loginBtn.disabled = false;
    });

    // 刷新订单
    refreshBtn.addEventListener('click', function() {
        // 添加旋转动画
        const icon = this.querySelector('i');
        icon.style.transition = 'transform 0.5s';
        icon.style.transform = 'rotate(360deg)';
        
        setTimeout(() => {
            icon.style.transform = 'rotate(0)';
        }, 500);
        
        loadOrdersData();
    });

    // 导出订单
    exportBtn.addEventListener('click', function() {
        alert('订单数据导出功能将在实际应用中实现');
    });

    // 实时验证
    usernameInput.addEventListener('input', function() {
        usernameError.textContent = '';
        this.parentElement.classList.remove('error');
    });

    passwordInput.addEventListener('input', function() {
        usernameError.textContent = '';
        this.parentElement.classList.remove('error');
    });
});