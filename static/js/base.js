$(document).ready(function(){

    // #id
    $('#delete').click(function(){
        return confirm("Are you sure to delete this post?");
    });
    // .class
    $('.reply-btn').click(function(){
        $(this).parent().parent().next('.replied-comments').fadeToggle();
    });

});


$(document).on('submit','.comment-form', function(event){
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response){
            $('.main-comment-section').html(response['form']);
            $('textarea').val('');
            $('.reply-btn').click(function(){
                $(this).parent().parent().next('.replied-comments').fadeToggle();
                $('textarea').val('');
            });
        },
        error: function(rs, e){
            console.log(rs.responseText);
        },
    });
});


$(document).on('submit','.reply-form', function(event){
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response){
            $('.main-comment-section').html(response['form']);
            $('textarea').val('');
            $('.reply-btn').click(function(){
                $(this).parent().parent().next('.replied-comments').fadeToggle();
                $('textarea').val('');
            });
        },
        error: function(rs, e){
            console.log(rs.responseText);
        },
    });
});

var perfEntries = performance.getEntriesByType("navigation");

if (perfEntries[0].type === "back_forward") {
    location.reload(true);
}