#! /usr/bin/env py.test

from mwlib import metabook
print metabook.__dict__

test_wikitext1 = '''== Title ==
=== Subtitle ===
{{Template}}

Summary line 1
Summary line 2

;Chapter 1
:[[Article 1]]
:[[:Article 2]]

;Chapter 2
:[[Article 3|Display Title 1]]
:[{{fullurl:Article 4|oldid=4}}Display Title 2]

'''

test_wikitext2 = '''== Title ==
=== Subtitle ===
{{
Template
}}

Summary line 1
Summary line 2

;Chapter 1
:[[Article 1]]
:[[:Article 2]]

;Chapter 2
:[[Article 3|Display Title 1]]
:[{{fullurl:Article 4|oldid=4}}Display Title 2]

'''

test_metabook = {
    'type': 'collection',
    'version': metabook.METABOOK_VERSION,
    'items': [
        {
            'type': 'chapter',
            'title': 'Chapter 1',
            'items': [
                {
                    'type': 'article',
                    'title': 'Article 1',
                    'content-type': 'text/x-wiki',
                },
                {
                    'type': 'article',
                    'title': 'Article 2',
                    'content-type': 'text/x-wiki',
                },
            ],
        },
        {
            'type': 'chapter',
            'title': 'Chapter 2',
            'items': [
                {
                    'type': 'article',
                    'title': 'Article 3',
                    'displaytitle': 'Display Title',
                    'content-type': 'text/x-wiki',
                },
            ],
        },
    ],
}

def test_parse_collection_page():
    #first parsestring
    mb = metabook.parse_collection_page(test_wikitext1)
    assert mb['type'] == 'collection'
    assert mb['version'] == metabook.METABOOK_VERSION
    assert mb['title'] == 'Title'
    assert mb['subtitle'] == 'Subtitle'
    assert mb['summary'] == 'Summary line 1 Summary line 2 '
    items = mb['items']
    assert len(items) == 2
    assert items[0]['type'] == 'chapter'
    assert items[0]['title'] == 'Chapter 1'
    arts = items[0]['items']
    assert len(arts) == 2
    assert arts[0]['type'] == 'article'
    assert arts[0]['title'] == 'Article 1'
    assert arts[1]['type'] == 'article'
    assert arts[1]['title'] == 'Article 2'
    assert items[1]['type'] == 'chapter'
    assert items[1]['title'] == 'Chapter 2'
    arts = items[1]['items']
    assert len(arts) == 2
    assert arts[0]['type'] == 'article'
    assert arts[0]['title'] == 'Article 3'
    assert arts[0]['displaytitle'] == 'Display Title 1'
    assert arts[1]['title'] == 'Article 4'
    assert arts[1]['revision'] == '4'
    assert arts[1]['displaytitle'] == 'Display Title 2'
    
    #second parsestring
    mb = metabook.parse_collection_page(test_wikitext2)
    assert mb['type'] == 'collection'
    assert mb['version'] == metabook.METABOOK_VERSION
    assert mb['title'] == 'Title'
    assert mb['subtitle'] == 'Subtitle'
    assert mb['summary'] == 'Summary line 1 Summary line 2 '
    items = mb['items']
    assert len(items) == 2
    assert items[0]['type'] == 'chapter'
    assert items[0]['title'] == 'Chapter 1'
    arts = items[0]['items']
    assert len(arts) == 2
    assert arts[0]['type'] == 'article'
    assert arts[0]['title'] == 'Article 1'
    assert arts[1]['type'] == 'article'
    assert arts[1]['title'] == 'Article 2'
    assert items[1]['type'] == 'chapter'
    assert items[1]['title'] == 'Chapter 2'
    arts = items[1]['items']
    assert len(arts) == 2
    assert arts[0]['type'] == 'article'
    assert arts[0]['title'] == 'Article 3'
    assert arts[0]['displaytitle'] == 'Display Title 1'
    assert arts[1]['title'] == 'Article 4'
    assert arts[1]['revision'] == '4'
    assert arts[1]['displaytitle'] == 'Display Title 2'

def test_get_item_list():
    expected = [
        {
            'type': 'chapter',
            'title': 'Chapter 1',
        },
        {
            'type': 'article',
            'title': 'Article 1',
        },
        {
            'type': 'article',
            'title': 'Article 2',
        },
        {
            'type': 'chapter',
            'title': 'Chapter 2',
        },
        {
            'type': 'article',
            'title': 'Article 3',
        },
    ]
    
    result = metabook.get_item_list(test_metabook)
    assert len(result) == len(expected)
    for e, r in zip(expected, result):
        assert e['type'] == r['type']
        assert e['title'] == r['title']
    
    expected = [
        {
            'type': 'article',
            'title': 'Article 1',
        },
        {
            'type': 'article',
            'title': 'Article 2',
        },
        {
            'type': 'article',
            'title': 'Article 3',
        },
    ]
    result = metabook.get_item_list(test_metabook, filter_type='article')
    assert len(result) == len(expected)
    for e, r in zip(expected, result):
        assert e['type'] == r['type']
        assert e['title'] == r['title']

