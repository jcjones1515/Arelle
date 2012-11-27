'''
Save SKOS is an example of a plug-in to both GUI menu and command line/web service
that will save the concepts a DTS into an RDF file.

(c) Copyright 2012 Mark V Systems Limited, All rights reserved.
'''

def generateHtmlEbaTablesetFiles(dts, indexFile, lang="en"):
    try:
        if dts.fileSource.isArchive:
            return
        import os, io
        from arelle import Version
        from arelle import XmlUtil, XbrlConst
        from arelle import XmlUtil, XbrlConst
        from arelle.ViewFileRenderedGrid import viewRenderedGrid
        
        numTableFiles = 0
        
        file = io.StringIO('''
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Left">
  <link type="text/css" rel="stylesheet" href="http://www.eba.europa.eu/CMSPages/GetCSS.aspx?stylesheetname=EBA" /> 
  <link type="text/css" rel="stylesheet" href=">http://www.eba.europa.eu/extras.css" />
  <link href=">http://www.eba.europa.eu/CMSPages/GetCSS.aspx?stylesheetname=PrinterFriendlySheet" type="text/css" rel="stylesheet" media="print" />
  <link rel="shortcut icon" href="http://www.eba.europa.eu/favicon.ico" />
  <link rel="icon" href="http://www.eba.europa.eu/favicon.ico" />
</head>
<body class="LTR IE7 ENGB">
    <ul class="CMSListMenuUL" id="Vertical2"/>
</body>
</html>
'''
         )
        from arelle.ModelObjectFactory import parser
        parser, parserLookupName, parserLookupClass = parser(dts,None)
        from lxml import etree
        indexDocument = etree.parse(file,parser=parser,base_url=indexFile)
        file.close()
        #xmlDocument.getroot().init(self)  ## is this needed ??
        for listElt in  indexDocument.iter(tag="{http://www.w3.org/1999/xhtml}ul"):
            break
    
        class nonTkBooleanVar():
            def __init__(self, value=True):
                self.value = value
            def set(self, value):
                self.value = value
            def get(self):
                return self.value
    
        class View():
            def __init__(self, tableOrELR, ignoreDimValidity, xAxisChildrenFirst, yAxisChildrenFirst):
                self.tblELR = tableOrELR
                # context menu boolean vars (non-tkinter boolean
                self.ignoreDimValidity = nonTkBooleanVar(value=ignoreDimValidity)
                self.xAxisChildrenFirst = nonTkBooleanVar(value=xAxisChildrenFirst)
                self.yAxisChildrenFirst = nonTkBooleanVar(value=yAxisChildrenFirst)
    
        indexBase = indexFile.rpartition(".")[0]
    
        modelTables = []
        # order number is missing
        for rel in dts.modelXbrl.relationshipSet(XbrlConst.euGroupTable).modelRelationships:
            modelTables.append((rel.toModelObject, rel.sourceline))
        for modelTable, order in sorted(modelTables, key=lambda x: x[1]):
            # for table file name, use table ELR
            tblFile = os.path.join(os.path.dirname(indexFile), modelTable.id + ".html")
            viewRenderedGrid(dts, tblFile, lang=lang, sourceView=View(modelTable, False, False, True))
            
            # generaate menu entry
            elt = etree.SubElement(listElt, "{http://www.w3.org/1999/xhtml}li")
            elt.set("class", "CMSListMenuLI")
            elt.set("id", modelTable.id)
            elt = etree.SubElement(elt, "{http://www.w3.org/1999/xhtml}a")
            elt.text = modelTable.genLabel(lang=lang, strip=True)
            elt.set("class", "CMSListMenuLink")
            elt.set("href", "javascript:void(0)")
            elt.set("onClick", "javascript:parent.body.location.href='{0}';".format(modelTable.id + ".html"))
            elt.text = modelTable.genLabel(lang=lang, strip=True)
    
        
        with open(indexBase + "FormsFrame.html", "wt", encoding="utf-8") as fh:
            XmlUtil.writexml(fh, indexDocument, encoding="utf-8")
            
        with open(indexFile, "wt", encoding="utf-8") as fh:
            fh.write(
'''
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Head1">
  <title>European Banking Authority - EBA  - FINREP Taxonomy</title>
  <meta name="generator" content="Arelle(r) {0}" /> 
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" /> 
  <meta http-equiv="pragma" content="no-cache" /> 
  <meta http-equiv="content-style-type" content="text/css" /> 
  <meta http-equiv="content-script-type" content="text/javascript" /> 
  <link type="text/css" rel="stylesheet" href="http://www.eba.europa.eu/CMSPages/GetCSS.aspx?stylesheetname=EBA" /> 
  <link type="text/css" rel="stylesheet" href=">http://www.eba.europa.eu/extras.css" />
  <link href=">http://www.eba.europa.eu/CMSPages/GetCSS.aspx?stylesheetname=PrinterFriendlySheet" type="text/css" rel="stylesheet" media="print" />
  <link rel="shortcut icon" href="http://www.eba.europa.eu/favicon.ico" />
  <link rel="icon" href="http://www.eba.europa.eu/favicon.ico" />
</head>
<frameset border="0" frameborder="0" rows="90,*">
   <frame name="head" src="{1}" scrolling="no" marginwidth="0" marginheight="10"/>
   <frameset  bordercolor="#0000cc" border="10" frameborder="no" framespacing="0" cols="360, *">
      <frame src="{2}" name="menu" bordercolor="#0000cc"/>
      <frame src="{3}" name="body" bordercolor="#0000cc"/>
   </frameset>
</frameset>
'''.format(Version.version,
           os.path.basename(indexBase) + "TopFrame.html",
           os.path.basename(indexBase) + "FormsFrame.html",
           os.path.basename(indexBase) + "CenterLanding.html",
           ))
        
        with open(indexBase + "TopFrame.html", "wt", encoding="utf-8") as fh:
            fh.write(
'''
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Top">
  <link type="text/css" rel="stylesheet" href="http://www.eba.europa.eu/CMSPages/GetCSS.aspx?stylesheetname=EBA" /> 
  <link type="text/css" rel="stylesheet" href=">http://www.eba.europa.eu/extras.css" />
  <link href=">http://www.eba.europa.eu/CMSPages/GetCSS.aspx?stylesheetname=PrinterFriendlySheet" type="text/css" rel="stylesheet" media="print" />
  <link rel="shortcut icon" href="http://www.eba.europa.eu/favicon.ico" />
  <link rel="icon" href="http://www.eba.europa.eu/favicon.ico" />
</head>
  <body class="LTR IE7 ENGB">
   <div id="topsection">
      <div id="topsectionLeft" style="cursor:pointer;" onclick="location.href='http://www.eba.europa.eu/home.aspx';"></div>
      <div id="topsectionRight"></div>
      <div id="topnavigation">
      <ul id="menuElem">
        <li><a href="http://www.eba.europa.eu/topnav/Contacts.aspx">Contacts</a></li>
        <li><a href="http://www.eba.europa.eu/topnav/Links.aspx">Links</a></li>
        <li><a href="http://www.eba.europa.eu/topnav/Sitemap.aspx">Sitemap</a></li>
        <li><a href="/topnav/Legal-Notice.aspx">Legal Notice</a></li>
      </ul>
    </div>
  </body>
</html>
''')
        
        with open(indexBase + "CenterLanding.html", "wt", encoding="utf-8") as fh:
            fh.write(
'''
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Center">
  <link type="text/css" rel="stylesheet" href="http://www.eba.europa.eu/CMSPages/GetCSS.aspx?stylesheetname=EBA" /> 
  <link type="text/css" rel="stylesheet" href=">http://www.eba.europa.eu/extras.css" />
  <link href=">http://www.eba.europa.eu/CMSPages/GetCSS.aspx?stylesheetname=PrinterFriendlySheet" type="text/css" rel="stylesheet" media="print" />
  <link rel="shortcut icon" href="http://www.eba.europa.eu/favicon.ico" />
  <link rel="icon" href="http://www.eba.europa.eu/favicon.ico" />
</head>
<body class="LTR IE7 ENGB">
  <div id="plc_lt_zoneContent_usercontrol_userControlElem_ContentPanel">
    <div id="plc_lt_zoneContent_usercontrol_userControlElem_PanelTitle">
      <div id="pagetitle" style="float:left;width:500px;">
        <h1>Taxonomy Tables Viewer</h1>
      </div>
    </div>
  </div>
  <div style="clear:both;"></div>
  <div id="contentcenter">
    <p style="text-align: justify; margin-top: 0pt; margin-bottom: 0pt">Please select tables to view by clicking in the left column.</p>
  </div>
</body>
</html>
''')
        
        
        dts.info("info:saveEBAtables",
                 _("Tables index file of %(entryFile)s has %(numberTableFiles)s table files with index file %(indexFile)s."),
                 modelObject=dts,
                 entryFile=dts.uri, numberTableFiles=numTableFiles, indexFile=indexFile)
    
        dts.modelManager.showStatus(_("Saved EBA HTML Table Files"), 5000)
    except Exception as ex:
        dts.error("exception",
            _("HTML EBA Tableset files generation exception: %(error)s"), error=ex,
            modelXbrl=dts,
            exc_info=True)

