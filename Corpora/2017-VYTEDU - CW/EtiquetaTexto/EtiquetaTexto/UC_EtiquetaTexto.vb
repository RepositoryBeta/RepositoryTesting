Imports System.IO
Imports System.Data.SQLite
Public Class UC_EtiquetaTexto
    Public Event ConfiguraEIL(ByVal Contraseña As String, ByVal Admin As String)
    Private Sub UC_EtiquetaTexto_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        RaiseEvent ConfiguraEIL("ugelo2", "9999999999") 'Aqui va su contraseña
    End Sub
    Dim UltimaPos As Integer = 0
#Region "Datos de Entrada"
    Private ColorLetra_ As Color
    Private BackColor_ As Color
    Private Negritas_ As Boolean
    Private TamañoLetra_ As Decimal
    Public Sub ConfiguracionRichTextBox(ByVal ColorLetra_ As Color, ByVal BackColor_ As Color, ByVal Negritas_ As Boolean, ByVal TamañoLetra_ As Decimal)
        RichTextBox1.SelectAll()
        RichTextBox1.SelectionColor = ColorLetra_
        RichTextBox1.Select(0, 0)
        RichTextBox1.BackColor = BackColor_
        If Negritas_ Then
            RichTextBox1.Font = New Font(RichTextBox1.Font.FontFamily, CSng(TamañoLetra_), FontStyle.Bold)
        Else
            RichTextBox1.Font = New Font(RichTextBox1.Font.FontFamily, CSng(TamañoLetra_), FontStyle.Regular)
        End If
    End Sub
    Sub New()
        InitializeComponent()
    End Sub
    Public Sub Reset()
        RichTextBox1.Text = ""
    End Sub
    Public Sub CargandoDatos(ByVal Ruta As String, ByVal Usuario As String, ByVal TipoUsuario As String, ByVal TipoPalabra As String, ByVal TextoOrigen As String, ByVal T0 As DateTime, ByVal RutaDb As String, ByVal EsAdmin As Boolean)
        RichTextBox1.Select(0, 0)
        RtfScroll(RichTextBox1.Handle, EM_SETSCROLLPOS, 0, New System.Drawing.Point(0, 0))
        Me.Ruta = Ruta : Me.Usuario = Usuario : Me.TipoUsuario = TipoUsuario : Me.TipoPalabra = TipoPalabra : Me.TextoOrigen = TextoOrigen : Me.T0 = T0
        Leer(Me.Ruta, Texto_)
        RichTextBox1.Text = Texto_ & " "
        BaseDeDatos.Ruta = RutaDb
        If Not EsAdmin Then
            BaseDeDatos.CSR("insert into " & "Entradas" & " values" & "('" & Usuario & "', '" & TextoOrigen & "', '" & T0 & "')" & ";")
        End If
        Actualizar()
    End Sub
    Public Property Ruta As String
        Get
            Return Ruta_
        End Get
        Set(value As String)
            Ruta_ = value
        End Set
    End Property
    Public Property Usuario As String
        Get
            Return Usuario_
        End Get
        Set(value As String)
            Usuario_ = value
        End Set
    End Property
    Public Property TipoUsuario As String
        Get
            Return TipoUsuario_
        End Get
        Set(value As String)
            TipoUsuario_ = value
        End Set
    End Property
    Public Property TipoPalabra As String
        Get
            Return TipoPalabra_
        End Get
        Set(value As String)
            TipoPalabra_ = value
        End Set
    End Property
    Public Property TextoOrigen As String
        Get
            Return TextoOrigen_
        End Get
        Set(value As String)
            TextoOrigen_ = value
        End Set
    End Property
    Public Ruta_ As String
    Public Texto_ As String
    Public Usuario_ As String
    Public TipoUsuario_ As String
    Public TipoPalabra_ As String
    Public TextoOrigen_ As String
    Public T0 As DateTime
    Public BaseDeDatos As New SQLiteDB
#End Region
    Public Function Leer(Ruta As String, ByRef Texto As String) As Boolean
        Try
            Texto = File.ReadAllText(Ruta, System.Text.Encoding.UTF8)
        Catch ex As Exception
            Return False
        End Try
        Return True
    End Function
