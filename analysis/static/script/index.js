$(
    () => {

        const topAppBar = mdc.topAppBar.MDCTopAppBar.attachTo(document.getElementById('app-bar'));
        const drawer = mdc.drawer.MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));
        const snackbar = mdc.snackbar.MDCSnackbar.attachTo(document.querySelector('.mdc-snackbar'));
        topAppBar.setScrollTarget(document.getElementById('main-content'));
        topAppBar.listen('MDCTopAppBar:nav', () => {
            drawer.open = !drawer.open;
        });
        
        R = (() => {
            return {
                snackbarText: {
                    emptySelection: '未选择任何子项',
                    removeFailed: '移除子项失败'
                },
                showSnackbar(label) {
                    snackbar.labelText = label;
                    snackbar.open();
                }
            };
        })();

        let initCodeList = (fund_codes, fund_names) => {
            let i = 0;
            fund_codes.forEach((code) => {
                ++i;
                $('.fund-code-list').append(`
                <li class="mdc-list-item" role="checkbox" aria-checked="false">
                    <span class="mdc-list-item__ripple"></span>
                    <span class="mdc-list-item__graphic">
                        <div class="mdc-checkbox">
                            <input type="checkbox" class="mdc-checkbox__native-control" id="code-list-checkbox-item-${i}}" />
                            <div class="mdc-checkbox__background">
                                <svg class="mdc-checkbox__checkmark"
                                    viewBox="0 0 24 24">
                                <path class="mdc-checkbox__checkmark-path"
                                        fill="none"
                                        d="M1.73,12.91 8.1,19.28 22.79,4.59"/>
                                </svg>
                                <div class="mdc-checkbox__mixedmark"></div>
                            </div>
                            </div>
                    </span>
                    <label class="mdc-list-item__text" for="code-list-checkbox-item-${i}">${fund_names[i-1]}-${code}</label>
                </li>
                `);
            });
        };

        let getData = (name) => {
                    
                    $.ajax({
                        url: '/analysis/api/data/' + name,
                        method: 'GET',
                        success(resp) {
                            let $nextActivate = $('.figure-container[data-hook=' + name + ']');
                            resp.data.forEach(n => {
                                $nextActivate.find('.figure-list').append(`<li><img class="figure-thumbnail" src="/static/image/${name}/${n}.png" title="${n}" data-type="${name}" /></li>`);
                                $nextActivate.attr('data-fetch', 'true');
                            });
    
                            if (!$nextActivate.hasClass('page--activated')) {
                                $nextActivate.addClass('page--activated');
                            }
                        }
                    });
                };
        let getConfigData = () => {
            let config;
            if (localStorage.getItem('ryougi-fund-simulation-config')) {
                config = JSON.parse(localStorage.getItem('ryougi-fund-simulation-config'));
                initCodeList(config.fund.code_list, config.fund.code_name_list);
            } else {
                $.ajax({
                    url: '/analysis/api/data/config',
                    method: 'GET',
                    success(resp) {
                        let fund_codes = resp.data.fund.code_list,
                            fund_names = resp.data.fund.code_name_list;
                        if (fund_codes) {
                            localStorage.setItem('ryougi-fund-simulation-config', JSON.stringify(resp.data));
                            initCodeList(fund_codes, fund_names);
                        }
                    }
                });
            }
        };

        $('.mdc-drawer .mdc-list').on('click', function (e) {
            drawer.open = false;
            if (e.target.nodeName === 'A') {
                $('.page--activated').fadeOut();
                $('.page--activated').removeClass('page--activated')
                $('.mdc-top-app-bar__title').text($(e.target).find('.mdc-list-item__text').text());
                let $nextActivate = $('.figure-container[data-hook=' + $(e.target).attr('data-hook') + ']');
                $nextActivate.addClass('page--activated');
                if ($nextActivate.attr('data-fetch') === 'false') {
                    switch ($nextActivate.attr('data-type')) {
                        case 'figure':
                            getData($nextActivate.attr('data-hook'));
                            break;
                        case 'config':
                            getConfigData();
                            break;
                    }
                    $nextActivate.attr('data-fetch', 'true');
                }
                $nextActivate.fadeIn();

            }
        });
        $(document.body).on('MDCDrawer:closed', () => {
            $('.main-content').find('input, button').focus();
        });
        $('.figure-list').on('click', '.figure-thumbnail', function (e) {
            let name = $(this).attr('title').split('.')[0];
            $('.figure>iframe').attr('src', `/static/html/${$(this).attr('data-type')}/${name}.html`);
            $('.figure').fadeIn();
        });
        $('.figure').on('click', function (e) {
            if (e.currentTarget.nodeName !== 'IFRAME') {
                $(this).fadeOut();
            }
        });
        let removeConfigFund = () => {
            let $collected = $('.fund-code-list .mdc-checkbox input[type=checkbox]:checked');
            if (!$collected.length) R.showSnackbar(R.snackbarText.emptySelection);
            let data = [...$collected].map(ele => $(ele).parents('.mdc-list-item').children('.mdc-list-item__text').text().trim()),
                config = JSON.parse(localStorage.getItem('ryougi-fund-simulation-config')),
                code_list = config.fund.code_list, 
                code_name_list = config.fund.code_name_list;
            data.forEach(d => {
                let t = d.split('-'),
                    fund_name = t[0],
                    fund_code = t[1],
                    i = code_list.indexOf(fund_code);
                code_list.splice(i, i+1);
                code_name_list.splice(i, i+1);
            });
            config.fund.code_list = code_list;
            config.fund.code_name_list = code_name_list;
            localStorage.setItem('ryougi-fund-simulation-config', JSON.stringify(config));
            [...$collected].forEach(ele => $(ele).parents('.mdc-list-item').remove());
            R.showSnackbar('移除子项成功');
        };
        let addConfigFund = () => {
            
        };
        const CLICK_HANDER = new Map().set('remove-config-fund', removeConfigFund);
        $('button').on('click', function() {
            let action = $(this).attr('data-action');

            if(action && CLICK_HANDER.get(action)) CLICK_HANDER.get(action)();
        });
        getData('simulation_trade');

    }
);