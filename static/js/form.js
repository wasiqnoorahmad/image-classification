$(document).ready(function(){

    $('form').on('submit', function(event){

        event.preventDefault();

        var form_data = new FormData($('#upload')[0]);
        $.ajax({

            url: '/classify',
            type: 'POST',
            headers: {"Content-Type": "application/json"},
            data: form_data
        })
            .done(function(data){
               if (data.mess){
                   window.alert("I'm Here")
               }
            });
    });
});