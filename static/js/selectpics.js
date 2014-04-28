// add image to timeline when clicked
$('.no-select').click(function()
{
	$(this).clone().removeClass('no-select').addClass('selected').appendTo('#timeline');
});

// remove image from timeline when clicked
$(document).on('click', 'img.selected', function()
{
	$(this).remove();
});

// sends gif info to server
function makeGif()
{
    // get selected images
    s = new Array();
    $('.selected').each(function(i) {
        s[i] = $(this).attr('src');	
    });

    // make sure there's some pics
    if (s.length < 1)
    {
        alert ("You've got to select some images");
        return false;
    }
 
    var time = $('#time').val()

    // make sure time is set and valid
    if ( time == "")
    {
        alert ("You've go to enter a frame time");
        return false;
    }

    if (isNaN(time))
    {
        alert ("Not a valid number");
        return false;
    }
        
    // show loading modal
    $('#load-modal').modal('show');
        
    // make gif!!!
    $.post('/make_gif',{'time' : $('#time').val(), 'pics[]' : s})
    .done(function(file_name)
    {
        window.location.href= "/gif/"+file_name;	
    });
}
