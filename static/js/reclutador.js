const internList     = document.getElementById('internList');
const emptyState     = document.getElementById('emptyState');
const internDetail   = document.getElementById('internDetail');
const detailName     = document.getElementById('detailName');
const detailBadge    = document.getElementById('detailBadge');
const detailEmail    = document.getElementById('detailEmail');
const detailPhone    = document.getElementById('detailPhone');
const detailDegree   = document.getElementById('detailDegree');
const detailSemester = document.getElementById('detailSemester');
const btnViable      = document.getElementById('btnViable');
const btnNoViable    = document.getElementById('btnNoViable');
const btnDownloadCV  = document.getElementById('btnDownloadCV');
const actionMessage  = document.getElementById('actionMessage');

let currentEmail  = null;
let currentCVRoute = null;

// Colores por estado 
// viable: true → verde    viable: false → rojo    viable: null → gris
const STATE_CLASS = {
    true:  'item-viable',
    false: 'item-no-viable',
    null:  'item-none',
};

const BADGE_CLASS = {
    true:  { cls: 'badge-viable',    text: 'Viable' },
    false: { cls: 'badge-no-viable', text: 'No viable' },
    null:  { cls: 'badge-none',      text: 'Sin evaluar' },
};

//  Carga la lista lateral 
async function loadList() {
    try {
        const res  = await fetch('/lista_practicantes');
        const data = await res.json();   // [{ email, viable }, ...]

        internList.innerHTML = '';

        if (!data.length) {
            internList.innerHTML = '<li class="list-placeholder">Sin practicantes registrados.</li>';
            return;
        }

        data.forEach(({ email, viable }) => {
            const li = document.createElement('li');
            li.textContent = email;
            li.dataset.email  = email;
            li.dataset.viable = viable === null ? 'null' : String(viable);
            li.className = `intern-item ${STATE_CLASS[viable]}`;

            li.addEventListener('click', () => selectIntern(email, li));
            internList.appendChild(li);
        });

    } catch (err) {
        internList.innerHTML = '<li class="list-placeholder">Error al cargar la lista.</li>';
        console.error(err);
    }
}

//  Selecciona un practicante y carga su detalle 
async function selectIntern(email, liEl) {
    // Resalta el ítem seleccionado
    document.querySelectorAll('.intern-item').forEach(el => el.classList.remove('selected'));
    liEl.classList.add('selected');

    actionMessage.textContent = '';
    showDetail(false);

    try {
        const res  = await fetch(`/practicante?email=${encodeURIComponent(email)}`);
        const data = await res.json();   // { email, fullname, phone, degree, semester, cv_route, viable }

        currentEmail   = data.email;
        currentCVRoute = data.cv_route || null;

        detailName.textContent     = data.fullname  || '—';
        detailEmail.textContent    = data.email     || '—';
        detailPhone.textContent    = data.phone     || '—';
        detailDegree.textContent   = data.degree    || '—';
        detailSemester.textContent = data.semester  !== null ? `Semestre ${data.semester}` : '—';

        const viable = data.viable === undefined ? null : data.viable;
        updateBadge(viable);

        btnDownloadCV.disabled = !currentCVRoute;
        showDetail(true);

    } catch (err) {
        actionMessage.textContent = 'Error al cargar la información del practicante.';
        console.error(err);
    }
}

//  Muestra u oculta el panel de detalle 
function showDetail(show) {
    emptyState.classList.toggle('hidden', show);
    internDetail.classList.toggle('hidden', !show);
}

//  Actualiza el badge de estado 
function updateBadge(viable) {
    const key   = viable === null ? null : (viable === true || viable === 'true');
    const { cls, text } = BADGE_CLASS[key] ?? BADGE_CLASS[null];

    detailBadge.className   = `badge ${cls}`;
    detailBadge.textContent = text;
}

//  Actualiza el color del ítem en la lista ─
function updateListItem(email, viable) {
    const li = internList.querySelector(`[data-email="${email}"]`);
    if (!li) return;

    li.classList.remove('item-viable', 'item-no-viable', 'item-none');
    li.classList.add(STATE_CLASS[viable]);
    li.dataset.viable = viable === null ? 'null' : String(viable);
}

//  Marca como viable o no viable 
async function markIntern(viable) {
    if (!currentEmail) return;

    actionMessage.textContent = '';

    try {
        const res = await fetch('/marcar_viable', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ email: currentEmail, viable }),
        });

        if (!res.ok) throw new Error('Respuesta no exitosa');

        updateBadge(viable);
        updateListItem(currentEmail, viable);
        actionMessage.style.color    = viable ? '#4caf50' : '#e02323';
        actionMessage.textContent    = viable
            ? 'Practicante marcado como Viable.'
            : 'Practicante marcado como No Viable.';

    } catch (err) {
        actionMessage.style.color   = '#e02323';
        actionMessage.textContent   = 'Error al guardar el estado.';
        console.error(err);
    }
}

//  Descarga el CV ─
btnDownloadCV.addEventListener('click', () => {
    if (!currentCVRoute) return;
    const a = document.createElement('a');
    a.href     = `/descargar_cv?cv_route=${currentCVRoute}`;
    a.download = '';
    a.click();
});

btnViable.addEventListener('click',   () => markIntern(true));
btnNoViable.addEventListener('click', () => markIntern(false));

//  Init 
loadList();
