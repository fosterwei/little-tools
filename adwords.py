#coding:utf-8
#!/usr/bin/python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example retrieves keywords that are related to a given keyword.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

import gevent
from gevent import monkey
monkey.patch_all()

import io
import argparse
from os.path import realpath, dirname, join
from googleads import adwords


PAGE_SIZE = 100
client = None
lang_maps = {
    'en': '1000',
    'hi': '1023',
    'id': '1025',
}


def search(query, lang):
    global client
    # Initialize appropriate service.
    targeting_idea_service = client.GetService('TargetingIdeaService', version='v201609')

    results = []

    # Construct selector object and retrieve related keywords.
    offset = 0
    selector = {
        'searchParameters': [
            {
                'xsi_type': 'RelatedToQuerySearchParameter',
                'queries': [query],
            },
            {
                # Language setting (optional).
                # The ID can be found in the documentation:
                # MOE:begin_strip
                # pylint: disable=line-too-long
                # MOE:end_strip
                # https://developers.google.com/adwords/api/docs/appendix/languagecodes
                # English: 1000
                # Hindi: 1023
                # Indonesian: 1025
                'xsi_type': 'LanguageSearchParameter',
                'languages': [{'id': lang}]
            },
            {
                # Network search parameter (optional)
                'xsi_type': 'NetworkSearchParameter',
                'networkSetting': {
                    'targetGoogleSearch': True,
                    'targetSearchNetwork': False,
                    'targetContentNetwork': False,
                    'targetPartnerSearchNetwork': False
                }
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'requestedAttributeTypes': [
            'KEYWORD_TEXT',
            'SEARCH_VOLUME',
            'CATEGORY_PRODUCTS_AND_SERVICES'
        ],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(PAGE_SIZE)
        }
    }
    more_pages = True
    while more_pages:
        page = targeting_idea_service.get(selector)
        # Display results.
        if 'entries' in page:
            for entry in page['entries']:
                for data in entry.data:
                    if data.key == 'KEYWORD_TEXT':
                        new_keyword = data.value.value
                    elif data.key == 'SEARCH_VOLUME':
                        vol = data.value.value
                results.append((new_keyword, vol))
        else:
            print 'No related keywords were found.'
        offset += PAGE_SIZE
        selector['paging']['startIndex'] = str(offset)
        more_pages = offset < int(page['totalNumEntries'])

    #  print u'Number of related keywords of {0}: {1}'.format(query, len(results))
    return query, results


def read(fin):
    for line in fin:
        query = line.strip()
        yield query


def output(fh, query, results):
    for keyword, vol in results:
        fh.write(u'{0}\t{1}\t{2}\n'.format(query, keyword, vol))


def main():
    global client
    
    parser = argparse.ArgumentParser()
    parser.add_argument('inpath', help='Path to seed words')
    parser.add_argument('outpath', help='Path to output related words')
    parser.add_argument('lang', help='Language of seed words', choices=['en', 'hi', 'id'])
    parser.add_argument('--config',
                        help='Yaml file of Google AdWords tokens',
                        default=join(dirname(__file__), 'googleads.yaml'))
    parser.add_argument('--timeout', help='Timeout of gevent',
                        type=int, default=60)
    args = parser.parse_args()

    client = adwords.AdWordsClient.LoadFromStorage(args.config)

    with io.open(realpath(args.inpath), 'r', encoding='utf8') as fin,\
            io.open(realpath(args.outpath), 'w', encoding='utf8', errors='ignore') as fh:
        lang = lang_maps[args.lang]
        queries = []

        for line in fin:
            query = line.strip()
            queries.append(query)

        start = 0
        while start < len(queries):
            length = min(10, len(queries) - start)
            subqueries = queries[start: start + length]
            jobs = [gevent.spawn(search, q, lang) for q in subqueries]
            gevent.joinall(jobs, timeout=args.timeout)
            for job in jobs:
                query, results = job.value
                if results:
                    output(fh, query, results)
            start += length
            print 'Processed {0} queries'.format(start + length)


if __name__ == '__main__':
    main()
