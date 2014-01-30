$(".circleG").hide();

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
	});
	if (s.length < 1)
	{
		alert ("Select some pics bro");
		return false;
	}

	if ($('#time').val() == "")
	{
		alert ("enter in some frame times man");
		return false;
	}
	$(".circleG").show();
	$.post('/make_gif',{'time' : $('#time').val(), 'pics[]' : s})
	.done(function(file_name)
	{
		window.location.href= "/gif/"+file_name;	
	});
}
