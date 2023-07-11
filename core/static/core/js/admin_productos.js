$(document).ready(function() {
    $.validator.setDefaults({
        messages: {
            required: 'Este campo es obligatorio',
        },
    });

    $('#form').validate({
        rules: {
            'tipo_usuario': {
                required: true,
            },
            'rut': {
                required: true,
            },
            'direccion': {
                required: true,
            },
            'subscrito': {
                required: true,
            },
        },
        messages: {
            'tipo_usuario': {
                required: 'Debe seleccionar el tipo de usuario',
            },
            'rut': {
                required: 'Debe ingresar el RUT',
            },
            'direccion': {
                required: 'Debe ingresar la dirección',
            },
            'subscrito': {
                required: 'Debe seleccionar si está suscrito',
            },
        },
        errorPlacement: function(error, element) {
            error.insertAfter(element);
            error.addClass('error-message');
        },
    });

    // Eliminación de usuario
    $('#form').on('submit', function(e) {
        e.preventDefault(); // Evita el envío del formulario por defecto

        // Mostrar confirmación de eliminación
        if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
            // Enviar la solicitud de eliminación
            var url = $(this).attr('action');
            $.ajax({
                url: url,
                type: 'POST',
                data: $(this).serialize(),
                success: function(response) {
                    // Manejar la respuesta de éxito
                    alert('El usuario ha sido eliminado correctamente.');
                    // Redireccionar a la página deseada o actualizar la lista de usuarios, etc.
                },
                error: function(xhr, status, error) {
                    // Manejar el error en caso de que ocurra
                    alert('Ocurrió un error al intentar eliminar el usuario.');
                }
            });
        }
    });

    $('#id_imagen').change(function() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#admin-usuario-imagen').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(input.files[0]);
        }
    });
});
