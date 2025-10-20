document.addEventListener('DOMContentLoaded', function() {
    // 图片处理
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            if (this.naturalHeight > this.clientHeight) {
                this.style.cursor = 'zoom-in';
                this.addEventListener('click', function() {
                    this.classList.toggle('zoomed');
                });
            }
        });
    });

    // 代码块增强
    const codeBlocks = document.querySelectorAll('pre');
    codeBlocks.forEach(block => {
        // 添加语言标识
        const code = block.querySelector('code');
        if (code && code.className) {
            const lang = code.className.replace('language-', '');
            if (lang) {
                block.setAttribute('data-language', lang.toUpperCase());
            }
        }
    });

    // 表格增强
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        // 添加响应式包装
        const wrapper = document.createElement('div');
        wrapper.style.overflowX = 'auto';
        wrapper.style.marginBottom = '20px';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });

    // 确保内容不超出
    function ensureContentFit() {
        const card = document.querySelector('.card');
        const content = document.querySelector('.content');
        if (card && content) {
            content.style.maxHeight = 'none';
            content.style.overflow = 'visible';
        }
    }

    ensureContentFit();
    window.addEventListener('resize', ensureContentFit);
});

// 禁用所有滚动
window.addEventListener('scroll', function(e) {
    e.preventDefault();
    window.scrollTo(0, 0);
}, { passive: false });

window.addEventListener('wheel', function(e) {
    e.preventDefault();
}, { passive: false });

window.addEventListener('touchmove', function(e) {
    e.preventDefault();
}, { passive: false });