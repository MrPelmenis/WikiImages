import requests

def get_wikipedia_image_url(title=None, pageid=None):
    params = {
        'action': 'query',
        'format': 'xml',
        'prop': 'pageimages',
        'piprop': 'original',
        'pilicense': 'any'       # allow non-free images if needed
    }
    if title:
        params['titles'] = title
    elif pageid:
        params['pageids'] = str(pageid)
    else:
        return None
    response = requests.get('https://en.wikipedia.org/w/api.php', params=params)
    xml = response.text
    # Parse XML to extract <original> tag's source attribute
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    orig = root.find('.//original')
    if orig is not None:
        return orig.get('source')
    return None