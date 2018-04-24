$(document).ready(function() {
  // Show add user modal
  $(this).on("click", "#add-user-btn", function(event) {
    event.preventDefault();
    $("#add-user-modal").modal("show");
  });

  // Handle add user
  $(this).on("submit", "#add-user-form", function(event) {
    event.preventDefault();
    var url = $("#add-user-form").attr("action");
    $.post(url, $(this).serialize())
    .success(function(resp) {
      if (resp !== "OK") {
        if (resp.name) {
          var div = $("#add-user-form").find("#name").parent();
          div.addClass("has-error");

          // Get all errors and append
          var help = $.map(resp.name, function(entry) {
            var span = "<span id=\"help\" class=\"help-block\">";
            span += entry;
            span += "</span>";
            return span;
          });
          div.append(help);
        }
      } else {
        location.reload();
      }
    });
  });

  var userRows = $(this).find("[id^=users_]");

  // Delete row
  userRows.find("i.glyphicon-remove")
  .on("click", function(event) {
    event.preventDefault();
    var token = $(this).siblings("input#csrf_token").val()
    var url = $(this).data("url");
    var row = $(this).parents("tr");
    var email = row.data("email");
    var id = row.data("id");
    var data = {
      "email": email,
      "csrf_token": token
    };

    $.post(url, data)
    .success(function(resp) {
      if (resp !== "OK") {
        console.log(resp);
        alert("Unable to delete user. Check console");
      } else {
        location.reload();
      }
    })
  });
});
