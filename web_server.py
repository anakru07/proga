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
                        <input type = 'submit' name = 'search'>
                        <br>
                        <br>
                        <input type = 'number' name = 'offset' placeholder = 'offset'>
                        <br>
                        <br>
                        <label for="limit"> show <input type="number" name="limit"> documents on a page </label> 
                    </form>
                </body>
            </html>
            ''', encoding='UTF-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        form = cgi.FieldStorage(self.rfile, self.headers, environ={'REQUEST_METHOD': 'POST'})
        query = str(form.getvalue('query'))
        offset = int(form.getvalue('offset'))
        limit = int(form.getvalue('limit'))

        indexing = search.indexer.Indexer('database')

        indexing.indexing_with_lines('text.txt')
        searching = search.SearchEngine('database')
        result = searching.search_to_context(query)
        del searching

        self.items = list(result.items())
        self.cur_item = offset
        action = form.getvalue('action')
        if action == 'Next' and self.cur_item < len(self.items):
            self.cur_item += limit
        elif action == 'Prev' and self.cur_item > 0:
            self.cur_item -= limit
        elif action == 'First page':
            self.cur_item = 0

        self.wfile.write(bytes('''
            <html>
                <body>
                    <form method = 'post'>
                        <input type = 'text' name = 'query' value = {query}>
                        <input type = 'submit' name = 'search'>
                        <br>
                        <br>
                        <input type = 'number' name = 'offset' value = {offset}>
                        <br>
                        <br>
                        <label for="limit"> 
                        show <input type="number" name="limit" value = {limit}> documents on a page 
                        </label> 
                        <br>
                        <br>
                        <input type="submit" name="action%d" value="Previous" %s/>
                        <input type="submit" name="action%d" value="To the beginning" %s/>
                        <input type="submit" name="action%d" value="Next" %s/>
                    </form>
                </body>
            </html>
            '''.format(query=query, offset=offset, limit=limit), encoding='UTF-8'))
        if self.cur_item >= len(self.items):
            self.wfile.write(bytes('Offset is bigger than the number of results', encoding='UTF-8'))
        else:
            cur_limit = self.cur_item
            while self.cur_item < cur_limit and self.cur_item < len(self.items):
                self.wfile.write(bytes(self.get_doc(self.items[self.cur_item][0], self.items[self.cur_item][1]), encoding='UTF-8'))
                self.cur_item += 1

    def get_list(self, dict_to_htmllist):
        answer_ord_list = '<ol> '
        for cur_file in dict_to_htmllist:
            answer_ord_list += self.get_doc(cur_file, dict_to_htmllist[cur_file])
        answer_ord_list += '</ol>'
        return answer_ord_list

    @staticmethod
    def get_doc(name: str, cur_file: list):
        answer_ord_list = '<ol> '
        answer_ord_list += '<li> <p> ' + name + ' </p> </li> ' + '<ul>'
        for cur_cit in cur_file:
            answer_ord_list += '<li> <p> ' + str(cur_cit) + ' </p> </li> '
        answer_ord_list += '</ul> '
        answer_ord_list += '</ol>'
        return answer_ord_list


def main():
    server = http.HTTPServer(('localhost', 8000), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
