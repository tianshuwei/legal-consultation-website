import jpype

vmPath = jpype.getDefaultJVMPath()
jpype.startJVM(vmPath, "-Djava.ext.dirs=./org/jodconverter-2.2.2/lib")
Connection = jpype.JPackage('com.artofsolving.jodconverter.openoffice.connection').SocketOpenOfficeConnection
Converter = jpype.JPackage('com.artofsolving.jodconverter.openoffice.converter').OpenOfficeDocumentConverter
File = jpype.java.io.File
FormatRegistry = jpype.JPackage('com.artofsolving.jodconverter').DefaultDocumentFormatRegistry
conn = Connection()
conn.connect()
converter = Converter(conn, FormatRegistry())
converter.convert(File('./tmp/test.docx'), File('./tmp/test.pdf'))
conn.disconnect()
jpype.shutdownJVM()

