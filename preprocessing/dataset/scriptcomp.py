from lxml import etree
import datetime
import re

# used to get composition

source = "c.xml" 

with open('middle_chinese_character_list.txt', 'r') as f:
    chars = f.read().replace('\n', '')

time = datetime.datetime.now().isoformat()
name = "comp_output/output" + time + ".txt"
f= open(name,"w+")
# get an iterable
context = etree.iterparse(source, events=("start", "end"))
# turn it into an iterator
context = iter(context)
# get the root element
event, root = next(context)
counter1 = 0
counter2 = 0
for event, elem in context:
    # print(elem.tag)
    if event == "end" and elem.tag == "{http://www.mediawiki.org/xml/export-0.10/}page":
        # print(elem.tag)
        counter1 += 1
        if counter1 % 10000 == 0:
            print("Processed " + str(counter1) + " total entries.")
        # print(elem.tag)
            # print(elem.tag)
        title = elem.findall("{http://www.mediawiki.org/xml/export-0.10/}title")
        # print(title.text)
        if len(title) > 0 and title[0].text in chars:
            li = []

            counter2 += 1
            if counter2 % 10 == 0:
                print("!!! Processed " + str(counter2) + " valid entries.")
            s1 = title[0].text[-1]

            try:
                s2 = elem.findall("{http://www.mediawiki.org/xml/export-0.10/}id")[0].text
                d = elem.findall("{http://www.mediawiki.org/xml/export-0.10/}revision")[0]
                s = d.findall("{http://www.mediawiki.org/xml/export-0.10/}text")[0].text
                s.replace("\n","")
                su = s.partition("ids=")[2]
                su = su.partition("|")[0]
                su = su.partition("}")[0]
                su = su.partition("(")[0]
                if not su:
                    su = s1
                li.append(su);
                f.write(s1 + "," + s2 + "," + su + '\n')
            except:
                pass
        root.clear()
    root.clear()


