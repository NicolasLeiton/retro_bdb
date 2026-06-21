const form = document.getElementById("loginForm");
const message = document.getElementById("message");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    // Validaciones básicas
    if (!username) {
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

    showMessage("Validando...", "orange");

    try {
        const response = await fetch(
            "http://localhost:5000/login",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        const data = await response.json();

        // Elemento que se actualiza con la respuesta
        showMessage(data.message, data.success ? "green" : "red");

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