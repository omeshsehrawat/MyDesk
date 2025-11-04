document.getElementById("registrationButton").addEventListener("click", function(e){
    e.preventDefault();
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value; 
    const repassword = document.getElementById('repassword').value;

    if(password !== repassword){
        alert("Passwords do not match!");
        return;
    }

    fetch('/register', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, username, password})
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            alert("Registration successful! Redirecting to login....");
            
        }else{
            alert("Registration failed: " + data.message);
        }
        window.location.href = "/";
    })
    .catch(error => console.error(err));

});