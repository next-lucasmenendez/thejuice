$(document).ready(function () {
	var button = $('button#friends');
	button.on('click', function() {
		var input	= $('input[name="name"]'),
			query	= input.val();
	
		if (query) {
			var uri		= "/search?q="+ query +"&type=user&limit=10",
				token	= getCookie("accesstoken");

			var list	= $('#friend-list'),
				msg		= $('#message');

			FB.api(uri, {access_token: token}, function(response) {
				var users	= response.data,
					content	= "";
		
				for (var index in users) {	
					var user		= users[index],
						profile_uri	= "/"+user.id+"/picture";

					console.log(user);

					FB.api(profile_uri, {access_token: token}, function(result) {
						content = '<label class="panel-block">';
						if (result && !result.error) {
							content +=	'<figure class="image is-32x32">'+
										'<img src="'+ result.data.url +'">'+
									'</figure>';
						}
						content +=	user.name +
									'<input type="radio" name="target" class="is-pulled-right" value="'+ user.id +'">' +
								'</label>';
						
						var now = list.html();
						list.html(now + content);
					});
				}

				input.val('');
				list.fadeIn();
			});
		}
	});

	function getCookie(key) {
		var cookies	= decodeURIComponent(document.cookie),
			decoded	= cookies.split("; ");

		var needle = key + "=";
		for (var index in cookies) {
			var cookie = decoded[index];

			if (cookie.startsWith(needle)) {
				return cookie.slice(needle.length);
			}
		}
	}
});
