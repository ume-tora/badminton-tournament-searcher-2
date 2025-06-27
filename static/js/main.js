// バドミントン大会サーチサイト メインJavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // CSRFトークンの設定
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        // Ajaxリクエスト用のCSRFトークン設定
        const token = csrfToken.value;
        
        // fetch APIでのCSRF対応
        const originalFetch = window.fetch;
        window.fetch = function(url, options = {}) {
            if (options.method && options.method.toUpperCase() !== 'GET') {
                options.headers = options.headers || {};
                options.headers['X-CSRFToken'] = token;
            }
            return originalFetch(url, options);
        };
    }
    
    // お気に入り機能
    initializeFavoriteButtons();
    
    // 検索フォームの強化
    enhanceSearchForms();
    
    // ツールチップの初期化
    initializeTooltips();
    
    // スムーススクロール
    initializeSmoothScroll();
    
    // レスポンシブ画像の遅延読み込み
    initializeLazyLoading();
});

/**
 * お気に入りボタンの初期化
 */
function initializeFavoriteButtons() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            toggleFavorite(this);
        });
    });
}

/**
 * お気に入りの切り替え
 */
async function toggleFavorite(button) {
    const tournamentId = button.dataset.tournamentId;
    const icon = button.querySelector('i');
    
    // ローディング状態
    const originalContent = button.innerHTML;
    button.innerHTML = '<span class="loading"></span>';
    button.disabled = true;
    
    try {
        const response = await fetch(`/tournaments/tournament/${tournamentId}/favorite/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            updateFavoriteButton(button, data.is_favorited);
            showToast(data.message, 'success');
        } else {
            throw new Error('サーバーエラー');
        }
    } catch (error) {
        console.error('お気に入り更新エラー:', error);
        showToast('お気に入りの更新に失敗しました。', 'error');
    } finally {
        button.innerHTML = originalContent;
        button.disabled = false;
    }
}

/**
 * お気に入りボタンの表示更新
 */
function updateFavoriteButton(button, isFavorited) {
    const icon = button.querySelector('i');
    
    if (isFavorited) {
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
        button.classList.remove('btn-outline-danger');
        button.classList.add('btn-danger');
    } else {
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
        button.classList.remove('btn-danger');
        button.classList.add('btn-outline-danger');
    }
    
    // アニメーション効果
    button.style.transform = 'scale(1.2)';
    setTimeout(() => {
        button.style.transform = 'scale(1)';
    }, 200);
}

/**
 * 検索フォームの強化
 */
function enhanceSearchForms() {
    const searchForms = document.querySelectorAll('form[method="get"]');
    
    searchForms.forEach(form => {
        const inputs = form.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', debounce(function() {
                // 自動検索などの機能をここに追加可能
            }, 500));
        });
    });
}

/**
 * トーストメッセージの表示
 */
function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // 自動削除
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

/**
 * トーストコンテナの取得または作成
 */
function getOrCreateToastContainer() {
    let container = document.querySelector('.toast-container');
    
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    return container;
}

/**
 * ツールチップの初期化
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * スムーススクロールの初期化
 */
function initializeSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * 遅延読み込みの初期化
 */
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // フォールバック
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

/**
 * デバウンス関数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 日付フォーマット関数
 */
function formatDate(date, format = 'YYYY-MM-DD') {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day);
}

/**
 * 文字列のエスケープ
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

/**
 * 検索ハイライト機能
 */
function highlightSearchTerms(text, searchTerm) {
    if (!searchTerm || searchTerm.length < 2) return text;
    
    const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

/**
 * 正規表現エスケープ
 */
function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// エクスポート（モジュール環境用）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        toggleFavorite,
        showToast,
        formatDate,
        escapeHtml,
        highlightSearchTerms
    };
}