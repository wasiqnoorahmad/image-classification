$(function() {
    $('#submit').click(function(event) {
        event.preventDefault();
        var form_data = new FormData($('#uploadform')[0]);
        $.ajax({
            type: 'POST',
            url: '/classify',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            console.log(data);
            console.log(textStatus);
            console.log(jqXHR);
            console.log('Success!');
            $("#resultFilename").text(data['name']);
            $("#resultCat").text(data['category']);
	    $("#resultPer").text(data['per']);
        }).fail(function(data){
            alert('error!');
        });
    });
}); 
