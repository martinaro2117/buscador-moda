async function buscarPrenda() {
    const prenda = document.getElementById('prenda').value;
    const min = document.getElementById('minPrice').value;
    const max = document.getElementById('maxPrice').value;
    const contenedor = document.getElementById('resultados');

    if(!prenda) return alert("Escribe qué buscas");

    contenedor.innerHTML = '<p class="text-center col-span-3">Buscando...</p>';

    try {
        // Ejemplo con la API de Mercado Libre (Pública y no requiere Auth complejo para pruebas)
        const response = await fetch(`https://api.mercadolibre.com/sites/MLA/search?q=${prenda}&price=${min}-${max}`);
        const data = await response.json();

        mostrarResultados(data.results);
    } catch (error) {
        console.error("Error:", error);
        contenedor.innerHTML = "Hubo un error al conectar con la API.";
    }
}

function mostrarResultados(productos) {
    const contenedor = document.getElementById('resultados');
    contenedor.innerHTML = '';

    productos.slice(0, 12).forEach(prod => {
        contenedor.innerHTML += `
            <div class="bg-white p-4 rounded shadow hover:shadow-lg transition">
                <img src="${prod.thumbnail}" alt="${prod.title}" class="w-full h-48 object-contain mb-4">
                <h3 class="font-bold text-sm h-10 overflow-hidden">${prod.title}</h3>
                <p class="text-indigo-600 font-bold text-xl mt-2">$ ${prod.price}</p>
                <a href="${prod.permalink}" target="_blank" class="block text-center bg-gray-800 text-white mt-4 py-2 rounded text-sm">Ver producto</a>
            </div>
        `;
    });
}
