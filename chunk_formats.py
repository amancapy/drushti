formats = {
    'document': {
        'params': {
            'left_margin': 1440,
            'right_margin': 1440,
            'header_': 1440,
            'top_': 1979,
            'footer_': 1440,
            'bottom_': 1979,
            'line_pitch': 100
        },

        'body': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" mc:Ignorable="w14 wp14 w15"><w:body>'
                '\nparagraphs_here\n'
                '<w:sectPr><w:headerReference w:type="default" r:id="rId2"/><w:footerReference w:type="default" r:id="rId3"/><w:type w:val="nextPage"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:left="1440" w:right="1440" w:gutter="0" w:header="1440" w:top="1979" w:footer="1440" w:bottom="1979"/><w:pgNumType w:fmt="decimal"/><w:formProt w:val="false"/><w:textDirection w:val="lrTb"/><w:docGrid w:type="default" w:linePitch="100" w:charSpace="0"/></w:sectPr></w:body></w:document>'
    },

    'paragraph': {
        'params': {
            'paragraph_style': 'Normal',
            'spacing_before': 480,
            'spacing_after': 0,
            'font_name': 'Gautami',
            'font_size': 40,
        },

        'body': '<w:p>\n'
                '<w:pPr>\n'
                '<w:pStyle w:val="paragraph_style"/>'
                '<w:spacing w:before="0" w:after="0"/>'
                '<w:rFonts w:ascii="font_name" w:hAnsi="font_name"/>'
                '</w:pPr>'
                'word_here'
                '</w:p>\n\n'
    },

    'word': {
        'params': {
            'bold': '<w:b/><w:b/><w:bCs/>',
            'italics': '<w:i/><w:i/><w:iCs/>',
            'underline': '<w:u w:val="single"/>',
            'strikethrough': '<w:strike/>'
        },

        'body': '<w:r>'
                '<w:rPr>'
                '<w:rFonts w:cs="font_name"/>'
                'bold'
                'italics'
                'strikethrough'
                ''
                '<w:sz w:val="font_size"/><w:sz w:val="font_size"/><w:szCs w:val="font_size"/>'
                'underline'
                '</w:rPr>'
                '<w:t>text_here</w:t>'
                '</w:r>'
    }
}