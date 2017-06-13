/**
 * Created by axelblanco on 7/06/17.
 */

$(function() {
    randomizeAnswers();

    $('.submit button').on('click', function(e) {
    	var email = checkEmail();
    	var questions = checkQuestions();

	    $('#spinner').slideDown();
    	if (email && questions) {
    		$.ajax({
				url: '/validate',
				type: 'POST',
				data: JSON.stringify({
	                studentEmail: email,
					teacherEmail: $('.submit input#teacherEmail').val(),
					title: $('.header .text .name').text() + ' ' + $('.header .text .surname').text(),
				    questions: questions
		        }),
			    contentType: 'application/json; charset=utf-8',
			    dataType: 'json',
				success: function(success) {
					showCongratulations(success.score);
				},
			    error: function(error) {
					$('#spinner').slideUp()
					printErrors('send-email', 'There was a problem and your Trivia wasn\'t sent');
			    }
			});
	    } else {
    		$('#spinner').slideUp();
	    }
    });
});

function randomizeAnswers() {
	$('.answers').each(function() {
        $(this).children().sort(function(){
            return Math.round(Math.random()) - 0.5;
        }).detach().appendTo(this);
	});
}

function checkEmail() {
	var email = $('.submit input#studentEmail').val();

	if (email) {
		if (email.match(/.+@.+\..+/g)) {
			removeError('email');
			return email;
		}
	}

	printErrors('email', 'Insert a valid email address.');
	return false;
}

function checkQuestions() {
	var questions = [];
	var error = false;
	$('.question').each(function() {
		if ($(this).find('input:checked').length === 0) {
			error = true;
			return false;
		}
		questions.push({
			question: $(this).find('.text').text(),
			correct: $(this).find('.answers').find('label[data="True"]').text(),
			select: $(this).find('input:checked').val()
		});
	});

	if (error) {
		printErrors('questions', 'Some answers need to be completed.');
		return false;
	} else {
		removeError('questions');
	}

	return questions;
}

function showCongratulations(score) {
	$('.submit').remove();
	$('.question').remove();
	$('.header').remove();
	$('.questions').prepend(
		'<div class="congrats">' +
		'<h1>Congratulations</h1>' +
		'<p>You have finished the Trivia.</p>' +
		'<p>Your score was <span class="score">' + score + '%</span></p>' +
		'</div>'
	);

}

function printErrors(id, error) {
	if ($('.error #' + id).length === 0) {
		$('.error').append('<li id="' + id + '">' + error + '</li>');
		$('.error').slideDown();
	}

}

function removeError(id) {
	if ($('.error #' + id).length > 0) {
		$('.error #' + id).remove();
	}
	if ($('.error')[0].childNodes.length === 0) {
		$('.error').slideUp();
	}
}