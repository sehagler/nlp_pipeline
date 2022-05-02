# (c) 2018 Linguamatics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals, print_function

from io import open
import logging
import re
import sys
import unicodecsv as csv
import xml.etree.ElementTree as etree

logging.basicConfig(format='[%(asctime)s.%(msecs)03d]%(levelname)s:%(module)s:%(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S',
                    stream=sys.stderr, level=logging.INFO)

logger = logging.getLogger()


'''
def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Turns I2E XML output '
                                                 '(expanded table) into'
                                                 ' Gold Standard Evaluation'
                                                 ' CSV format.')
    parser.add_argument('xml', help='XML file from I2E')
    parser.add_argument('--no-text-spans', dest='text_spans',
                        action='store_false', default=True,
                        help='flag to ignore text spans highlights '
                             'during evaluation')
    parser.add_argument('--old', default=False, action='store_true',
                        help='flag to produce CSV in old format which '
                             'includes URL and Annotation Type columns')
    parser.add_argument('--outfile', default=None, 
                        help='Name of the output file. If not specified,'
                             'the index name from the xml will be used.')
    
    argv = parser.parse_args()
    return argv
'''


def get_col_ids(xml):
    """
    Args:
        xml: parse xml object

    Returns:
        column_names, query_items. Lists of column names and output columns
        from query items.
    """
    column_names = dict()
    query_items = list()
    # Identify column with doc_ids
    colset = xml.find('.//ColumnSet')
    for col in colset.findall('.//Column'):
        if col.attrib['type'] != 'queryItem':
            key = col.attrib['type']
        else:
            key = col.find('.//Name').text
            if key != 'docId' and '[PT]' not in key:
                query_items.append(key)
        if key != 'docId' and '[PT]' not in key:
            column_names[key] = int(col.attrib['id'])
    return column_names, query_items


def get_hit_highlights(text_in, targets):
    """
    Args:
        text (str): text for hit
        coords (list): tuples with starting and indexes of highlights

    Returns:
        text with added <mark> elements to indicate highlights
    """
    #sorted_coords = sorted(coords, key=lambda x: x[0], reverse=True)
    #prev_coords = (999999, -1)
    text = []
    #for n, coord in enumerate(sorted_coords):
    for target in targets:
        target_in_hit = target[0]
        target_in_text = target[1]
        start = target_in_hit[0]
        stop = target_in_hit[1]
        #if stop > prev_coords[0]:
        #    stop = prev_coords[0]
        #text_tmp = '{}<mark>{}</mark>{}'.format(text_in[:start],
        #                                        text_in[start:stop],
        #                                        text_in[stop:])
        text_tmp = tuple([ target_in_text, text_in[start:stop] ])
        text.append(text_tmp)
        #prev_coords = coord
    return text


'''
def remove_overlaps(spans):
    """
    Merges overlapping spans.

    Args:
        spans (list): list of sorted start-end tuples

    Returns:
        list of start-end tuples without overlaps
    """
    new_spans = list()
    skip_next = 0
    for i in range(len(spans)):
        span_i = spans[i]
        new_end = span_i[1]
        if skip_next:
            skip_next -= 1
            continue
        if i+1 < len(spans) and span_i[1] > spans[i+1][0]:
            new_end = max(span_i[1], new_end)
            for j in range(i+1, len(spans)):
                span_j = spans[j]
                if new_end > span_j[0]:
                    new_end = max(new_end, span_j[1])
                    skip_next += 1
                else:
                    break
            new_span = (span_i[0], new_end)
            new_spans.append(new_span)
        else:
            new_spans.append(span_i)
    return new_spans
'''


