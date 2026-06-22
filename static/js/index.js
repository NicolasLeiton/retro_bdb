const form = document.getElementById("loginForm");
const message = document.getElementById("message");
const registerBtn = document.getElementById("registerBtn");
const backBtn = document.getElementById("backBtn");
const confirmPasswordGroup = document.getElementById("confirmPasswordGroup");

let registerMode = false;
// Intercambio entre modo de registro y modo de login
registerBtn.addEventListener("click", () => {
    registerMode = true;

    document.querySelector("h2").textContent =
        "Crear Cuenta";

    confirmPasswordGroup.style.display = "block";

    form.querySelector("button[type='submit']").textContent =
        "Crear Cuenta";

    registerBtn.style.display = "none";
    backBtn.style.display = "block";

    message.textContent = "";
});

backBtn.addEventListener("click", () => {

    registerMode = false;

    document.querySelector("h2").textContent =
        "Iniciar Sesión";

    confirmPasswordGroup.style.display = "none";

    form.querySelector("button[type='submit']").textContent =
        "Ingresar";

    registerBtn.style.display = "block";
    backBtn.style.display = "none";

    message.textContent = "";
});

//Verificaciones y envio de datos al endpoint
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    // Validaciones básicas
    if (!email) {
        showMessage("Debe ingresar un usuario", "red");
        return;
    }

    if (!password) {
        showMessage("Debe ingresar una contraseña", "red");
        return;
    }

    if (password.length < 6) {
        showMessage(
            "La contraseña debe tener al menos 6 caracteres",
            "red"
        );
        return;
    }
    if (registerMode) {

    const confirmPassword =
        document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {

        showMessage(
            "Las contraseñas no coinciden",
            "red"
        );

        return;
    }
}

    showMessage("Validando...", "orange");

    try {
        const formData = new FormData();
        formData.append("email", email);
        formData.append("password", password);
        
        const response = await fetch(
            registerMode ? "/registrar_user": "/login",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        // Elemento que se actualiza con la respuesta
        showMessage(data.message, data.success ? "green" : "red");
        if (data.success) {
            
            if (data.is_analist){
                window.location.href = "/reclutador";
            }
            else{
                window.location.href = "/registro";}
        }

    } catch (error) {
        showMessage(
            "No fue posible conectar con el servidor",
            "red"
        );
    }
});


function showMessage(text, color) {
    message.textContent = text;
    message.style.color = color;
}