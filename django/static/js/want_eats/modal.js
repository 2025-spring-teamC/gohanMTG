class RecipeModal {
    constructor() {
        this.modal = document.getElementById('addRecipeModal');
        this.openBtn = document.getElementById('openModalBtn');
        this.closeBtn = document.getElementById('closeModalBtn');
        this.cancelBtn = document.getElementById('cancelBtn');
        this.form = document.getElementById('addRecipeForm');
        this.urlInput = document.getElementById('recipe_url');
        this.errorMessage = this.urlInput.parentNode.querySelector('.error-message');

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // モーダルを開く
        this.openBtn.addEventListener('click', () => this.open());
        // ×ボタン
        this.closeBtn.addEventListener('click', () => this.close());
        // キャンセルボタン
        this.cancelBtn.addEventListener('click', () => this.close());
        // モーダル外クリックで閉じる
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });
    }

    open() {
        this.modal.classList.remove('hidden');
        this.modal.classList.add('flex');
        document.body.style.overflow = 'hidden';
    }
    close() {
        this.modal.classList.add('hidden');
        this.modal.classList.remove('flex');
        document.body.style.overflow = '';
        this.resetForm();
    }
    resetForm() {
        this.form.reset();
        this.clearError();
    }
    clearError() {
        if (this.errorMessage) {
            this.errorMessage.textContent = '';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new RecipeModal();
});