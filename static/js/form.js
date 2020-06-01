const url="http://localhost:5000";


$('#upload-form').modal();

$('#modal-submit').on('click', function(){
    data = new FormData();
    
    data.append('author', $('#modal-author').val());
    data.append('date', $('#modal-date').val());
    data.append('quarter', $('#modal-quarter').val());
    data.append('title', $('#modal-title').val());
    data.append('desc', $('#modal-desc').val());
    data.append('files', $('#modal-files').prop('files'));

    console.log(data)

    errString = 

    request_url = url + "/upload";
    $.ajax({
        type: 'POST',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        url: request_url,
        data: data,
        success: function(data, status) {
            if (status == 200) {
                console.log(`Upload succeeded: ${data}`);
                $('#upload-form').modal('hide');
            } else {
                $('#upload-modal').prepend(`
                <div class='alert alert-warning alert-dismissible fade show' role='alert'>
                <strong>Failed to upload post!</strong>: ${data}.
                <button type='button' class='close' data-dismiss='alert' aria-label='Close'>
                  <span aria-hidden='true'>&times;</span>
                </button>
              </div>`)
            }
        },
        error: function(e, status) {
            console.log(`Upload failed: ${data}`);
            $('#upload-modal').prepend(`
                <div class='alert alert-warning alert-dismissible fade show' role='alert'>
                <strong>Failed to upload post!</strong>: ${e}.
                <button type='button' class='close' data-dismiss='alert' aria-label='Close'>
                  <span aria-hidden='true'>&times;</span>
                </button>
              </div>`);
        }
    });
})