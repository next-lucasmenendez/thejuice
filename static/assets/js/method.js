$(document).ready(function() {
	var labels = $('#methods label');

	labels.on('click', function () {
		var _this = $(this);
		if (_this.css('opacity') == 1) {
			labels.css("border", "none");
			setTimeout(function () {
				if (_this.hasClass('selected')) {
					_this.removeClass('selected');
				} else {
					_this.css("border", "3px solid #0085AC").addClass('selected');
				}
			}, 100);
		}
	});
});
