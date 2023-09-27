function getCorreoConfiguradoReg() {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "/get_correo",
    success: function (response) {
      if (response == "") {
        Swal.fire({
          html: '<div class="note note-danger"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Error al realizar el registro!.</b></div></div>',
        });
        guardarCorreo();
      }
      if (response != "") {
        Swal.fire({
          html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>El registro ya existe!.</b></div></div>',
        });
      }
    },
  });
}
function guardarCorreo() {
  var html = "";
  if ($("#IdServidor").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-serv").html(html);
    $("#IdServidor").focus();
    setTimeout(function () {
      $("#alert-serv").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdPuerto").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-prto").html(html);
    $("#IdPuerto").focus();
    setTimeout(function () {
      $("#alert-prto").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdRemitente").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-rmtte").html(html);
    $("#IdRemitente").focus();
    setTimeout(function () {
      $("#alert-rmtte").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdPassRemitente").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-psrmtte").html(html);
    $("#IdPassRemitente").focus();
    setTimeout(function () {
      $("#alert-psrmtte").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdAsunto").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-ast").html(html);
    $("#IdAsunto").focus();
    setTimeout(function () {
      $("#alert-ast").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdMensaje").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-msj").html(html);
    $("#IdMensaje").focus();
    setTimeout(function () {
      $("#alert-msj").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var serv = $("#IdServidor").val();
    var prt = $("#IdPuerto").val();
    var rmtte = $("#IdRemitente").val();
    var psrmtte = $("#IdPassRemitente").val();
    var ast = $("#IdAsunto").val();
    var msj = $("#IdMensaje").val();
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/guardar_correo",
      data:
        "Servidor=" +
        serv +
        "&Puerto=" +
        prt +
        "&Remitente=" +
        rmtte +
        "&Password=" +
        psrmtte +
        "&Asunto=" +
        ast +
        "&Mensaje=" +
        msj,
      success: function (response) {
        response = JSON.parse(response);
        if (response == false) {
          alert(response);
          Swal.fire({
            html: '<div class="note note-danger"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Error al realizar el registro!.</b></div></div>',
          });
        }
        if (response == true) {
          Swal.fire({
            html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Registro OK!.</b></div></div>',
          });
          window.location.href = "/correo_configurado";
        }
      },
    });
  }
}
function getModalConfiguracionCorreoAdmin() {
  $("#config-correo").modal("show");
}
function getCorreoConfigurado() {
  alert("Correo");
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/correo_configurado",
    success: function (response) {
      //print(response)
      if (response) {
        $.each(response, function (i, item) {
          $("#IdConfig").val(item[0]);
          $("#IdServidor").val(item[1]);
          $("#IdPuerto").val(item[2]);
          $("#IdRemitente").val(item[3]);
          $("#IdPassRemitente").val(item[4]);
          $("#IdAsunto").val(item[5]);
          $("#IdMensaje").val(item[6]);
        });
      } else {
        Swal.fire({
          html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Debes realizar la configuracion del correo!.</b></div></div>',
        });
      }
    },
  });
}
function ModificarChat() {
  var html = "";
  if ($("#IdPreguntasMod").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-prgm").html(html);
    $("#IdPreguntas").focus();
    setTimeout(function () {
      $("#alert-prgm").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdRespuestasMod").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-respm").html(html);
    $("#IdRespuestasMod").focus();
    setTimeout(function () {
      $("#alert-respm").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var idchat = $("#IdChatMod").val();
    var prg = $("#IdPreguntasMod").val();
    var resp = $("#IdRespuestasMod").val();
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
          url: "/modchat",
          data:
            "IdChat=" + idchat + "&Preguntas=" + prg + "&Respuestas=" + resp,
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
              window.location.href = "/chat";
            }
          },
        });
      }
    });
  }
}
function getEliminarChat(IdChat) {
  Swal.fire({
    title: "Desea eliminar este registro?",
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
        url: "/eliminar_chat",
        data: "IdChat=" + IdChat,
        success: function (response) {
          response = JSON.parse(response);
          if (response == 0) {
            Swal.fire({
              html: '<div class="note note-warning"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>No se elimino!.</b></div></div>',
            });
          }
          if (response == true) {
            Swal.fire({
              html: '<div class="note note-success"><div class="note-icon"><i class="fa-solid fa-thumbs-up"></i></div><div class="note-content"><b>Eliminado OK!.</b></div></div>',
            });
            window.location.href = "/chat";
          }
        },
      });
    }
  });
}
$(document).ready(function () {
  getCorreoConfigurado();
});
