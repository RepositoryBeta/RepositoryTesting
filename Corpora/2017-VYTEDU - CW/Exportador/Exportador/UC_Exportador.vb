Imports System.Data.SQLite
Imports System.IO
Imports System.Threading
Public Class UC_Exportador
    Dim Hilo As Thread
    Dim SePuedeCerrar As Boolean = True
    Dim Sep As String = ";"
    Dim ext As String = "csv"
    Public SZ_Width As Integer = 0
    Public SZ_Height As Integer = 0
    Dim EsAnci As Boolean = True
    Private Sub UC_Exportador_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        CargarSize(238 + 20, 74 + 50) 'Si redimenciona el tamaño de la ventana en el (Diseño). Colocar ese valor aqui para que se refleje en el programa EIL
        'El + 20 y + 50 Es para compensar tamaño
        SFD_.InitialDirectory = My.Computer.FileSystem.CurrentDirectory & "\BasesDeDatos"
        OFD_.InitialDirectory = My.Computer.FileSystem.CurrentDirectory & "\BasesDeDatos"
    End Sub
    Private Sub CargarSize(ByVal Width As Integer, ByVal Height As Integer)
        SZ_Width = Width
        SZ_Height = Height
    End Sub
#Region "Unificar DB"
    Private Sub BT_UnifBases_Click(sender As Object, e As EventArgs) Handles BT_UnifBases.Click
        SFD_.Title = "Guardar base de datos unificada"
        SFD_.FileName = "DB_Unificada.db"
        If SFD_.ShowDialog = DialogResult.OK Then
            OFD_.Title = "Cargar bases de datos a unificar"
            OFD_.Multiselect = True
            If OFD_.ShowDialog = DialogResult.OK Then
                SePuedeCerrar = False
                Me.UseWaitCursor = True
                Hilo = New Thread(New ThreadStart(AddressOf UnificarBases))
                Hilo.Start()
            End If
        End If
    End Sub
    Private Function Existe(Str As String, EnLista As List(Of String))
        For Each Str2 As String In EnLista
            If Str = Str2 Then
                Return True
            End If
        Next
        Return False
    End Function
    Private Sub UnificarBases()
        Dim ListaTipPal As New List(Of DataRow)
        Dim ListaUsu As New List(Of DataRow)
        Dim ListaEnt As New List(Of DataRow)
        Dim ListaArchivo As New List(Of String)
        ListaTipPal.Clear()
        ListaArchivo.Clear()
        Dim Encontro As Boolean = False
        Dim ListaElementos As New List(Of String)
        Dim Contador As Integer = 0
        For Each Str As String In OFD_.FileNames
            ListaArchivo.Add(Str)
            Contador += 1
        Next
        Dim HayEntradas As Boolean = False
        Dim BTP As Boolean = False
        Dim BU As Boolean = False
        Dim BE As Boolean = False
        For Each Str As String In ListaArchivo
            Dim DB As New SQLiteDB
            DB.Ruta = Str
            Dim Ds As DataSet
            Ds = DB.Ver("SELECT * FROM " & "TipoPalabras" & ";")
            If Ds.Tables(0).Rows.Count > 0 Then
                BTP = True
                Dim StrLower As String = ""
                For Each Row_ As DataRow In Ds.Tables(0).Rows
                    StrLower = FiltraChar(Row_(0))
                    Row_(0) = StrLower.ToLower()
                    ListaTipPal.Add(Row_)
                Next
            End If
            Ds = DB.Ver("SELECT * FROM " & "Usuario" & ";")
            If Ds.Tables(0).Rows.Count > 0 Then
                BU = True
                For Each Row_ As DataRow In Ds.Tables(0).Rows
                    ListaUsu.Add(Row_)
                Next
            End If
            Ds = DB.Ver("SELECT * FROM " & "Entradas" & ";")
            If Ds.Tables(0).Rows.Count > 0 Then
                BE = True
                For Each Row_ As DataRow In Ds.Tables(0).Rows
                    ListaEnt.Add(Row_)
                Next
            End If
            DB.Dispose()
        Next
        CrearBaseDeDatos(SFD_.FileName)
        Dim DB_ As New SQLiteDB(SFD_.FileName)
        Dim Numero As Integer = 0
        Dim Registros As String = 0
        Dim LisSQL As New List(Of Char)
        Dim LisCSV As New List(Of Char)
        Dim LisUsu As New List(Of Char)
        Dim LisEnt As New List(Of Char)
        Dim LisAux As New List(Of Char)
        Dim Soporte As String = ""
        If BTP Then
            ListaAconsulta(ListaTipPal, LisSQL, LisCSV, 8)
            DB_.CSR("insert into " & "TipoPalabras" & " values" & LisSQL.ToArray & ";")
        End If
        If BU Then
            ListaAconsulta(ListaUsu, LisUsu, LisAux, -1)
            DB_.CSR("insert into " & "Usuario" & " values" & LisUsu.ToArray & ";")
        End If
        If BE Then
            ListaAconsulta(ListaEnt, LisEnt, LisAux, -1)
            DB_.CSR("insert into " & "Entradas" & " values" & LisEnt.ToArray & ";")
        End If
        Dim CSV As String = ""
        CSV = New String(LisCSV.ToArray)
        Me.UseWaitCursor = False
        MsgBox("Se ha creado su base de datos unificada")
        SePuedeCerrar = True
        Process.Start("explorer.exe", System.IO.Path.GetDirectoryName(SFD_.FileName))
    End Sub
    Private Sub ListaAconsulta(ByRef LisDrow As List(Of DataRow), ByRef LisSQL As List(Of Char), ByRef LisCSV As List(Of Char), ByRef Num As Integer)
        Dim Index As Integer = 0
        For Each Rows_ As DataRow In LisDrow
            If LisSQL.Count > 0 Then
                LisSQL.AddRange(", ")
                LisCSV.AddRange(vbCr & vbLf)
            End If
            Dim Coma As Boolean = False
            LisSQL.AddRange("(")
            Dim Contar As Integer = 0
            For Each Str As Object In Rows_.ItemArray
                If Coma Then
                    LisSQL.AddRange(", ")
                    LisCSV.AddRange(Sep)
                End If
                LisSQL.AddRange("'" & Str & "'")
                Coma = True
                Try
                    LisCSV.AddRange(Str)
                Catch ex As Exception
                    MsgBox(ex.Message)
                End Try
                Contar += 1
            Next
            Dim Soporte As String = ""
            If Contar = Num Then
                Soporte = ", ''"
            End If
            LisSQL.AddRange(Soporte & ")")
            Index += 1
        Next
    End Sub
