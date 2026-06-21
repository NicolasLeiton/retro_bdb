const form = document.getElementById("registerForm");
const message = document.getElementById("message");


function showMessage(text, color) {
    message.textContent = text;
    message.style.color = color;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fullname = document.getElementById("fullname").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const career = document.getElementById("career").value.trim();
    const semester = document.getElementById("semester").value.trim();
    const cv = document.getElementById("cv").files[0];

    // Validaciones

    if (!fullname) {
        return showMessage(
            "El nombre completo es obligatorio",
            "red"
        );
    }

    if (!phone || isNaN(phone)) {
        return showMessage(
            "Debes ingresar un número de teléfono",
            "red"
        );
    }

    if (!career) {
        return showMessage(
            "La carrera es obligatoria",
            "red"
        );
    }

    if (!semester) {
        return showMessage(
            "El semestre es obligatorio",
            "red"
        );
    }


    if (cv && cv.type !== "application/pdf") {
        return showMessage(
            "Solo se permiten archivos PDF",
            "red"
        );
    }

    try {

        const formData = new FormData();

        formData.append("fullname", fullname);
        formData.append("phone", phone);
        formData.append("career", career);
        formData.append("semester", semester);
        formData.append("cv", cv);

        showMessage(
            "Enviando información...",
            "orange"
        );

        const response = await fetch(
            "/registro",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        showMessage(
            data.message,
            data.success ? "lightgreen" : "red"
        );

    } catch (error) {

        showMessage(
            "No fue posible conectar con el servidor",
            "red"
        );

    }
});

