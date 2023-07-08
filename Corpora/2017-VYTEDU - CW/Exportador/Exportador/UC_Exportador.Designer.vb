<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class UC_Exportador
    Inherits System.Windows.Forms.UserControl

    'UserControl1 reemplaza a Dispose para limpiar la lista de componentes.
    <System.Diagnostics.DebuggerNonUserCode()>
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Requerido por el Diseñador de Windows Forms
    Private components As System.ComponentModel.IContainer

    'NOTA: el Diseñador de Windows Forms necesita el siguiente procedimiento
    'Se puede modificar usando el Diseñador de Windows Forms.  
    'No lo modifique con el editor de código.
    <System.Diagnostics.DebuggerStepThrough()>
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Me.BT_UnifBases = New System.Windows.Forms.Button()
        Me.BT_Exportar = New System.Windows.Forms.Button()
        Me.OFD_ = New System.Windows.Forms.OpenFileDialog()
        Me.SFD_ = New System.Windows.Forms.SaveFileDialog()
        Me.ToolTip1 = New System.Windows.Forms.ToolTip(Me.components)
        Me.CHB_ConEtiqueta = New System.Windows.Forms.CheckBox()
        Me.CHB_UsarTab = New System.Windows.Forms.CheckBox()
        Me.SuspendLayout()
        '
        'BT_UnifBases
        '
        Me.BT_UnifBases.FlatStyle = System.Windows.Forms.FlatStyle.Flat
        Me.BT_UnifBases.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BT_UnifBases.Location = New System.Drawing.Point(3, 3)
        Me.BT_UnifBases.Name = "BT_UnifBases"
        Me.BT_UnifBases.Size = New System.Drawing.Size(140, 40)
        Me.BT_UnifBases.TabIndex = 6
        Me.BT_UnifBases.Text = "Unificar Bases"
        Me.BT_UnifBases.UseVisualStyleBackColor = True
        '
        'BT_Exportar
        '
        Me.BT_Exportar.FlatStyle = System.Windows.Forms.FlatStyle.Flat
        Me.BT_Exportar.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BT_Exportar.Location = New System.Drawing.Point(149, 3)
        Me.BT_Exportar.Name = "BT_Exportar"
        Me.BT_Exportar.Size = New System.Drawing.Size(84, 40)
        Me.BT_Exportar.TabIndex = 7
        Me.BT_Exportar.Text = "Exportar"
        Me.BT_Exportar.UseVisualStyleBackColor = True
        '
        'OFD_
        '
        Me.OFD_.Filter = "Base dedados SQLite (*.db)|*.db"
        Me.OFD_.Multiselect = True
        '
        'SFD_
        '
        Me.SFD_.FileName = "00 Nueva DB"
        Me.SFD_.Filter = "Base dedados SQLite (*.db)|*.db"
        '
        'CHB_ConEtiqueta
        '
        Me.CHB_ConEtiqueta.AutoSize = True
        Me.CHB_ConEtiqueta.Location = New System.Drawing.Point(149, 49)
        Me.CHB_ConEtiqueta.Name = "CHB_ConEtiqueta"
        Me.CHB_ConEtiqueta.Size = New System.Drawing.Size(86, 17)
        Me.CHB_ConEtiqueta.TabIndex = 8
        Me.CHB_ConEtiqueta.Text = "Con etiqueta"
        Me.CHB_ConEtiqueta.UseVisualStyleBackColor = True
        '
        'CHB_UsarTab
        '
        Me.CHB_UsarTab.AutoSize = True
        Me.CHB_UsarTab.Location = New System.Drawing.Point(3, 49)
        Me.CHB_UsarTab.Name = "CHB_UsarTab"
        Me.CHB_UsarTab.Size = New System.Drawing.Size(116, 17)
        Me.CHB_UsarTab.TabIndex = 9
        Me.CHB_UsarTab.Text = "No usar ; Usar Tab"
        Me.CHB_UsarTab.UseVisualStyleBackColor = True
        '
        'UC_Exportador
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.BackColor = System.Drawing.SystemColors.ActiveCaption
        Me.Controls.Add(Me.CHB_UsarTab)
        Me.Controls.Add(Me.CHB_ConEtiqueta)
        Me.Controls.Add(Me.BT_UnifBases)
        Me.Controls.Add(Me.BT_Exportar)
        Me.Name = "UC_Exportador"
        Me.Size = New System.Drawing.Size(238, 74)
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents BT_UnifBases As Button
    Friend WithEvents BT_Exportar As Button
    Friend WithEvents OFD_ As OpenFileDialog
    Friend WithEvents SFD_ As SaveFileDialog
    Friend WithEvents ToolTip1 As ToolTip
    Friend WithEvents CHB_ConEtiqueta As CheckBox
    Friend WithEvents CHB_UsarTab As CheckBox
End Class
