import unittest
import parser


class ParserTestCase(unittest.TestCase):
    def test_extract_html_text(self):
        data = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Sample HTML with JavaScript</title>
                </head>
                <body>
                    <h1>JavaScript Example</h1>
                    <script type="text/javascript">
                        // JavaScript code here
                        alert("This is a JavaScript alert!");
                    </script>
                    <a>1234545（123456，1234566）</a>
                    <p class="p1">This is a paragraph with a &nbsp; non-breaking space entity.</p>
                </body>
                </html>
                """
        from lxml.html.clean import clean_html
        # result = clean_html(data)
        data = parser.clean_snapshot(data)
        result = parser.extract_snapshot_text(data)
        print(result)


if __name__ == '__main__':
    unittest.main()
