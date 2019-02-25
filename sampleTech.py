import bs4 as bs
##import urllib.request
import re
import os
import nltk

print(os.getcwd())
fp = open("textBooks/effectiveDev/ch01.html", "r")
parsed_article = bs.BeautifulSoup(fp, 'lxml')

#scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
#article = scraped_data.read()

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text


formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(article_text)
