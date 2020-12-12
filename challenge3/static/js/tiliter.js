
/**
 * This file includes all the JS functions for interacting with the web interface
 * 
 * Author: Cameron Moore
 * 
 */


 // Initialise global variables
 // Movie list for theatre
let theatreMovieList = [];
// Movie list with ID dict for theatre
let theatreMovieListDict = [];
// Total movie list
let movieListTotal = [];
// Total list with ID dict
let movieListDictTotal = [];

// Executes when page is fully loaded
$(document).ready(function(){

    // Grab the movie title and id from all of the movies
    $( ".media" ).each(function(idx, el){
        movieListTotal.push($( this ).attr("name"))
        movieListDictTotal.push({
            name:  $( this ).attr("name"),
            id: $( this ).attr("id")
        });
    })

    // Trigger event for arclight button
    $("#arclight-button").change(function(){
        getShowTimes('Arclight')
        let input = $('#movieSearch').val()
        filterMovieList(input)
    });

    // Show arclight cinema as default
    $("#arclight-button").trigger('click')

    // Trigger event for pacific theatres button
    $("#pacific-theatres-button").change(function(){
        getShowTimes('Pacific Theatres')
        let input = $('#movieSearch').val()
        filterMovieList(input)
    }); 

    // Trigger event for amc button
    $("#amc-button").change(function(){
        getShowTimes('AMC')
        let input = $('#movieSearch').val()
        filterMovieList(input)
    }); 

    // Trigger event when key pressed in movie title search input form
    $( "#movieSearch" ).keyup(function() {
        let input = $(this).val().toLowerCase()
        filterMovieList(input)
      });

});

/**
 * Filters movie list for 'movies titles that contain' what the user entered
 * Displays matches and hides non matches
 * 
 * @param {string} input- Search input from user
 */
function filterMovieList(input){

    // Filters list of currently selected theatre with input of user
    let filteredList = theatreMovieList.filter(element => element.includes(input));
    // If no results, hide all elements
    if (filteredList.length == 0){
        for (let i=0; i < theatreMovieListDict.length; i++){
            $("#"+ theatreMovieListDict[i]["id"]).hide()
        }
    }
    else{
        // Loop through filtered list and movie list avaialble at that theatre and display results
        for (let i=0; i < theatreMovieListDict.length; i++){
            for (let j=0; j < filteredList.length; j++){
                if (theatreMovieListDict[i]["name"]  == filteredList[j]){
                    $("#"+ theatreMovieListDict[i]["id"]).show()
                    break;
                }
                else{
                    $("#"+ theatreMovieListDict[i]["id"]).hide()
                }
            }
        }
    }

}

/**
 * Filters movie list avaliable at selected theatre
 * 
 * @param {json object} showTimes - showtimes for movie id
 * @returns {list} movieList - List of avalailable movies at theatre. movieListDict - dict of name and id of available movies.
 */
function getMovieList(showTimes){
    let movieList = [];
    let movieListDict = [];
    // Loop through json objectg
    for (let id in showTimes){
        // Loop through all movie divs
        $( ".media" ).each(function(idx, el){
            if ($( this ).attr("id") == id){
                movieList.push($( this ).attr("name"))
                movieListDict.push({
                    name:  $( this ).attr("name"),
                    id: $( this ).attr("id")
                });
            }
        });
    }
    return [movieList, movieListDict]
}

/**
 * Shows all movies avaialble at theatre
 * @param {list} filteredList - List of movies available at theatre
 */
function showAllTheatreMovies(filteredList){

    for (let i=0; i < movieListDictTotal.length; i++){
        for (let j=0; j < filteredList.length; j++){
            if (movieListDictTotal[i]["name"]  == filteredList[j]){
                $("#"+ movieListDictTotal[i]["id"]).show()
                break;
            }
            else{
                $("#"+ movieListDictTotal[i]["id"]).hide()
            }
        }
    }
}

/**
 * Requests list of showtimes for theatre
 * @param {string} theatre - Name of theatre
 */
function getShowTimes(theatre){
    $.ajax({
        url: '/get-show-times/'+ theatre,
        type: 'POST',
        async: false,
        success: function(result) {
            let showTimes = result;
            let movieLists = getMovieList(showTimes)
            // Assign results to global variables
            theatreMovieList = movieLists[0]
            theatreMovieListDict = movieLists[1]
            showAllTheatreMovies(theatreMovieList)

            // Update showtimes for each movie
            for (let id in showTimes){
                let timesString = "";
                for (let i=0; i < showTimes[id].length; i++){
                    timesString += " " + showTimes[id][i]
                }
                $("#"+id+"-times").text(timesString);
            }
        }
    });
}


function uploadVideo(){
    let formData = new FormData();
    let uploadedFile = $('#uploadVideoButton')[0].files[0]; //Get the one file
    formData.append('file', uploadedFile)

    $.ajax({
        url: '/upload-files',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success:function(result){
            console.log(result)

        }
    });
}