#End Region
#Region "Exporta"
    Private Sub BT_Exportar_Click(sender As Object, e As EventArgs) Handles BT_Exportar.Click
        If CHB_UsarTab.Checked Then
            Sep = vbTab
            ext = "txt"
            EsAnci = True
        Else
            Sep = ";"
            ext = "csv"
            EsAnci = True
        End If
        OFD_.Title = "Cargar la base de datos a exportar"
        OFD_.Multiselect = False
        OFD_.FileName = "DB_Unificada.db"
        If OFD_.ShowDialog = DialogResult.OK Then
            ExortarLosDatos(OFD_.FileName)
            CuentaPalabrasCorpus("C:\Users\CGE\Documents\Visual Studio 2017\Projects\01 EIL\EIL Final\EIL\EIL\Corpus")
            ExportaPorArchivo(OFD_.FileName)
            CalculaValores()
            Dim ExportaGeneral As String = "Todos los registros" & vbCrLf &
                                           "# de terminos:" & Sep & TiPal_Count & vbCrLf &
                                           "# de usuarios:" & Sep & Usu_Count & vbCrLf &
                                           "# de entradas al corpus:" & Sep & Ent_Count & vbCrLf &
                                           "Registros sin repeticion" & vbCrLf &
                                           "# de terminos:" & Sep & TiPal_SR_Count & vbCrLf &
                                           "# de usuarios:" & Sep & Usu_SR_Count & vbCrLf &
                                           "Corpus" & vbCrLf &
                                           "# de palabras:" & Sep & TotalPalabrasCorpus & vbCrLf &
                                           "# de palabras sin repeticion:" & Sep & PalabrasSinRepeticion & vbCrLf &
                                           "Corpus vs marcas" & vbCrLf &
                                           "% terminos:" & Sep & Math.Round(ProcentajeTemino, 2) & "%" & vbCrLf &
                                           "% terminos Sin repeticion:" & Sep & Math.Round(ProcentajeTeminoSR, 2) & "%" & vbCrLf
            Dim Ruta_ As String = ""
            Ruta_ = System.IO.Path.GetDirectoryName(OFD_.FileName) & "\" & System.IO.Path.GetFileNameWithoutExtension(OFD_.FileName) & " N_Pal N_Usu." & ext
            Guardar(Ruta_, ExportaGeneral, EsAnci)
            MsgBox("Ya estan sus archivos listos")
        End If
    End Sub

    Private Sub CalculaValores()
        ProcentajeTemino = (100 * TiPal_Count) / TotalPalabrasCorpus
        ProcentajeTeminoSR = (100 * TiPal_SR_Count) / PalabrasSinRepeticion
    End Sub
    Private Sub ExportaPorArchivo(RutaDB As String)
        Dim DB_ As New SQLiteDB
        Dim Encontro As Boolean = False
        Dim DB As New SQLiteDB
        Dim Lista As New List(Of FilaPal)
        Dim TLista As New List(Of LiFilaPal)
        Dim LiCh1 As New List(Of Char)
        Dim LiCh2 As New List(Of Char)
        Dim LFrases As New List(Of String)
        Dim LUsuarios As New List(Of String)
        Dim NumRegistros As Integer = 0
        DB.Ruta = RutaDB
        Dim Ds As DataSet
        Ds = DB.Ver("SELECT * FROM " & "TipoPalabras" & ";")
        If Ds.Tables(0).Rows.Count > 0 Then
            For Each Row_ As DataRow In Ds.Tables(0).Rows
                NumRegistros += 1
                Row_(0) = FiltraChar(Row_(0))
                'A partir de aqui se hacen todas las clasificaciones.
                Dim FilP As New FilaPal(Row_(0), Row_(1), Row_(4), Row_(5), Row_(6), Row_(7), 1)
                If Not BuscaPal(Row_(0), LFrases) Then
                    LFrases.Add(Row_(0))
                End If
                If Not HayEnLista(Lista, FilP) Then
                    Lista.Add(FilP)
                End If
            Next
            Dim CSV As String = ""
            Dim Ruta As String
            If CHB_ConEtiqueta.Checked Then
                LiCh1.AddRange("Palabra" & Sep & "TipoPalabra" & Sep & "TextoOrigen" & Sep & "Posicion" & Sep & "Largo" & Sep & "SaltoLinea" & Sep & "Aparicion" & vbCr & vbLf)
            End If
            For Each F As FilaPal In Lista
                LiCh1.AddRange(F.Pa0 & Sep & F.Ti1 & Sep & F.Te2 & Sep & F.Po3 & Sep & F.La4 & Sep & F.Sa5 & Sep & F.Ap6 & vbCr & vbLf)
                If Not HayEnLista(TLista, F.Te2, F) Then
                    TLista.Add(New LiFilaPal(F.Te2, F))
                End If
            Next
            CSV = New String(LiCh1.ToArray)
            Ruta = System.IO.Path.GetDirectoryName(OFD_.FileName) & "\" & System.IO.Path.GetFileNameWithoutExtension(OFD_.FileName) & "CuTo." & ext
            Guardar(Ruta, CSV, EsAnci)
            LiCh1.Clear()
            Directory.CreateDirectory(Path.GetDirectoryName(Ruta) & "\PorArchivo")
            Dim RutaPorArchivo As String = Path.GetDirectoryName(Ruta) & "\PorArchivo"
            For Each L As LiFilaPal In TLista
                If CHB_ConEtiqueta.Checked Then
                    LiCh1.AddRange("Palabra" & Sep & "TipoPalabra" & Sep & "TextoOrigen" & Sep & "Posicion" & Sep & "Largo" & Sep & "SaltoLinea" & Sep & "Aparicion" & vbCr & vbLf)
                End If
                For Each F As FilaPal In L.LFP
                    LiCh1.AddRange(F.Pa0 & Sep & F.Ti1 & Sep & F.Te2 & Sep & F.Po3 & Sep & F.La4 & Sep & F.Sa5 & Sep & F.Ap6 & vbCr & vbLf)
                Next
                CSV = New String(LiCh1.ToArray)
                Ruta = RutaPorArchivo & "\" & System.IO.Path.GetFileNameWithoutExtension(OFD_.FileName) & L.TextoOrigen & "." & ext
                Guardar(Ruta, CSV, EsAnci)
                LiCh1.Clear()
            Next
        End If
        DB.Dispose()
    End Sub
