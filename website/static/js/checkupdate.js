(function () {
    function showMessage(message, type) {
        $('#check-update-info a.close').trigger('click.fndtn.alert');
        var alertBox = '<div data-alert id="check-update-info" class="alert-box ' +
            type + '">' + message +
            '<a href="#" class="close">&times;</a> ' + '</div>';
            $(".large-10").prepend(alertBox).foundation();
    }

    function showLoading() {
        var loading = '<div id="loading" class="alert-box loader"><img src="/static/img/loader.gif" alt="Loading..." /></div>';
        $(".large-10").prepend(loading);
    }

    function hideLoading() {
        $('#loading').remove();
    }

    $("#checkupdate").bind('click', function (event) {
        $.ajax({
            url: "/api/checkupdate",
            type: "get",
            dataType: "json",
            beforeSend: function (xhr) {
                $('#check-update-info a.close').trigger('click.fndtn.alert');
                showLoading();
            },
            success: function (res, status, xhr) {
                console.log(res);
                var message = res.message + '<a class="box-link" href="/docs/update">点此</a>查看升级方法。'
                showMessage(message, 'success');
            },
            complete: function (xhr, status) {
                hideLoading();
            },
            error: function (xhr, status, thrown) {
                var err = xhr.responseJSON;
                console.log(err);
                showMessage(err.message, 'alert');
            }
        });
    });
})();
