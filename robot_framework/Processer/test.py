"""Test enkelte funktioner og simple metoder"""
from robot_framework.Processer.Fileconvert.docx_to_pdf import docx_to_pdf
from robot_framework.Processer.Fileconvert.msg_to_pdf import msg_to_pdf

wordfil = r"\\srvsql46\INDBAKKE\AAK_Aktindsigt\Testfiler\Testfil med LoremIpsum og billeder.docx"
# msgfil = r"\\srvsql46\INDBAKKE\AAK_Aktindsigt\Testfiler\3 ekstraordinære tilbud venter på dig! .msg"
msgfil = r"\\srvsql46\INDBAKKE\AAK_Aktindsigt\Testfiler\Test 01.msg"

# docx_to_pdf(wordfil)
msg_to_pdf(msgfil)
