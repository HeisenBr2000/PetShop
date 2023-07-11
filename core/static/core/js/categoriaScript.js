// Obtener el campo de categoría y el campo de producto
const categoriaSelect = document.getElementById('id_categoria');
const productoSelect = document.getElementById('id_producto');

// Función para actualizar el queryset del campo de producto
function actualizarProductos() {
    // Obtener el valor de la categoría seleccionada
    const categoriaId = categoriaSelect.value;
    
    // Hacer una solicitud AJAX para obtener los productos de la categoría seleccionada
    fetch(`/obtener-productos/${categoriaId}/`)  // Reemplaza "/obtener-productos/" con tu URL adecuada
        .then(response => response.json())
        .then(data => {
            // Limpiar las opciones actuales del campo de producto
            productoSelect.innerHTML = '';

            // Crear nuevas opciones para cada producto
            data.forEach(producto => {
                const option = document.createElement('option');
                option.value = producto.id;
                option.textContent = producto.nombre;
                productoSelect.appendChild(option);
            });
        });
}

// Escuchar el evento de cambio en el campo de categoría
categoriaSelect.addEventListener('change', actualizarProductos);

// Llamar a la función inicialmente para cargar los productos de la categoría seleccionada (si es necesario)
actualizarProductos();