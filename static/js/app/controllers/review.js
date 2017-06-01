/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.controller('reviewCtrl', function ($window, $rootScope, $scope, $state, $stateParams, $timeout, service, route, DataStorage) {
	$scope.$on('$stateChangeSuccess', function () {
		var prev = route.Link('Search', 'search', 'base.search'),
			current = route.Link('Review', 'review', 'base.review'),
			next = route.Button('Design', 'design', $scope.design);

		route.clear();
		route.setPrev(prev);
		route.setCurrent(current);
		route.setNext(next);
		route.apply();
	});

	$scope.showEdit	= false;
	var query = $stateParams.query;
	if (query) {
		$scope.results = DataStorage.get(query);
		$scope.lang = DataStorage.get("lang") || 'en';
	} else {
		$state.go('base.search');
	}

	if (!Boolean($scope.results)) {
		var query = $stateParams.query;

		if (query) {
			$rootScope.$broadcast('showSpinner', 'Wait a second while we take the data out of Wikipedia...');
			$window.ga('send', 'event', 'index', 'search', query);

			service.request('POST', '/review', {query: query, force: true, lang: $scope.lang}).then(
				function (response) {
					if (response.success) {
						$scope.results 	= response.result;
					} else {
						$state.go('base.search');
					}
					$rootScope.$broadcast('hideSpinner');
				},
				function (error) {
					$state.go('base.search');
					$rootScope.$broadcast('hideSpinner');
					$rootScope.$broadcast('showNotification', error.data.message);
				}
			);
		} else {
			$state.go('base.search');
		}
	}

	$scope.edit = function (hit) {
		var empty = !Boolean(hit);
		if (empty) {
			$scope.current = {}
		} else {
			$scope.current = hit;
			var datetime 	= new Date($scope.current.date),
				flag 		= $scope.current.format.flag;

			var check = parseFlag(flag);
			$scope.current.datetime = {
				day:	(check.d) ? datetime.getDate() : undefined,
				month:	(check.m) ? datetime.getMonth() + 1 : undefined,
				year:	(check.y) ? datetime.getFullYear() : undefined
			}
		}
		$scope.showEdit	= true;
	}

	$scope.closeEdit = function () {
		$scope.current	= null;
		$scope.showEdit	= false;
	}

	$scope.delete = function (hit) {
		var index = $scope.results.hits.indexOf(hit);
		$scope.results.hits.splice(index, 1);
	}

	$scope.save = function () {
		var res = parseDate($scope.current.datetime, $scope.lang);
		$scope.current.date = res.date;
		if ($scope.current.hasOwnProperty('format')) {
			$scope.current.format['flag'] = res.flag;
		} else {
			$scope.current.format = {flag: res.flag};
		}

		if (!$scope.current.hasOwnProperty('$$hashKey')) {
			$scope.results.hits.push(angular.copy($scope.current));
		}
		$scope.showEdit	= false;
	}

	$scope.sortByDate = function(hit) {
		return new Date(hit.date);
	}

	$scope.design = function() {
		var query = $stateParams.query || $scope.query;
		if ($scope.results && query) {
			DataStorage.set(query, $scope.results);
			DataStorage.set("lang", $scope.lang);
			$state.go('base.design', {query: query});
		}
	}

	function parseFlag (flag) {
		var y = flag % 10,
			f = Math.floor(flag / 10),
			m = f % 10,
			d = Math.floor(f / 10);

		return {
			d: Boolean(d),
			m: Boolean(m),
			y: Boolean(y)
		}
	}

	function parseDate(datetime, lang) {
		moment.updateLocale(lang || 'en');
		var fmt		= "",
			flag	= 0,
			date	= moment();

		if (datetime.day && datetime.month) {
			fmt += "D ";
			flag += 1;
			date.date(datetime.day);
		}

		if (datetime.month) {
			fmt += "MMMM ";
			flag = (flag * 10) + 1;
			date.month(datetime.month - 1);
		}

		if (datetime.year) {
			fmt += "YYYY";
			flag = (flag * 10) + 1;
			date.year(datetime.year);
		}

		return {
			date: date.format(fmt),
			flag: flag
		}
	}
});
