$(document).ready(function() {
  // Show add facility modal
  $(this).on("click", "#add-facility-btn", function(event) {
    event.preventDefault();
    $("#add-facility-modal").modal("show");
  });

  // Handle add facility
  $(this).on("submit", "#add-facility-form", function(event) {
    event.preventDefault();
    var url = $("#add-facility-form").attr("action");
    $.post(url, $(this).serialize())
    .success(function(resp) {
      if (resp !== "OK") {
        if (resp.name) {
          var div = $("#add-facility-form").find("#name").parent();
          addHelp(resp.name, div);
        }
      } else {
        location.reload();
      }
    });
  });

  // Close add facility modal
  $(this).on("click", ".add-dismiss-btn", function(event) {
    event.preventDefault();
    var form = $("#add-facility-form");
    removeHelp(form);
    form.find("#name").val("");
    $("#add-facility-modal").modal("hide");
  })

  var facilityRows = $(this).find("[id^=facility_]");

  // Show edit modal
  facilityRows.find("i.glyphicon-edit")
  .on("click", function(event) {
    event.preventDefault();
    var row = $(this).parents("tr");
    var form = $("#edit-facility-form");
    var name = row.data("name");
    var id = row.data("id");
    form.find("#name").val(name);
    form.find("#facility_id").val(id);
    $("#edit-facility-modal").modal("show");
  });

  // Close edit modal
  $(this).on("click", ".edit-dismiss-btn", function(event) {
    event.preventDefault();
    var form = $("#edit-facility-form");
    removeHelp(form);
    $("#edit-facility-modal").modal("hide");
  });

  // Update facility
  $(this).on("submit", "#edit-facility-form", function(event) {
    event.preventDefault();

    var form = $(this);
    var name = form.find("#name").val();
    var id = form.find("#facility_id").val();
    var token = form.find("#csrf_token").val();
    var data = {
      "name": name,
      "csrf_token": token,
      "facility_id": id
    };
    var url = form.attr("action");

    $.post(url, data)
    .success(function(resp) {
      if (resp !== "OK") {
        console.log(resp);
        if (resp.name) {
          var nameDiv = form.find("#name").parent();
          addHelp(resp.name, nameDiv);
        } else if (resp.facility_id) {

        } else {
          alert("Unable to update facility. Check console");
        }
      } else {
        location.reload();
      }
    });
  });

  // Delete row
  facilityRows.find("i.glyphicon-remove")
  .on("click", function(event) {
    event.preventDefault();
    var token = $(this).siblings("input#csrf_token").val()
    var url = $(this).data("url");
    var row = $(this).parents("tr");
    var name = row.data("name");
    var id = row.data("id");
    var data = {
      "name": name,
      "csrf_token": token
    };

    $.post(url, data)
    .success(function(resp) {
      if (resp !== "OK") {
        console.log(resp);
        alert("Unable to delete facility. Check console");
      } else {
        location.reload();
      }
    })
  });
});
