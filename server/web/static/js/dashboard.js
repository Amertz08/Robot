$(document).ready(function() {
  // Show add facility modal
  $(this).on("click", "#add-facility-btn", function(event) {
    event.preventDefault();
    $("#add-facility-modal").modal("show");
  });

  // Handle add facility
  $(this).on("submit", "#add-facility-form", function(event) {
    event.preventDefault();
    $.post('/dashboard/facility/add', $(this).serialize())
    .success(function(resp) {
      if (resp !== 'OK') {
        if (resp.name) {
          var div = $("#add-facility-form").find("#name").parent();
          div.addClass("has-error");

          // Get all errors and append
          var help = $.map(resp.name, function(entry) {
            var span = '<span id="help" class="help-block">';
            span += entry;
            span += '</span>';
            return span;
          });
          div.append(help);
        }
      } else {
        location.reload();
      }
    });
  });

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

  // Update facility
  $(this).on("submit", "#edit-facility-form", function(event) {
    event.preventDefault();
    $("#edit-facility-modal").modal("hide");

    var form = $("#edit-facility-form");
    var name = form.find("#name").val();
    var id = form.find("#facility_id").val();
    var token = form.find("#csrf_token").val();
    var data = {
      'name': name,
      'csrf_token': token,
      'facility_id': id
    };

    $.post('/dashboard/facility/edit', data)
    .success(function(resp) {
      if (resp !== 'OK') {
        console.log(resp);
      } else {
        location.reload();
      }
    });
  });

  // Delete row
  facilityRows.find("i.glyphicon-remove")
  .on("click", function(event) {
    event.preventDefault();
    var token = $(this).data("csrf");
    var row = $(this).parents("tr");
    var name = row.data("name");
    var id = row.data("id");
    var data = {
      'name': name,
      'csrf_token': token
    };

    $.post('/dashboard/facility/delete', data)
    .success(function(resp) {
      if (resp !== 'OK') {
        console.log(resp);
        alert('Unable to delete facility. Check console');
      } else {
        location.reload();
      }
    })
  });
});
