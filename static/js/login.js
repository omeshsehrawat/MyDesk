document.getElementById("loginButton").addEventListener("click", function(e){
    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    if(!email || !password){
        alert("Please enter both email and password.");
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            alert("Login successful! Redirecting to home...");
            window.location.href = "/home";
        }else{
            alert("Login failed: " + data.message);
        }
    })
    .catch(error => console.error(error));
    
});