#Region "Area de marcado de texto"
    Dim NoValChar As String = " "" '¿?¡!#$%&()={[(|)]}:;-_<>•.," & vbTab & vbCr & vbLf
    Private Sub RichTextBox1_Click(sender As Object, e As EventArgs) Handles RichTextBox1.Click
        LockWindowUpdate(RichTextBox1.Handle.ToInt32)
        VerPosicion = GetScrollPos(RichTextBox1.Handle, SBS_VERT)
        Dim SS As Integer = RichTextBox1.SelectionStart
        If Not UltimaPos = SS Then
            UltimaPos = SS
            Dim Str As String = RichTextBox1.Text
            Dim Max As Integer = Str.Length
            Dim Pos As Integer = RichTextBox1.SelectionStart
            Dim StrRec As String = ""
            Dim PosIni As Integer = 0
            If Pos = Max Then
                Pos -= 1
            End If
            For i As Integer = Pos To 0 Step -1
                If InStr(1, NoValChar & ".,", Str(i)) > 0 Then
                    If Not (i = Pos And i > 0) Then : Exit For : End If
                End If
                Pos = i
                PosIni = Pos
            Next
            For i As Integer = Pos To Max - 1 Step 1
                If InStr(1, NoValChar & ".,", Str(i)) > 0 Then
                    Exit For
                Else
                    StrRec = StrRec & Char.ToLower(Str(i))
                End If
            Next
            Dim S1 As String = RichTextBox1.SelectedText
            Dim S2 As String = ""
            Dim C As Boolean = False
            For i As Integer = S1.Length - 1 To 0 Step -1
                If Not C Then
                    If Not InStr(1, NoValChar, S1(i)) > 0 Then
                        C = True
                    End If
                End If
                If C Then
                    S2 = S2 & S1(i)
                End If
            Next
            C = False
            S1 = ""
            For i As Integer = S2.Length - 1 To 0 Step -1
                If Not C Then
                    If Not InStr(1, NoValChar, S2(i)) > 0 Then
                        C = True
                    End If
                End If
                If C Then
                    S1 = S1 & S2(i)
                End If
            Next
            If S1 <> "" Then
                AccionFrasePalabra(S1, PosIni, False)
            ElseIf StrRec <> "" Then
                AccionFrasePalabra(StrRec, PosIni, True)
            End If

        End If
        RichTextBox1.SelectionStart = SS
        RtfScroll(RichTextBox1.Handle, EM_SETSCROLLPOS, 0, New System.Drawing.Point(0, VerPosicion))
        LockWindowUpdate(0)
    End Sub
    Private Sub AccionFrasePalabra(Texto As String, PosIni As Integer, TipoPalabra As Boolean)
        Select Case TipoUsuario_
            Case "Alumno"
                If TipoPalabra Then
                    If MessageBox.Show("Desea registrar la palabra: " & Texto, "Registro de palabra", MessageBoxButtons.YesNo) = DialogResult.Yes Then
                        RegistraPalabra(Texto, PosIni)
                        Actualizar()
                    End If
                Else
                    If MessageBox.Show("Desea registrar la frase: " & Texto, "Registro de palabra", MessageBoxButtons.YesNo) = DialogResult.Yes Then
                        RegistraPalabra(Texto, PosIni)
                        Actualizar()
                    End If
                End If
            Case "Profesor"
                If TipoPalabra Then
                    If MessageBox.Show("Desea registrar la palabra: " & Texto, "Registro de palabra", MessageBoxButtons.YesNo) = DialogResult.Yes Then
                        RegistraPalabra(Texto, PosIni)
                        Actualizar()
                    End If
                Else
                    If MessageBox.Show("Desea registrar la frase: " & Texto, "Registro de palabra", MessageBoxButtons.YesNo) = DialogResult.Yes Then
                        RegistraPalabra(Texto, PosIni)
                        Actualizar()
                    End If
                End If
        End Select
    End Sub
    Public Event TerminoMarcado(ByVal Termino As String)
    Private Sub RegistraPalabra(Str As String, PosIni As Integer)
        If Str <> "" Then
            RaiseEvent TerminoMarcado(Str)
            RegistroDePalabra(Str, PosIni)
        Else
            MsgBox("Errror cientquiniento-4 en la seleccion." & vbCrLf & "Recuerde en que condiciones salio el error e informe el codigo y las sircunstancias del errror al administrador del sistema")
        End If
    End Sub
    Private Sub RegistroDePalabra(ByVal Str As String, PosIni As Integer)
        Dim Valor As Integer = RichTextBox1.SelectionStart
        Dim SaltoLinea As Integer = ContarvbCr(RichTextBox1.Text, Valor)
        Valor = PosIni + SaltoLinea
        If Not Existe(Str) Then
            BaseDeDatos.CSR("insert into " & "TipoPalabras" & " values" & "('" & Str & "', '" & TipoPalabra_ & "', '" & Usuario_ & "', '" & TipoUsuario_ & "', '" & TextoOrigen_ & "', '" & Valor & "', '" & Str.Length & "', '" & SaltoLinea & "','" & T0 & "')" & ";")
        Else
            MsgBox("Ya esta ingresada")
        End If
    End Sub
    Public Actu As Boolean = True
    Dim ControlDisposed_ As Boolean = False
    Private Sub Actualizar()
        If Actu Then
            Try
                Dim SeleccionStart As Integer = RichTextBox1.SelectionStart
                RichTextBox1.SelectionStart = 0
                RichTextBox1Text = RichTextBox1.Text
                RichTextBox1.SelectionLength = RichTextBox1.TextLength
                RichTextBox1.SelectionBackColor = Nothing
                RichTextBox1.SelectionColor = RichTextBox1.ForeColor
                RichTextBox1.Invoke(New MethodInvoker(AddressOf Pintado02))
                RichTextBox1.SelectionStart = 0
                RichTextBox1.SelectionStart = SeleccionStart
            Catch ex As Exception
            End Try
        End If
    End Sub
    Dim RichTextBox1Text As String = ""
    Public Event ActualizaContador(ByVal TextoOrigen As String, ByVal Cantidad As Integer)
    Private Sub Pintado02()
        Dim Lista As List(Of String) = ActualizarPalabras()
        RaiseEvent ActualizaContador(TextoOrigen_, Lista.Count)
        Dim Str As String = RichTextBox1Text.ToLower()
        Dim Palabra As String = ""
        Dim Index As Integer = 0
        Dim PosIni As Integer = 0
        Dim Pos As Integer = 0
        Dim Antes As Integer = 0
        Dim Despues As Integer = 0
        For Each Cla As String In Lista
            Index = 1
            While Index < Str.Length
                Pos = InStr(Index, Str, Cla)
                If Pos > 0 Then
                    Antes = Pos - 2
                    If Antes < 0 Then
                        Antes = 0
                    End If
                    Despues = Antes + Cla.Length + 1
                    If Despues > Str.Length - 1 Then
                        Despues = Str.Length - 1
                    End If
                    If InStr(1, NoValChar, Str(Antes)) > 0 Then
                        If InStr(1, NoValChar, Str(Despues)) > 0 Then
                            Pos_DLGD = Pos - 1
                            ClaLength = Cla.Length
                            RichTextBox1.Invoke(New MethodInvoker(AddressOf RTBDelegadoActualiza))
                        End If
                    End If
                    Index = Pos + 1
                Else
                    Exit While
                End If
            End While
        Next
        RichTextBox1.SelectionStart = RichTextBox1.TextLength
        RichTextBox1.SelectionColor = RichTextBox1.ForeColor
    End Sub
    Dim Pos_DLGD As Integer
    Dim ClaLength As Integer
    Private Sub RTBDelegadoActualiza()
        If Not ControlDisposed_ Then
            RichTextBox1.SelectionStart = Pos_DLGD
            RichTextBox1.SelectionLength = ClaLength
            RichTextBox1.SelectionBackColor = Color.GreenYellow
        End If
    End Sub
    Private Function ActualizarPalabras()
        Return ActualizarPalabras(Usuario_, TipoUsuario_, TextoOrigen_)
    End Function
    Private Function ActualizarPalabras(ByVal Usuario As String, ByVal TipoUsuario As String, ByVal TextoOrigen As String)
        Dim Ds As DataSet = BaseDeDatos.Ver("SELECT Palabra FROM TipoPalabras WHERE Usuario = '" & Usuario & "' AND TipoUsuario = '" & TipoUsuario & "' AND TextoOrigen = '" & TextoOrigen & "';")
        Dim Dt As DataTable = Ds.Tables(0)
        Dim Lista As New List(Of String)
        Try
            If Ds.Tables(0).Rows.Count > 0 Then
                For Each Row_ As DataRow In Dt.Rows
                    Lista.Add(Row_("Palabra"))
                Next
            End If
        Catch ex As Exception
        End Try
        Return Lista
    End Function
    Private Sub UC_EtiquetaTexto_DragDrop(sender As Object, e As DragEventArgs) Handles Me.DragDrop
        ControlDisposed_ = True
    End Sub
