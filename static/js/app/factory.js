/**
 * Created by lucas.menendez on 16/5/17.
 */

var app = angular.module("app");

app.factory('DataStorage', function() {
	return {
        set: function (key, value) {
        	var local 	= localStorage.getItem('mem'),
				mem		= (Boolean(local)) ? JSON.parse(local) : {};
			mem[key] = value;

			localStorage.setItem('mem', JSON.stringify(mem));
        },
        get: function (key) {
        	var local = localStorage.getItem('mem')
        	if (Boolean(local)) {
        		var mem = JSON.parse(local);
            	return mem[key] || false;
			}
        }
    };
});
