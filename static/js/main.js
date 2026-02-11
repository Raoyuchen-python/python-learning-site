// main.js - 网站主要JavaScript功能

document.addEventListener('DOMContentLoaded', function() {
    console.log('Python学习网站已加载');
    
    // 代码运行器功能
    const runCodeButtons = document.querySelectorAll('.run-code-btn');
    runCodeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const codeBlock = this.previousElementSibling.querySelector('code');
            if (codeBlock) {
                runPythonCode(codeBlock.textContent);
            }
        });
    });
    
    // 示例代码运行函数
    function runPythonCode(code) {
        fetch('/run_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('运行结果：\n' + data.output);
            } else {
                alert('运行错误：\n' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('请求失败，请检查网络连接');
        });
    }
    
    // 进度跟踪
    const progressButtons = document.querySelectorAll('.mark-complete');
    progressButtons.forEach(button => {
        button.addEventListener('click', function() {
            const lessonId = this.dataset.lessonId;
            updateProgress(lessonId);
        });
    });
    
    function updateProgress(lessonId) {
        fetch('/api/progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                lesson_id: lessonId,
                progress: 100
            })
        })
        .then(response => response.json())
        .then(data => {
            alert('🎉 恭喜！课程已完成！');
            // 更新按钮状态
            const button = document.querySelector(`.mark-complete[data-lesson-id="${lessonId}"]`);
            if (button) {
                button.innerHTML = '<i class="fas fa-check-circle"></i> 已完成';
                button.classList.add('completed');
                button.disabled = true;
            }
        });
    }
    
    // 代码复制功能
    const copyButtons = document.querySelectorAll('.copy-code-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const codeBlock = this.previousElementSibling.querySelector('code');
            if (codeBlock) {
                navigator.clipboard.writeText(codeBlock.textContent)
                    .then(() => {
                        const originalText = this.innerHTML;
                        this.innerHTML = '<i class="fas fa-check"></i> 已复制';
                        setTimeout(() => {
                            this.innerHTML = originalText;
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('复制失败: ', err);
                    });
            }
        });
    });
    
    // 响应式导航菜单
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('show');
        });
    }
});