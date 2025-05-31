// バリデーション関数
function validateEmail(email) {
    if (!email || email.trim() === '') {
        return 'メールアドレスを入力してください。';
    }

    return '';
}

function validatePassword(password) {
    if (!password || password.trim() === '') {
        return 'パスワードを入力してください。';
    }
    return '';
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form[action*="login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = this.querySelector('[name="email"]').value;
            const password = this.querySelector('[name="password"]').value;

            const emailError = validateEmail(email);
            const passwordError = validatePassword(password);

            // エラーメッセージをクリア
            const errorMessages = this.querySelectorAll('.error-message');
            errorMessages.forEach(msg => {
                msg.textContent = '';
                msg.className = 'error-message';
            });

            let hasError = false;

            if (emailError) {
                const errorDiv = this.querySelector('[name="email"]').parentNode.querySelector('.error-message');
                errorDiv.textContent = emailError;
                hasError = true;
            }

            if (passwordError) {
                const errorDiv = this.querySelector('[name="password"]').parentNode.querySelector('.error-message');
                errorDiv.textContent = passwordError;
                hasError = true;
            }

            if (!hasError) {
                this.submit();
            }
        });
    }
});