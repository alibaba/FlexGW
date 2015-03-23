(function () {
    $("#showpass").bind('click', function (event) {
        event.preventDefault();
        if ($("#password")[0].type == 'password') {
            $("#password")[0].type = 'text';
            $("#showpass").html('隐藏密码');
        } else {
            $("#password")[0].type = 'password';
            $("#showpass").html('显示密码');
        }
    });
})();
