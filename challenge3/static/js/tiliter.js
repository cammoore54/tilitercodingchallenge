

let theatreMovieList = [];
let theatreMovieListDict = [];

let movieListTotal = [];
let movieListDictTotal = [];


$(document).ready(function(){

    $("#arclight-button").focus()
    $("#arclight-button").click()
    $("#arclight-button").click(function(){
        getShowTimes('Arclight')

    }); 
    $("#pacific-theatres-button").click(function(){
        getShowTimes('Pacific Theatres')

    }); 
    $("#amc-button").click(function(){
        getShowTimes('AMC')

    }); 

    $( ".media" ).each(function(idx, el){

        movieListTotal.push($( this ).attr("name"))
        movieListDictTotal.push({
            name:  $( this ).attr("name"),
            id: $( this ).attr("id")
        });
    })

    $( "#movieSearch" ).keyup(function() {
        let input = $(this).val().toLowerCase()

        let filteredList = theatreMovieList.filter(element => element.includes(input));
        if (filteredList.length == 0){
            for (let i=0; i < theatreMovieListDict.length; i++){
                $("#"+ theatreMovieListDict[i]["id"]).hide()
            }
        }
        else{
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

        console.log(movieList.filter(element => element.includes(input) ) );
      });

});

function getMovieList(showTimes){
    let movieList = [];
    let movieListDict = [];
    for (let id in showTimes){
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


function showHideMovies(filteredList){

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

function getShowTimes(theatre){

    $.ajax({
        url: '/get-show-times/'+ theatre,
        type: 'POST',
        success: function(result) {
            
            let showTimes = result;
            let movieLists = getMovieList(showTimes)
            theatreMovieList = movieLists[0]
            theatreMovieListDict = movieLists[1]
            
            showHideMovies(theatreMovieList)

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