#Region "Utilidades"
    Private Function FiltraChar(Texto As String)
        Dim Str As String = ""
        For Each Char_ As Char In Texto
            If Not InStr(1, "!•"“"”"",	+-*/""·$%&/()=?¿^*`+¨Ç;:_,.-«»" & vbTab, Char_, CompareMethod.Text) > 0 Then
                Str = Str & Char_
            End If
        Next
        Return Str
    End Function
    Private Function HayEnLista(Lista As List(Of LiFilaPal), E As String, F As FilaPal)
        For Each Ele As LiFilaPal In Lista
            If EsIgial(Ele, E) Then
                Ele.LFP.Add(F)
                Return True
            End If
        Next
        Return False
    End Function
    Private Function EsIgial(A As LiFilaPal, B As String)
        If (A.TextoOrigen = B) Then
            Return True
        Else
            Return False
        End If
    End Function
    Private Function HayEnLista(Lista As List(Of FilaPal), E As FilaPal)
        For Each Ele As FilaPal In Lista
            If EsIgial(Ele, E) Then
                Ele.Ap6 = Ele.Ap6 + 1
                Return True
            End If
        Next
        Return False
    End Function
    Private Function EsIgial(A As FilaPal, B As FilaPal)
        If (A.Pa0 = B.Pa0 And A.Ti1 = B.Ti1 And A.Te2 = B.Te2) Then
            Return True
        Else
            Return False
        End If
    End Function
    Class LiFilaPal
        Public TextoOrigen As String
        Public LFP As New List(Of FilaPal)
        Sub New(TextoOrigen As String, F As FilaPal)
            Me.TextoOrigen = TextoOrigen
            LFP.Add(F)
        End Sub
    End Class
    Class FilaPal
        Public Pa0 As String '0
        Public Ti1 As String '1
        Public Te2 As String '2
        Public Po3 As Integer '3
        Public La4 As Integer '4
        Public Sa5 As Integer '5
        Public Ap6 As Integer '6
        Sub New(Palabra As String, Tipo As String, TextoOrigen As String, Posicion As Integer, Largo As Integer, SaltoLinea As Integer, Aparicion As Integer)
            Pa0 = Palabra
            Ti1 = Tipo
            Te2 = TextoOrigen
            Po3 = Posicion
            La4 = Largo
            Sa5 = SaltoLinea
            Ap6 = Aparicion
        End Sub
    End Class
