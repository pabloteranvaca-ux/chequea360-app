const CSV_URL =
"https://docs.google.com/spreadsheets/d/1ong4kdAkmigKBT0Ra5LLJJmsrAEPYivh/gviz/tq?tqx=out:csv&gid=828045008";

const universidades = [
  "Universidad Central del Ecuador",
  "Universidad Politécnica Salesiana",
  "Pontificia Universidad Católica",
  "Universidad Técnica Particular de Loja",
  "Universidad Técnica de Cotopaxi",
  "Universidad Técnica de Manabí",
  "Universidad de Especialidades Espíritu Santo",
  "Universidad Estatal de Bolívar"
];

async function cargarDatos() {
  let data = universidades.map(nombre => ({
    universidad: nombre,
    falso: 0,
    enganoso: 0,
    impreciso: 0,
    cierto: 0,
    satira: 0,
    inverificable: 0
  }));

  try {
    const response = await fetch(CSV_URL + "&t=" + Date.now(), {
      cache: "no-store"
    });

    const text = await response.text();

    universidades.forEach((nombre, i) => {
      const fila = text
        .split(/\r?\n/)
        .find(linea => linea.includes(nombre));

      if (fila) {
        const c = fila.split(",");

        data[i] = {
          universidad: nombre,
          falso: numero(c[5]),
          enganoso: numero(c[6]),
          impreciso: numero(c[7]),
          cierto: numero(c[8]),
          satira: numero(c[9]),
          inverificable: numero(c[10])
        };
      }
    });

  } catch (e) {
    console.error("No se pudo leer el Sheet:", e);
  }

  pintar(data);
}

function numero(valor) {
  const n = parseInt(String(valor || "").replaceAll('"', "").trim(), 10);
  return isNaN(n) ? 0 : n;
}

function poner(id, valor) {
  const el = document.getElementById(id);
  if (el) el.innerText = valor;
}

function pintar(data) {
  poner("falsos", data.reduce((s,u) => s + u.falso, 0));
  poner("enganosos", data.reduce((s,u) => s + u.enganoso, 0));
  poner("imprecisos", data.reduce((s,u) => s + u.impreciso, 0));
  poner("verdaderos", data.reduce((s,u) => s + u.cierto, 0));
  poner("satiras", data.reduce((s,u) => s + u.satira, 0));
  poner("inverificables", data.reduce((s,u) => s + u.inverificable, 0));

  const cards = document.getElementById("cards");
  if (!cards) return;

  cards.innerHTML = "";

  data.forEach(u => {
    cards.innerHTML += `
      <div class="card">
        <h2>${u.universidad}</h2>
        <hr>
        <p>🔴 Falso: <strong>${u.falso}</strong></p>
        <p>🟠 Engañoso: <strong>${u.enganoso}</strong></p>
        <p>🟡 Impreciso: <strong>${u.impreciso}</strong></p>
        <p>🟢 Cierto: <strong>${u.cierto}</strong></p>
        <p>🟣 Sátira: <strong>${u.satira}</strong></p>
        <p>⚫ Inverificable: <strong>${u.inverificable}</strong></p>
      </div>
    `;
  });
}

cargarDatos();
setInterval(cargarDatos, 10000);