


// Executes when page is fully loaded
$(document).ready(function(){
    $("#challenge42Div").hide();
    $("#4-1Button").change(function(){
        $("#challenge41Div").show();
        $('#challenge42Div').hide();
      });
    $("#4-2Button").change(function(){
        $("#challenge41Div").hide();
        $('#challenge42Div').show();
      });

});

function downloadFile(){
    let uploadedFile = $('#uploadVideoButton')[0].files[0];
    if (!uploadedFile){
        toastr.warning('File not selected');
        return;
    }
    else{
        $('#changeResButton').html("Processing File  <i class='fa fa-spinner fa-spin'></i>")
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
        datatype : "application/json",
        success:function(result){
            if (result['status'] == 'success')
            {
                saveFile(result['path'])
            }
            else{
                toastr.error("File type not accepted, please upload .mp4")
                $('#changeResButton').html('Process Video')
            }
            
        }
    });
}

function removeBackground(){

    let uploadedFile = $('#uploadVideoButton')[0].files[0];
    if (!uploadedFile){
        toastr.warning('File not selected');
        return;
    }else{
        $('#removeBackgroundButton').html("Processing File  <i class='fa fa-spinner fa-spin'></i>")
        var formData = new FormData();
        formData.append('file', uploadedFile)
        if($('#MOG2Radio').is(':checked')){
            formData.append('algorithm', 'MOG2')
        }
        else if($('#knnRadio').is(':checked')){
            formData.append('algorithm', 'KNN')
        }
        else{
            formData.append('algorithm', 'ABSDIFF')
        }
    }

    $.ajax({
        url: '/background-removal',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        datatype : "application/json",
        success:function(result){
            if (result['status'] == 'success')
            {
                saveFile(result['path'])
            }
            else{
                toastr.error("File type not accepted, please upload .mp4")
                $('#removeBackgroundButton').html('Process Video')
            }
        }
    });
}

function saveFile(result){
    window.location.href = result +  "?dummy=" + Math.floor((Math.random() * 100000) +1);
    toastr.success("File successfully processed")
    $('#changeResButton').html('Process Video')
    $('#removeBackgroundButton').html('Process Video')
}