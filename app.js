async function buscarPrenda() {
    const query = document.getElementById('prenda').value.toLowerCase();
    const minPrice = parseFloat(document.getElementById('minPrice').value) || 0;
    const maxPrice = parseFloat(document.getElementById('maxPrice').value) || Infinity;
    const contenedor = document.getElementById('resultados');

    contenedor.innerHTML = '<p class="text-white">Cargando catálogo inteligente...</p>';

    try {
        const response = await fetch('./catalog.json');
        const productos = await response.json();

        // 1. FILTRAR
        let resultados = productos.filter(p => {
            const coincideNombre = p.title.toLowerCase().includes(query);
            const coincidePrecio = p.price >= minPrice && p.price <= maxPrice;
            return coincideNombre && coincidePrecio;
        });

        // 2. ORDENAR (Menor a Mayor precio)
        resultados.sort((a, b) => a.price - b.price);

        // 3. MOSTRAR
        mostrarResultados(resultados);

    } catch (e) {
        contenedor.innerHTML = '<p class="text-red-500">Error al conectar con la base de datos.</p>';
    }
}

function mostrarResultados(lista) {
    const contenedor = document.getElementById('resultados');
    contenedor.innerHTML = lista.length ? '' : '<p>No se encontraron prendas.</p>';
    
    lista.forEach(p => {
        contenedor.innerHTML += `
            <div class="bg-[#1a1a1a] border border-white/10 rounded-xl overflow-hidden shadow-2xl">
                <img src="${p.image}" class="w-full h-72 object-cover">
                <div class="p-5">
                    <h3 class="text-gray-400 text-xs uppercase tracking-widest">${p.category}</h3>
                    <h2 class="text-white font-bold text-lg">${p.title}</h2>
                    <p class="text-2xl text-indigo-400 font-light mt-2">${p.price} €</p>
                    <a href="${p.link}" target="_blank" class="block w-full text-center bg-indigo-600 hover:bg-indigo-700 text-white mt-4 py-3 rounded-lg transition">Comprar en Zara</a>
                </div>
            </div>
        `;
    });
}