#End Region
#End Region
#Region "CRUD Archivos"
    Public Function Leer(Ruta As String, ByRef Texto As String) As Boolean
        Try
            Texto = File.ReadAllText(Ruta, System.Text.Encoding.UTF8)
        Catch ex As Exception
            Return False
        End Try
        Return True
    End Function
    Public Function Abrir_Crear(ByVal Ruta As String)
        Try
            If System.IO.File.Exists(Ruta) Then
                Dim sr As New System.IO.StreamReader(Ruta)
                Dim Str As String = sr.ReadToEnd()
                sr.Close()
                Return Str
            Else
                Dim fs As System.IO.FileStream = System.IO.File.Create(Ruta)
                fs.Close()
                fs.Dispose()
                Return ""
            End If
        Catch ex As Exception
            MsgBox(ex.Message)
            Return ""
        End Try
    End Function
    Public Sub Guardar(ByVal Ruta As String, ByVal Dato As String)
        Guardar(Ruta, Dato, False)
    End Sub
    Public Sub Guardar(ByVal Ruta As String, ByVal Dato As String, ANCI As Boolean)
        Try
            If ANCI Then
                If System.IO.File.Exists(Ruta) Then
                    System.IO.File.Delete(Ruta)
                End If
                Dim fs As New System.IO.StreamWriter(Ruta, False, System.Text.Encoding.Default)
                fs.WriteLine(Dato)
                fs.Close()
                fs.Dispose()
            Else
                Dim fs As System.IO.FileStream = System.IO.File.Create(Ruta)
                Dim info As Byte() = New System.Text.UTF8Encoding(True).GetBytes(Dato)
                fs.Write(info, 0, info.Length)
                fs.Close()
                fs.Dispose()
            End If
        Catch ex As Exception
            MsgBox(ex.Message)
        End Try

    End Sub
    Public Sub Guardar01(ByVal Ruta As String, ByVal Dato As String)
        Dim info As Byte() = New System.Text.UTF8Encoding(True).GetBytes(Dato)
        File.WriteAllBytes(Ruta, info)
    End Sub
