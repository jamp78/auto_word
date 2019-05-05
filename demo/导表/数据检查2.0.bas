Attribute VB_Name = "数据检查"
Sub 数据检查()
Dim YqV As Integer, YqD As Integer, YqT As Integer, YqP As Integer, Yq_VD_Z As Integer, YqZ As Integer '仪器数量
Dim NumYK
Dim X_Tem As Single, X_HB As Single
'输入每种仪器个数
YqV = 5  '风速计
YqD = 3 '风向标
YqT = 1 '温度传感器
YqP = 1 '压力传感器
YqZ = YqV + YqD + YqT + YqP
Yq_VD_Z = YqV + YqD
'输入每个仪器数据占多少列
NumYK = 4
'输入现场海拔及年平均温度
X_Tem = -2     '年平均温度 摄氏度
'X_HB = 1509     '测量处海拔
X_HB = Split(Cells(5, 1), " ")(2)

ReDim Vspeed(YqV) As Integer
ReDim HVgao(YqV) As String
Dim Rng As Range

ReDim Ddirect(YqD) As Integer
ReDim HDgao(YqD) As Integer

ReDim YqTP(YqT + YqP) As Integer
ReDim YqTPm(YqT + YqP) As String
ReDim Cha(YqT + YqP) As Single


ReDim Yqm(YqZ) As String
Dim Vlow As Single, Vtop As Single, Dlow As Single, Dtop As Single, Plow As Single, Ptop As Single, Tlow As Single, Ttop As Single
ReDim Fanw(YqZ, 2) As Single
Dim col As Integer, Tcol As Integer



Dim Snum As Long
Set Rng = Range("e3")  '统计数据起始行，不包含上侧和左侧标题栏，至少从3行2列开始
V_X_Qrow = Rng.Row
V_X_Qcolumn = Rng.Column
D_X_Qrow = Rng.Row
D_X_Qcolumn = Rng.Column + 6 + UBound(Vspeed)
V_Q_Qrow = Rng.Row - 1
V_Q_Qcolumn = D_X_Qcolumn + UBound(Ddirect) + 2
Y_Q_Qrow = Rng.Row - 1
Y_Q_Qcolumn = V_Q_Qcolumn + 3
Z_F_Qrow = Rng.Row - 2
Z_F_Qcolumn = Y_Q_Qcolumn + 3
Z_B_Qrow = Rng.Row - 2
Z_B_Column = Z_F_Qcolumn + 3 + UBound(Yqm)
V_XX_Qrow = Rng.Row - 1
V_XX_Qcolumn = Z_B_Column + 4
Z_SZH_Qrow = Rng.Row
Z_SZH_QColumn = V_XX_Qcolumn + UBound(Vspeed) + 3

Application.ScreenUpdating = False
  '读取应测数据个数
  Snum = Range("a14").CurrentRegion.Rows.Count - 1


'输入仪器名称
For i = 1 To YqV
    mn = Split(Cells(13, 2 + (i - 1) * NumYK), " ")
    For j = 1 To UBound(mn) - 1
        Yqm(i - 1) = Yqm(i - 1) & mn(j)
    Next j
Next i

For i = 1 To YqD
    mn = Split(Cells(13, 2 + (YqV + i - 1) * NumYK), " ")
    Yqm(YqV + i - 1) = mn(1) & "D"
Next i

Yqm(YqV + YqD) = "温度"
Yqm(YqV + YqD + 1) = "气压"


'输入变化限值
Vlow = 0 '风速最小值
Vtop = 40 '风速最大值
Dlow = 0 '风向最小值
Dtop = 360.1 '风向最大值
Plow = 94 / (10 ^ (X_HB / 18400 * (1 + (1 / 273) * (X_Tem + X_HB / 200 * 0.6)))) '气压最小值kPa， 假设海拔升高100米气温降低0.6℃，压高公式
Ptop = 106 / (10 ^ (X_HB / 18400 * (1 + (1 / 273) * (X_Tem + X_HB / 200 * 0.6))))  '气压最大值kPa
Tlow = -40 '温度最小值摄氏度
Ttop = 50 '温度最大值摄氏度

