import arcpy
import os
import csv

aprx = arcpy.mp.ArcGISProject("CURRENT")
outpath = arcpy.GetParameterAsText(0)
inputFile = arcpy.GetParameterAsText(1)
export_type = arcpy.GetParameterAsText(2)

f = open(inputFile, 'r', encoding='utf-8', errors='replace')
cursor = csv.reader(f)

display = aprx.listMaps("Main Map")[0]
overview = aprx.listMaps("OverviewMap")[0]
govt = overview.listLayers("Governorate boundary focus")[0]
dist_labels = display.listLayers("District boundary labels")[0]

l = aprx.listLayouts()[0]
ms = l.mapSeries
firstline = True
for row in cursor:
    if firstline:
        firstline = False
        continue
    siteGov = row[4]
    admin1 = row[5]
    for t in os.listdir(outpath):
        if siteGov in t:
            arcpy.AddMessage("Already exported!")
            break
    else:
        pageNum = ms.getPageNumberFromName(siteGov)
        ms.currentPageNumber = pageNum
        mapName = ms.pageRow.governorate_name
        mapCode = ms.pageRow.governorate_pcode
        govPcode = ms.pageRow.governorate_pcode
        arcpy.AddMessage("Governorate: %s" % str(govPcode))
        g_query = "admin1pcod = \'" + govPcode + "'"
        govt.definitionQuery = g_query
        dist_labels.definitionQuery = g_query
        if export_type == "PDF":
            outputName = os.path.join(outpath, "YEM_CCCM_")
            ms.exportToPDF(outputName, "CURRENT", multiple_files="PDF_MULTIPLE_FILES_PAGE_NAME", resolution=300)
        else:
            outputName = os.path.join(outpath, "YEM_CCCM" + "_" + siteGov + ".png")
        l.exportToPNG(outputName, resolution=300)
f.close()
