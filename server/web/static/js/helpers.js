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
