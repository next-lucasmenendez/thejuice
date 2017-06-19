/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.service('requests', function ($rootScope, $q, $http) {
	this.call = function (method, url, data, as_json) {
		var payload = {
			method: method,
			url: url
		};

		if (data) {
			if (method === "GET") {
				payload.params = data;
			} else {
				if (Boolean(as_json)) {
					payload.data = angular.toJson(data);
					payload.headers = {
						'Content-Type': 'application/json'
					}
				} else {
					payload.data = $.param(data);
					payload.headers = {
						'Content-Type': 'application/x-www-form-urlencoded'
					}
				}
			}

		}

		var result = $q.defer();
		$http(payload).then(
			function (response) {
				if (response.status >= 200 && response.status <= 300) {
					result.resolve(response.data);
				} else {
					result.reject(response.data);
				}
			},
			function (error) {
				result.reject(error);
			}
		);
		return result.promise;
	};
});
