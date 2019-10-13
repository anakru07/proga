import http.server as http
import cgi
import search_engine as search


class RequestHandler(http.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes('''
            <html>
                <body>
                    <form method = 'post'>
                        <input type = 'text' name = 'query'>
                        <input type = 'submit'>
                    </form>
                </body>
            </html>
            ''',
                               encoding='UTF-8'))

    def do_POST(self):
        form = cgi.FieldStorage(self.rfile, self.headers, environ={'REQUEST_METHOD': 'POST'})
        query = str(form.getvalue('query'))

        indexing = search.indexer.Indexer('database')
        with open('text.txt', 'w') as test_file_1:
            test_file_1.write('The class . 10 English paper .was conducted from 10:30 am to 01')

        indexing.indexing_with_lines('text.txt')
        searching = search.SearchEngine('database')
        result = searching.search_to_sentence(query, 6)
        del searching

        request_val = self.get_list(result)
        self.wfile.write(bytes(f'''
            <html>
                <body>
                    <form method = 'post'>
                        <input type = 'text' name = 'query' value = {query}>
                        <input type = 'submit'>
                    </form>
                </body>
            </html>
            ''',
                               encoding='UTF-8'))
        self.wfile.write(bytes(request_val, encoding='UTF-8'))

    @staticmethod
    def get_list(dict_to_htmllist):
        answer_ord_list = '<ol> '
        for cur_file in dict_to_htmllist:
            answer_ord_list += '<li> <p> ' + cur_file + ' </p> </li> '
            for cur_cit in dict_to_htmllist[cur_file]:
                answer_ord_list += '<ul> <li> <p> ' + cur_cit.line + ' </p> </li> '
            answer_ord_list += '</ul> '
        answer_ord_list += '</ol>'
        print(answer_ord_list)
        return answer_ord_list


def main():
    server = http.HTTPServer(('localhost', 80), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
