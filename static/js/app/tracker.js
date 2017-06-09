/**
 * Created by lucas.menendez on 7/6/17.
 */

var app = angular.module('app');

app.service('tracker', function ($window) {
	this.all = function (location, action, data) {
		this.ga(location, action, data);
		this.fb(location, action, data);
	}

	this.ga = function (location, action, data) {
		$window.ga('send', 'event', location, action, data);
	}

	this.fb = function (location, action, data) {
		$window.fbq('track', location, {
			action: action,
			value: data
		});
	}
});