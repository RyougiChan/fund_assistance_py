$(
    () => {

        const topAppBar = mdc.topAppBar.MDCTopAppBar.attachTo(document.getElementById('app-bar'));
        const drawer = mdc.drawer.MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));
        const snackbar = mdc.snackbar.MDCSnackbar.attachTo(document.querySelector('.mdc-snackbar'));
        const textField = mdc.textField.MDCTextField.attachTo(document.querySelector('#add-new-fund-codes'));
        const linearProgress = mdc.linearProgress.MDCLinearProgress.attachTo(document.querySelector('.mdc-linear-progress'));
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
        let getStsAccessCredential = (async = true) => {
            let result;
            let credential = localStorage.getItem('cirno-fund-oss-credential');
            if (credential && credential !== 'undefined') {
                result = JSON.parse(localStorage.getItem('cirno-fund-oss-credential'));
                store = new OSS({
                    accessKeyId: result.AccessKeyId,
                    accessKeySecret: result.AccessKeySecret,
                    stsToken: result.SecurityToken,
                    region: 'oss-cn-hongkong',
                    bucket: 'cirno-fund-assistance',
                    // 30 minutes
                    refreshSTSTokenInterval: 1800000,
                    refreshSTSToken: async () => {
                        await fetch('api/security/credential', {
                            headers: { 'authorization': localStorage.getItem('cirno-fund-jwt-token') },
                        })
                        .then(response => response.json())
                        .then(d => {
                            localStorage.setItem('cirno-fund-oss-credential', JSON.stringify(d.data.Credentials));
                            let st = setTimeout(() => {
                                localStorage.removeItem('cirno-fund-oss-credential');
                                clearTimeout(st);
                            }, 1800000);
                            return {
                                accessKeyId: d.data.Credentials.AccessKeyId,
                                accessKeySecret: d.data.Credentials.AccessKeySecret,
                                stsToken: d.data.Credentials.SecurityToken
                            }
                        });
                    },
                });
                return;
            }
            
            $.ajax({
                url: 'api/security/credential',
                method: 'GET',
                headers: { 'authorization': localStorage.getItem('cirno-fund-jwt-token') },
                async: async,
                success(resp, textStatus, request) {
                    if (request.readyState === 4 && request.status === 200) {
                        console.log('credential', resp.data)
                        if (resp.data && resp.error_code === 0) {
                            result = resp.data.Credentials;
                            store = new OSS({
                                accessKeyId: result.AccessKeyId,
                                accessKeySecret: result.AccessKeySecret,
                                stsToken: result.SecurityToken,
                                region: 'oss-cn-hongkong',
                                bucket: 'cirno-fund-assistance',
                                // 30 minutes
                                refreshSTSTokenInterval: 1800000,
                                refreshSTSToken: async () => {
                                    await fetch('api/security/credential', {
                                        headers: { 'authorization': localStorage.getItem('cirno-fund-jwt-token') },
                                    })
                                    .then(response => response.json())
                                    .then(d => {
                                        localStorage.setItem('cirno-fund-oss-credential', JSON.stringify(d.data.Credentials));
                                        let st = setTimeout(() => {
                                            localStorage.removeItem('cirno-fund-oss-credential');
                                            clearTimeout(st);
                                        }, 1800000);
                                        return {
                                            accessKeyId: d.data.Credentials.AccessKeyId,
                                            accessKeySecret: d.data.Credentials.AccessKeySecret,
                                            stsToken: d.data.Credentials.SecurityToken
                                        }
                                    });
                                },
                            });
                            localStorage.setItem('cirno-fund-oss-credential', JSON.stringify(resp.data.Credentials));
                            let t = setTimeout(() => {
                                localStorage.removeItem('cirno-fund-oss-credential');
                                clearTimeout(t);
                            }, 1800000);
                        } else {
                            R.showSnackbar(resp.message);
                        }
                    }else {
                        console.log(resp)
                        R.showSnackbar('Failed to get credential');
                    }
                },
                error(err) {
                    R.showSnackbar('Request error!');
                    console.error(err);
                    if (err.status === 500) {
                        location.replace('/error');
                        return;
                    }
                    location.replace('/signin');
                }
            });
        };
        
        let getSignedUrl = (file) => {
            if (!store) {
                getStsAccessCredential(false);
            }
            return store.signatureUrl(file).replace('http://cirno-fund-assistance.oss-cn-hongkong.aliyuncs.com', 'http://oss.cirnon.com');
        }
        // 初始化第三页的基金列表
        let initCodeList = (fund_codes, fund_names) => {
            let i = 0;
            let j = 0;
            fund_codes.forEach((code) => {
                ++i;
                j = $('.fund-code-list>li').length + 1; // 1,2,3...
                $('.fund-code-list').append(`
                <li class="mdc-list-item" role="checkbox" aria-checked="false">
                    <span class="mdc-list-item__ripple"></span>
                    <span class="mdc-list-item__graphic">
                        <div class="mdc-checkbox">
                            <input type="checkbox" class="mdc-checkbox__native-control" id="code-list-checkbox-item-${j}}" />
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
                    <label class="mdc-list-item__text" for="code-list-checkbox-item-${j}">${fund_names[i - 1]}-${code}</label>
                </li>
                `);
            });
        };
        let initFigureList = ($nextActivate, name, data) => {
            data.forEach(n => {
                $nextActivate.find('.figure-list')
                    // .append(`<li><img class="figure-thumbnail" src="/static/image/${name}/${n}.png" title="${n}" data-type="${name}" /></li>`)
                    .append(`
                    <li data-title="${n}" data-type="${name}">
                        <div class="mdc-card demo-card">
                            <div class="mdc-card__primary-action demo-card__primary-action" tabindex="0">
                                <div class="mdc-card__media mdc-card__media--16-9 demo-card__media" style="background-image: url(&quot;${getSignedUrl('image/'+name+'/'+n+'.png')}&quot;);"></div>
                                <div class="demo-card__primary">
                                <h2 class="demo-card__title mdc-typography mdc-typography--headline6">${n.split('-')[0]}</h2>
                                <h3 class="demo-card__subtitle mdc-typography mdc-typography--subtitle2">${n.split('-')[1]}</h3>
                                </div>
                            </div>
                        </div>
                    </li>
                    `);
            });

            if (!$nextActivate.hasClass('page--activated')) {
                $nextActivate.addClass('page--activated');
            }
        };
        // 获取分析图表
        let getFigureData = (name) => {
            let data = localStorage.getItem('cirno-fund-simulation-config');
            let $nextActivate = $('.figure-container[data-hook=' + name + ']');
            if (data) {
                let res = [],
                    td = JSON.parse(data),
                    code_list = td.fund.code_list,
                    code_name_list = td.fund.code_name_list;
                for (let i = 0; i < code_list.length; i++) {
                    res.push(`${code_name_list[i]}-${code_list[i]}`);
                }
                initFigureList($nextActivate, name, res);
            }
        };
        let addFigureData = (code_list) => {
            if (!code_list) {
                R.showSnackbar('所加代码列表为空');
                return;
            }
            let localSimulationConfig = localStorage.getItem('cirno-fund-simulation-config');
            let fixed_codes = [];
            if (localSimulationConfig) {
                let lsc = JSON.parse(localSimulationConfig),
                    local_code_list = lsc.fund.code_list;

                code_list.forEach(c => {
                    if (local_code_list.indexOf(c) < 0 && c.trim() !== '') fixed_codes.push(c);
                });
                if (fixed_codes.length) {
                    $.ajax({
                        url: '/analysis/api/data/figure',
                        method: 'POST',
                        headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(), 'authorization': localStorage.getItem('cirno-fund-jwt-token') },
                        contentType: 'application/json;charset=utf-8',
                        data: JSON.stringify(fixed_codes),
                        success(resp, textStatus, request) {
                            if (request.readyState === 4 && request.status === 200) {
                                if (resp.data && resp.error_code === 0) {
                                    lsc.fund.code_list = lsc.fund.code_list.concat(resp.data.fund.code_list);
                                    lsc.fund.code_name_list = lsc.fund.code_name_list.concat(resp.data.fund.code_name_list);
                                    localStorage.setItem('cirno-fund-simulation-config', JSON.stringify(lsc));
                                    initCodeList(resp.data.fund.code_list, resp.data.fund.code_name_list);
                                    R.showSnackbar("添加成功");
                                } else {
                                    R.showSnackbar(resp.message);
                                }
                            } else {
                                console.log(resp);
                                R.showSnackbar("Invalid http state");
                            }
                        },
                        error(err) {
                            R.showSnackbar("Request error!");
                            console.error(err);
                            if (err.status === 500) {
                                location.replace('/error');
                                return;
                            }
                            location.replace('/signin');
                        }
                    });
                } else {
                    R.showSnackbar("Nothing to change!");
                }
            }

        };
        // 获取配置
        let getConfigData = () => {
            let config;
            if (localStorage.getItem('cirno-fund-simulation-config')) {
                config = JSON.parse(localStorage.getItem('cirno-fund-simulation-config'));
                initCodeList(config.fund.code_list, config.fund.code_name_list);
            } else {
                $.ajax({
                    url: '/analysis/api/data/config',
                    headers: { 'authorization': localStorage.getItem('cirno-fund-jwt-token') },
                    method: 'GET',
                    success(resp, textStatus, request) {
                        if (request.readyState === 4 && request.status === 200) {
                            if (resp.data && resp.error_code === 0) {
                                let fund_codes = resp.data.fund.code_list,
                                    fund_names = resp.data.fund.code_name_list;
                                if (fund_codes) {
                                    localStorage.setItem('cirno-fund-simulation-config', JSON.stringify(resp.data));
                                    initCodeList(fund_codes, fund_names);
                                }
                            }else {
                                R.showSnackbar(resp.message);
                            }
                        }else {
                            console.log(resp);
                            R.showSnackbar('Invalid http state');
                        }
                    },
                    error(err) {
                        R.showSnackbar('Request error!');
                        console.error(err);
                        if (err.status === 500) {
                            location.replace('/error');
                            return;
                        }
                        location.replace('/signin');
                    }
                });
            }
        };
        let store;

        $('.mdc-drawer .mdc-list').on('click', function (e) {
            drawer.open = false;
            if (e.target.nodeName === 'A') {
                $('.page--activated').fadeOut();
                $('.page--activated').removeClass('page--activated')
                $('.mdc-top-app-bar__title').text($(e.target).find('.mdc-list-item__text').text());
                let $nextActivate = $('.figure-container[data-hook=' + $(e.target).attr('data-hook') + ']');
                $nextActivate.addClass('page--activated');
                if (!localStorage.getItem('cirno-fund-simulation-config')) {
                    getConfigData();
                }

                switch ($nextActivate.attr('data-type')) {
                    case 'figure':
                        getFigureData($nextActivate.attr('data-hook'));
                        break;
                }
                $nextActivate.fadeIn();

            }
        });
        $(document.body).on('MDCDrawer:closed', () => {
            $('.main-content').find('input, button').focus();
        });
        $('.figure-list').on('click', 'li', function (e) {
            let name = $(this).attr('data-title');
            // /static/html/${$(this).attr('data-type')}/${name}.html
            $('.figure>iframe').attr('src', `${getSignedUrl('html/' + $(this).attr('data-type') + '/' + name + '.html')}`);
            $('.figure').fadeIn();
        });
        $('.figure').on('click', function (e) {
            if (e.currentTarget.nodeName !== 'IFRAME') {
                $(this).fadeOut();
            }
        });
        let removeConfigFund = () => {
            let $collected = $('.fund-code-list .mdc-checkbox input[type=checkbox]:checked');
            if (!$collected.length) {
                R.showSnackbar(R.snackbarText.emptySelection);
                return;
            }
            let data = [...$collected].map(ele => $(ele).parents('.mdc-list-item').children('.mdc-list-item__text').text().trim()),
                config = JSON.parse(localStorage.getItem('cirno-fund-simulation-config')),
                code_list = config.fund.code_list,
                code_name_list = config.fund.code_name_list;
            data.forEach(d => {
                let t = d.split('-'),
                    fund_name = t[0],
                    fund_code = t[1],
                    i = code_list.indexOf(fund_code);
                code_list.splice(i, i + 1);
                code_name_list.splice(i, i + 1);
            });
            config.fund.code_list = code_list;
            config.fund.code_name_list = code_name_list;
            localStorage.setItem('cirno-fund-simulation-config', JSON.stringify(config));
            [...$collected].forEach(ele => $(ele).parents('.mdc-list-item').remove());
            R.showSnackbar('移除子项成功');
        };
        let addConfigFund = () => {
            if (!/^(\d{6},)+$/.test(textField.value)) {
                R.showSnackbar('数据格式错误 /^(\d{6},)+$/');
                return;
            }
            addFigureData(textField.value.split(','));
        };
        let updateAllSignal = () => {
            let localSimulationConfig = localStorage.getItem('cirno-fund-simulation-config');
            if (localSimulationConfig) {
                let lsc = JSON.parse(localSimulationConfig),
                    local_code_list = lsc.fund.code_list;

                if (local_code_list.length) {
                    linearProgress.open();
                    $.ajax({
                        url: '/analysis/api/data/figure',
                        method: 'POST',
                        headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(), 'authorization': localStorage.getItem('cirno-fund-jwt-token') },
                        contentType: 'application/json;charset=utf-8',
                        data: JSON.stringify(local_code_list),
                        
                        success(resp, textStatus, request) {
                            if (request.readyState === 4 && request.status === 200) {
                                if (resp.data && resp.error_code === 0) {
                                    if (resp.data) {
                                        R.showSnackbar("更新成功");
                                    } else {
                                        R.showSnackbar("Nothing update!");
                                    }
                                }else {
                                    R.showSnackbar(resp.message);
                                }
                            }else {
                                console.log(resp);
                                R.showSnackbar('Invalid http state');
                            }
                            linearProgress.close();
                        },
                        error(err) {
                            R.showSnackbar("Nothing update!");
                            linearProgress.close();
                            console.error(err);
                            if (err.status === 500) {
                                location.replace('/error');
                                return;
                            }
                            location.replace('/signin');
                        }
                    });
                } else {
                    R.showSnackbar("Nothing to change!");
                }
            }
        }
        const CLICK_HANDER = new Map()
            .set('remove-config-fund', removeConfigFund)
            .set('add-config-fund', addConfigFund)
            .set('update-all-signal', updateAllSignal);
        $('button').on('click', function () {
            let action = $(this).attr('data-action');

            if (action && CLICK_HANDER.get(action)) CLICK_HANDER.get(action)();
        });
        getConfigData();
        getFigureData('simulation_trade');
    }
);