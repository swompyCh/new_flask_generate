from docxtpl import DocxTemplate
from docx2pdf import convert
from zipfile import ZipFile


def dogovor(choose, fio, fio2, klass, programa, direction, date3, telephone2, telephone):
    f = fio2.split("\r\n")
    zipObj = ZipFile('dogovor.zip', 'w')
    print(f)
    if choose == "s_14":
        for person in f:
            doc = DocxTemplate("Zayavlenia_s_14_let.docx")
            context = {'fio': fio, 'fio2': fio2.rstrip(), 'klass': klass, 'programa': programa, 'direction': direction, 'date3': date3, 'telephone2': telephone2, 'telephone': telephone, }
            doc.render(context)
            doc.save("{}_dogovor_s_14.docx".format(person.rstrip()))
            convert("{}_dogovor_s_14.docx".format(person.rstrip()))
            zipObj.write('{}_dogovor_s_14.pdf'.format(person.rstrip()))
        else:
            for person in f:
                doc = DocxTemplate("zayavlenie_do_14_let_novaya_forma.docx")
                context = {'fio': fio, 'fio2': fio2.rstrip(), 'klass': klass, 'programa': programa, 'direction': direction, 'date3': date3, 'telephone2': telephone2, 'telephone': telephone, }
                doc.render(context)
                doc.save("{}_dogovor_do_14.docx".format(person.rstrip()))
                convert("{}_dogovor_do_14.docx".format(person.rstrip()))
                zipObj.write('{}_dogovor_do_14.pdf'.format(person.rstrip()))
