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
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        form = cgi.FieldStorage(self.rfile, self.headers, environ={'REQUEST_METHOD': 'POST'})
        query = str(form.getvalue('query'))

        indexing = search.indexer.Indexer('database')

        indexing.indexing_with_lines('text.txt')
        searching = search.SearchEngine('database')
        result = searching.search_to_context(query)
        print(result)
        del searching

        request_val = self.get_list(result)
        self.wfile.write(bytes('''
            <html>
                <body>
                    <form method = 'post'>
                        <input type = 'text' name = 'query' value = ''' + query + '''>
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
            answer_ord_list += '<li> <p> ' + cur_file + ' </p> </li> ' + '<ul>'
            for cur_cit in dict_to_htmllist[cur_file]:
                answer_ord_list += '<li> <p> ' + str(cur_cit) + ' </p> </li> '
            answer_ord_list += '</ul> '
        answer_ord_list += '</ol>'
        return answer_ord_list


def main():
    server = http.HTTPServer(('localhost', 8000), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
