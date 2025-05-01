'use strict'; {

    document.addEventListener('DOMContentLoaded', function() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');

        // タブ切り替えの関数
        function switchTab(tabId) {
            // タブボタンのアクティブ状態を切り替え
            tabButtons.forEach(btn => {
                btn.classList.remove('active-tab');
                if (btn.getAttribute('data-tab') === tabId) {
                    btn.classList.add('active-tab');
                }
            });

            // タブコンテンツの表示/非表示を切り替え
            tabContents.forEach(content => {
                content.classList.remove('active-tab-content');
                if (content.getAttribute('data-content') === tabId) {
                    content.classList.add('active-tab-content');
                }
            });

            // URLにタブの状態を反映
            const url = new URL(window.location.href);
            url.searchParams.set('action', tabId);
            window.history.pushState({}, '', url);
        }

        // タブボタンのクリックイベント設定
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.getAttribute('data-tab');
                switchTab(tabId);
                window.location.reload();

            });
        });

        // 初期状態の設定
        const urlParams = new URLSearchParams(window.location.search);
        const initialTab = urlParams.get('action');
        if (initialTab) {
            switchTab(initialTab);
        }
    });
}