#End Region
#Region "SQLite"
#Region "Codigo para crear la base de datos"
    Dim CT_TipoPalabras As String = "CREATE TABLE TipoPalabras (Palabra TEXT, TipoPalabra TEXT, Usuario TEXT, TipoUsuario TEXT, TextoOrigen TEXT, Posicion TEXT, Largo TEXT, SaltoLinea TEXT, Fecha TEXT);"
    Dim CT_Usuario As String = "CREATE TABLE Usuario (Cedula Text, TipoUsuario Text, Nombre TEXT, Apellidos TEXT, UltAcceso TEXT);"
    Dim CT_Entradas As String = "CREATE TABLE Entradas (Cedula Text, Texto Text, Fecha TEXT);"
    Public Sub CrearBaseDeDatos(ByVal Ruta As String)
        Dim NuevaBaseDeDatos As New SQLiteDB(Ruta)
        NuevaBaseDeDatos.CSR(CT_TipoPalabras & CT_Usuario & CT_Entradas)
    End Sub
#End Region
    Public DB_ As New SQLiteDB
    Class SQLiteDB
        Private Ruta_ As String = ""
        Public Property Ruta As String
            Get
                Return Ruta_
            End Get
            Set(value As String)
                Ruta_ = value
                Conexion = "Data Source = " & Ruta_ & ";"
            End Set
        End Property
        Private Property Conexion As String
            Get
                Return Conexion_
            End Get
            Set(ByVal value As String)
                Conexion_ = value
                SQLConn = New SQLiteConnection(Conexion)
            End Set
        End Property
        Dim Conexion_ As String = ""
        Dim SQLConn As SQLiteConnection
        Dim SQLCom As SQLiteCommand
        Dim SQLReader As SQLiteDataAdapter
        Sub New()
        End Sub
        Sub New(ByVal Ruta As String)
            Me.Ruta = Ruta
        End Sub
        Public Sub CSR(ByVal Comando As String)
            AbrirDB()
            SQLCom.CommandText = Comando
            SQLCom.ExecuteNonQuery()
            SQLiteClose()
        End Sub
        Public Sub Ver(ByVal Comando As String, ByRef _DGV_ As DataGridView)
            Dim Ds As DataSet = Ver(Comando)
            Try
                If Ds.Tables(0).Rows.Count > 0 Then
                    _DGV_.DataSource = Ds.Tables(0)
                Else
                    _DGV_.DataSource = Nothing
                End If
            Catch ex As Exception
                _DGV_.DataSource = Nothing
            End Try
            SQLiteClose()
        End Sub
        Public Function Ver(ByVal Comando As String)
            Dim Ds As New DataSet
            Try
                AbrirDB()
                SQLCom.CommandText = Comando
                SQLReader = New SQLiteDataAdapter(SQLCom)
                SQLReader.Fill(Ds)
                SQLiteClose()
                Return Ds
            Catch ex As Exception
            End Try
            Return Ds
        End Function
        Public Sub Dispose()
            SQLReader.Dispose()
            SQLCom.Dispose()
            SQLConn.Dispose()
        End Sub
        Public Sub Insertar(ByVal Tabla As String,
                            ByVal Lista As List(Of String))
            If Lista.Count < 1 Then
                Throw New Exception("No hay nada en la lista")
                Exit Sub
            End If
            Dim Str As String = ""
            For Each Str_ As String In Lista
                If Str <> "" Then
                    Str = Str & ","
                End If
                Str = Str & "'" & Str_ & "'"
            Next
            CSR("insert into " & Tabla & " values(" & Str & ");")
        End Sub
        Public Sub AbrirDB()
            Try
                SQLConn.Open()
                SQLCom = SQLConn.CreateCommand()
            Catch ex As Exception
                Try
                    SQLCom = SQLConn.CreateCommand()
                Catch ex_ As Exception
                    SQLiteClose()
                    MsgBox("No se a podido abrir la base de datos")
                End Try
            End Try
        End Sub
        Public Sub SQLiteClose()
            If Not IsNothing(SQLConn) Then
                SQLConn.Close()
            End If
        End Sub
    End Class
