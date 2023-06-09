fonts = ["Baloo Tammudu 2", "Baloo Tammudu", "GIST-TLOTChandana", "Dhurjati", "GIST-TLOTDraupadi", "Gautami", "Gidugu",
         "Gurajada", "GIST-TLOTKrishna", "Lakki Reddy", "Lohit Telugu", "Mallanna", "Mandali", "GIST-TLOTMenaka", "NTR",
         "GIST-TLOTPavani", "Peddanna", "Pothana2000", "GIST-TLOTRajani", "Ramabhadra", "RamaneeyaWin", "Ramaraja",
         "Ravi Prakash", "GIST-TLOTSitara", "Sree Krushnadevaraya", "Suranna", "GIST-TLOTSwami", "Tenali Ramakrishna",
         "Timmana", "Vemana2000", "GIST-TLOTVennela"]


formats = {
    'document': {
        'params': {
            'left_margin': range(900, 1500),
            'right_margin': range(900, 1500),
            'header_': range(900, 1500),
            'top_': range(1800, 2200),
            'footer_': range(900, 1500),
            'bottom_': range(1800, 2200),
            'line_pitch': range(0, 150),
            'page_w': range(12000, 16000),
            'page_h': range(17000, 21000),
            'header_margin': range(900, 1600),
            'char_space': range(0, 100),
            'gutter_': range(0, 100)
        },

        'body': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document '
                'xmlns:o="urn:schemas-microsoft-com:office:office" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:v="urn:schemas-microsoft-com:vml" '
                'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:w10="urn:schemas-microsoft-com:office:word" '
                'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
                'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
                'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
                'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
                'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
                'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
                'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" mc:Ignorable="w14 wp14 w15"><w:body>'
                '\nparagraphs_here\n'
                '<w:sectPr><w:headerReference w:type="default" r:id="rId2"/><w:footerReference w:type="default" '
                'r:id="rId3"/><w:type w:val="nextPage"/><w:pgSz w:w="page_w" w:h="page_h"/><w:pgMar w:left="left_margin" '
                'w:right="right_margin" w:gutter="gutter_" w:header="header_" w:top="top_" w:footer="footer_" '
                'w:bottom="bottom_"/><w:pgNumType w:fmt="decimal"/><w:formProt w:val="false"/><w:textDirection '
                'w:val="lrTb"/><w:docGrid w:type="default" w:linePitch="line_pitch" '
                'w:charSpace="char_space"/></w:sectPr></w:body></w:document>'
    },

    'paragraph': {
        'params': {
            'paragraph_style': ['Normal'],
            'spacing_before': range(350, 550),
            'spacing_after': range(0, 100),
            'font_name': fonts,
            'font_size': range(35, 45),
            'align': [*["left"] * 4, *["center"]*3, *["right"]*1, *["both"]*4]
        },

        'body': '<w:p>\n'
                '<w:pPr>\n'
                '<w:pStyle w:val="paragraph_style"/>'
                '<w:spacing w:before="0" w:after="0"/>'
                '<w:jc w:val="align"/>'
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
                '<w:sz w:val="font_size"/><w:sz w:val="font_size"/><w:szCs w:val="font_size"/>'
                'underline'
                '</w:rPr>'
                '<w:t xml:space="preserve">text_here</w:t>'
                '</w:r>',

        'space': '<w:t xml:space="preserve">'
    },

    'header': {
        'params': {
            'font_name': fonts,
            'font_size': range(15, 30),
        },

        'body': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr '
                'xmlns:o="urn:schemas-microsoft-com:office:office" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:v="urn:schemas-microsoft-com:vml" '
                'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:w10="urn:schemas-microsoft-com:office:word" '
                'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
                'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
                'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
                'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
                'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
                'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
                'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" mc:Ignorable="w14 wp14 '
                'w15"><w:p><w:pPr><w:pStyle w:val="Header"/><w:rPr><w:rFonts w:ascii="font_name" w:hAnsi="font_name" '
                'w:cs="font_name"/><w:sz w:val="font_size"/><w:szCs w:val="font_size"/></w:rPr></w:pPr>'
                '\nheader_here\n'
                '</w:p></w:hdr>',

        'tab': '<w:r><w:rPr><w:rFonts w:cs="font_name" w:ascii="font_name" w:hAnsi="font_name"/><w:sz '
               'w:val="font_size"/><w:szCs w:val="font_size"/></w:rPr><w:tab/></w:r>'
    },

    'footer': {
        'params': {
            'font_name': fonts,
            'font_size': range(15, 30),
        },

        'body': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr '
                'xmlns:o="urn:schemas-microsoft-com:office:office" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:v="urn:schemas-microsoft-com:vml" '
                'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                'xmlns:w10="urn:schemas-microsoft-com:office:word" '
                'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
                'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
                'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
                'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
                'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
                'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
                'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" mc:Ignorable="w14 wp14 '
                'w15"><w:p><w:pPr><w:pStyle w:val="Footer"/><w:rPr><w:rFonts w:ascii="font_name" w:hAnsi="font_name" '
                'w:cs="font_name"/><w:sz w:val="font_size"/><w:szCs w:val="font_size"/></w:rPr></w:pPr>'
                '\nfooter_here\n'
                '</w:p></w:ftr>',

        'tab': '<w:r><w:rPr><w:rFonts w:cs="font_name" w:ascii="font_name" w:hAnsi="font_name"/><w:sz '
               'w:val="font_size"/><w:szCs w:val="font_size"/></w:rPr><w:tab/></w:r>'
    }
}
