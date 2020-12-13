


// Executes when page is fully loaded
$(document).ready(function(){
    
    $("#4-1Button").change(function(){
        $("#challenge41Div").show();
      });
    $("#4-2Button").change(function(){
        $("#challenge41Div").hide();
      });

});

function downloadFile(){
    let uploadedFile = $('#uploadVideoButton')[0].files[0];
    if (!uploadedFile){
        toastr.warning('File not selected');
        return;
    }
    else{
        $('#DownloadButton').html("Processing File  <i class='fa fa-spinner fa-spin'></i>")
        var formData = new FormData();
        var frameWidth = $('#inputFrameWidth').val();
        var frameHeight = $('#inputFrameHeight').val();
        var frameRate = $('#inputFramerate').val();
        if($('#colourRadio').is(':checked')){
            formData.append('colour', true)
        }
        else{
            formData.append('colour', false)
        }
        formData.append('file', uploadedFile)
        formData.append('frameWidth', frameWidth)
        formData.append('frameHeight', frameHeight)
        formData.append('frameRate', frameRate)
    }

    $.ajax({
        url: '/upload-files',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        dataType: 'html',
        success:function(result){
            saveFile(result)
        }
    });
}

function saveFile(result){
    window.location.href = result +  "?dummy=" + Math.floor((Math.random() * 100000) +1);
    $('#DownloadButton').html('Download')
}