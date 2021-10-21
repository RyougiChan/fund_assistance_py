$(
    () => {
        let close_page = false;
        $(window).on('beforeunload', function() {
            if (close_page) {
                localStorage.removeItem('cirno-fund-oss-credential');
                localStorage.removeItem('cirno-fund-jwt-token');
            }
        })

        $(window).on('visibilitychange', function() {
            if (document.visibilityState == 'hidden') {
                close_page = true;
            }
        })
    }
)