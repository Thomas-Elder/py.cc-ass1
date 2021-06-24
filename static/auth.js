window.addEventListener('load', function () {
    document.getElementById('sign-in').onclick = function () {
        SignIn();
    };
  
    document.getElementById('sign-out').onclick = function () {
        SignOut();
    };

    document.getElementById('create').onclick = function(){
        CreateNew();
    };

    SignIn = function(){

        // Show signout/login info
        document.getElementById('sign-out').hidden = false;
        document.getElementById('login-info').hidden = false;
    };
    
    SignOut = function(){

        // Hide signout/login info
        document.getElementById('sign-out').hidden = true;
        document.getElementById('login-info').hidden = true;

        // Show create
        document.getElementById('create').hidden = false;
    };

    CreateNew = function(){

        var user = document.getElementById('user');
        var email = document.getElementById('email');

        // datastore stuff?

        // Show signout/login info
        document.getElementById('sign-out').hidden = false;
        document.getElementById('login-info').hidden = false;

        // Hide create 
        document.getElementById('create').hidden = true;
    };
  });