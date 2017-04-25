$(document).ready(function(){

    $('form').on('submit', function(event){

        event.preventDefault();

        var form_data = new FormData($('#upload')[0]);
        $.ajax({

            url: '/classify',
            type: 'POST',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false
        })
            .done(function(data){
               if (data.mess){
                   alert("I'm Here");
               }
            });
    });
});