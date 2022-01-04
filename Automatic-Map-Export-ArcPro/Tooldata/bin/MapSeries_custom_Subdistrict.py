import arcpy
import os
import csv

aprx = arcpy.mp.ArcGISProject("CURRENT")
outpath = arcpy.GetParameterAsText(0)
inputFile = arcpy.GetParameterAsText(1)
export_type = arcpy.GetParameterAsText(2)

f = open(inputFile, 'r', encoding='utf-8', errors='replace')
cursor = csv.reader(f)

display = aprx.listMaps("Map")[0]
overview = aprx.listMaps("OverviewMap")[0]
govt = overview.listLayers("District boundary")[0]
subdist = overview.listLayers("Subdistrict boundary")[0]
subdist_display = display.listLayers("Subdistrict boundary surrounding")[0]
l = aprx.listLayouts()[0]
ms = l.mapSeries
firstline = True
for row in cursor:
    if firstline:
        firstline = False
        continue
    siteLoc = row[10]
    admin3 = row[9]
    pageNum = ms.getPageNumberFromName(admin3)

    ms.currentPageNumber = pageNum
    mapName = ms.pageRow.admin2name
    mapCode = ms.pageRow.admin2pcod
    govPcode = ms.pageRow.admin1pcod
    arcpy.AddMessage("Sub-district: %s" % str(mapName))
    arcpy.AddMessage("Governorate: %s" % str(govPcode))
    g_query = "admin1pcod = \'" + govPcode + "'"
    s_query = "admin2pcod = \'" + mapCode + "'"
    s_query2 = "admin2pcod <> \'" + mapCode + "'"
    govt.definitionQuery = g_query
    subdist.definitionQuery = s_query
    subdist_display.definitionQuery = s_query2
    mf = l.listElements('MAPFRAME_ELEMENT', "Overview Frame")[0]
    mf.camera.setExtent(mf.getLayerExtent(govt, False, True))
    if export_type == "PDF":
        outputName = os.path.join(outpath, "YEM_CCCM_" + siteLoc + "_")
        ms.exportToPDF(outputName, "CURRENT", multiple_files="PDF_MULTIPLE_FILES_PAGE_NAME", resolution=300)
    else:
        outputName = os.path.join(outpath, siteLoc + ".png")
        l.exportToPNG(outputName, resolution=300)