#End Region
#Region "Piloto"
    Private Sub ExportaDBCompleta(Ruta As String)
        Dim ListaTipPal As New List(Of DataRow)
        Dim ListaUsu As New List(Of DataRow)
        Dim ListaEnt As New List(Of DataRow)
        Dim LisCSV As New List(Of Char)
        Dim LisSQL As New List(Of Char)
        Dim DB As New SQLiteDB
        DB.Ruta = Ruta
        Dim Ruta_ As String = Path.GetDirectoryName(Ruta)
        Dim Ds As DataSet
        Ds = DB.Ver("SELECT * FROM " & "TipoPalabras" & ";")
        If Ds.Tables(0).Rows.Count > 0 Then
            For Each Row_ As DataRow In Ds.Tables(0).Rows
                Row_(0) = FiltraChar(Row_(0))
                ListaTipPal.Add(Row_)
            Next
        End If
        Ds = DB.Ver("SELECT * FROM " & "Usuario" & ";")
        If Ds.Tables(0).Rows.Count > 0 Then
            For Each Row_ As DataRow In Ds.Tables(0).Rows
                ListaUsu.Add(Row_)
            Next
        End If
        Ds = DB.Ver("SELECT * FROM " & "Entradas" & ";")
        If Ds.Tables(0).Rows.Count > 0 Then
            For Each Row_ As DataRow In Ds.Tables(0).Rows
                ListaEnt.Add(Row_)
            Next
        End If
        DB.Dispose()
        Directory.CreateDirectory(Ruta_ & "\DB_Entera")
        If CHB_ConEtiqueta.Checked Then
            LisCSV.AddRange("Palabra" & Sep & "TipoPalabra" & Sep & "Usuario" & Sep & "TipoUsuario" & Sep & "TextoOrigen" & Sep & "Posicion" & Sep & "Largo" & Sep & "SaltoLinea" & Sep & "Fecha" & vbCrLf)
        End If
        ListaAconsulta(ListaTipPal, LisSQL, LisCSV, -1)
        Guardar(Ruta_ & "\DB_Entera\TipoPalabras." & ext, New String(LisCSV.ToArray), EsAnci)
        LisCSV.Clear()

        If CHB_ConEtiqueta.Checked Then
            LisCSV.AddRange("Cédula" & Sep & "TipoUsuario" & Sep & "Nombre" & Sep & "Apellido" & Sep & "UltAcceso" & vbCrLf)
        End If
        ListaAconsulta(ListaUsu, LisSQL, LisCSV, -1)
        Guardar(Ruta_ & "\DB_Entera\Usuario." & ext, New String(LisCSV.ToArray), EsAnci)
        LisCSV.Clear()

        If CHB_ConEtiqueta.Checked Then
            LisCSV.AddRange("Cédula" & Sep & "Texto" & Sep & "Fecha" & vbCrLf)
        End If
        ListaAconsulta(ListaEnt, LisSQL, LisCSV, -1)
        Guardar(Ruta_ & "\DB_Entera\Entradas." & ext, New String(LisCSV.ToArray), EsAnci)
    End Sub
