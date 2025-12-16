async function buscarPrenda() {
    const prenda = document.getElementById('prenda').value;
    const min = document.getElementById('minPrice').value;
    const max = document.getElementById('maxPrice').value;
    const contenedor = document.getElementById('resultados');

    if(!prenda) return alert("Tienes que introducir la prenda para que te funcione");

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

    productos.forEach(prod => {
        contenedor.innerHTML += `
            <div class="bg-[#222] p-4 rounded-2xl border border-white/5 hover:border-white/20 transition group">
                <img src="${prod.thumbnail}" alt="${prod.title}" class="w-full h-64 object-contain mb-4 rounded-lg bg-white/5">
                <h3 class="text-sm font-medium h-10 overflow-hidden text-gray-300">${prod.title}</h3>
                <p class="text-white font-bold text-xl mt-2">${prod.price} €</p>
                <a href="${prod.permalink}" target="_blank" class="block text-center bg-white/5 text-white border border-white/10 mt-4 py-2 rounded-lg hover:bg-white hover:text-black transition">Ver detalle</a>
            </div>
        `;
    });
}