def xml_to_gold(xml, text_spans=True, old_format=False):
    """
    Writes gold csv file from i2e xml results.

    Args:
        xml (str): i2e gold query result xml
        text_spans (bool): True if text spans to be considered part of gold
                           evaluation or just presented

    Returns:
        headers, outfile, rows
    """
    logger.info('parsing XML')
    parsed = etree.parse(xml)
    index_name = parsed.find('.//IndexName').text.replace('.i2etmp', '')
    #outfile = '{}.csv'.format(index_name)

    col_to_id, query_cols = get_col_ids(parsed)
    logger.info('query output columns: {}'.format(query_cols))
    logger.info('evaluate text spans: {}'.format(text_spans))
    id_to_col = {v: k for k, v in list(col_to_id.items())}

    #first_cols = ['Doc Id']
    first_cols = []
    #if old_format:
    #    first_cols += ['URL', 'Annotation Type']
    #headers = first_cols + query_cols + ['Coords', 'Text span']
    headers = first_cols + query_cols + ['Coords']
    #headers = first_cols + query_cols + [ 'Coords' ]
    cell_to_colix = {k: headers.index(k) for k in query_cols}
    #cell_to_colix['docId'] = headers.index('Doc Id')
    #cell_to_colix['hit'] = headers.index('Text span')
    cell_to_colix['hit'] = headers.index('Coords')
    if text_spans:
        cell_to_colix['coords'] = headers.index('Coords')
    rows = list()

    for n, rowxml in enumerate(parsed.findall('.//Row')):
        extractions = []
        row = ['' for _ in headers]
        for cell_group in rowxml:
            if cell_group.tag == 'List':
                cells = cell_group.findall('.//Cell')
            else:
                cells = [cell_group]
            for cell in cells:
                cellid = int(cell.attrib['columnId'])
                
                ###
                #colname = id_to_col[cellid]
                if cellid in id_to_col.keys():
                    colname = id_to_col[cellid]
                else:
                    colname = None
                ###
                    
                if colname is not None and colname in cell_to_colix:
                    if colname != 'hit':
                        text = cell.find('.//Text').text
                        if text is not None:
                            if row[cell_to_colix[colname]]:
                                text = ' {}'.format(text)
                                row[cell_to_colix[colname]] += text
                            else:
                                text = text.strip()
                                row[cell_to_colix[colname]] = text
                        else:
                            row[cell_to_colix[colname]] = ''
                        if colname not in [ 'DOCUMENT_ID', 'DATETIME', 'Section Title', 'Speciment Id']:
                            extractions.append(text)
                    else:
                        hit_spans = cell.findall('.//HitSpan')
                        if hit_spans:
                            hit_spans = set(
                                [etree.tostring(h).strip() for h in hit_spans])
                            htext = cell.find('.//Text').text
                            targets = list()
                            #targets_in_hit = list()
                            #targets_in_text = list()
                            for hit_span in hit_spans:
                                hit_span = etree.fromstring(hit_span)
                                is_sent = hit_span.find('.//IsSentence')
                                if is_sent is None:
                                    url = hit_span.find('.//URL').text
                                    target_id = re.search(r"#(.+)", url).group(1)
                                    start = int(target_id.split('-')[1])
                                    hit_len = int(hit_span.find('.//Length').text)
                                    stop = start + hit_len
                                    start_in_hit = int(
                                        hit_span.find('.//Start').text) - 1
                                    stop_in_hit = start_in_hit + hit_len
                                    #if (start_in_hit, stop_in_hit) not in targets_in_hit:
                                    targets_in_hit = (start_in_hit, stop_in_hit)
                                    #if (start, stop) not in targets_in_text:
                                    targets_in_text = (start, stop)
                                    targets.append(tuple([ targets_in_hit,
                                                           targets_in_text ]))
                            #targets = remove_overlaps(sorted(targets))
                            #targets_in_hit = remove_overlaps(sorted(targets_in_hit))
                            #highlighted_span = get_hit_highlights(htext,
                            #                                      targets_in_hit)
                            highlighted_spans = get_hit_highlights(htext,
                                                                   targets)
                            targets = []
                            for i in range(len(extractions)):
                                extraction = extractions[i]
                                highlighted_span_found_flg = False
                                for highlighted_span in highlighted_spans:
                                    if not highlighted_span_found_flg and \
                                       highlighted_span[1] == extraction:
                                        targets.append(highlighted_span[0])
                                        highlighted_span_found_flg = True
                                if not highlighted_span_found_flg:
                                    targets.append('')
                            targets = targets[1:-1]
                            #row_text = '{}'.format(highlighted_spans)
                            #row[cell_to_colix['hit']] = row_text
                            if text_spans:
                                row[cell_to_colix['coords']] = targets
                                #row[cell_to_colix['coords']] = highlighted_spans
                        else:
                            if text_spans:
                                row[cell_to_colix['coords']] = '[]'
                            #row[cell_to_colix['hit']] = ''
        #if old_format:
        #    row[1] = 'no_gold_url'
        #    row[2] = 'Results'
        rows.append(row)

    #return headers, outfile, rows
    return headers, rows


def write_to_file(headers, outfile, rows):
    """

    Args:
        headers (list): file headers
        outfile (str): file path
        rows (list): file rows

    Returns:
        None
    """
    with open(outfile, 'wb') as outf:
        logger.info('written {}'.format(outfile))
        writer = csv.writer(outf, delimiter=str(','), lineterminator='\n')
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
            
            
def generate_gold(inxml, text_spans):
    outcsv = inxml.replace('.xml', '.csv')
    headers, rows = xml_to_gold(inxml, text_spans)
    write_to_file(headers, outcsv, rows)


'''
if __name__ == '__main__':
    args = parse_args()
    inxml = args.xml
    text_spans = args.text_spans
    old_format = args.old
    headers, outfile, rows = xml_to_gold(inxml, text_spans, old_format)
    
    if args.outfile:
        outfile = args.outfile
    
    write_to_file(headers, outfile, rows)
'''
