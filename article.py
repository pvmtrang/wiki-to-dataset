#input: pages-articals.xml, a wiki dump of all articles with their full contents and config(id, revision, creator...)
#1. Parse into pages. Dictionary?? [article name]: content of <title>, <text>, the loai
#2. Parse page contents -> sentences. Remove components? table, image, outgoing links - chú thích, markup
#??? nhung ma readline anyway??? parse all -> sentences? NO -> parse by articles first -> propagate links??
# 2 maps: article_id - article_name. article_id-all sentences??
# or: article_name-count of all sentences. list of all sentences??
#also need somewhere to store the type of articles

import config

def convert_wikidump_to_articles():
    article_title_text = {} #format: 'title':'text'
    articles = {
        'id':[],
        'title':[],
        'redirect_title':[],
        'text':[]
    } #all str, ofc
    current_id = ''
    current_title = ''
    current_redirect_title = ''
    current_page_text = ''
    page_start = False
    current_page_text_start = False
    current_table_start = False



    with open(config.DATA_PATH, encoding='utf-8') as file: #chua filter data
        for line in file:
            line = line.strip()
            if line == '':
                continue
            if line.startswith("<page"): #reset saved data for each page
                # page_start = True
                current_page_text_start = False
                # current_table_start = False
                current_title = ''
                current_page_text = ''
                # print("page starts")
            elif line.startswith("<title"):
                if current_title == '' and line.endswith('/title>'): #make sure title on 1 single line
                    current_title = line[len("<title>"):-len("</title>")] 
                    # print(current_page_title)
                else:
                    print("huh?")
            elif line.startswith("<text"):
                if line.endswith("/text>"): #text in a single line
                    current_page_text += line[line.find('>') + 1:line.find('</')] + '\n'
                else: #only opening tag
                    current_page_text_start = True    
                    current_page_text += (line[line.find('>') + 1:]) + "\n" #cut <text....> part
            elif line.endswith("/text>"): #only end tag
                current_page_text_start = False
                current_page_text += (line[:line.find('</')]) + "\n"
                article_title_text[current_title] = current_page_text
            elif current_page_text_start:
                # if line.startswith('=') and line.endswith('='): #skip headings
                #     continue
                # elif line.startswith('{|'): #skip tables
                #     current_table_start = True
                # elif line == '|}':
                #     current_table_start = False
                # else:
                #     if not current_table_start:
                current_page_text += line + "\n"
    with open('output/output.txt', 'w') as file:
        pass

convert_wikidump_to_articles()