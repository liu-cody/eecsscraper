#! /usr/bin/env python3
def isfloat(var):
    try:
        float(var)
        return True
    except ValueError:
        return False
    

import requests, bs4
res = requests.get('http://www.eecs.umich.edu/eecs/undergraduate/survey/all_survey.2016.htm')
res.raise_for_status()
survey = bs4.BeautifulSoup(res.text, "html.parser")
classes = survey.select('td[colspan=3]')
difficulty = survey.select('td[style*="border-top:none;border-left:none"]')


#create a dict that maps a class number to an index
classesindex = dict()

for i in range(len(classes)):
    classesindex[str(classes[i].get_text())[0:3]] = i

#create a dict that maps an index to a class difficulty
indexesdifficulty = dict()

start_row = survey.find(lambda tag: tag and tag.name == "td" and
                        "Average" in tag.get_text(strip=True)).find_parent("tr")

count = 0
for row in start_row.find_next_siblings("tr"):
    cells = row.find_all("td")

    average_score = cells[6].get_text()

    if isfloat(average_score) :
        indexesdifficulty[count] = float(average_score)
        count += 1

#user input
totalscore = 0
classcount = 0

while True:
    if classcount == 0:
        classnumber = input('Please enter the number of an EECS class you are taking. Data is based on the Spring 2016 EECS student survey. For example, if you are taking EECS 183, enter "183". If you are done entering classes, press "d". ')
    else:
        classnumber = input('Enter the number of another EECS class you are taking or press "d" to quit. ')

    if classnumber == 'd':
        break
    elif classnumber in classesindex:
        classcount += 1
        totalscore += indexesdifficulty[classesindex[classnumber]]
    else:
        print(str(classnumber) + ' is not an EECS class. Please try again.')
    
            
print('You have selected classes with a total difficulty of ' + str(round(totalscore, 2)) + '.')

if totalscore > 5:
    print('Just so you know, the EECS department recommends not taking more than 5 points.')
else:
    print('Looks good! Have a great semester!')
