var currentUserId = 0;
var currentClickedId = 0;
function whoami(){
        $('#mal').hide();
        $('#bien').hide()
        $.ajax({
            url:'/current',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                //alert(JSON.stringify(response));
                $('#cu_username').html(response['username'])
                var name = response['name']+" "+response['fullname'];
                currentUserId = response['id']
                $('#cu_name').html(name);
                loadwords();
            },
            error: function(response){
                alert(JSON.stringify(response));
            }
        });
    }


    function loadwords(){
        //alert(user_from_id);
        //alert(user_to_id);

        random = Math.floor(Math.random() * (8) );
        $.ajax({
            url:'/words/'+random,
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                //alert(JSON.stringify(response));
                 e = '';
                 t = '';
                 e = '<input type="text" id="answer" value="'+response["answer"]+'" style="display: none;"/>';
                 t = '<div id = "pregunta" class="alert alert-secondary"><P align=center>'+response["question"]+'<P></div>';

                    $('#messages').append(e);
                    $('#text').append(t);



                //alert("funciona")

            },

            error: function(response){
                alert(JSON.stringify(response));
            }

        });
    }

    function sendwords(){
        var message = $('#postmessage').val();
        $('#postmessage').val('');

        var answer2 = $('#answer').val();
        $('#answer').val('');


        var data = JSON.stringify({
                "content": message,
                "answer": answer2
            });

        $.ajax({
            url:'/gabriel/word',
            type:'POST',
            contentType: 'application/json',
            data : data,
            dataType:'json',
            success: function(response){
                //alert(JSON.stringify(response));
                t = '<div class="alert alert-secondary" ><P align=center>Tu respuesta esta'+response+'</P></div><input type="button" onclick="window.location.reload();" value="otra pregunta">';
                //t = '<button value="Dale click para otra pregunta" onClick="window.location.reload();">';
                $('#text').append(t);



            },
            error: function(response){
                alert(JSON.stringify(response));
            }
        });


    }