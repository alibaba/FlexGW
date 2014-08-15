$(function() {
  $(document).on('click', 'button.snat-del', function() {
    var tr = $(this).closest("tr");
    $.ajax({
      type: 'POST',
      url: '/snat/del',
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: {
        source: tr.find(".snat-source").text(),
        gateway: tr.find(".snat-gateway").text()
      },
      success: function(res, status, xhr) {
        if (status === "success") {
          tr.fadeOut();
        }
        var alertBox = '<div data-alert class="alert-box {{ category }}">' +
                       '删除SNAT 规则成功：' +
                       res.rules.source + ' ==> ' + res.rules.gateway +
                       '<a href="#" class="close">&times;</a></div>'
        $(".alert-box").remove();
        $("#snat-list").prepend(alertBox).foundation();
      },
      error: function(xhr, status, err) {
        console.error('Del snat failure: ' + err);
      }
    });
  });
});
