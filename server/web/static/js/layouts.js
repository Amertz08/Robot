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
  });

  // Handle add layout form submit
  $(this).on("submit", "#add-layout-form", function(event) {
    event.preventDefault();
    var form = $(this);
    // Get rid of errors
    form.find(".has-error").find("span").remove();
    
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
        var help;
        if (resp.name) {
          div = name.parent();
          div.addClass("has-error");

          help = $.map(resp.name, function(entry) {
            var span = "<span id=\"help\" class=\"help-block\">";
            span += entry;
            span += "</span>";
            return span;
          });
          div.append(help);
        }

        if (resp.layout) {
          div = layout.parent();
          div.addClass("has-error");

          help = $.map(resp.layout, function(entry) {
            var span = "<span id=\"help\" class=\"help-block\">";
            span += entry;
            span += "</span>";
            return span;
          });
          div.append(help);
        }
      }
    });
  });
});
