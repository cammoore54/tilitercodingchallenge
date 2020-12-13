/**
 * Includes all the JS functions for challenge 4/5 (video-processing.html)
 * 
 * Author: Cameron Moore
 */


// Executes when page is fully loaded
$(document).ready(function(){
    // onclick events to show/hide challenge 4.1 and 4.2 functionality
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

function challenge4_1(){
    /**
     * Takes input mp4 file and proccess it based on user input of resolution, frame rate and colour
     * 
     */

     //Get file
    let uploadedFile = $('#uploadVideoButton')[0].files[0];
    if (!uploadedFile){
        toastr.warning('File not selected');
        return;
    }
    else{
        // Show file is processing
        $('#changeResButton').html("Processing File  <i class='fa fa-spinner fa-spin'></i>")
        // Get input data
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

    //  Send data to server to process
    $.ajax({
        url: '/resize-video',
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

function challenge4_2(){
    /**
     * Takes input mp4 file and removes background from each frame
     * 
     */
    //Get file
    let uploadedFile = $('#uploadVideoButton')[0].files[0];
    if (!uploadedFile){
        toastr.warning('File not selected');
        return;
    }else{
        // Show file is processing
        $('#removeBackgroundButton').html("Processing File  <i class='fa fa-spinner fa-spin'></i>")
        var formData = new FormData();
        formData.append('file', uploadedFile)
        // Get background removal method
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

    // Send data to server
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

/**
 * Prompts browser to download file
 * @param {path} result - Path to download file
 */
function saveFile(result){
    window.location.href = result +  "?dummy=" + Math.floor((Math.random() * 100000) +1);
    toastr.success("File successfully processed")
    $('#changeResButton').html('Process Video')
    $('#removeBackgroundButton').html('Process Video')
}