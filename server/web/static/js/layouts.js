$(document).ready(function() {
  var addModal = $("#add-layout-modal");

  // TODO: add to own file and import on base
  function addHelp(helpMessages, div) {
    div.addClass("has-error");
    var help = $.map(helpMessages, function(entry) {
      var span = "<span id=\"help\" class=\"help-block\">";
      span += entry;
      span += "</span>";
      return span;
    });
    div.append(help);
  }

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
    form.find(".has-error").find("span").remove();
    form.find(".has-error").removeClass("has-error");
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
