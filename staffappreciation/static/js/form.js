const url="http://localhost:5000";


$('#upload-form').modal();

$('#modal-submit').on('click', function(){
    date = $('#modal-date').val();
    quarter = $('#modal-quarter').val();
    type = $('#modal-type').val();
    path = $('#modal-path').val();
    data = {
        'date': date, 'quarter': quarter, 'type': type, 'path':path
    }
    request_url = url + "/insert";
    $.post(request_url, data,  function(data, status) {
        console.log(`Insert request returned ${data} with status ${status}`)
    });
})