const form = document.querySelector("form");
var error;

form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (validateForm()) {
        submitForm();
        form.submit();
        form.reset();
        setTimeout(() => {
            window.location.href = "../index.html";
        }, 5000);
    }
})

// function to validate name , email , message

function validateForm() {
    let error = false;
    const data = [
        { id: "nombre", regex: /^[a-zA-Z\s]*$/, msj: "Ingrese un nombre valido" },
        { id: "email", regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, msj: "Ingrese un correo electronico valido" },
        { id: "mensaje", regex: /.{10,}/, msj: "Ingrese un mensaje valido, minimo 10 caracteres" }
    ];
    for ( let field of data ) {
        const value = document.getElementById(field.id).value;
        const label = document.getElementById(`${field.id}-label`);
        if (!field.regex.test(value) || value.length == 0) {
            label.style.color = "red";
            label.innerHTML = field.msj;
            error = true;
        } else {
            label.style.color = "black";
            // Only first letter Uppercase
            label.innerHTML = field.id.charAt(0).toUpperCase() + field.id.slice(1);
        }
    }
    return !error;
}

function submitForm() {
    const subText = document.getElementById("sub-text");
    const text = document.getElementById("text");
    const hidden = document.querySelectorAll(".info");
    subText.style.display = "block";
    subText.innerHTML = "Seras redirigido a la pagina principal en 5 segundos.";
    text.innerHTML = "Gracias por tu consulta! Nos pondremos en contacto contigo a la brevedad.";
    subText.style.color = "#9fc131";
    text.style.fontSize = "3rem";
    subText.style.textAlign = "center";
    text.style.textAlign = "center";
    hidden.forEach(element => {
        element.style.display = "none";
    });
}