

$(document).ready(function(){

    let movieList = [];
    let movieListDict = [];
    let $elementList = $( ".media" ).each(function(idx, el){

        movieList.push($( this ).attr("name"))
        movieListDict.push({
            name:  $( this ).attr("name"),
            id: $( this ).attr("id")
        });
        //here this/el refers to the current image dom reference
        //do soemthing
    })
    console.log(movieList)

    $( "#movieSearch" ).keyup(function() {
        let input = $(this).val().toLowerCase()

        let filteredList = movieList.filter(element => element.includes(input));
        if (filteredList.length == 0){
            for (let i=0; i < movieListDict.length; i++){
                $("#"+ movieListDict[i]["id"]).hide()
            }
        }
        else{
            for (let i=0; i < movieListDict.length; i++){
                for (let j=0; j < filteredList.length; j++){
                    if (movieListDict[i]["name"]  == filteredList[j]){
                        $("#"+ movieListDict[i]["id"]).show()
                        break;
                    }
                    else{
                        $("#"+ movieListDict[i]["id"]).hide()
                    }
                }
            }
        }

        console.log(movieList.filter(element => element.includes(input) ) );
      });

    // $.ajax({
    //     url: '/get-movie-data',
    //     type: 'POST',
    //     success: function(result) {
    //         console.log(result)
    //         let movieData = result["movieData"]
    //         let showTimes = result["showTimes"]
    //         // result = JSON.parse(result)
    //         // for (let i = 0; i < data.length; i++) {
    //         //     if (data[i] == "movieData"){
    //         //         let movieData = data[key]
    //         //     }
    //         //     else if (data[i] == "showTimes"){
    //         //         let showTimes = data[key]
    //         //     }
    //         // }
    //     }
    // });


});