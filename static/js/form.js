$(document).ready(function () {
  $('#upload-link').removeClass('d-none')
})

$('#upload-form').modal();

$('#modal-submit').on('click', function () {
  data = new FormData();

  data.append('author', $('#modal-author').val());
  data.append('date', $('#modal-date').val());
  data.append('quarter', $('#modal-quarter').val());
  data.append('title', $('#modal-title').val());
  data.append('body', $('#modal-desc').val());
  fileInput = $('#modal-files')
  for (var i = 0; i < fileInput.length; ++i) {
    data.append('file', fileInput.prop('files')[i]);
  }

  request_url = "/upload";
  $.ajax({
    type: 'POST',
    enctype: 'multipart/form-data',
    processData: false,
    contentType: false,
    cache: false,
    url: request_url,
    data: data,
    success: function (data) {
      console.log(data);
      $('#upload-form').modal('hide');
    },
    error: function (e) {
      console.log(`Upload failed: ${e.responseText}`);
      $('#upload-modal').prepend(`
              <div class='alert alert-warning alert-dismissible fade show' role='alert'>
              <strong>Upload failed!</strong>: ${e.responseText}
              <button type='button' class='close' data-dismiss='alert' aria-label='Close'>
                <span aria-hidden='true'>&times;</span>
              </button>
            </div>`);
    }
  });
})