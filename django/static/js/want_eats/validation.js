class RecipeValidation {
    constructor(form, urlInput, errorMessage) {
        this.form = form;
        this.urlInput = urlInput;
        this.errorMessage = errorMessage;

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.form.addEventListener('submit', (e) => {
            if (!this.validateInput()) {
                e.preventDefault();
                this.urlInput.focus();
            }
        });
    }

    validateInput() {
        const value = this.urlInput.value.trim();

        if (value === '') {
            this.showError('URLを入力してください');
            return false;
        }

        if (!this.validateUrl(value)) {
            this.showError('有効なURLを入力してください（例:https://recipe.example.com/...）');
            return false;
        }

        this.clearError();
        return true;
    }

    validateUrl(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    }

    showError(message) {
        this.errorMessage.textContent = message;
    }

    clearError() {
        this.errorMessage.textContent = '';
    }
}

// ページ読み込み時にバリデーションを初期化
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addRecipeForm');
    const urlInput = document.getElementById('recipeUrl');
    const errorMessage = urlInput.parentNode.querySelector('.error-message');

    if (form && urlInput && errorMessage) {
        new RecipeValidation(form, urlInput, errorMessage);
    }
});