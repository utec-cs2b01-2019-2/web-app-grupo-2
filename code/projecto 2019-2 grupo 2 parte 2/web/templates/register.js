function register(){
        var name = $('#name').val();
        var fullname = $('#username').val();
        var username = $('#username').val();
        var password = $('#password').val();
        var message = JSON.stringify({
                "name": name,
                "username": username,
                "fullname": fullname,
                "password": password
            });

        $.ajax({
            url:'/users2',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json',
            }
        });
    }