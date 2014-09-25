(function () {
    $("#showpass").bind('click', function (event) {
        event.preventDefault();
        if ($("#password")[0].type == 'password') {
            $("#password")[0].type = 'text';
        } else {
            $("#password")[0].type = 'password';
        }
    });
})();
