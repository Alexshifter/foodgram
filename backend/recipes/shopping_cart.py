from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, ListFlowable, ListItem, Paragraph,
                                SimpleDocTemplate, Spacer)

from foodgram_backend.settings import MEDIA_ROOT


def create_pdf_template(buffer, queryset, username):

    """Формирование списка покупок в формате *.pdf"""

    pdfmetrics.registerFont(TTFont(
        'Roboto', MEDIA_ROOT / 'fonts/Roboto-Regular.ttf', 'UTF-8'
    ))
    pdf_template = SimpleDocTemplate(buffer, pagesize=A4)
    logo = Image(MEDIA_ROOT / 'logo_foodgram.png', width=159, height=43)
    space_after_logo = Spacer(1, 30)
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        name='HeaderStyle',
        parent=styles['Heading1'],
        fontName='Roboto',
        fontSize=18,
        alignment=1
    )
    row_style = ParagraphStyle(
        name='RowStyle',
        parent=styles['Normal'],
        fontName='Roboto',
        fontSize=16,
        leading=20,
        wordWrap='CJK'
    )
    header_text = Paragraph(
        f'Привет, {username}! Список ингредиентов для покупки сформирован.',
        header_style
    )
    space_after_header = Spacer(1, 30)
    result_data = [logo, space_after_logo, header_text, space_after_header]
    list_items = []
    for row in queryset:
        ingredient_row = "{}, {}  -  {}".format(*row.values())
        list_items.append(ListItem(Paragraph(ingredient_row, style=row_style)))
    bullet_list = ListFlowable(list_items,
                               bulletType='bullet',
                               bulletFontName='Roboto',
                               bulletFontSize=20, bulletColor='black')

    result_data.append(bullet_list)

    pdf_template.build(result_data)
    buffer.seek(0)
    return buffer
