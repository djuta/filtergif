$('.no-select').click(function()
{
	$(this).clone().removeClass('no-select').addClass('selected').appendTo('#timeline');
});

$(document).on('click', 'img.selected', function()
{
	$(this).remove();
});


function makeGif()
{
	s = new Array();
	$('.selected').each(function(i) {
		s[i] = $(this).attr('src');	
	})
}
