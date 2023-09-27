//VALIDACIONES
var ced = document.getElementById('Identificacion');
if (ced == null) {
} else {
	ced.addEventListener('input', function () {
		if (this.value.length > 13) {
			this.value = this.value.slice(0, 13);
			var ms = '*El campo Ruc es de 13 dígitos.';
			$('#alert-ident').text('' + ms).css('background', 'white');
			$('#alert-ident').show();
		} else {
			$('#alert-ident').hide();
		}
	})
}
$("#Identificacion").bind('keypress', function (event) {
    var regex = new RegExp("^[0-9]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        var ms = '*Este campo acepta solo números.';
        $('#alert-ident').text('' + ms).css('background', 'white');
        $('#alert-ident').show();
        event.preventDefault();
        return false;
    } else {
        $('#alert-ident').hide();
    }
});
$("#IdNombres").bind('keypress', function (event) {
    var regex = new RegExp("^[a-zA-Z ]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        var ms = '*Este campo acepta solo letras.';
        $('#alert-nomb').text('' + ms).css('background', 'white');
        $('#alert-nomb').show();
        event.preventDefault();
        return false;
    } else {
        $('#alert-nomb').hide();
    }
});
$("#IdApellidos").bind('keypress', function (event) {
    var regex = new RegExp("^[a-zA-Z ]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        var ms = '*Este campo acepta solo letras.';
        $('#alert-ape').text('' + ms).css('background', 'white');
        $('#alert-ape').show();
        event.preventDefault();
        return false;
    } else {
        $('#alert-ape').hide();
    }
});
var tel = document.getElementById('IdTelefono');
if (tel == null) {
} else {
	tel.addEventListener('input', function () {
		if (this.value.length > 10) {
			this.value = this.value.slice(0, 10);
			var ms = '*El campo Teléfono es de 10 dígitos.';
			$('#alert-tel').text('' + ms).css('background', 'white');
			$('#alert-tel').show();
		} else {
			$('#alert-tel').hide();
		}
	})
}
$("#IdTelefono").bind('keypress', function (event) {
    var regex = new RegExp("^[0-9]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        var ms = '*Este campo acepta solo números.';
        $('#alert-tel').text('' + ms).css('background', 'white');
        $('#alert-tel').show();
        event.preventDefault();
        return false;
    } else {
        $('#alert-tl').hide();
    }
});
function validateEmail(){
	var correo_empresa = document.getElementById('IdEmail');
	var validar =  /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/;
	if(validar.test(correo_empresa.value)){
        var ms = '*Correo válido!.';
			$('#alert-ema').text('' + ms).css('background', 'white');
			$('#alert-ema').show();
		return true;
	}else{
        var ms = '*Ingrese un correo válido.';
			$('#alert-ema').text('' + ms).css('background', 'white');
			$('#alert-ema').show();
		$("#IdEmail").val('');
		return false;
	}
}