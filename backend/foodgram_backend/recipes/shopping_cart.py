from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, ListItem, ListFlowable



def create_pdf_template(buffer, queryset, username):

    pdfmetrics.registerFont(TTFont('Roboto', 'roboto/Roboto-Regular.ttf', 'UTF-8'))
    r = SimpleDocTemplate(buffer, pagesize=A4)
    img = 'media/logo_foodgram.png'
    image = Image(img)
    space_after_logo = Spacer(1, 30)
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        name='HeaderStyle',
        parent=styles['Heading1'],
        fontName='Roboto',
        fontSize=20,
        alignment=1  # Центрирование
    )
    space_after_header = Spacer(1, 30)
    row_style = ParagraphStyle(
        name='RowStyle',
        parent=styles['Normal'],
        fontName='Roboto',
        fontSize=16,
        leading=20,
        wordWrap='CJK'
    )
    header_text = Paragraph(f'Привет, {username}! Список ингредиентов для покупки сформирован.', header_style)
  
    list_ingredients = [image, space_after_logo, header_text, space_after_header]
    list_items = []
    for row in queryset:
        ingredient_row = "{}, {}  -  {}".format(*row.values())
        list_items.append(ListItem(Paragraph(ingredient_row, style=row_style)))

    bullet_list = ListFlowable(list_items, bulletType='bullet'
                               ,bulletFontName='Roboto', bulletFontSize=20, bulletColor='black')
                               
    list_ingredients.append(bullet_list)
    print(list_ingredients)
    r.build(list_ingredients)
    buffer.seek(0)
    return buffer




    
   



