// バリデーション関数
function validateName(name) {
    if (!name || name.trim() === '') {
        return '名前を入力してください。';
    }
    if (name.length > 50) {
        return '名前は50文字以内で入力してください。';
    }
    return '';
}

function validateEmail(email) {
    if (!email || email.trim() === '') {
        return 'メールアドレスを入力してください。';
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return '有効なメールアドレスを入力してください。';
    }
    return '';
}

function validatePassword(password) {
    if (!password || password.trim() === '') {
        return 'パスワードを入力してください。';
    }
    if (password.length < 8) {
        return 'パスワードは8文字以上で入力してください。';
    }
    return '';
}

function validatePasswordConfirm(password, passwordConfirm) {
    if (!passwordConfirm || passwordConfirm.trim() === '') {
        return '確認用パスワードを入力してください。';
    }
    if (password !== passwordConfirm) {
        return 'パスワードと確認用パスワードが一致しません。';
    }
    return '';
}

document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.querySelector('form[action*="signup"]');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const name = this.querySelector('[name="name"]').value;
            const email = this.querySelector('[name="email"]').value;
            const password = this.querySelector('[name="password"]').value;
            const passwordConfirm = this.querySelector('[name="password_confirm"]').value;

            const nameError = validateName(name);
            const emailError = validateEmail(email);
            const passwordError = validatePassword(password);
            const passwordConfirmError = validatePasswordConfirm(password, passwordConfirm);

            // エラーメッセージをクリア
            const errorMessages = this.querySelectorAll('.error-message');
            errorMessages.forEach(msg => {
                msg.textContent = '';
                msg.className = 'error-message';
            });

            let hasError = false;

            if (nameError) {
                const errorDiv = this.querySelector('[name="name"]').parentNode.querySelector('.error-message');
                errorDiv.textContent = nameError;
                hasError = true;
            }

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

            if (passwordConfirmError) {
                const errorDiv = this.querySelector('[name="password_confirm"]').parentNode.querySelector('.error-message');
                errorDiv.textContent = passwordConfirmError;
                hasError = true;
            }

            if (!hasError) {
                this.submit();
            }
        });
    }
});