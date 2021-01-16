import copy
import json
import urllib.request
from datetime import datetime
from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup
from slugify import slugify

debug = False

# Preparing JSON file with recipes
pk_val = 1
empty_dict = {
    'model': 'popcorn.recipe',
    'pk': pk_val,
    'fields':
        {
            'vote_score': 0,
            'num_vote_up': 0,
            'num_vote_down': 0,
            'slug': None,
            'name': None,
            'content': None,
            'icon': None,
            'author': 1,
            'created_on': None,
            'last_modified': None,
            'preparation_time': 60,
            'servings_count': 4,
            'difficulty': 1,
            'hidden_on': None,
            'hidden_by': None,
            'deleted_on': None,
            'deleted_by': None,
            'categories': []
        }
}
przyslij_przepis_urls = ['https://www.przyslijprzepis.pl/przepis/bruschetta-z-pomidorami-suszonymi',
                         'https://www.przyslijprzepis.pl/przepis/lazanki-z-kielbasa',
                         'https://www.przyslijprzepis.pl/przepis/placuszki-nadziewane-nutella',
                         'https://www.przyslijprzepis.pl/przepis/grillowane-piersi-z-kurczaka-w-boczku',
                         'https://www.przyslijprzepis.pl/przepis/nalesniki-smietanowe-1',
                         'https://www.przyslijprzepis.pl/przepis/surowka-na-slodko-z-kiszonej-kapusty-i-marchewki-z-dodatkiem-jablka',
                         'https://www.przyslijprzepis.pl/przepis/roladki-z-tortilli-z-jajkiem-avocado-i-rzezucha',
                         'https://www.przyslijprzepis.pl/przepis/zajac-w-kolorowym-pieprzu-duszony-w-smietanie',
                         'https://www.przyslijprzepis.pl/przepis/zupa-pieczarkowa-z-kasza-peczak',
                         'https://www.przyslijprzepis.pl/przepis/babka-z-coca-cola-1',
                         'https://www.przyslijprzepis.pl/przepis/chipsy-solone-1',
                         'https://www.przyslijprzepis.pl/przepis/churros-z-sosem-czekoladowym-z-chili',
                         'https://www.przyslijprzepis.pl/przepis/grzaniec-bez-alkoholu',
                         'https://www.przyslijprzepis.pl/przepis/imprezowe-ciasteczka-serowo-cebulowe-z-ziolami',
                         'https://www.przyslijprzepis.pl/przepis/tarta-kakaowo-waniliowa-z-mascarpone',
                         'https://www.przyslijprzepis.pl/przepis/mega-kwasny-kapusniak-z-duza-iloscia-pieprzu-ziolowego'
                         ]

smaker_urls = ['https://smaker.pl/przepisy-sniadania/przepis-pasta-z-ciecierzycy,185592,asia67.html',
               'https://smaker.pl/przepisy-dania-glowne/przepis-zapiekanka-z-makaronem-i-tunczykiem-szybki-obiad,185758,slodkismakpasji.html',
               'https://smaker.pl/przepisy-sniadania/przepis-pasta-z-piklinga,185401,gregorhspeed.html',
               'https://smaker.pl/przepisy-dania-glowne/przepis-schab-po-bieszczadzku,185756,tradycyjna-kuchnia.html',
               'https://smaker.pl/przepisy-przekaski/przepis-pierogi-pieczone-z-nadzieniem-pieczarkowym,185739,tradycyjna-kuchnia.html',
               'https://smaker.pl/przepisy-przekaski/przepis-prawdziwe-frytki-z-mcdonald-s,185682,przepisykuby.html',
               'https://smaker.pl/przepisy-przekaski/przepis-malze-w-sosie-winno-czosnkowym,185730,maloni.html',
               'https://smaker.pl/przepisy-dania-glowne/przepis-bitki-wolowe-w-sosie,185701,agnes72.html',
               'https://smaker.pl/przepisy-zupy/przepis-zupa-kalafiorowa-na-mleku-kokosowym,185679,gregorhspeed.html',
               'https://smaker.pl/przepisy-desery/przepis-napoleonka-na-ciescie-francuskim,185757,gotowaniepomojemu.html',
               'https://smaker.pl/przepisy-przekaski/przepis-frytki-z-obierek-ziemniaczanych,185650,agnes72.html',
               'https://smaker.pl/przepisy-desery/przepis-sernik-warzony,185740,wanilioweimprowizacje.html',
               'https://smaker.pl/przepisy-napoje/przepis-kompot-z-suszu,185713,malgoskawkuchni.html',
               'https://smaker.pl/przepisy-desery/przepis-francuski-krem-mleczno-jajeczny-creme-brulee,185698,turek.html',
               'https://smaker.pl/przepisy-przekaski/przepis-tatar-ze-sledzia-z-mandarynkowym-twistem,185308,kulinarnyfreestyle.html',
               'https://smaker.pl/przepisy-dodatki/przepis-quot-lemoniada-quot-uodparniajaca-na-infekcje,184635,koral.html']

