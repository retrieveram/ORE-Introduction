import pandas as pd ; import numpy as np ; import gzip ; import csv

#---- 共通メソッドの短縮形 (bound method)
def asDA(obj): return obj.dataAsDate
def asST(obj): return obj.dataAsString
def asPE(obj): return obj.dataAsPeriod
def asRE(obj): return obj.dataAsReal
def asSI(obj): return obj.dataAsSize

def format_report(rOBJ):
  rptHead = [[ii, rOBJ.header(ii), rOBJ.columnType(ii)]
                                        for ii in range(rOBJ.columns())]
  rptFM = dict() ; nullNUM = 1.0e30
  for jj, colNM, dType in rptHead:
    if   dType == 0: rptFM[colNM] = list(asSI(rOBJ)(jj))
    elif dType == 1: rptFM[colNM] = [np.nan if (vv is None or abs(vv) > nullNUM)
                              else vv for vv in list(asRE(rOBJ)(jj))]
    elif dType == 2: rptFM[colNM] = list(asST(rOBJ)(jj))
    elif dType == 3: rptFM[colNM] = [d.ISO() for d in asDA(rOBJ)(jj)]
    elif dType == 4: rptFM[colNM] = list(asPE(rOBJ)(jj))
  return pd.DataFrame(rptFM)
rOBJxdf = format_report
# ---------------------------------------------------

def checkErrorsAndRunTime(oreOBJ):
  err = oreOBJ.getErrors()
  print ("Run time:%.2f sec" % oreOBJ.getRunTime(), end=', ')
  print ("Errors:%d" % len(err))
  if len(err) > 0:
    for i, e in enumerate(err): print(f'{i}: {repr(e)}')
chkERR = checkErrorsAndRunTime
# ---------------------------------------------------

# column types: see PlainInMemoryReport definition
def checkReportStructure(rOBJ, rptNM=None):
  dcTyp = {0:"Size",1:"Real",2:"string",3:"Date",4:"Period"}
  styFM = "%-6s %-20s %-8s %-10s"
  if rptNM: print("Report:%-s" % rptNM,end=', ')
  print("columns:%d" % rOBJ.columns(), end=', ')
  print("rows:%d"    % rOBJ.rows()             )
  print(styFM % ("Column", "Header", "Type", "TypeString"))
  for ii in range(0, rOBJ.columns()):
    cTP = rOBJ.columnType(ii)
    print(styFM % (ii, rOBJ.header(ii),cTP, dcTyp[cTP]))
showCOL = checkReportStructure
# ---------------------------------------------------

# 感応度分析をシングルカーブにまとめる
def calcSingleGPS(dfSENSI):
	colCAL = {'Delta':'sum', 'Gamma':'sum'}
	dfSENSI['Tenor'] = dfSENSI.Factor_1.str.rsplit('/', n=1).str[-1]
	dfSGL = (dfSENSI.groupby(['Tenor'], as_index=False).agg(colCAL))
	dfSGL = dfSGL.loc[[0,4,1,2,3]].reset_index(drop=True)
	return dfSGL
# ---------------------------------------------------
