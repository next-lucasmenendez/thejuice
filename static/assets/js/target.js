$(document).ready(function () {
	targets		= [];
	limit		= $(window).width() > 753 ? 10 : 5;
	page		= 0;
	has_next	= true;

	function getCookie(key) {
		var cookies	= decodeURIComponent(document.cookie),
			decoded	= cookies.split("; ");

		var needle = key + "=";
		for (var i = 0; i < cookies.length; i++) {
			var cookie = decoded[i];

			if (cookie && cookie.startsWith(needle)) {
				return cookie.slice(needle.length);
			}
		}

		return false;
	}

	var form = $('form#friends');
	form.on('submit', function(e) {
		e.preventDefault();

		var input	= $('input[name="name"]'),
			query	= input.val();
	
		if (query) {
			var uri		= "/search?q="+ query +"&type=user&fields=id,name,picture&limit="+ limit,
				token	= getCookie("accesstoken");

			searchCall(uri, token);
		}
	});

	var next	= $('#next-results'),
		prev	= $('#prev-results');
	
	next.on('click', function () {
		var input	= $('input[name="name"]'),
			query	= input.val();
	
		if (query && !next.hasClass('is-disabled')) {
			page++;
			offset = limit * page;
			var uri			= "/search?q="+ query +"&type=user&fields=id,name,picture&limit="+limit+"&offset="+offset,
				token		= getCookie("accesstoken");

			searchCall(uri, token);

			if (page > 0 && prev.hasClass('is-disabled')) 
				prev.removeClass('is-disabled')

			if (!has_next)
				next.addClass('is-disabled')
		}
	});

	prev.on('click', function () {
		var input	= $('input[name="name"]'),
			query	= input.val();
	
		if (query && !prev.hasClass('is-disabled')) {
			page--;
			offset = limit * page;
			var uri			= "/search?q="+ query +"&type=user&fields=id,name,picture&limit="+limit+"&offset="+offset,
				token		= getCookie("accesstoken");

			searchCall(uri, token);

			if (page == 0) 
				prev.addClass('is-disabled')

			if (has_next)
				next.removeClass('is-disabled')
		}
	});

	$('#search-list').on('click', 'a.friend', function() {
		var _this	= $(this),
			id		= _this.attr('attr-id'),
			name	= _this.attr('attr-name');
		
		if (targets.indexOf(id) == -1) {
			targets.push(id);

			var list	= $('#friends-list'),
				content	= list.html();
			content += '<span id="'+id+'" class="tag is-medium" style="margin: 5px">'+ 
							name + 
							'<span class="delete" attr-id="'+id+'"></a>' +
						'</span>';
			list.html(content);

			if (targets.length > 0)
				$('#send-button').removeClass('is-disabled').removeClass('is-light').addClass('is-primary');
		}
	});

	$('#friends-list').on('click', 'span.tag span.delete', function () {
		var list	= $('#friends-list'),
			_this	= $(this),
			id		= _this.attr('attr-id'),
			target	= targets.indexOf(id);
	
		targets.splice(target, 1);
		$('#friends-list #' + id).remove();

		if (targets.length == 0)
			$('#send-button').removeClass('is-primary').addClass('is-light').addClass('is-disabled');
	});

	$('#send-button').on('click', function(e) {
		e.preventDefault();
		var inputs = "";
		for (var index in targets) 
			inputs += "<input type='hidden' name='targets["+index+"]' value='"+targets[index]+"'>";

		$('#send-form').append(inputs).submit();
	});

	function searchCall(uri, token) {
		var container	= $('#search-list'),
			list		= $('#search-list .panel');

		FB.api(uri, {access_token: token}, function(response) {
			if (!response.error) {
				if (response.data) {
					has_next = typeof response.paging.previous != 'undefined'
					var users	= response.data,
						content	= "";
			
					for (var index in users) {	
						var user	= users[index],
							id		= user.id,
							name	= user.name,
							picture	= user.picture.data.url;

						content +=	'<a class="panel-block friend" attr-id="'+id+'" attr-name="'+name+'">' +
										'<figure class="image is-32x32" style="margin-right: 10px;">' +
											'<img src="'+ picture +'">' +
										'</figure>' +
										'<span>'+ name +'</span>'+
									'</a>';
					}

					list.html(content);
					container.fadeIn();
				}
			} else {
				window.location.href = "/logout/expired";
			}
		});
	}
});
