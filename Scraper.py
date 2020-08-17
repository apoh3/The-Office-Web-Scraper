# web scraper using Beautiful Soup
# Allison Poh
# 2020

import requests as r
import re
from bs4 import BeautifulSoup as bsoup

output = []

#limit crawling if season given
def get_range(season):
    switcher = {
        '01': [0,0],
        '02': [0,25],
        '03': [25,50],
        '04': [50,50],
        '05': [50,100],
        '06': [100,100],
        '07': [125,125],
        '08': [150,150],
        '09': [175,175]
    }

    return switcher.get(season,[0,175])

#find links to transcripts based on season + episode given
def scrape_titles(season,episode,speaker,keyword):
    output.clear()
    rang = get_range(season)
    min_val = rang[0]
    max_val = rang[1]
    incr = 25

    for number in range(min_val, max_val+1, incr):
        URL = 'https://transcripts.foreverdreaming.org/viewforum.php?f=574&start='+str(number)
        page = r.get(URL)
        soup = bsoup(page.content, 'html.parser')
        results = soup.find(id='pagecontent')

        title_elems = results.find_all('h3')
        start = 0
        sea_and_epi = ''
        ignore_sea = False
        ignore_epi = False

        #determine if season and/or episode given
        if season != 'n/a' and episode != 'n/a':
            sea_and_epi = season + 'x' + episode
        elif season == 'n/a' and episode == 'n/a':
            ignore_sea = True
            ignore_epi = True
        elif season == 'n/a':
            ignore_sea = True
        elif episode == 'n/a':
            ignore_epi = True

        for t_elems in title_elems:
            title = t_elems.text.strip()
            link = t_elems.find('a')['href']

            if title[0].isdigit():
                part_a = title.split(' ')[0]  #seasonXepisode
                part_b = part_a.split('x')[0] #season
                part_c = part_a.split('x')[1] #episode

                if (part_a == sea_and_epi) or (ignore_sea == True and ignore_epi == True) or (ignore_epi == True and part_b == season): #valid
                    scrape_transcript(title,link,speaker,keyword)
                    start = 1
                elif ignore_sea == True and part_c == episode: #valid
                    scrape_transcript(title,link,speaker,keyword) 
                    if title[1] == 9: #max scrapes = max # of seasons
                        return output
                elif start == 1: #stop
                    return output

    return output

#scrape transcript for speaker and/or keyword
def scrape_transcript(title,extra,speaker,keyword):
    path = re.search('.(.*)&',extra).group(1)
    URL = 'https://transcripts.foreverdreaming.org' + path
    page = r.get(URL)
    soup = bsoup(page.content, 'html.parser')
    results = soup.find(id='pagecontent')

    text_elems = results.find_all('p')

    #ckeck for speaker and keyword
    no_speaker = False
    if speaker == 'n/a':
        no_speaker = True
    if keyword == 'keyword...':
        keyword = ''

    for t_elems in text_elems:
        text = t_elems.text.strip()
        person = text.split(':')[0]

        if (len(text) > 0) and (no_speaker == False) and (person == speaker) and (keyword.lower() in text.lower()): #valid with speaker
            output.append(title + " ... " + text)
        elif (len(text) > 0) and (no_speaker == True) and (keyword.lower() in text.lower()): #valid without speaker
            output.append(title + " ... " + text)

