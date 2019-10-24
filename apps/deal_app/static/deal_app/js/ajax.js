$(document).ready(function(){
    $('#click_btn').click(function(){
        console.log('clicked buttons')
        $.ajax({
            method:"GET",
            url:"/deals/update_price"
        })
        .done(function(){
            console.log("We did it!!")
        })
    })
    setTimeout(function(){ 
        $.ajax({
            method:"GET",
            url:"/deals/update_price"
        })
        location.reload();
    }, 60000);

})

$(document).ready(function(){
    $('.add_btn').click(function(){
        $('.loading').css('display','inline-block');
        $('.add_btn').hide();
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