'输入变化限值
Cha(0) = 5 '小时温度变化限值
Cha(1) = 1 '小时气压变化限值

For i = 0 To YqV - 1

Fanw(i, 0) = Vlow    '风速合理范围
Fanw(i, 1) = Vtop
Vspeed(i) = i * NumYK + 2 '风速所在列
HVgao(i) = Replace(Replace(Replace(Yqm(i), "A", ""), "B", ""), "m", "") '风速名
Next i

For i = 0 To YqD - 1
Fanw(i + YqV, 0) = Dlow   '风向合理范围
Fanw(i + YqV, 1) = Dtop
Ddirect(i) = (i + YqV) * NumYK + 2    '风向所在列
HDgao(i) = CInt(Replace(Replace(Replace(Yqm(i + YqV), "A", ""), "B", ""), "D", "")) 'CInt(Left(Yqm(i + YqV), 2))   '风向所在高度
Next i

For i = 0 To YqT - 1
Fanw(i + YqV + YqD, 0) = Tlow    '温度合理范围
Fanw(i + YqV + YqD, 1) = Ttop
YqTP(i) = (i + YqV + YqD) * NumYK + 2   '温度所在列  *****注意温度气压的顺序
YqTPm(i) = Yqm(YqV + YqD)
Next i

Tcol = YqTP(0) '温度所在列  *****冰冻数据检查用

For i = 0 To YqP - 1
Fanw(i + YqV + YqD + YqT, 0) = Plow    '气压合理范围
Fanw(i + YqV + YqD + YqT, 1) = Ptop
YqTP(YqT + i) = (i + YqV + YqD + YqT) * NumYK + 2   '气压所在列
YqTPm(i + YqT) = Yqm(YqV + YqD + YqT)
Next i

'统计测风塔设置
Dim Str_CV$, Str_CX$, Str_CT$, Str_CP$
Cells(Z_SZH_Qrow - 1, Z_SZH_QColumn) = "地理位置"
Range(Cells(Z_SZH_Qrow, Z_SZH_QColumn), Cells(Z_SZH_Qrow + 1, Z_SZH_QColumn)).Merge
Cells(Z_SZH_Qrow, Z_SZH_QColumn) = Replace(Split(Range("a3"), " ")(3), "?", "°") & Split(Range("a3"), " ")(4)
Range(Cells(Z_SZH_Qrow + 2, Z_SZH_QColumn), Cells(Z_SZH_Qrow + 3, Z_SZH_QColumn)).Merge
Cells(Z_SZH_Qrow + 2, Z_SZH_QColumn) = Replace(Split(Range("a4"), " ")(3), "?", "°") & Split(Range("a3"), " ")(4)
Cells(Z_SZH_Qrow - 1, Z_SZH_QColumn + 1) = "高程(m)"
Range(Cells(Z_SZH_Qrow, Z_SZH_QColumn + 1), Cells(Z_SZH_Qrow + 3, Z_SZH_QColumn + 1)).Merge
Cells(Z_SZH_Qrow, Z_SZH_QColumn + 1) = X_HB
Cells(Z_SZH_Qrow - 1, Z_SZH_QColumn + 2) = "高度(m)"
Range(Cells(Z_SZH_Qrow, Z_SZH_QColumn + 2), Cells(Z_SZH_Qrow + 3, Z_SZH_QColumn + 2)).Merge
Cells(Z_SZH_Qrow, Z_SZH_QColumn + 2) = HVgao(0)
Cells(Z_SZH_Qrow - 1, Z_SZH_QColumn + 3) = "项目及测层"
'Str_CV = Yqm(0)
'For i = 1 To YqV - 1
'Str_CV = Str_CV & "/" & Yqm(i)
'Next
'Cells(Z_SZH_Qrow, Z_SZH_QColumn + 3) = "风速：" & Str_CV
'Str_CX = Yqm(YqV)
'For i = YqV + 1 To YqV + YqD - 1
'Str_CX = Str_CX & "/" & Yqm(i)
'Next
'Cells(Z_SZH_Qrow + 1, Z_SZH_QColumn + 3) = "风向：" & Str_CX
Str_CV = HVgao(0)
For i = 1 To YqV - 1
Str_CV = Str_CV & "/" & HVgao(i)
Next
Cells(Z_SZH_Qrow, Z_SZH_QColumn + 3) = "风速：" & Str_CV
Str_CX = HDgao(0)
For i = 1 To YqD - 1
Str_CX = Str_CX & "/" & HDgao(i)
Next
Cells(Z_SZH_Qrow + 1, Z_SZH_QColumn + 3) = "风向：" & Str_CX

