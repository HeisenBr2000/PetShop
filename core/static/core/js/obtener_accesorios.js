
$(document).ready(function () {

    
    $('#btn-obtener-accesorios').click(function () { 

        $.get('https://fakestoreapi.com/products?limit=10', 

        function(data){
            

            $('#tabla-accesorios tbody').empty();
            console.log($('#tabla-accesorios tbody'))
            
            $.each(data, function(i, item) {
                

                var fila = '';
                fila += '<tr>';
                fila += '    <td>' + i + '</td>';
                fila += '    <td>' + item.id + '</td>';
                fila += '    <td>' + item.title + '</td>';
                fila += '    <td>' + item.price + '</td>';
                fila += '    <td>' + item.description + '</td>';
                fila += '    <td>' + item.category + '</td>';
                fila += '    <td><img src="' + item.image + '"></td>';
                fila += '    <td>' + item.rating + '</td>';
                fila += '</tr>';
                $('#tabla-accesorios').append(fila);   
            
            });
        });

    });  

});  

