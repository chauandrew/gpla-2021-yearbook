$(document).ready(function () {
  $('#upload-link').removeClass('d-none')
  toastr.options.closeButton = true
  toastr.options.positionClass = 'toast-bottom-right'
})

$('.custom-file-input').on('change', function (e) {
  filenames = []
  files = $(this).prop('files')
  for (i = 0; i < files.length; i++) {
    filenames.push(files[i].name)
  }
  console.log(`Selected ${filenames.toString()}`)
  $(this).siblings('.custom-file-label').text(filenames.toString())
})

$('#upload-form').modal();

$('#modal-submit').on('click', function () {
  // Pop up loading screen
  $('#upload-modal').prepend(`
  <div id="loadingoverlay" class="d-flex justify-content-center">
    <div id="loadingtext" class="row justify-content-center text-white">
      <h3>Uploading...</h3>
    </div>
  </div>`)

  // Send API call
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
      $('#loadingoverlay').remove()
      console.log(data);
      $('#upload-modal').modal('hide');
      toastr.success("Uploaded successfully! Your post *should* be visible soon.")
    },
    error: function (e) {
      $('#loadingoverlay').remove()
      console.log(`Upload failed: ${e.responseText}`);
      toastr.warning(`Upload failed! Response: ${e.responseText}`)
    }
  });
})