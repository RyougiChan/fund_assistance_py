$(
    () => {
        const snackbar = mdc.snackbar.MDCSnackbar.attachTo(document.querySelector('.mdc-snackbar'));
        const textFields = document.querySelectorAll('.mdc-text-field');
        textFields.forEach(t => {
            mdc.textField.MDCTextField.attachTo(t);
        });
        let showSnackbar = (label) => {
            snackbar.labelText = label;
            snackbar.open();
        }
        let chivesSignin = () => {
            let login_name = $('input[name=login_name]').val();
            let login_password = $('input[name=login_password]').val();
            if (!login_name || !login_password || !login_name.trim() || !login_password.trim()) {
                showSnackbar('EMPTY INPUT!');
                return;
            }
            if (!/^\w{4,}$/.test(login_name) || !/^\w{8,}$/.test(login_password)) {
                showSnackbar('INVALID PATTERN OF INPUT');
                return;
            }
            $.ajax({
                url: '/analysis/api/chives/signin',
                method: 'POST',
                headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
                contentType: 'application/json;charset=utf-8',
                data: JSON.stringify({
                    'login_name': login_name,
                    'login_password': login_password
                }),
                success(resp, textStatus, request) {
                    if (request.readyState === 4 && request.status === 200) {
                        if (resp && resp.error_code === 0) {
                            localStorage.setItem('cirno-fund-jwt-token', request.getResponseHeader('authorization'));
                            showSnackbar(resp.message);
                            location.replace('/analysis/')
                        } else {
                            showSnackbar(resp.message);
                        }
                    } else {
                        console.log(resp, request);
                        showSnackbar('Invaild http state');
                    }
                },
                error(err) {
                    showSnackbar("Request error");
                    console.error(err);
                    if (err.status === 500) {
                        location.replace('/error');
                        return;
                    }
                }
            })
        }
        const CLICK_HANDER = new Map()
            .set('chives-signin', chivesSignin);
        $('button').on('click', function() {
            let action = $(this).attr('data-action');
            console.log($(this), action)
            if (action && CLICK_HANDER.get(action)) CLICK_HANDER.get(action)();
        });
    }
)