#Region "Varios"
    Private Function ContarvbCr(ByRef Str As String, ByVal Valor As Integer) 'RTB_.SelectionStart + EspacioDelante
        Dim a As Integer = 0
        If Valor > Str.Length - 1 Then
            Valor = Str.Length - 1
        End If
        For i As Integer = 0 To Valor
            If Str(i) = vbLf Then
                a += 1
            End If
        Next
        Return a
    End Function
    Private Function Existe(Palabra As String) As Boolean
        Dim Ds As DataSet
        Ds = BaseDeDatos.Ver("SELECT Palabra FROM TipoPalabras WHERE TipoPalabras.Palabra = '" & Palabra & "' AND TipoPalabras.Usuario = '" & Usuario_ & "' AND TipoPalabras.TipoUsuario = '" & TipoUsuario_ & "' AND TipoPalabras.TextoOrigen = '" & TextoOrigen_ & "';")
        Try
            If Ds.Tables(0).Rows.Count > 0 Then
                Return True
            End If
        Catch ex As Exception
        End Try
        Return False
    End Function
#End Region
#End Region
#Region "Codigo SQLite"
#Region "Codigo para crear la base de datos"
    Dim CT_TipoPalabras As String = "CREATE TABLE TipoPalabras (Palabra TEXT, TipoPalabra TEXT, Usuario TEXT, TipoUsuario TEXT, TextoOrigen TEXT, Posicion TEXT, Largo TEXT, SaltoLinea TEXT, Fecha TEXT);"
    Dim CT_Usuario As String = "CREATE TABLE Usuario (Cedula Text, TipoUsuario Text, Nombre TEXT, Apellidos TEXT, UltAcceso TEXT);"
    Dim CT_Entradas As String = "CREATE TABLE Entradas (Cedula Text, Texto Text, Fecha TEXT);"
    Public Sub CrearBaseDeDatos(ByVal Ruta As String)
        Dim NuevaBaseDeDatos As New SQLiteDB(Ruta)
        NuevaBaseDeDatos.CSR(CT_TipoPalabras & CT_Usuario & CT_Entradas)
    End Sub