def saveHtmlEbaTablesMenuEntender(cntlr, menu):
    # Extend menu with an item for the save infoset plugin
    menu.add_command(label="Save HTML EBA Tables", 
                     underline=0, 
                     command=lambda: saveHtmlEbaTablesMenuCommand(cntlr) )

def saveHtmlEbaTablesMenuCommand(cntlr):
    # save Infoset menu item has been invoked
    from arelle.ModelDocument import Type
    if cntlr.modelManager is None or cntlr.modelManager.modelXbrl is None:
        cntlr.addToLog("No DTS loaded.")
        return

        # get file name into which to save log file while in foreground thread
    indexFile = cntlr.uiFileDialog("save",
            title=_("arelle - Save HTML EBA Tables Index file"),
            initialdir=cntlr.config.setdefault("htmlEbaTablesFileDir","."),
            filetypes=[(_("HTML index file .html"), "*.html")],
            defaultextension=".html")
    if not indexFile:
        return False
    import os
    cntlr.config["htmlEbaTablesFileDir"] = os.path.dirname(indexFile)
    cntlr.saveConfig()

    import threading
    thread = threading.Thread(target=lambda 
                                  _dts=cntlr.modelManager.modelXbrl,
                                  _indexFile=indexFile: 
                                        generateHtmlEbaTablesetFiles(_dts, _indexFile))
    thread.daemon = True
    thread.start()

