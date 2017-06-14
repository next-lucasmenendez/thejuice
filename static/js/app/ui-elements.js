/**
 * Created by lucas.menendez on 17/5/17.
 */

var app = angular.module('app');


/**
 * Spinner, Notification and Route Controllers
 */
app.controller('spinnerCtrl', function ($scope, $timeout) {
	$scope.show = function(e, msg) {
		$scope.spinner = {
			show: true,
			msg: msg
		}
	}

	$scope.hide = function() {
		$timeout(function (){
			$scope.spinner = {show: false}
		}, 1000);
	}

	$scope.$on('showSpinner', $scope.show);
	$scope.$on('hideSpinner', $scope.hide);
});

app.controller('notificationCtrl', function ($scope, $timeout) {
	$scope.show = function(e, msg) {
		$scope.notification = {
			show: true,
			msg: msg
		}

		$timeout(function () {
			$scope.notification.show = false;
		}, 2000);
	}

	$scope.$on('showNotification', $scope.show);
});

app.controller('routeCtrl', function ($scope) {
	$scope.route = false;
	function setRoute(e, route) {
		$scope.route = route;
	}

	$scope.$on('setRoute', setRoute);
});

app.service('route', function ($rootScope, $timeout) {
	var route = {
		prev:		false,
		current:	false,
		next:		false
	};

	this.Link = function(name, alias, uri, params) {
		return {
			type: 'link',
			uri: uri,
			params: params || {},
			name: name,
			alias: alias
		}
	};

	this.Button = function(name, alias, func) {
		return {
			type: 'button',
			func: func,
			name: name,
			alias: alias
		}
	};

	function set(pos, item) {
		var pos_chk		= (pos == "prev" || pos == "current" || pos == "next"),
			type_chk	= (item.type == 'link' || item.type == 'button');

		if (pos_chk && type_chk) {
			route[pos] = item;
		}
	}
	this.setPrev = function(item) {
		set('prev', item);
	}

	this.setCurrent = function(item) {
		set('current', item);
	}

	this.setNext = function(item) {
		set('next', item);
	}

	this.clear = function() {
		route = {
			prev:		false,
			current:	false,
			next:		false
		}
	};

	this.apply = function() {
		$timeout(function() {
			$rootScope.$broadcast('setRoute', route);
		});
	}
});


/**
 * Directives
 */
app.directive("contenteditable", function() {
	return {
		restrict: "A",
		require: "ngModel",
		link: function(scope, element, attrs, ngModel) {
			function read() {
				ngModel.$setViewValue(element.html());
			}

			ngModel.$render = function() {
				element.html(ngModel.$viewValue || "");
			};

			element.bind("blur keyup change", function() {
				scope.$apply(read);
			});
		}
	};
});

app.directive("autosuggestions", function($rootScope, $compile, $timeout, requests) {
	return {
		restrict: "E",
		replace: true,
		scope: {
            query: '=',
			items: "=",
			lang: '=',
			search: '&',
			submit: '&'
        },
		templateUrl: "/static/templates/autosuggestions.html",
		link: function (scope, elem) {
			scope.$watch('items', function (newValues, oldValues) {
				if (newValues != oldValues) {
					$timeout(function () {
						scope.searchAvalible = false;
						scope.current = false;
						scope.results = newValues;
						scope.$apply();
					});
				}
			});

			scope.$watch('query', function (newValue, oldValue) {
				if (newValue != oldValue) {
					if (newValue.length > 2) {
						var uri = '/autosuggest/' + newValue;

						requests.call('GET', uri, {lang: scope.lang}).then(
							function (result) {
								$timeout(function () {
									scope.searchAvalible = true;
									scope.current = false;
									scope.results = result.results;
									scope.$apply();
								});
							},
							function (error) {
								$timeout(function () {
									scope.searchAvalible = false;
									scope.current = false;
									scope.results = false;
									scope.$apply();
								});
							}
						)
					} else {
						$timeout(function () {
							scope.searchAvalible = false;
							scope.current = false;
							scope.results = false;
							scope.$apply();
						});
					}
				}
			});

			var current = false;
			elem.parent().on("keydown", function (e) {
				var key = e.keyCode || e.which,
					up = 38,
					down = 40,
					enter = 13;

				if (scope.results) {
					var old 	= current,
						first	= 0,
						last	= scope.results.length - 1;

					if (current === false) { // Activate key selection
						if (key == up) {
							current = last;
						} else if (key == down) {
							current = first;
						}
					} else { // Regular behaviour
						if (key == up) {
							current = (current > first) ? current - 1 : last;
						} else if (key == down) {
							current = (current < last) ? current + 1 : first;
						} else if (key == enter) {
							scope.chooseItem(current);
						}
					}
					if (current !== false) scope.changeItem(old, current);
				}
			});

			scope.changeItem = function (old, index) {
				if (old !== false) scope.results[old].active = false;
				scope.results[index].active = true;

				var current_elem = document.getElementById("result" + scope.results[index].id);
				elem.scrollTop(current_elem.offsetTop);
				scope.$apply();
			}

			scope.chooseItem = function(index) {
				var q = scope.results[index].name;
				scope.callback({name: q});
			}
		}
	}
})