Cells(Z_SZH_Qrow + 2, Z_SZH_QColumn + 3) = "气温：" & Replace(Split(Cells(13, YqTP(0)), " ")(1), "m", "")
Cells(Z_SZH_Qrow + 3, Z_SZH_QColumn + 3) = "气压：" & Replace(Split(Cells(13, YqTP(1)), " ")(1), "m", "")
Cells(Z_SZH_Qrow - 1, Z_SZH_QColumn + 4) = "数据时段"
Range(Cells(Z_SZH_Qrow, Z_SZH_QColumn + 4), Cells(Z_SZH_Qrow + 3, Z_SZH_QColumn + 4)).Merge
Cells(Z_SZH_Qrow, Z_SZH_QColumn + 4) = Split(Range("a14"), " ")(0) & " ～ " & Split(Cells(Snum + 13, 1), " ")(0)

'统计各风速层不合理相关性数量
For i = 0 To UBound(Vspeed) - 2
For j = 1 + i To UBound(Vspeed) - 1
If CInt(HVgao(j)) = CInt(HVgao(i)) Then
Cells(V_X_Qrow + i, V_X_Qcolumn + j).Value = ""
Else
Cells(V_X_Qrow + i, V_X_Qcolumn + j).Value = 完整年风速相关性检查(Vspeed(i), Vspeed(j), (CInt(HVgao(i)) - CInt(HVgao(j))) \ 10, Snum)
End If
Next
Next
'完善表格
For j = 0 To UBound(Vspeed)
For i = 0 To UBound(Vspeed) - 1
If j = 0 Then
Cells(V_X_Qrow - 1 + j, i + V_X_Qcolumn).Value = Yqm(i)
ElseIf i < j Then
Cells(V_X_Qrow - 1 + j, i + V_X_Qcolumn - 1).Value = Cells(V_X_Qrow - 1 + i, j + V_X_Qcolumn - 1).Value
Else
End If
Next
Next
'统计各风速层不合理相关性数据
For i = 0 To UBound(Vspeed) - 1
Cells(V_X_Qrow + i, 5 + UBound(Vspeed)).Value = 统计列不合理数据(Vspeed(i), Snum)
Cells(V_X_Qrow + i, 6 + UBound(Vspeed)).Value = 统计列实测数据(Vspeed(i), Snum)
Next
Cells(V_X_Qrow - 1, 5 + UBound(Vspeed)) = "风速相关性不合理数据合计"
Cells(V_X_Qrow - 2, 6 + UBound(Vspeed)) = "风速应测数据合计"
Cells(V_X_Qrow - 1, 6 + UBound(Vspeed)) = "统计列实测数据"
Cells(V_X_Qrow - 1, 7 + UBound(Vspeed)) = "实测数据完整率"
Cells(V_X_Qrow - 1, 8 + UBound(Vspeed)) = "缺测数据"
'统计各风速层实测数据完整率
Cells(V_X_Qrow - 2, 7 + UBound(Vspeed)).Value = Snum
For i = 0 To UBound(Vspeed) - 1
Cells(V_X_Qrow + i, 7 + UBound(Vspeed)).Value = Cells(V_X_Qrow + i, 6 + UBound(Vspeed)).Value / Snum
Cells(V_X_Qrow + i, 8 + UBound(Vspeed)).Value = Snum - Cells(V_X_Qrow + i, 6 + UBound(Vspeed)).Value
Next