kuchnia_domowa_urls = ['https://www.kuchnia-domowa.pl/przepisy/dania-glowne/469-frittata-z-bobem',
                       'https://www.kuchnia-domowa.pl/przepisy/dania-glowne/421-biala-kielbasa-z-kiszona-kapusta',
                       'https://www.kuchnia-domowa.pl/przepisy/dania-glowne/308-calzone',
                       'https://www.kuchnia-domowa.pl/przepisy/dania-glowne/248-filet-z-kurczaka-w-sosie-pomidorowym',
                       'https://www.kuchnia-domowa.pl/przepisy/zupy/261-barszcz-czerwony-czysty',
                       'https://www.kuchnia-domowa.pl/przepisy/dipy-pasty/322-dip-z-baklazana',
                       'https://www.kuchnia-domowa.pl/przepisy/przystawki-przekaski/450-carpaccio-z-burakow',
                       'https://www.kuchnia-domowa.pl/przepisy/dania-glowne/528-filet-z-kurczaka-w-sosie-pieczarkowym-z-serkiem-mascarpone',
                       'https://www.kuchnia-domowa.pl/przepisy/zupy/538-zupa-pomidorowa-z-pomidorow-z-puszki',
                       'https://www.domowe-wypieki.pl/przepisy/ciasta/324-3-bit',
                       'https://www.kuchnia-domowa.pl/przepisy/przystawki-przekaski/436-orzechy-solone',
                       'https://www.domowe-wypieki.pl/przepisy/ciasteczka/1227-ciasteczka-cynamonowe',
                       'https://www.kuchnia-domowa.pl/przepisy/napoje/smoothie/480-smoothie-z-mango-ananasem-marakuja',
                       'https://www.kuchnia-domowa.pl/przepisy/przystawki-przekaski/433-tosty-francuskie-na-slono',
                       'https://www.kuchnia-domowa.pl/przepisy/przystawki-przekaski/429-tosty-francuskie-na-slodko',
                       'https://www.kuchnia-domowa.pl/przepisy/zupy/401-zakwas-buraczany']

recipes = []


def p(phrase):
    return '<p>' + phrase + '</p>'


def przyslij_przepis(pk_val):
    caterogy = 1
    for i in range(len(przyslij_przepis_urls)):
        uClient = uReq(przyslij_przepis_urls[i])
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "html.parser")

        # get recipe title
        container = page_soup.findAll("div", {"class": "view-headline"})
        recipe_title = container[0].h1.text
        if debug:
            print(recipe_title)

        # save recipe image
        container = page_soup.findAll("div", {"class": "rich-gallery-see"})
        recipe_image_link = "http:" + container[0].a.span.div.img["src"]
        urllib.request.urlretrieve(recipe_image_link, slugify(recipe_title) + '.jpeg')

        # get recipe ingredients
        container = page_soup.findAll("div", {"class": "inner", "itemprop": "recipeIngredient"})
        ingredients = container[0].text
        ingredients = ingredients.replace('Składniki', '')
        ingredients = ingredients.lstrip()
        if debug:
            print(ingredients)

        # get recipe description
        container = page_soup.findAll("div", {"class": "col-xs-12"})
        recipe_description = container[4].text
        # properly format description
        recipe_description = recipe_description.replace('Sposób przygotowania przepisu:', '')
        recipe_description = recipe_description.replace(recipe_title, '')
        recipe_description = " ".join(recipe_description.split())
        # add newline between numbers of steps
        for i in range(10):
            current = str(i + 2)
            current += '.'
            recipe_description = recipe_description.replace(current, '<br>' + current)

        if debug:
            print(recipe_description)

        image_dir = 'recipes/' + slugify(recipe_title) + '.jpeg'
        current_recipe = copy.deepcopy(empty_dict)
        current_recipe['pk'] = pk_val
        current_recipe['fields']['slug'] = slugify(recipe_title) + '-' + str(pk_val)
        pk_val += 1
        current_recipe['fields']['name'] = recipe_title
        current_recipe['fields']['content'] = p('Składniki<br>')
        for line in ingredients.splitlines():
            current_recipe['fields']['content'] += p(line + '<br>')
        for line in recipe_description.splitlines():
            current_recipe['fields']['content'] += p(line + '<br>')
        current_recipe['fields']['icon'] = image_dir
        current_recipe['fields']['created_on'] = datetime.now().strftime('%Y-%m-%dT%H:%MZ')
        current_recipe['fields']['last_modified'] = datetime.now().strftime('%Y-%m-%dT%H:%MZ')
        current_recipe['fields']['categories'] = [caterogy]
        caterogy += 1

        recipes.append(current_recipe)


