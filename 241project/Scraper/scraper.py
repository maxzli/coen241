from lxml import html
from lxml import etree
from .contents import parsecontent
from .toc import menu
import requests
import re
import boto3
import json

"""
Retrieves the HTML from a webpage for processing.

Uses:
contents.py for parsing the data of the webpage
toc.py for parsing the menu actions of the webpage
login.py for parsing possible login forms from the webpage
images.py for parsing the most relevant image from the webpage

Passes back an array of two elements:
0 -> string representing the data of the webpage
1 -> an array of tuples representing possible menu actions
2 -> an optional relevant image
"""
def navigate(url):
    try:
        page = requests.get(url)
    except:
        return 404
    #print(page.status_code)
    #print(page.headers['content-type'])
    #print(page.encoding)

    if (page.status_code == 200):
        tree = html.fromstring(page.content)

        for head in tree.xpath('//head'):
            head.getparent().remove(head)

        for script in tree.xpath('//script'):
            script.getparent().remove(script)

        for style in tree.xpath('//style'):
            style.getparent().remove(style)

        for pre in tree.xpath('//pre'):
            pre.getparent().remove(pre)

        for code in tree.xpath('//code'):
            code.getparent().remove(code)

        for aside in tree.xpath('//aside'):
            aside.getparent().remove(aside)

        ##print(etree.tostring(tree, pretty_print=True))

        # Generate table of contents
        parsed_menu = menu(tree, url)


        # Generate contents from cleaned tree
        parsed_webpage_data = parsecontent(tree)[1]


        lambda_client = boto3.client('lambda')
        lambda_dict = {'content': parsed_webpage_data}
        result = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-2:612568176270:function:preprocessing',
            InvocationType='RequestResponse',
            Payload=json.dumps(lambda_dict).encode('utf-8')
        )
        processed_data = json.loads(result['Payload'].read().decode())

        if len(processed_data) > 1250:
            processed_data = processed_data[:1247] + '...'

        re.sub(r'[^\x00-\x7F]+', '', processed_data)

        parsed_image = None
        #parsed_image = None

        return [processed_data, parsed_menu, parsed_image];

    else:
        return page.status_code

if (__name__ == '__main__'):
    data = navigate('http://www.wikipedia.org/wiki/elizabeth_ii')
    print(data[0])
