function page_title (title) {
  $("header.main-header .page-title").text(title);
}

function breadcrumb (label, url) {
  $("header.main-header .breadcrumb").append('<li><a href="'+url+'">'+label+'</a></li>');
}

$(function () {
  select_nav("Blog");
});

function search_action (url) {
  $("#frmSearch").attr("action",url);
}

function $djform (selector) {
	$(selector).find(".form-group label").addClass("col-sm-1 control-label");
	$(selector).find(".form-group input,textarea,select").addClass("form-control");
}
