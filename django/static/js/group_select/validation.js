// バリデーション関数
function validateCreateGroupName(name) {
    if (!name || name.trim() === '') {
        return 'グループ名を入力してください。';
    }
    if (name.length > 20) {
        return 'グループ名は20文字以内で入力してください。';
    }
    return '';
}

function validateJoinGroupName(name) {
    if (!name || name.trim() === '') {
        return 'グループ名を入力してください。';
    }
    return '';
}

function validateCreatePassword(password) {
    if (!password || password.trim() === '') {
        return '合言葉を入力してください。';
    }
    if (password.length < 8) {
        return '合言葉は8文字以上で入力してください。';
    }

    return '';
}

function validateJoinPassword(password) {
    if (!password || password.trim() === '') {
        return '合言葉を入力してください。';
    }
    return '';
}

document.addEventListener('DOMContentLoaded', function() {
    // グループ作成フォームのバリデーション
    const createForm = document.querySelector('#create form');
    if (createForm) {
        createForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('グループ作成フォームのバリデーション');

            const groupName = this.querySelector('[name="new_group_name"]').value;
            const password = this.querySelector('[name="new_group_password"]').value;

            const nameError = validateCreateGroupName(groupName);
            console.log(nameError);
            const passwordError = validateCreatePassword(password);

            // エラーメッセージをクリア
            const errorMessages = this.querySelectorAll('.error-message');
            errorMessages.forEach(msg => msg.remove());

            let hasError = false;

            if (nameError) {
                const nameInput = this.querySelector('[name="new_group_name"]');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.textContent = nameError;
                nameInput.parentNode.appendChild(errorDiv);
                hasError = true;
            }

            if (passwordError) {
                const passwordInput = this.querySelector('[name="new_group_password"]');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.textContent = passwordError;
                passwordInput.parentNode.appendChild(errorDiv);
                hasError = true;
            }

            if (!hasError) {
                this.submit();
            }
        });
    }

    // グループ参加フォームのバリデーション
    const joinForm = document.querySelector('#join form');
    if (joinForm) {
        joinForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const groupName = this.querySelector('[name="group_name"]').value;
            const password = this.querySelector('[name="group_password"]').value;

            const nameError = validateJoinGroupName(groupName);
            const passwordError = validateJoinPassword(password);

            // エラーメッセージをクリア
            const errorMessages = this.querySelectorAll('.error-message');
            errorMessages.forEach(msg => msg.remove());

            let hasError = false;

            if (nameError) {
                const nameInput = this.querySelector('[name="group_name"]');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.textContent = nameError;
                nameInput.parentNode.appendChild(errorDiv);
                hasError = true;
            }

            if (passwordError) {
                const passwordInput = this.querySelector('[name="group_password"]');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.textContent = passwordError;
                passwordInput.parentNode.appendChild(errorDiv);
                hasError = true;
            }

            if (!hasError) {
                this.submit();
            }
        });
    }
});