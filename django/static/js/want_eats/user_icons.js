// ユーザーアイコンの色を管理
const COLORS = [
    'bg-user-icon-1',
    'bg-user-icon-2',
    'bg-user-icon-3',
    'bg-user-icon-4',
    'bg-user-icon-5',
    'bg-user-icon-6',
    'bg-user-icon-7',
    'bg-user-icon-8',
    'bg-user-icon-9',
    'bg-user-icon-10',
];

/**
 * ユーザーアイコンのCSSクラスを取得
 * @param {string|number} iconCode - icon code (1-10)
 * @returns {string} 対応するCSSクラス
 */
function getIconClass(iconCode) {
    const index = parseInt(iconCode) - 1;
    return COLORS[index] || COLORS[0]; // 無効な場合は最初の色を使用
}

/**
 * ユーザーアイコンの色を設定
 */
function initializeUserIcons() {
    document.querySelectorAll('[data-icon-code]').forEach(element => {
        const iconCode = element.dataset.iconCode;
        element.classList.add(getIconClass(iconCode));
    });
}

// ページ読み込み時にユーザーアイコンの色を設定
document.addEventListener('DOMContentLoaded', initializeUserIcons);