'统计各风向层不合理相关性数量
For i = 0 To UBound(Ddirect) - 2
For j = 1 + i To UBound(Ddirect) - 1
If HDgao(j) = HDgao(i) Then
Cells(D_X_Qrow + i, D_X_Qcolumn + j).Value = ""
Else
Cells(D_X_Qrow + i, D_X_Qcolumn + j).Value = 完整年风向相关性检查(Ddirect(i), Ddirect(j), (HDgao(i) - HDgao(j)) * 1.125, Snum)
End If
Next
Next
'完善表格
For j = 0 To UBound(Ddirect)
For i = 0 To UBound(Ddirect) - 1
If j = 0 Then
Cells(D_X_Qrow - 1 + j, i + D_X_Qcolumn).Value = HDgao(i) & "D"
ElseIf i < j Then
Cells(D_X_Qrow - 1 + j, i + D_X_Qcolumn - 1).Value = Cells(D_X_Qrow - 1 + i, j + D_X_Qcolumn - 1).Value
Else
End If
Next
Next
'统计各风向层不合理相关性数据
For i = 0 To UBound(Ddirect) - 1
Cells(D_X_Qrow + i, D_X_Qcolumn + UBound(Ddirect)).Value = 统计列不合理数据(Ddirect(i), Snum)
Next
Cells(D_X_Qrow - 1, D_X_Qcolumn + UBound(Ddirect)) = "风向相关性不合理数据合计"

'统计各风风速计不合理变化趋势数量
For i = 0 To UBound(Vspeed) - 1

Cells(V_Q_Qrow + i + 1, V_Q_Qcolumn + 1).Value = 完整年风速变化趋势检查(Vspeed(i), 6, Snum)

Next
'完善表格
For i = 0 To UBound(Vspeed) - 1
Cells(V_Q_Qrow + i + 1, V_Q_Qcolumn).Value = Yqm(i)
Next
Cells(V_Q_Qrow, V_Q_Qcolumn + 1) = "风速变化趋势不合理数据合计"

'统计各温度计气压计不合理变化趋势数量
For i = 0 To UBound(YqTP) - 1

Cells(Y_Q_Qrow + i + 1, Y_Q_Qcolumn + 1).Value = 单列完整年差值检查(YqTP(i), Cha(0), Snum)

Next
'完善表格
For i = 0 To UBound(YqTP)
Cells(Y_Q_Qrow + i + 1, Y_Q_Qcolumn).Value = YqTPm(i)
Next
Cells(Y_Q_Qrow, Y_Q_Qcolumn + 1) = "温度气压变化趋势不合理数据合计"

'统计各仪器不合理变化趋势数量

For i = 0 To YqZ - 1
col = i * 4 + 2
Cells(Z_F_Qrow + 1, Z_F_Qcolumn + i + 1).Value = 单列完整年范围检查(col, Fanw(i, 0), Fanw(i, 1), Snum)

Next
'完善表格
For i = 0 To YqZ - 1
Cells(Z_F_Qrow, Z_F_Qcolumn + i + 1).Value = Yqm(i)
Next
Cells(Z_F_Qrow + 1, Z_F_Qcolumn) = "仪器数据范围不合理合计"

'统计各风向风速计冰冻数量

For i = 0 To Yq_VD_Z - 1
col = i * NumYK + 2
Cells(Z_B_Qrow + i + 1, Z_B_Column + 1).Value = 单列完整年冰冻检查(col, Tcol, Snum)
Cells(Z_B_Qrow + i + 1, Z_B_Column + 2).Value = Round(Cells(Z_B_Qrow + i + 1, Z_B_Column + 1).Value / Snum * 100, 2)
Next
'完善表格
For i = 0 To Yq_VD_Z - 1
Cells(Z_B_Qrow + i + 1, Z_B_Column).Value = Yqm(i)
Next
Cells(Z_B_Qrow, Z_B_Column + 1) = "冰冻数据合计"
Cells(Z_B_Qrow, Z_B_Column + 2) = "冰冻数据占比（%）"

'清除冰冻及范围不合理数据
For i = 0 To YqZ - 1
col = i * NumYK + 2
    For j = 14 To Snum + 12
    If Cells(j, col).style = "注释" Or Cells(j, col).style = "计算" Then
    Range(Cells(j, col), Cells(j, col + 3)).ClearContents
    End If
    Next
