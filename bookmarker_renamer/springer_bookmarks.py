__author__ = 'grahamcrowell'
'''
search working directory for *.csv files which it assumes SpringerLink csv Search Results
parses csv file and
builds a html bookmark file
'''

default_folder_size = 5

import os
import itertools
import csv

def user_chooser(choices):
    if len(choices) == 1:
        print('\nASSUMING:')
        print('\t{}'.format(choices[0]))
        return choices[0]
    else:
        opts = list(map(str,choices))
        max_len = max(list(map(len,opts)))
        _format = '{: >'+'{}'.format(len(str(len(choices))))+'s}\t{:'+'{}'.format(max_len)+'s}'
        print('\nCHOOSE:')
        print(_format.format('#','CHOICES'))
        for i,opt in enumerate(opts):
            print(_format.format(str(i+1),opt))
        user = raw_input('USER CHOICE: ')
        if user.isdigit() and int(user) > 0 and int(user) <= len(choices):
            print('\t{} CHOSEN'.format(opts[int(user)-1]))
            return choices[int(user)]
        elif len(user) == 0:
            raw_input('\tALL CHOSEN.  CONFIRM?')
            return choices
        else:
            print('INVALID CHOICE.')
            user_chooser(choices)


def load_csv_dict(index_csv):
    lookup = {}
    with open(index_csv) as csvfile:
        # lines
        reader = csv.DictReader(csvfile)
        for row in reader:
            lookup[row['Item DOI']] = row
    return lookup


def bookmark_line(url, title):
    # return '<DT><A HREF="{}" ADD_DATE="1421998587" LAST_MODIFIED="1421998587">{}</A>\n'.format(url, title)
    return '<DT><A HREF="{}">{}</A>\n'.format(url, title)


# csv_url =
# http://link.springer.com/book/10.1007/978-3-319-00233-0
# csv_doi =
# 10.1007/978-3-319-00233-0
# download_url =
# http://link.springer.com/content/pdf/10.1007%2F978-3-319-00233-0.pdf
# http://link.springer.com.ezproxy.library.ubc.ca/content/pdf/10.1007%2F978-3-642-38091-4.pdf
def get_download_url(doi):
    # return 'http://link.springer.com/content/pdf/' + '{}%2F{}.pdf'.format(*doi.split('/'))
    return 'http://link.springer.com.ezproxy.library.ubc.ca/content/pdf/' + '{}%2F{}.pdf'.format(*doi.split('/'))


def bookmark_html(title, entries):
    html = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <!-- This is an automatically generated file.
         It will be read and overwritten.
         DO NOT EDIT! -->
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    '''
    html += '<TITLE>{}</TITLE>\n<H1>{}</H1>\n\n<DL><p>\n'.format(title,title)
    html += '    <DT><H3 ADD_DATE="1421998587" LAST_MODIFIED="1421998587">{}</H3>\n    <DL><p>\n'.format(title)
    for key, val in entries:
        html += bookmark_line(val['Item Title'], get_download_url(val['Item DOI']))
    html += '    </DL><p>\n</DL>\n'
    return html


def bookmark_folder(title, entries):
    html = ''
    # html += '\t\t<DT><H3 ADD_DATE="1421998587" LAST_MODIFIED="1421998587">{}</H3>\n\t\t<DL><p>\n'.format(title)
    html += '\t\t<DT><H3>{}</H3>\n\t\t<DL><p>\n'.format(title)
    for val in entries:
        html += '\t\t\t'+bookmark_line(get_download_url(val['Item DOI']),val['Item Title'])
    html += '\t\t</DL><p>\n'
    return html


def partitioned_bookmark_html(title, entries, sz=default_folder_size):
    html = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
    It will be read and overwritten.
    DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
'''
    html += '<TITLE>{}</TITLE>\n<H1>{}</H1>\n\n<DL><p>\n'.format(title,title)
    # html += '\t<DT><H3 ADD_DATE="1421998587" LAST_MODIFIED="1421998587">{}</H3>\n    <DL><p>\n'.format(title)
    html += '\t<DT><H3>{}</H3>\n    <DL><p>\n'.format(title)
    entry_list = entries.values()
    cnt = len(entry_list)

    for i in range(0, cnt, sz):
        sub_section = entry_list[i:min(i + sz, cnt)]
        html += bookmark_folder('books {} to {}'.format(i + 1, i + sz), sub_section)

    # html += '    <DT><H3 ADD_DATE="1421998587" LAST_MODIFIED="1421998587">{}</H3>\n    <DL><p>\n'.format(title)
    # for key,val in entries.items():
    #     html += bookmark_line(val['Item Title'], get_download_url(val['Item DOI']))
    # html += '    </DL><p>\n'
    html += '\t</DL><p>\n</DL>\n'
    return html


def make_bookmark_html_file(csv_search_result_files):
    for csv_search_results in csv_search_result_files:
        name = os.path.splitext(csv_search_results)[0]
        csv_dict = load_csv_dict(csv_search_results)
        html = partitioned_bookmark_html(name, csv_dict)
        print('\nWRITING TO HTML BOOKMARK FILE:\n\t{}.html'.format(name))
        with open(name + '.html', 'w') as f:
            f.write(html)


if __name__ == '__main__':
    print('SEARCHING CSV FILES')
    csv_search_result_files = list(itertools.ifilter(lambda filename: os.path.splitext(filename)[1] == '.csv', os.listdir(os.getcwd())))
    print('BUILDING HTML BOOKMARKS FILE')
    csv_search_result = user_chooser(csv_search_result_files)
    make_bookmark_html_file(csv_search_result_files)