(function($) {

    //your code here
    function onFormSubmit(event){
    	var data = $(event.target).serializeArray();


       
        var thesis = {};
        for (var i = 0; i < data.length; i++) {
            var key = data[i].name;
            var value = data[i].value;
            thesis[key] = value;
        }
        var thesis_create_api = '/api/thesis';
        $.post(thesis_create_api, thesis, function(response){
            //read response from server
             //if Thesis save is successful
            if (response.status = 'OK'){
                 //display Thesis
                var year_thesis_title = response.data.year + ' '+ response.data.thesis_title;
                $('.list-section').append('<li>'+year_thesis_title+'</li>');
            }else{
                //display error message
               
            }               
        })
        return false;
    }
    function loadAllThesis(){
        var thesis_list_api = 'api/thesis';
        $.get(thesis_list_api,{},function (response){
            console.log('thesis list', response)
            response.data.forEach(function (thesis){
                var year_thesis_title = thesis.year + ' ' + thesis.thesis_title;
                $('.thesis-list').append('<li>' + year_thesis_title + '</li>');
            });
        });
    }
    $('.create-form').submit(onFormSubmit)
    loadAllThesis();
}
)(jQuery)

    function myDelete(){

        confirm("Are you sure you want to delete account?"); 
        $('ul').on('click', 'li', function() 
        {
            $(this).remove();
            return false;
        });   
	}