Next

'统计各风速计相关性系数
For i = 0 To UBound(Vspeed) - 1
For j = 1 + i To UBound(Vspeed) - 1

Cells(V_XX_Qrow + j, V_XX_Qcolumn + i + 1).Value = Round(Application.Correl(Range(Cells(14, Vspeed(i)), Cells(14 + 8783, Vspeed(i))), Range(Cells(14, Vspeed(j)), Cells(14 + 8783, Vspeed(j)))), 3)

Next
Next
'完善表格
For i = 0 To UBound(Vspeed) - 1
For j = 0 To UBound(Vspeed) - 1
If i = 0 Then
Cells(V_XX_Qrow, V_XX_Qcolumn + 1 + j).Value = Yqm(j)
ElseIf j = 0 Then
Cells(V_XX_Qrow + i, V_XX_Qcolumn).Value = Yqm(i)
ElseIf i <= j Then
Cells(V_XX_Qrow + i, V_XX_Qcolumn + 1 + j).Value = "/"
End If
Next
Next
Cells(V_XX_Qrow, V_XX_Qcolumn).Value = "高度"


Application.ScreenUpdating = True
End Sub
Function 完整年风速相关性检查(V1 As Integer, V2 As Integer, Cha As Integer, Snum As Long)
Dim n As Integer, Row As Integer, Col1 As Integer, Col2 As Integer '统计两高度风速不合理性数量
Row = 14
Col1 = V1
Col2 = V2
n = 0
For i = 0 To Snum - 1
If 风速相关性检查(Cells(Row + i, Col1).Value, Cells(Row + i, Col2).Value, Cha) = 1 Then
    If Cells(Row + i, Col2).Value < 0.5 Then
    Else
    Cells(Row + i, Col1).style = "差"
    End If
    If Cells(Row + i, Col1).Value < 0.5 Then
    Else
     Cells(Row + i, Col2).style = "差"
     End If
 Cells(Row + i, 3).style = "差"
 n = n + 1
End If
Next
完整年风速相关性检查 = n
End Function
Function 风速相关性检查(V1 As Single, V2 As Single, Cha As Integer)
If Abs(V1 - V2) >= Cha And V1 <> 0 And V2 <> 0 Then
风速相关性检查 = 1
Else
风速相关性检查 = 0
End If
End Function
Function 统计列不合理数据(col As Integer, Snum As Long)
n = 0
For i = 14 To 13 + Snum
If Cells(i, col).style = "差" Then
n = n + 1
End If
Next
统计列不合理数据 = n
End Function
Function 统计列实测数据(col As Integer, Snum As Long)
n = 0
For i = 14 To 13 + Snum
If Cells(i, col).Value <> "" Then
n = n + 1
End If
Next
统计列实测数据 = n
End Function

Function 完整年风向相关性检查(V1 As Integer, V2 As Integer, Cha As Single, Snum As Long)
Dim n As Integer, Row As Integer, Col1 As Integer, Col2 As Integer '统计两高度风向不合理性数量
Row = 14
Col1 = V1
Col2 = V2
n = 0
For i = 0 To Snum - 1
If 风向相关性检查(Cells(Row + i, Col1).Value, Cells(Row + i, Col2).Value, Cha) = 1 Then
   If Cells(Row + i, Col2 + 1).Value < 0.4 And Cells(Row + i, Col1 + 1).Value >= 0.4 Then
   Else
    Cells(Row + i, Col1).style = "差"
    End If
   If Cells(Row + i, Col1 + 1).Value < 0.4 And Cells(Row + i, Col2 + 1).Value >= 0.4 Then
   Else
     Cells(Row + i, Col2).style = "差"
     End If
 Cells(Row + i, 3).style = "差"
 n = n + 1
