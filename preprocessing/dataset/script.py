from lxml import etree
import datetime

source = "c.xml" 
time = datetime.datetime.now().isoformat()
name = "output/output" + time + ".txt"
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
        if len(title) > 0 and "Module:zh/data/ltc-pron/" in title[0].text:
            counter2 += 1
            if counter2 % 10 == 0:
                print("!!! Processed " + str(counter2) + " valid entries.")
            s1 = title[0].text[-1]
            try:
                s2 = elem.findall("{http://www.mediawiki.org/xml/export-0.10/}id")[0].text
                d = elem.findall("{http://www.mediawiki.org/xml/export-0.10/}revision")[0]
                s = d.findall("{http://www.mediawiki.org/xml/export-0.10/}text")[0].text
                start = '{'
                end = '}'
                s3 = s[s.find(start)+len(start):s.rfind(end)].replace("\n", "").lstrip().rstrip()
                f.write(s1 + ',' + s2 + ',' + s3 + '\n')
            except:
                pass
            # print(s1 + ',' + s2 + ',' + s3 + '\n')
        root.clear()
    root.clear()


