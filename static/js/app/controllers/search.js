/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module('app');


app.controller('searchCtrl', function ($window, $rootScope, $scope, $state, service, tracker, route, DataStorage) {
	$scope.$on('$stateChangeSuccess', function () {
		var current = route.Link('Search', 'search', 'base.search');

		route.clear();
		route.setCurrent(current);
		route.apply();
		DataStorage.clear()
	});

	$scope.lang = "en";
	$scope.query = "";
	$scope.showPaidPopup = false;
	$scope.submitSearchForm = function() {
        $rootScope.$broadcast('showSpinner', 'Wait a second while we take the data out of Wikipedia...');
        tracker.all('index', 'search', $scope.query);
        service.request('POST', '/question', {query: $scope.query, lang: $scope.lang}).then(
            function (response) {
                if (response.success) {
                    DataStorage.set($scope.query, response.result);
                    DataStorage.set("lang", $scope.lang);
                    $state.go('base.review', {query: $scope.query});
                } else {
                    $scope.results = response.options;
                }
                $rootScope.$broadcast('hideSpinner');
            },
            function (error) {
            	if (error.data.type === 'DisambiguationError') {
            		$window.ga('send', 'event', 'search', 'DisambiguationError', $scope.lang, $scope.query);
	            }
                $rootScope.$broadcast('hideSpinner');
                $rootScope.$broadcast('showNotification', error.data.message);
                $state.go('base.search');
            }
        );
	}

	$scope.forceSearchForm = function(query) {
		$scope.query = query;
		$scope.submitSearchForm(true);
	}

	$scope.paidPopup = function() {
		$scope.showPaidPopup = true;
	}

	$scope.closePaidPoup = function() {
		$scope.showPaidPopup = false;
	}

	$scope.informPaid = function() {
		var email = sessionStorage.getItem('email');
		tracker.all('index', 'premiumSearch', email);
		$scope.closePaidPoup();
	}
});
