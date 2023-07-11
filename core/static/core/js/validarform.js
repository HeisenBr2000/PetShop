
$(document).ready(function() {
  $("#submitBtn").click(function(e) {
    e.preventDefault();

    // Clear previous error messages
    $('.error-message').remove();

    // Validate email
    var email = $('#email').val();
    if (!emailIsValid(email)) {
      $('<span class="error-message">Por favor, introduce un correo electrónico válido</span>').insertAfter('#email');
      return;
    }

    // Validate password
    var password = $('#password').val();
    if (password.length < 6) {
      $('<span class="error-message">La contraseña debe tener al menos 6 caracteres</span>').insertAfter('#password');
      return;
    }

    // Validate confirm password
    var confirmPassword = $('#confirmPassword').val();
    if (password !== confirmPassword) {
      $('<span class="error-message">Las contraseñas no coinciden</span>').insertAfter('#confirmPassword');
      return;
    }

    // Validate phone
    var phone = $('#phone').val();
    if (!phoneIsValid(phone)) {
      $('<span class="error-message">Por favor, introduce un número de teléfono válido</span>').insertAfter('#phone');
      return;
    }

    // Validate country
    var country = $('#country').val();
    if (country.length === 0) {
      $('<span class="error-message">Por favor, introduce el país</span>').insertAfter('#country');
      return;
    }

    // Validate address
    var address = $('#address').val();
    if (address.length === 0) {
      $('<span class="error-message">Por favor, introduce la dirección</span>').insertAfter('#address');
      return;
    }

    // Validate postal code
    var postalCode = $('#postalCode').val();
    if (postalCode.length === 0) {
      $('<span class="error-message">Por favor, introduce el código postal</span>').insertAfter('#postalCode');
      return;
    }

    // Validate age
    var age = parseInt($('#age').val());
    if (isNaN(age) || age < 18 || age > 99) {
      $('<span class="error-message">Por favor, introduce una edad válida (entre 18 y 99)</span>').insertAfter('#age');
      return;
    }

    // Validate terms acceptance
    if (!$('#terms').is(':checked')) {
      $('<span class="error-message">Debes aceptar los términos y condiciones</span>').insertAfter('#terms');
      return;
    }

    // Email validation function
    function emailIsValid(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Phone validation function
    function phoneIsValid(phone) {
      return /^\d{10}$/.test(phone);
    }

    // RUT validation function
    function rutIsValid(rut) {
      if (rut.length < 3) {
        return false;
      }

      // Remove non-digit characters and leading zeros
      rut = rut.replace(/[^0-9kK]/g, '').replace(/^0+/, '');

      if (rut.length < 2) {
        return false;
      }

      var dv = rut.slice(-1).toUpperCase();
      var rutNumber = parseInt(rut.slice(0, -1));

      if (isNaN(rutNumber)) {
        return false;
      }

      var calcDV = calculateDV(rutNumber);

      return calcDV === dv;
    }

    function calculateDV(rutNumber) {
      var m = 0;
      var s = 1;

      while (rutNumber > 0) {
        s = (s + rutNumber % 10 * (9 - m++ % 6)) % 11;
        rutNumber = Math.floor(rutNumber / 10);
      }

      return s ? String.fromCharCode(s + 47) : 'K';
    }

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