#End Region
#Region "Datos a capturar y sus respectivas operaciones"
    Public RegistrosTotales As Integer 'Aqui se pueden ver todas las marcaciones que a tenido el corpus
    Public PalabrasTotalesCorpus As Integer 'cuenta todas las palabras que se cuentan en todo el corpus
    Public RegistrosDistintos As Integer 'Aqui se cuenta la cantidad de marcaciones distintas entre si
    Public PalabrasDistintasCorpus As Integer 'Se cuentan las palabras tidtintas que tiene el corpus
#Region "Cantidad de registros en las tablas"
    Dim TiPal_Count As Integer = 0
    Dim Usu_Count As Integer = 0
    Dim Ent_Count As Integer = 0
#End Region
#Region "Cantidad de registros sin repeticion en las tablas"
    Dim TiPal_SR_Count As Integer = 0
    Dim Usu_SR_Count As Integer = 0
    Dim Ent_SR_Count As Integer = 0
#End Region
#Region "Palabras en corpus"
    Dim TotalPalabrasCorpus As Integer = 0
    Dim PalabrasSinRepeticion As Integer = 0
    Dim ProcentajeTemino As Double = 0
    Dim ProcentajeTeminoSR As Double = 0
#End Region
#Region "Terminos"
    Dim ListaPalabras As New List(Of String)
#End Region
    Private Sub CuentaPalabrasCorpus(Ruta As String)
        Dim DirInfo As New DirectoryInfo(Ruta) 'My.Computer.FileSystem.CurrentDirectory & "\Corpus")
        Dim CorpusCompleto As String = ""
        For Each FilInfo As FileInfo In DirInfo.GetFiles
            Dim Str As String = ""
            Leer(FilInfo.FullName, Str)
            CorpusCompleto = CorpusCompleto & Str & " "
        Next
        Dim ListaPalabras As New List(Of String)
        Dim Str2 As String = ""
        Dim Inte As Integer = 0
        For Each Char_ As Char In CorpusCompleto
            If Not InStr(1, "áéíóúÁÉÍÓÚ0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz", Char_) > 0 Then
                If Str2 <> "" Then
                    AgregaA(Str2, ListaPalabras)
                    Str2 = ""
                    Inte += 1
                End If
            Else
                Str2 = Str2 & Char_
            End If
        Next
        If Str2 <> "" Then
            AgregaA(Str2, ListaPalabras)
            Str2 = ""
            Inte += 1
        End If
        TotalPalabrasCorpus = Inte
        PalabrasSinRepeticion = ListaPalabras.Count
        Me.ListaPalabras = ListaPalabras
    End Sub
    Private Sub ExortarLosDatos(Ruta As String)
#Region "Listas de los registros que hay en las bases de datos"
        Dim ListaTipPal As New List(Of DataRow)
        Dim ListaUsu As New List(Of DataRow)
        Dim ListaEnt As New List(Of DataRow)
#End Region
#Region "Lista Sin repeticion"
        Dim ListaSR_TipPal As New List(Of String)
        Dim ListaSR_Usu As New List(Of String)
        Dim ListaSR_Ent As New List(Of String)
