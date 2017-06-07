/**
 * Created by axelblanco on 7/06/17.
 */

$(function() {
    randomizeAnswers();
});

function randomizeAnswers() {
	$('.answers').each(function() {
        $(this).children().sort(function(){
            return Math.round(Math.random()) - 0.5;
        }).detach().appendTo(this);
	});
}