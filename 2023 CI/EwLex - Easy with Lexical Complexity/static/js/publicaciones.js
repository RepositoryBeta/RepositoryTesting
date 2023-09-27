function getPublicados() {
    window.location.href = "/publicados";
}
function getPublicacionesArticulos() {
  window.location.href = "/articulos";
}
function getPublicaciones() {
    window.location.href = "/publicaciones";
}
  function getPublicarDocumento() {
      var html = "";
    if ($("#IdFecha").val() == "") {
      html += '<div class="alert alert-danger">';
      html += "*Este campo es obligatorio!.";
      html += "</div>";
      $("#alert-fh").html(html);
      $("#IdFecha").focus();
      setTimeout(function () {
        $("#alert-fh").fadeOut(1500);
      }, 3000);
      return false;
    } if ($("#IdAutor").val() == "") {
      html += '<div class="alert alert-danger">';
      html += "*Este campo es obligatorio!.";
      html += "</div>";
      $("#alert-aut").html(html);
      $("#IdAutor").focus();
      setTimeout(function () {
        $("#alert-aut").fadeOut(1500);
      }, 3000);
      return false;
    } if ($("#IdProyecto").val() == "") {
      html += '<div class="alert alert-danger">';
      html += "*Este campo es obligatorio!.";
      html += "</div>";
      $("#alert-py").html(html);
      $("#IdProyecto").focus();
      setTimeout(function () {
        $("#alert-py").fadeOut(1500);
      }, 3000);
      return false;
    } if ($("#IdDocumento").val() == "") {
      html += '<div class="alert alert-danger">';
      html += "*Este campo es obligatorio!.";
      html += "</div>";
      $("#alert-docu").html(html);
      $("#IdDocumento").focus();
      setTimeout(function () {
        $("#alert-docu").fadeOut(1500);
      }, 3000);
      return false;
    } if ($("#IdTipoDc").val() == "0") {
      html += '<div class="alert alert-danger">';
      html += "*Este campo es obligatorio!.";
      html += "</div>";
      $("#alert-tp").html(html);
      $("#IdTipoDc").focus();
      setTimeout(function () {
        $("#alert-tp").fadeOut(1500);
      }, 3000);
      return false;
    } else {
      var formData = new FormData();
      var files = $("#IdDocumento")[0].files[0];
      var fecha = $("#IdFecha").val();
      var autor = $("#IdAutor").val();
      var proyecto = $("#IdProyecto").val();
      var tpp = $("#IdTipoDc").val();
      formData.append("Documento", files);
      formData.append("Fecha", fecha);
      formData.append("Autor", autor);
      formData.append("Proyecto", proyecto);
      formData.append("IdTipo", tpp);
      $.ajax({
        type: "POST",
        url: "/UpDocumento",
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
          if (response) {
            window.location.href = "/publicar";
          }
          if (response == "null") {
            window.location.href = "/";
          }
        },
      });
    }
  }
  function getModificarPublicacion(IdPublicacion) {
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/get_mod_publicacion",
      data: "IdPublicacion=" + IdPublicacion,
      success: function (response) {
        if (response) {
          $.each(response, function (i, item) {
            $("#IdPublicacion").val(item[0]);
            $("#IdFechaMod").val(item[1]);
            $("#IdAutorMod").val(item[2]);
            $("#IdProyectoMod").val(item[3]);
          });
          $("#modal-mod-publicacion").modal("show");
        }
        if (response == "null") {
          window.location.href = "/";
        }
      },
    });
  }
  function MofificarPublicacion() {
    var html = "";
  if ($("#IdFechaMod").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-fhm").html(html);
    $("#Mod").focus();
    setTimeout(function () {
      $("#alert-fhm").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdAutorMod").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-autm").html(html);
    $("#IdAutorMod").focus();
    setTimeout(function () {
      $("#alert-autm").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdProyectoMod").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-pym").html(html);
    $("#IdProyectoMod").focus();
    setTimeout(function () {
      $("#alert-pym").fadeOut(1500);
    }, 3000);
    return false;
  } if ($("#IdDocumentoMod").val() == "") {
    html += '<div class="alert alert-danger">';
    html += "*Este campo es obligatorio!.";
    html += "</div>";
    $("#alert-docum").html(html);
    $("#IdDocumentoMod").focus();
    setTimeout(function () {
      $("#alert-docum").fadeOut(1500);
    }, 3000);
    return false;
  } else {
    var formData = new FormData();
    var files = $("#IdDocumentoMod")[0].files[0];
    var idp = $("#IdPublicacion").val();
    var fecha = $("#IdFechaMod").val();
    var autor = $("#IdAutorMod").val();
    var proyecto = $("#IdProyectoMod").val();
    formData.append("Documento", files);
    formData.append("IdPublicacion", idp);
    formData.append("Fecha", fecha);
    formData.append("Autor", autor);
    formData.append("Proyecto", proyecto);
    $.ajax({
      type: "POST",
      url: "/mod_publicacion",
      data: formData,
      contentType: false,
      processData: false,
      success: function (response) {
        if (response) {
          window.location.href = "/publicar";
        }
        if (response == "null") {
          window.location.href = "/";
        }
      },
    });
  }
}