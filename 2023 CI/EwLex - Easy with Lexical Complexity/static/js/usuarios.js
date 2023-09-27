function getModalLoginAdmin() {
  $("#login-admin").modal("show");
}
function getModalLoginUsuario() {
  $("#login-usuario").modal("show");
}
function getLoginAdmin() {
  var html = "";
  if ($("#IdUsuarioA").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-usera").html(html);
    $("#IdUsuarioA").focus();
    setTimeout(function () {
      $("#alert-usera").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdClaveA").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-passa").html(html);
    $("#IdClaveA").focus();
    setTimeout(function () {
      $("#alert-passa").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var user = $("#IdUsuarioA").val();
    var clave = $("#IdClaveA").val();
    var html = "";
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/loginadmin",
      data: "Email=" + user + "&Password=" + clave,
      success: function (response) {
        //response = JSON.stringify(response);
        if (response!='') {
          Swal.fire({
            html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Bienbeni@!.</b></div></div>',
          });
          window.location.href = "/administrador";
        }
        if (response == "") {
          Swal.fire({
            html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Credenciales incorrectas!.</b></div></div>',
          });
          $("#IdUsuarioA").val('');
          $("#IdClaveA").val('');
          //window.location.href = "/";
        }
      },
    });
  }
}
function getLoginUsuario() {
  var html = "";
  if ($("#IdUsuario").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-user").html(html);
    $("#IdUsuario").focus();
    setTimeout(function () {
      $("#alert-user").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdClave").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-pass").html(html);
    $("#IdClave").focus();
    setTimeout(function () {
      $("#alert-pass").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var user = $("#IdUsuario").val();
    var clave = $("#IdClave").val();
    var html = "";
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/loginuser",
      data: "Email=" + user + "&Password=" + clave,
      success: function (response) {
        //response = JSON.stringify(response);
        if (response!='') {
          Swal.fire({
            html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Bienbeni@!.</b></div></div>',
          });
          window.location.href = "/estudiantes";
        }
        if (response == "") {
          Swal.fire({
            html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Credenciales incorrectas!.</b></div></div>',
          });
          $("#IdUsuario").val('');
          $("#IdClave").val('');
          //window.location.href = "/";
        }
      },
    });
  }
}
function loginuser() {
  window.location.href = "/login";
}
function getModalRegistroUsuario() {
  $("#registro-usuario").modal("show");
  getTipoIdentificacion();
  getPreguntasValidacionReg();
}
function getModalRegistroUsuarioAdmin() {
  $("#registro-usuarioadm").modal("show");
  getTipoIdentificacion();
  getPreguntasValidacionRegAdmin();
}
function ValidarPasswordUser() {
  var html = "";
  var npass = $("#IdPassword").val();
  var vpass = $("#ValPassword").val();
  if (npass != vpass) {
    setTimeout(function () {
      html += '<div class="note note-danger" id="alert-passi">';
      html += '<i class="fa fa-thumbs-down"></i>';
      html += '<b style="color:red;"> Las Contraseñas no coinciden!.</b>';
      html += "</div>";
      $("#valida-vnpass").html(html);
      $("#alert-passi").fadeOut(3000);
    }, 0);
    $("#IdPassword").val("");
    $("#ValPassword").val("");
    $("#IdPassword").focus();
  } else {
    setTimeout(function () {
      html += '<div class="note note-danger" id="alert-passi">';
      html += '<i class="fa fa-thumbs-up"></i>';
      html += '<b style="color:green;"> Contraseñas ok!.</b>';
      html += "</div>";
      $("#valida-vnpass").html(html);
      $("#alert-passi").fadeOut(3000);
    }, 0);
  }
}
function ValidarPasswordRecuperaPass() {
  var html = "";
  var npass = $("#IdPasswordRq").val();
  var vpass = $("#ValPasswordRq").val();
  if (npass != vpass) {
    setTimeout(function () {
      html += '<div class="note note-danger" id="alert-passi">';
      html += '<i class="fa fa-thumbs-down"></i>';
      html += '<b style="color:red;"> Las Contraseñas no coinciden!.</b>';
      html += "</div>";
      $("#valida-vpass").html(html);
      $("#alert-passi").fadeOut(3000);
    }, 0);
    $("#IdPasswordRq").val("");
    $("#ValPasswordRq").val("");
    $("#IdPasswordRq").focus();
  } else {
    setTimeout(function () {
      html += '<div class="note note-danger" id="alert-passi">';
      html += '<i class="fa fa-thumbs-up"></i>';
      html += '<b style="color:green;"> Contraseñas ok!.</b>';
      html += "</div>";
      $("#valida-vpass").html(html);
      $("#alert-passi").fadeOut(3000);
    }, 0);
  }
}
function RegistrarUsuario() {
  var html = "";
  if ($("#IdNombres").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-nomb").html(html);
    $("#IdNombresIdNombres").focus();
    setTimeout(function () {
      $("#alert-nomb").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdApellidos").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ape").html(html);
    $("#IdApellidos").focus();
    setTimeout(function () {
      $("#alert-ape").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#TipoIdentificacion").val() == "0") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-tpident").html(html);
    $("#TipoIdentificacion").focus();
    setTimeout(function () {
      $("#alert-tpident").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#Identificacion").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ident").html(html);
    $("#Identificacion").focus();
    setTimeout(function () {
      $("#alert-ident").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdDireccion").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-dir").html(html);
    $("#IdDireccion").focus();
    setTimeout(function () {
      $("#alert-dir").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdTelefono").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-tel").html(html);
    $("#IdTelefono").focus();
    setTimeout(function () {
      $("#alert-tel").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdEmail").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ema").html(html);
    $("#IdEmail").focus();
    setTimeout(function () {
      $("#alert-ema").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdPassword").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-pass").html(html);
    $("#IdPassword").focus();
    setTimeout(function () {
      $("#alert-pass").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdPreguntasReg").val() == "0") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-preg").html(html);
    $("#IdPreguntasReg").focus();
    setTimeout(function () {
      $("#alert-preg").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdRespuestaReg").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-respreg").html(html);
    $("#IdRespuestaReg").focus();
    setTimeout(function () {
      $("#alert-respreg").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var nomb = $("#IdNombres").val();
    var ape = $("#IdApellidos").val();
    var tident = $("#TipoIdentificacion").val();
    var ident = $("#Identificacion").val();
    var dir = $("#IdDireccion").val();
    var tel = $("#IdTelefono").val();
    var ema = $("#IdEmail").val();
    var pass = $("#IdPassword").val();
    var preg = $("#IdPreguntasReg").val();
    var resp = $("#IdRespuestaReg").val();
    Swal.fire({
      title: "Desea continuar?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí continuar",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          type: "POST",
          dataType: "json",
          url: "/regusuario",
          data:
            "Nombres=" +
            nomb +
            "&Apellidos=" +
            ape +
            "&IdTipo=" +
            tident +
            "&Identificacion=" +
            ident +
            "&Direccion=" +
            dir +
            "&Telefono=" +
            tel +
            "&Email=" +
            ema +
            "&Password=" +
            pass +
            "&IdPregunta=" +
            preg + 
            "&Respuesta=" +
            resp,
          success: function (response) {
            if (response == 'existe') {
              Swal.fire({
                html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>El e-mail ya existe!.</b></div></div>',
              });
            }
            if (response == true) {
              Swal.fire({
                html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Registrado OK!.</b></div></div>',
              });
              $("#registro-usuario").modal("hide");
            }
          },
        });
      }
    });
  }
}
function RegistrarUsuarioAdmin() {
  var html = "";
  if ($("#IdNombres").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-nomb").html(html);
    $("#IdNombres").focus();
    setTimeout(function () {
      $("#alert-nomb").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdApellidos").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ape").html(html);
    $("#IdApellidos").focus();
    setTimeout(function () {
      $("#alert-ape").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#TipoIdentificacion").val() == "0") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-tident").html(html);
    $("#TipoIdentificacion").focus();
    setTimeout(function () {
      $("#alert-tident").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#Identificacion").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ident").html(html);
    $("#Identificacion").focus();
    setTimeout(function () {
      $("#alert-ident").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdDireccion").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-dir").html(html);
    $("#IdDireccion").focus();
    setTimeout(function () {
      $("#alert-dir").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdTelefono").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-tel").html(html);
    $("#IdTelefono").focus();
    setTimeout(function () {
      $("#alert-tel").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdEmail").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ema").html(html);
    $("#IdEmail").focus();
    setTimeout(function () {
      $("#alert-ema").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdPassword").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-pas").html(html);
    $("#IdPassword").focus();
    setTimeout(function () {
      $("#alert-pas").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdPreguntasRegAdm").val() == "0") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-pregadm").html(html);
    $("#IdPreguntasRegAdm").focus();
    setTimeout(function () {
      $("#alert-pregadm").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdRespuestaRegAdm").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-respregadm").html(html);
    $("#IdRespuestaRegAdm").focus();
    setTimeout(function () {
      $("#alert-respregadm").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var nomb = $("#IdNombres").val();
    var ape = $("#IdApellidos").val();
    var tident = $("#TipoIdentificacion").val();
    var ident = $("#Identificacion").val();
    var dir = $("#IdDireccion").val();
    var tel = $("#IdTelefono").val();
    var ema = $("#IdEmail").val();
    var pass = $("#IdPassword").val();
    var preg = $("#IdPreguntasRegAdm").val();
    var resp = $("#IdRespuestaRegAdm").val();
    Swal.fire({
      title: "Desea continuar?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí continuar",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          type: "POST",
          dataType: "json",
          url: "/regusuario_admin",
          data:
            "Nombres=" +
            nomb +
            "&Apellidos=" +
            ape +
            "&IdTipo=" +
            tident +
            "&Identificacion=" +
            ident +
            "&Direccion=" +
            dir +
            "&Telefono=" +
            tel +
            "&Email=" +
            ema +
            "&Password=" +
            pass +
            "&IdPregunta=" +
            preg +
            "&Respuesta=" +
            resp,
          success: function (response) {
            response = JSON.parse(response);
            if (response == 0) {
              Swal.fire({
                html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>No se realizo el registro!.</b></div></div>',
              });
            }
            if (response == true) {
              Swal.fire({
                html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Registrado OK!.</b></div></div>',
              });
              $("#registro-usuario").modal("hide");
            }
          },
        });
      }
    });
  }
}
function cantidadCarcteres() {
  const mensaje = document.getElementById('IngresoTexto');
  const contador = document.getElementById('contador');
  mensaje.addEventListener('input', function (e) {
    const target = e.target;
    const longitudMax = target.getAttribute('maxlength');
    const longitudAct = target.value.length;
    contador.innerHTML = `${longitudAct}/${longitudMax}`;
  });
}
function getBuscar() {
  getLimpiarBusqueda();
  var html = "";
  if ($("#IngresoTexto").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-txt").html(html);
    $("#IngresoTexto").focus();
    setTimeout(function () {
      $("#alert-txt").fadeOut(1500);
    }, 3000);
    return false;
  } else{
    var buscar = $("#IngresoTexto").val();
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/buscar",
    data: "cadena=" + buscar,
    beforeSend: function () {
      $(".loader_imagen").show();
    },
    success: function (response) {
      $(".loader_imagen").hide();
      if (response) {
        al = 0;
        $.each(response, function (i, item) {
          al = al + 1;
          html +=
            '<a class="btn btn-outline-info" href="#" onclick="getBuscarSinonimos(' +
            item[0] +
            ');" title="Buscar"><i class="fa fa-search"';
          html += 'aria-hidden="true"></i> ' + item[1] + "</a>&nbsp;";
          $("#palabras").html(html);
        });
        $("#NroPalabras").text(al);
      }
      if (response=="") {
        $("#alert-cpalabras").html('No se encontraron palabras en el diccionario.');
      }
    },
  });
  }
}
function getBuscarPalabraSeleccionada(idp){
  $("#alert-csinonimos").text('');
  $("#alert-cdefiniciones").text('');
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_palabra",
    data: "IdPalabra=" + idp,
    success: function (response) {
      if (response) {
        $("#IdPalabraSnm").text(" " + response[0]);
        $("#IdPalabraDf").text(" " + response[0]);
      }
      $("#sinonimos").text("");
      $("#definiciones").text("");
    },
  });
}
function getBuscarSinonimos(idp){
  getBuscarPalabraSeleccionada(idp)
  var html = "";
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_sinonimos",
    data: "IdPalabra=" + idp,
    beforeSend: function () {
			$('.loader_imagen').show();
		},
    success: function (response) {
      $('.loader_imagen').hide();
      if (response) {
        $.each(response, function (i, item) {
          html += '<cite style="color: green;"> | '+item+'</cite>';
          $("#sinonimos").html(html);
          $("#IdSinonim").text(item[1]);
        });
        getBuscarDeficiciones(idp)
      }
      if (response=="") {
        $("#alert-csinonimos").html('No se encontraron ninonimos.');
      }
    },
  });
}
function getBuscarDeficiciones(idp){
  var html = "";
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_deficiciones",
    data: "IdPalabra=" + idp,
    beforeSend: function () {
			$('.loader_imagen').show();
		},
    success: function (response) {
      $('.loader_imagen').hide();
      if (response) {
        $.each(response, function (i, item) {
          html += '<cite style="color: blue;"> | '+item+'</cite>';
          $("#definiciones").html(html);
        });
      }
      if (response=="") {
        $("#alert-cdefiniciones").html('No se encontraron definiciones.');
      }
    },
  });
}
function getUsuarios() {
  window.location.href = "/usuarios";
}
function getEstudiantes() {
  window.location.href = "/estudiantes";
}
function getActivarUsuario(IdUsuario){
  Swal.fire({
    title: "Desea activar este usuario?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Sí continuar",
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        type: "POST",
        dataType: "json",
        url: "/activar_usuario",
        data:
          "IdUsuario=" + IdUsuario,
        success: function (response) {
          response = JSON.parse(response);
          if (response == 0) {
            Swal.fire({
              html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>No se activo!.</b></div></div>',
            });
          }
          if (response == true) {
            Swal.fire({
              html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Usuario activado OK!.</b></div></div>',
            });
            window.location.href = "/usuarios";
          }
        },
      });
    }
  });
}
function getModificarRolUser(iduser){
  $("#modal_mod_rol").modal("show");
  $("#IdUserMod").val(iduser);
  getRolesUsuario();
}
function getModificarRolesUsuario() {
  var html = "";
  if ($("#IdMRolUser").val() == "0") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-mrol").html(html);
    $("#IdMRolUser").focus();
    setTimeout(function () {
      $("#alert-mrol").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var idusermod = $("#IdUserMod").val();
    var idrol = $("#IdMRolUser").val();
    Swal.fire({
      title: "Desea cambiar de rol a este usuario?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí continuar",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          type: "POST",
          dataType: "json",
          url: "/modroluser",
          data: "IdUsuario=" + idusermod + "&IdRol=" + idrol,
          success: function (response) {
            if (response == 0) {
              Swal.fire({
                html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>No se modificó!.</b></div></div>',
              });
            }
            if (response == true) {
              Swal.fire({
                html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Modificado OK!.</b></div></div>',
              });
              window.location.href = "/usuarios";
            }
          },
        });
      }
    });
  }
}
function getModalModificaUsuario(IdUsuario) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_modificar_usuario",
    data: "IdUsuario=" + IdUsuario,
    success: function (response) {
      if (response) {
        $.each(response, function (i, item) {
          $("#IdUsuarioMod").val(item[0]);
          $("#IdNombresMod").val(item[1]);
          $("#IdApellidosMod").val(item[2]);
          $("#IdentificacionMod").val(item[3]);
          $("#IdDireccionMod").val(item[4]);
          $("#IdTelefonoMod").val(item[5]);
          $("#IdEmailMod").val(item[6]);
        });
        $("#modal-mod-user").modal("show");
      }
      if (response == "null") {
        window.location.href = "/";
      }
    },
  });
}
function getModificarUsuario(){
  var idest = $("#IdUsuarioMod").val();
  var nom = $("#IdNombresMod").val();
  var ape = $("#IdApellidosMod").val();
  var ident = $("#IdentificacionMod").val();
  var dir = $("#IdDireccionMod").val();
  var tel = $("#IdTelefonoMod").val();
  var ema = $("#IdEmailMod").val();
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/moduser",
    data: "IdUsuario=" + idest + "&Nombres=" + nom + "&Apellidos=" + ape + "&Identificacion=" + ident +
    "&Direccion=" + dir + "&Telefono=" + tel + "&Email=" + ema,  
    success: function (response) {
      if (response == 0) {
        Swal.fire({
          html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>No se realizo el registro!.</b></div></div>',
        });
      }
      if (response == true) {
        Swal.fire({
          html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Modificado OK!.</b></div></div>',
        });
        window.location.href = "/usuarios";
      }
    },
  });
}
function getInactivarUsuario(IdUsuario){
  Swal.fire({
    title: "Desea eliminar este usuario?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Sí continuar",
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        type: "POST",
        dataType: "json",
        url: "/eliminar_usuario",
        data:
          "IdUsuario=" + IdUsuario,
        success: function (response) {
          response = JSON.parse(response);
          if (response == 0) {
            Swal.fire({
              html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>No se elimino!.</b></div></div>',
            });
          }
          if (response == true) {
            Swal.fire({
              html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Usuario eliminado OK!.</b></div></div>',
            });
            window.location.href = "/usuarios";
          }
        },
      });
    }
  });
}
function getBorrar(){
  $("#IngresoTexto").val('');
  $("#NroPalabras").text('');
  $("#palabras").text('');
  $("#sinonimos").text('');
  $("#definiciones").text('');
  $("#IngresoTexto").focus();
}
function getTipoIdentificacion() {
  $("#TipoIdentificacion").empty();
  $.ajax({
    type: "GET",
    url: "tipo_identificacion",
    success: function (response) {
      if (response) {
        var $select = $("#TipoIdentificacion");
        $select.append('<option value="0">Seleccione...</option>');
        $.each(response, function (i, item) {
        $select.append("<option value=" + item[0] + ">" + item[1] + "</option>");
      });
    }
    },
  });
}
function getTipoPublicacion() {
  $("#IdTipoDc").empty();
  $.ajax({
    type: "GET",
    url: "tipo_publicaion",
    success: function (response) {
      if (response) {
        var $select = $("#IdTipoDc");
        $select.append('<option value="0">Seleccione...</option>');
        $.each(response, function (i, item) {
        $select.append("<option value=" + item[0] + ">" + item[1] + "</option>");
      });
    }
    },
  });
}
function getRolesUsuario() {
  $("#IdMRolUser").empty();
  $.ajax({
    type: "GET",
    url: "roles_usuario",
    success: function (response) {
      if (response) {
        var $select = $("#IdMRolUser");
        $select.append('<option value="0">Seleccione...</option>');
        $.each(response, function (i, item) {
        $select.append("<option value=" + item[0] + ">" + item[1] + "</option>");
      });
    }
    },
  });
}
function getPreguntasValidacionReg() {
  $("#IdPreguntasReg").empty();
  $.ajax({
    type: "GET",
    url: "preguntas_validacion",
    success: function (response) {
      if (response) {
        var $select = $("#IdPreguntasReg");
        $select.append('<option value="0">Seleccione...</option>');
        $.each(response, function (i, item) {
        $select.append("<option value=" + item[0] + ">" + item[1] + "</option>");
      });
    }
    },
  });
}
function getPreguntasValidacionRegAdmin() {
  $("#IdPreguntasRegAdm").empty();
  $.ajax({
    type: "GET",
    url: "preguntas_validacion",
    success: function (response) {
      if (response) {
        var $select = $("#IdPreguntasRegAdm");
        $select.append('<option value="0">Seleccione...</option>');
        $.each(response, function (i, item) {
        $select.append("<option value=" + item[0] + ">" + item[1] + "</option>");
      });
    }
    },
  });
}
function getPreguntasValidacion() {
  $("#IdPreguntas").empty();
  $.ajax({
    type: "GET",
    url: "preguntas_validacion",
    success: function (response) {
      if (response) {
        var $select = $("#IdPreguntas");
        $select.append('<option value="0">Seleccione...</option>');
        $.each(response, function (i, item) {
        $select.append("<option value=" + item[0] + ">" + item[1] + "</option>");
      });
    }
    },
  });
}
function getLimpiarBusqueda(){
  $("#NroPalabras").text('');
  $("#palabras").text('');
  $("#sinonimos").text('');
  $("#definiciones").text('');
  $("#IdPalabraSnm").text('');
  $("#IdPalabraDf").text('');
  $("#IngresoTexto").focus();
}
function getModalRecuperarPassword(){
  $("#recuperarpass").modal("show");
  getPreguntasValidacion();
}
function getValidaRespuesta() {
  var html = "";
  if ($("#IdUsuarioRq").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ureq").html(html);
    $("#IdUsuarioRq").focus();
    setTimeout(function () {
      $("#alert-ureq").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdPreguntas").val() == "0") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-prg").html(html);
    $("#IdPreguntas").focus();
    setTimeout(function () {
      $("#alert-prg").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdRespuesta").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-resp").html(html);
    $("#IdRespuesta").focus();
    setTimeout(function () {
      $("#alert-resp").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var usu = $("#IdUsuarioRq").val();
    var prg = $("#IdPreguntas").val();
    var resp = $("#IdRespuesta").val();
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/valida_respuesta",
      data: "Usuario=" + usu + "&IdPreguntas=" + prg + "&Respuesta=" + resp,
      success: function (response) {
        if (response) {
          $.each(response, function (i, item) {
            if (resp == item) {
              setTimeout(function () {
                html += '<div class="note note-danger" id="alert-passi">';
                html += '<i class="fa fa-thumbs-up"></i>';
                html += '<b style="color:green;"> Respuesta ok!.</b>';
                html += "</div>";
                $("#valida-resp").html(html);
                $("#alert-passi").fadeOut(3000);
              }, 1500);
            }
          });
        }if (!response) {
          Swal.fire({
            html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>La pregunta seleccionada no es la correcta o la respuesta no coincide!.</b></div></div>',
          });
          $("#IdRespuesta").val('');
          $("#IdRespuesta").focus();
        }
      },
    });
  }
}
function getRecuperarPassword() {
  var html = "";
  if ($("#IdUsuarioRq").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ureq").html(html);
    $("#IdUsuarioRq").focus();
    setTimeout(function () {
      $("#alert-ureq").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdPreguntas").val() == "0") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-prg").html(html);
    $("#IdPreguntas").focus();
    setTimeout(function () {
      $("#alert-prg").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdRespuesta").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-resp").html(html);
    $("#IdRespuesta").focus();
    setTimeout(function () {
      $("#alert-resp").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdPasswordRq").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-passi").html(html);
    $("#IdPasswordRq").focus();
    setTimeout(function () {
      $("#alert-passi").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var usu = $("#IdUsuarioRq").val();
    var passi = $("#IdPasswordRq").val();
    Swal.fire({
      title: "Desea continuar?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí continuar",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          type: "POST",
          dataType: "json",
          url: "/nueva_password",
          data:
            "Usuario=" +
            usu +
            "&Password=" +
            passi,
          success: function (response) {
            response = JSON.parse(response);
            if (response == 0) {
              Swal.fire({
                html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>No se realizo la modificacion!.</b></div></div>',
              });
            }
            if (response == 1) {
              Swal.fire({
                html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Password Recuperada OK!.</b></div></div>',
              });
              $("#recuperarpass").modal("hide");
            }
          },
        });
      }
    });
  }
}
$(document).ready(function () {
	$('.loader_imagen').hide();
  getTipoPublicacion();
  $(".default-select2").select2();
});
