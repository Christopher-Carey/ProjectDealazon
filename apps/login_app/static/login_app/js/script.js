$(document).ready(function(){
    $('#login_btn').click(function(){
        $('.loading').show();
        console.log('clicked buttons')
        $.ajax({
            method:"POST",
            url:"/"
        })
        .done(function(){
            console.log("We did it!!")
        })
    })
})