import re
import urllib.request
from bs4 import BeautifulSoup


def lookup(filename, word):
    f = open(filename, encoding="utf8")
    line = f.readline()
    while line:
        if re.search(word, line, re.IGNORECASE):
            return line
        line = f.readline()
    f.close()
    return ''


def getAPI(word):
    return "https://www.oxfordlearnersdictionaries.com/definition/english/" + word.strip()


def getSource(url):
    try:
        f = urllib.request.urlopen(url)
        content = f.read().decode("utf-8")
        f.close()
        soup = BeautifulSoup(content, "html.parser")
        results = soup.findAll("span", {"class": "phon"})
        return str(results[0]), str(results[1])
    except:
        return ''


def getPhonetics(spans):
    results = ' '
    pattern = ">(.+?)<"
    sp1 = spans[0].replace('</span>', '')
    sp2 = spans[1].replace('</span>', '')
    r = re.findall(pattern, sp1)
    if len(r) == 5:
        results += '/' + r[3] + '/, '
    else:
        results += '/' + r[2] + '/, '
    r = re.findall(pattern, sp2)
    if len(r) == 5:
        results += '/' + r[3] + '/; '
    else:
        results += '/' + r[2] + '/; '
    return results.replace('//', '/')


def getPhoneticsFromWord(word):
    url = getAPI(word)
    s = getSource(url)
    if s != '':
        p = getPhonetics(s)
        return p
    else:
        return ';'


def process(filename):
    read = open(filename, encoding="utf-8-sig")
    write = open('new_' + filename, 'a', encoding='utf-8-sig')
    count = 1
    line = read.readline()
    while line:
        print(count)
        if ';' in line and '.' not in line:
            word = line.split(';')[0]
            phonetics = getPhoneticsFromWord(word)
            newline = line.replace(';', phonetics)
        else:
            newline = line
        write.write(newline)
        line = read.readline()
        count += 1
    read.close()
    write.close()


if __name__ == "__main__":
    process('toeic.txt')
    # print(getPhoneticsFromWord('accommodate'))
