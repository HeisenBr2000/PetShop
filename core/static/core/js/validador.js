$(document).ready(function() {
  $('#myForm').validate({
    rules: {
      rut: {
        required: true,
        pattern: /[0-9]{7,8}-[0-9Kk]/
      },
      name: 'required',
      email: {
        required: true,
        email: true
      },
      password: {
        required: true,
        minlength: 8
      },
      confirmPassword: {
        required: true,
        minlength: 8,
        equalTo: '#password'
      },
      phone: {
        required: true,
        pattern: /[0-9]{10}/
      },
      country: 'required',
      address: 'required',
      postalCode: {
        required: true,
        pattern: /[0-9]{5}/
      },
      age: {
        required: true,
        min: 18,
        max: 99
      },
      terms: 'required'
    },
    messages: {
      rut: {
        required: 'Por favor, ingresa tu RUT',
        pattern: 'Formato incorrecto. Debe ser 12345678-9'
      },
      name: 'Por favor, ingresa tu nombre',
      email: {
        required: 'Por favor, ingresa tu correo electrónico',
        email: 'Por favor, ingresa un correo electrónico válido'
      },
      password: {
        required: 'Por favor, ingresa una contraseña',
        minlength: 'La contraseña debe tener al menos 8 caracteres'
      },
      confirmPassword: {
        required: 'Por favor, confirma tu contraseña',
        minlength: 'La contraseña debe tener al menos 8 caracteres',
        equalTo: 'Las contraseñas no coinciden'
      },
      phone: {
        required: 'Por favor, ingresa tu número de teléfono',
        pattern: 'Formato incorrecto. Debe tener 10 dígitos'
      },
      country: 'Por favor, ingresa tu país',
      address: 'Por favor, ingresa tu dirección',
      postalCode: {
        required: 'Por favor, ingresa tu código postal',
        pattern: 'Formato incorrecto. Debe tener 5 dígitos'
      },
      age: {
        required: 'Por favor, ingresa tu edad',
        min: 'Debes tener al menos 18 años',
        max: 'Debes tener menos de 99 años'
      },
      terms: 'Debes aceptar los términos y condiciones'
    },
    submitHandler: function(form) {
      // Place your form submission logic here
      $('#formResult').text('Formulario enviado correctamente');
    }
  });
});