End If
Next
完整年风向相关性检查 = n
End Function
Function 风向相关性检查(V1 As Single, V2 As Single, Cha As Single)
If Abs(V1 - V2) >= Cha And V1 <> 0 And V2 <> 0 And Abs(V1 - V2) <= 360 - Cha Then
风向相关性检查 = 1
Else
风向相关性检查 = 0
End If
End Function
Function 完整年风速变化趋势检查(V1 As Integer, Cha As Single, Snum As Long)
Dim n As Integer, Row As Integer, Col1 As Integer, Col2 As Integer '统计两高度风向不合理性数量
Row = 14
Col1 = V1
'Col2 = V2
n = 0
For i = 0 To Snum - 2
If 风速变化趋势检查(Cells(Row + i, Col1).Value, Cells(Row + i + 1, Col1).Value, Cha) = 1 Then
Cells(Row + i + 1, Col1).style = "适中"
Cells(Row + i, Col1).style = "适中"
Cells(Row + i + 1, 3).style = "差"
Cells(Row + i, 3).style = "差"
 n = n + 1
End If
Next
完整年风速变化趋势检查 = n
End Function
Function 风速变化趋势检查(V1 As Single, V2 As Single, Cha As Single)
If Abs(V1 - V2) >= Cha And V1 <> 0 And V2 <> 0 Then
风速变化趋势检查 = 1
Else
风速变化趋势检查 = 0
End If
End Function

Function 单列完整年差值检查(V1 As Integer, Cha As Single, Snum)
Dim n As Integer, Row As Integer, Col1 As Integer, Col2 As Integer
Row = 14
Col1 = V1
n = 0
For i = 0 To Snum - 2
If 差值检查(Cells(Row + i, Col1).Value, Cells(Row + i + 1, Col1).Value, Cha) = 1 Then
Cells(Row + i + 1, Col1).style = "适中"
Cells(Row + i, Col1).style = "适中"
Cells(Row + i + 1, 3).style = "差"
Cells(Row + i, 3).style = "差"
 n = n + 1
End If
Next
单列完整年差值检查 = n
End Function
Function 差值检查(V1 As Single, V2 As Single, Cha As Single)
If Abs(V1 - V2) >= Cha And V1 <> 0 And V2 <> 0 Then
差值检查 = 1
Else
差值检查 = 0
End If
End Function

Function 单列完整年范围检查(col As Integer, Low As Single, Top As Single, Snum As Long)
Dim n As Integer, Row As Integer
Row = 14
n = 0
For i = 0 To Snum - 1 '完整年数据量
If 范围检查(Cells(Row + i, col).Value, Low, Top) = 1 And Cells(Row + i, col).Value <> "" Then
Cells(Row + i, col).style = "计算"
Cells(Row + i, 3).style = "差"
 n = n + 1
End If
Next
单列完整年范围检查 = n
End Function
Function 范围检查(Shu As Single, Low As Single, Top As Single) '合理范围大于等于最小值，小于最大值
If Shu >= Top Or Shu < Low Then
范围检查 = 1
Else
范围检查 = 0
End If
End Function

Function 单列完整年冰冻检查(col As Integer, ColT As Integer, Snum)
Dim n As Integer, Row As Integer
Row = 14
n = 0
For i = 0 To Snum - 1 '完整年数据量
If 冰冻检查(Cells(Row + i, col + 1).Value, Cells(Row + i, ColT).Value) = 1 And Cells(Row + i, col).Value <> "" And (Cells(Row + i, col).Value = Cells(Row + i + 1, col).Value Or Cells(Row + i, col).Value = Cells(Row + i - 1, col).Value) Then
Cells(Row + i, col).style = "注释"
Cells(Row + i, 3).style = "差"
 n = n + 1
End If
Next
单列完整年冰冻检查 = n
End Function
Function 冰冻检查(Sd As Double, Tem As Double) '温度低于0.5，标准偏差等于0
If Sd < 0.2 And Tem <= 0.7 Then
冰冻检查 = 1
Else
冰冻检查 = 0
End If
End Function
Function dtodfm(du As Single)
dtodfm = Int(du) & "°" & Int((du - Int(du)) * 60) & Chr(39) & ((du - Int(du)) * 60 - Int((du - Int(du)) * 60)) * 60 & Chr(34)
End Function

