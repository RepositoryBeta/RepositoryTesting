function getRespuesta() {
  var html = '';
  var idp = $("#IdPregunta").val();
  $("#IdPreg").text(idp);
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_chat",
    data: "IdPregunta=" + idp,
    success: function (response) {
      if (response) {
        $.each(response, function (i, item) {
          if(item[0]!==''){
            html += '<cite style="color: blue;"> | ' + item[0] + ' | ' +"</cite>";
            $("#IdRespuesta").html(html);
            $("#IdPregunta").val('');
            $("#IdPregunta").focus();
          }
        });
        if(response==''){
          html += '<cite style="color: blue;"> lo siento! ' 
          +'<b style="color: red;">' + idp + '</b>'+" no esta en mi memoria." + "</cite>";
          $("#IdRespuesta").html(html);
          $("#IdPregunta").val('');
          $("#IdPregunta").focus();
        }
      } else {
        $(this).val('');
      }
    },
  });
}
function toggleChat() {
    var chatContainer = document.querySelector('.chat-container');
    chatContainer.classList.toggle('open');
}
function RegistrarChat() {
  var html = "";
  if ($("#IdPreguntas").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-prg").html(html);
    $("#IdPreguntas").focus();
    setTimeout(function () {
      $("#alert-prg").fadeOut(1500);
    }, 3000);
    return false;
  }
  if ($("#IdRespuestas").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-resp").html(html);
    $("#IdRespuestas").focus();
    setTimeout(function () {
      $("#alert-resp").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var prg = $("#IdPreguntas").val();
    var resp = $("#IdRespuestas").val();
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
          url: "/regchat",
          data:
            "Preguntas=" +
            prg +
            "&Respuestas=" +
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
              window.location.href = "/chat";
            }
          },
        });
      }
    });
  }
}
function getModificarChat(IdChat) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_mod_chat",
    data: "IdChat=" + IdChat,
    success: function (response) {
      if (response) {
        $.each(response, function (i, item) {
          $("#IdChatMod").val(item[0]);
          $("#IdPreguntasMod").val(item[1]);
          $("#IdRespuestasMod").val(item[2]);
        });
        $("#modal-mod-chat").modal("show");
      }
      if (response == "null") {
        window.location.href = "/";
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
            "IdChat=" +
            idchat +
            "&Preguntas=" +
            prg +
            "&Respuestas=" +
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
              window.location.href = "/chat";
            }
          },
        });
      }
    });
  }
}
function getEliminarChat(IdChat){
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
        data:
          "IdChat=" + IdChat,
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