#End Region
#Region "Extrae datos de la DB"
        Dim LisCSV As New List(Of Char)
        Dim DB As New SQLiteDB
        DB.Ruta = Ruta
        Dim Ruta_ As String = Path.GetDirectoryName(Ruta)
        Dim Ds As DataSet
        Ds = DB.Ver("SELECT * FROM " & "TipoPalabras" & ";")
        TiPal_Count = Ds.Tables(0).Rows.Count
        If TiPal_Count > 0 Then
            For Each Row_ As DataRow In Ds.Tables(0).Rows
                Row_(0) = FiltraChar(Row_(0))
                ListaTipPal.Add(Row_)
                AgregaA(Row_(0), ListaSR_TipPal)
            Next
        End If
        Ds = DB.Ver("SELECT * FROM " & "Usuario" & ";")
        Usu_Count = Ds.Tables(0).Rows.Count
        If Usu_Count > 0 Then
            For Each Row_ As DataRow In Ds.Tables(0).Rows
                ListaUsu.Add(Row_)
                AgregaA(Row_(0), ListaSR_Usu)
            Next
        End If
        Ds = DB.Ver("SELECT * FROM " & "Entradas" & ";")
        Ent_Count = Ds.Tables(0).Rows.Count
        If Ent_Count > 0 Then
            For Each Row_ As DataRow In Ds.Tables(0).Rows
                ListaEnt.Add(Row_)
                AgregaA(Row_(0), ListaSR_Ent)
            Next
        End If
        DB.Dispose()
#End Region
        TiPal_SR_Count = ListaSR_TipPal.Count
        Usu_SR_Count = ListaSR_Usu.Count
        Ent_SR_Count = ListaSR_Ent.Count
        Directory.CreateDirectory(Ruta_ & "\DB_Entera")
        If CHB_ConEtiqueta.Checked Then
            LisCSV.AddRange("Palabra" & Sep & "TipoPalabra" & Sep & "Usuario" & Sep & "TipoUsuario" & Sep & "TextoOrigen" & Sep & "Posicion" & Sep & "Largo" & Sep & "SaltoLinea" & Sep & "Fecha" & vbCrLf)
        End If
        Guardar(Ruta_ & "\DB_Entera\TipoPalabras." & ext, Lista_A_Str(ListaTipPal), EsAnci)
        LisCSV.Clear()
        If CHB_ConEtiqueta.Checked Then
            LisCSV.AddRange("Cédula" & Sep & "TipoUsuario" & Sep & "Nombre" & Sep & "Apellido" & Sep & "UltAcceso" & vbCrLf)
        End If
        Guardar(Ruta_ & "\DB_Entera\Usuario." & ext, Lista_A_Str(ListaUsu), EsAnci)
        LisCSV.Clear()
        If CHB_ConEtiqueta.Checked Then
            LisCSV.AddRange("Cédula" & Sep & "Texto" & Sep & "Fecha" & vbCrLf)
        End If
        Guardar(Ruta_ & "\DB_Entera\Entradas." & ext, Lista_A_Str(ListaEnt), EsAnci)
    End Sub
#End Region
#Region "Utilidades 2"
    Private Function Lista_A_Str(ByRef LisDrow As List(Of DataRow))
        Dim LisCSV As New List(Of Char)
        For Each Rows_ As DataRow In LisDrow
            If LisCSV.Count > 0 Then
                LisCSV.AddRange(vbCr & vbLf)
            End If
            Dim Coma As Boolean = False
            For Each Str As Object In Rows_.ItemArray
                If Coma Then
                    LisCSV.AddRange(Sep)
                End If
                Coma = True
                LisCSV.AddRange(Str)
            Next
        Next
        Return New String(LisCSV.ToArray)
    End Function
    Private Function BuscaPal(ByVal Pal As String, ByRef Lista As List(Of String))
        For Each Str As String In Lista
            If Str = Pal Then
                Return True
            End If
        Next
        Return False
    End Function
    Private Sub AgregaA(ByVal Pal As String, ByRef Lista As List(Of String))
        If Not BuscaPal(Pal, Lista) Then
            Lista.Add(Pal)
        End If
    End Sub
#End Region
End Class