def smaker(pk_val):
    category = 1
    for i in range(len(smaker_urls)):
        uClient = uReq(smaker_urls[i])
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, 'html.parser')

        # get recipe title
        recipe_title = page_soup.h1.text
        if debug:
            print(recipe_title)

        # save recipe image
        container = page_soup.findAll('div', {'class': 'image_wrap'})
        recipe_image_link = container[0].img['src']
        recipe_image_link = 'http:' + recipe_image_link
        urllib.request.urlretrieve(recipe_image_link, slugify(recipe_title) + '.jpeg')
        if debug:
            print(recipe_image_link)

        # get recipe ingredients
        container = page_soup.findAll('ul', {'class': 'ingredients'})
        ingredients = container[0].text
        ingredients = ingredients.lstrip()
        ingredients = ingredients.rstrip()
        ingredients = ingredients.replace('  ', '')
        ingredients = ingredients.replace('\n\n\n', '')
        if debug:
            print(ingredients)

        # get recipe description
        container = page_soup.findAll('div', {'itemprop': 'step'})
        recipe_description = container[0].text
        recipe_description = recipe_description.replace('Przygotowanie', '')
        recipe_description = recipe_description.lstrip()
        recipe_description = recipe_description.rstrip()
        if debug:
            print(recipe_description)

        image_dir = 'recipes/' + slugify(recipe_title) + '.jpeg'
        current_recipe = copy.deepcopy(empty_dict)
        current_recipe['pk'] = pk_val
        current_recipe['fields']['slug'] = slugify(recipe_title) + '-' + str(pk_val)
        pk_val += 1
        current_recipe['fields']['name'] = recipe_title
        current_recipe['fields']['content'] = p('Składniki<br>')
        for line in ingredients.splitlines():
            current_recipe['fields']['content'] += p(line + '<br>')
        for line in recipe_description.splitlines():
            current_recipe['fields']['content'] += p(line + '<br>')
        current_recipe['fields']['icon'] = image_dir
        current_recipe['fields']['created_on'] = datetime.now().strftime('%Y-%m-%dT%H:%MZ')
        current_recipe['fields']['last_modified'] = datetime.now().strftime('%Y-%m-%dT%H:%MZ')
        current_recipe['fields']['categories'] = [category]
        category += 1

        recipes.append(current_recipe)


def kuchnia_domowa(pk_val):
    category = 1
    for i in range(len(kuchnia_domowa_urls)):
        uClient = uReq(kuchnia_domowa_urls[i])
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, 'html.parser')

        # get recipe title
        recipe_title = page_soup.h2.text
        recipe_title = recipe_title.strip()
        if debug:
            print(recipe_title)

        # save recipe image
        container = page_soup.findAll('div', {'class': 'articleBody'})
        recipe_image_link = container[0].div.img['data-src']
        recipe_image_link = 'http:' + recipe_image_link
        urllib.request.urlretrieve(recipe_image_link, slugify(recipe_title) + '.jpeg')
        if debug:
            print(recipe_image_link)

        # get recipe ingredients
        container = page_soup.findAll('div', {'id': 'recipe-ingredients'})
        ingredients = container[0].text
        ingredients = ingredients.strip()
        if debug:
            print(ingredients)

        # get recipe description
        container = page_soup.findAll('div', {'id': 'recipe-instructions'})
        recipe_description = container[0].text
        recipe_description = recipe_description.strip()
        if debug:
            print(recipe_description)

        image_dir = 'recipes/' + slugify(recipe_title) + '.jpeg'
        current_recipe = copy.deepcopy(empty_dict)
        current_recipe['pk'] = pk_val
        current_recipe['fields']['slug'] = slugify(recipe_title) + '-' + str(pk_val)
        pk_val += 1
        current_recipe['fields']['name'] = recipe_title
        current_recipe['fields']['content'] = p('Składniki<br>')
        for line in ingredients.splitlines():
            current_recipe['fields']['content'] += p(line + '<br>')
        for line in recipe_description.splitlines():
            current_recipe['fields']['content'] += p(line + '<br>')
        current_recipe['fields']['icon'] = image_dir
        current_recipe['fields']['created_on'] = datetime.now().strftime('%Y-%m-%dT%H:%MZ')
        current_recipe['fields']['last_modified'] = datetime.now().strftime('%Y-%m-%dT%H:%MZ')
        current_recipe['fields']['categories'] = [category]
        category += 1

        recipes.append(current_recipe)


przyslij_przepis(1)
smaker(17)
kuchnia_domowa(33)

# save recipes to .json file
with open('recipes.json', 'w', encoding='utf-8') as outfile:
    json.dump(recipes, outfile, indent=4, ensure_ascii=False)