def saveHtmlEbaTablesCommandLineOptionExtender(parser):
    # extend command line options with a save DTS option
    parser.add_option("--save-EBA-tablesets", 
                      action="store", 
                      dest="ebaTablesetIndexFile", 
                      help=_("Save HTML EBA Tablesets index file, with tablest HTML files to out directory specify 'generateOutFiles'."))

def saveHtmlEbaTablesCommandLineXbrlLoaded(cntlr, options, modelXbrl):
    # extend XBRL-loaded run processing for this option
    from arelle.ModelDocument import Type
    if options.ebaTablesetIndexFile and options.ebaTablesetIndexFile == "generateEBAFiles" and modelXbrl.modelDocument.type in (Type.TESTCASESINDEX, Type.TESTCASE):
        cntlr.modelManager.generateEBAFiles = True

def saveHtmlEbaTablesCommandLineXbrlRun(cntlr, options, modelXbrl):
    # extend XBRL-loaded run processing for this option
    if options.ebaTablesetIndexFile and options.ebaTablesetIndexFile != "generateEBAFiles":
        if cntlr.modelManager is None or cntlr.modelManager.modelXbrl is None:
            cntlr.addToLog("No taxonomy loaded.")
            return
        generateHtmlEbaTablesetFiles(cntlr.modelManager.modelXbrl, options.infosetfile)
        

__pluginInfo__ = {
    'name': 'Save HTML EBA Tables',
    'version': '0.9',
    'description': "This plug-in adds a feature to a directory containing HTML Tablesets with an EBA index page.  ",
    'license': 'Apache-2',
    'author': 'Mark V Systems Limited',
    'copyright': '(c) Copyright 2012 Mark V Systems Limited, All rights reserved.',
    # classes of mount points (required)
    'CntlrWinMain.Menu.Tools': saveHtmlEbaTablesMenuEntender,
    'CntlrCmdLine.Options': saveHtmlEbaTablesCommandLineOptionExtender,
    'CntlrCmdLine.Xbrl.Loaded': saveHtmlEbaTablesCommandLineXbrlLoaded,
    'CntlrCmdLine.Xbrl.Run': saveHtmlEbaTablesCommandLineXbrlRun,
}