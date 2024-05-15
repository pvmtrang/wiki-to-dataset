# - flat category: only articles point to it
# - nested category: other nested/flat categories and articles can link it

import config

cat_dict = {
    'id':[],
    'title':[],
    'pages':[],
    'subcats': [],
    'files':[]
    }
cat_map = {} #format: 'cat_title': 'NER_tag'

def from_sql():
    #according to the sql format of wiki, there are 5 cols, too lazy to write more auto code
    with open(config.CATEGORY_PATH, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            line = line.lower().strip()
            if line.startswith('insert into'):
                line = line[line.find('('):-1] #only take (),(),() part. skip code and ;
                list_cat = line.split(sep='),(') #'(1,a,!', '2,b,@', '3,c,#)'
                for cat_i in list_cat:
                    if cat_i.startswith('('):
                        cat_i = cat_i[1:]
                    elif cat_i.endswith(')'):
                        cat_i = cat_i[:-1]
                    cat_i = cat_i.split(',') #'list 1', 'a' , '!'
                    cat_dict['id'].append(cat_i[0]) #incremental, not neccessary consecutive: 1, 2, 4, 5
                    # cat_dict['title'].append(cat_i[1:-3]) #skip ' '. 
                    cat_dict['pages'].append(cat_i[-3])
                    cat_dict['subcats'].append(cat_i[-2])
                    cat_dict['files'].append(cat_i[-1])
                    tmp_title = ''
                    if len(cat_i) > 5:  #titles with ',' inside: 'kashima, _ibaraki' -> split ra > 5 elements
                        tmp_title = ','.join(cat_i[1:-3]).replace("'", '').replace('_', ' ')
                    else:
                        tmp_title = cat_i[1][1:-1].replace('_', ' ')
                    cat_dict['title'].append(tmp_title)
                    # if cnt < 50:
                    #     print(cat_dict)
                    #     print(str(cnt) + " " + 'id=' +cat_i[0] + ' ' + cat_i[1])
                    # cnt +=1
    
    with open(config.CATEGORY_OUTPUT_PATH, 'w', encoding='utf-8') as file:
        file.write("-- Total of " + str(len(cat_dict['id'])) + ' categories (including nested ones with(out) subcats, and empty ones\n\n')
        file.write('id | title | pages | subcats | files\n')
        for i in range(len(cat_dict['id'])):
            file.write(cat_dict['id'][i] + ' | ' + cat_dict['title'][i] + ' | ' + cat_dict['pages'][i] \
                       + ' | ' + cat_dict['subcats'][i] + ' | ' + cat_dict['files'][i] + '\n')
            


def label_cat_tag():
    ner_list_acr = ['p', 'l', 'c', 'g', 'w', '0']
    print("[per, loc, corp, grp, cw, none] -> " + str(ner_list_acr))
    
    with open(config.CATEGORY_NER_PATH, 'w', encoding='utf-8') as file:
        for i in range(len(cat_dict['id'])):
            print('\n'+cat_dict['id'][i] + ' | ' + cat_dict['title'][i] + ' | ' + cat_dict['pages'][i] \
                       + ' | ' + cat_dict['subcats'][i] + ' | ' + cat_dict['files'][i])
            if cat_dict['pages'][i] != '0': #skip empty cat, and nested cat with no articles
                print(cat_dict['pages'][i])
                title = cat_dict['title'][i]
                tag = input(title + ': ')
                tag = tag.split(' ')
                cat_map[title] = tag   
                file.write(title + ' | ' + str(tag) + '\n')
            else:
                print("skip empty category: " + cat_dict['title'][i])

    
    with open(config.CATEGORY_NER_PATH) as file1, open(config.CATEGORY_NER_PATH + "_1", 'r+') as file:
        content = file1.read()
        file.write(content)
        file.seek(0, 0)
        file.write("-- Total of " + str(len(cat_map.keys())) + ' flat, non-empty categories\n\n')
        file.write(content)

    
    # print('all done. \n writing to file...')

    # with open(config.CATEGORY_NER_PATH, 'w', encoding='utf-8') as file:
    #     file.write("-- Total of " + str(len(cat_map.keys())) + ' flat, non-empty categories\n\n')
    #     file.write('category | ner taxonomy\n')
    #     for cat_i in cat_map.keys():
    #         file.write(cat_i + ' | ' + cat_map[cat_i] + '\n')

from_sql()
label_cat_tag()








                    

