$(document).ready(function() {
  var addModal = $("#add-layout-modal");

  // Show add layout modal
  $(this).on("click", "#add-layout-btn", function(event) {
    event.preventDefault();
    addModal.modal("show");
  });

  // Dismiss add layout modal
  $(this).on("click", "#add-dismiss-btn", function(event) {
    event.preventDefault();
    $("#add-layout-modal").modal("hide");
    var form = $("#add-layout-form");
    form.find("#name").val("");
    form.find("#layout").val("");
    removeHelp(form);
  });

  // Handle add layout form submit
  $(this).on("submit", "#add-layout-form", function(event) {
    event.preventDefault();
    var form = $(this);
    // Get rid of errors
    removeHelp(form);

    var url = form.attr("action");
    var name = form.find("#name");
    var layout = form.find("#layout");
    $.post(url, form.serialize())
    .success(function(resp) {
      if (resp == "OK") {
        name.val("");
        layout.val("");
        addModal.modal("hide");
        location.reload();
      } else {
        var div;
        if (resp.name) {
          div = name.parent();
          addHelp(resp.name, div);
        }
        if (resp.layout) {
          div = layout.parent();
          addHelp(resp.layout, div);
        }
      }
    });
  });
});
