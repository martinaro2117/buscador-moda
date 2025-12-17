async function buscarPrenda() {
    const query = document.getElementById('prenda').value.toLowerCase();
    const minP = parseFloat(document.getElementById('minPrice').value) || 0;
    const maxP = parseFloat(document.getElementById('maxPrice').value) || 9999;
    const contenedor = document.getElementById('resultados');

    contenedor.innerHTML = '<p class="text-indigo-400 animate-pulse">Conectando con el catálogo de Zara...</p>';

    try {
        // Intentamos cargar el archivo usando una ruta relativa segura
        const response = await fetch('./catalog.json');
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const productos = await response.json();

        // Filtrar productos
        let filtrados = productos.filter(p => {
            const coincideNombre = p.title.toLowerCase().includes(query);
            const coincidePrecio = p.price >= minP && p.price <= maxP;
            return coincideNombre && coincidePrecio;
        });

        // Ordenar de menor a mayor precio
        filtrados.sort((a, b) => a.price - b.price);

        mostrarResultados(filtrados);

    } catch (error) {
        console.error("Detalles del error:", error);
        contenedor.innerHTML = `
            <div class="p-4 bg-red-900/20 border border-red-500 rounded-lg">
                <p class="text-red-500 font-bold">Error al conectar con la base de datos.</p>
                <p class="text-xs text-red-400 mt-2">Causa: El archivo catalog.json no se encuentra o está vacío.</p>
            </div>
        `;
    }
}

function mostrarResultados(productos) {
    const contenedor = document.getElementById('resultados');
    contenedor.innerHTML = '';

    if (productos.length === 0) {
        contenedor.innerHTML = '<p class="text-gray-500">No se han encontrado prendas que coincidan.</p>';
        return;
    }

    productos.forEach(prod => {
        contenedor.innerHTML += `
            <div class="bg-[#1a1a1a] rounded-2xl overflow-hidden border border-white/5 hover:border-indigo-500 transition-all group">
                <div class="relative overflow-hidden">
                    <img src="${prod.image}" alt="${prod.title}" class="w-full h-80 object-cover group-hover:scale-105 transition-transform duration-500">
                </div>
                <div class="p-6">
                    <p class="text-indigo-500 text-xs font-bold uppercase tracking-widest mb-1">${prod.category}</p>
                    <h3 class="text-white font-medium text-lg mb-2">${prod.title}</h3>
                    <div class="flex justify-between items-center mt-4">
                        <span class="text-2xl font-light text-white">${prod.price} €</span>
                        <a href="${prod.link}" target="_blank" class="bg-white text-black px-4 py-2 rounded-lg font-bold text-xs uppercase hover:bg-indigo-500 hover:text-white transition">Ver en Zara</a>
                    </div>
                </div>
            </div>
        `;
    });
}