#End Region
    Class SQLiteDB
        Private Ruta_ As String = ""
        Private Conexion_ As String = ""
        Public Property Ruta As String
            Get
                Return Ruta_
            End Get
            Set(value As String)
                Ruta_ = value
                Conexion_ = "Data Source = " & Ruta_ & ";"
                SQLConnetionLite = New SQLiteConnection(Conexion_)
            End Set
        End Property
        Dim SQLConnetionLite As SQLiteConnection
        Dim SQLCommandLite As SQLiteCommand
        Dim SQLDataAdapterLite As SQLiteDataAdapter
        Sub New()
        End Sub
        Sub New(ByVal Ruta As String)
            Me.Ruta = Ruta
        End Sub
        Public Sub CSR(ByVal Comando As String)
            AbrirDB()
            SQLCommandLite.CommandText = Comando
            SQLCommandLite.ExecuteNonQuery()
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
                SQLCommandLite.CommandText = Comando
                SQLDataAdapterLite = New SQLiteDataAdapter(SQLCommandLite)
                SQLDataAdapterLite.Fill(Ds)
                SQLiteClose()
                Return Ds
            Catch ex As Exception
            End Try
            Return Ds
        End Function
        Public Sub Dispose()
            SQLDataAdapterLite.Dispose()
            SQLCommandLite.Dispose()
            SQLConnetionLite.Dispose()
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
                SQLConnetionLite.Open()
                SQLCommandLite = SQLConnetionLite.CreateCommand()
            Catch ex As Exception
                SQLCommandLite = SQLConnetionLite.CreateCommand()
                'MsgBox("Errror al abrir la base de datos")
            End Try
        End Sub
        Public Sub SQLiteClose()
            If Not IsNothing(SQLConnetionLite) Then
                SQLConnetionLite.Close()
            End If
        End Sub
    End Class
#End Region
#Region "GestionDeRichTextBox"
    Public Declare Function LockWindowUpdate Lib "user32" (ByVal hWnd As Integer) As Integer
    Public Declare Function GetScrollPos Lib "user32.dll" (ByVal hWnd As IntPtr, ByVal nBar As Integer) As Integer
    Public VerPosicion As Integer = 0
    Public Const SBS_VERT As Integer = &H1
    Public Declare Auto Function RtfScroll _
                Lib "user32.dll" Alias "SendMessage" (
                ByVal hWnd As IntPtr,
                ByVal Msg As Integer,
                ByVal wParam As IntPtr,
                ByRef lParam As System.Drawing.Point) As Integer
    Public Const WM_USER = &H400
    Public Const EM_GETSCROLLPOS = WM_USER + 221
    Public Const EM_SETSCROLLPOS = WM_USER + 222
#End Region
End Class
