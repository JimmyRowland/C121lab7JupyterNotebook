from selenium import webdriver
import nbformat
import re
from testRegex import test_regex
from settings import *
from IPython.display import display, Markdown

from selenium.common.exceptions import NoSuchElementException


def scrape_lab7_save_as_jupyter():
    driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
    driver.get(URL)
    tags = driver.find_elements_by_xpath('/html/body/*')
    nb = nbformat.v4.new_notebook()
    filename = FILENAME
    htmlBuilder = ""
    importedModule = False
    for tag in tags:
        if tag.tag_name != "form":
            htmlBuilder = htmlBuilder + tag.get_attribute("outerHTML").replace('$','\$') + "\n"

        else:
            nb['cells'].append(nbformat.v4.new_markdown_cell(htmlBuilder))
            if not importedModule:
                importedModule = True
                nb['cells'].append(nbformat.v4.new_code_cell('import re\nfrom testRegex import test_regex\nfrom IPython.display import display, Markdown'))
            htmlBuilder = ""

            form = tag
            title = form.find_element_by_xpath('.//tr[1]/td')
            testString = form.find_element_by_xpath('.//tr[4]/td').text.split("\n")
            if testString == [""]:
                testString = []
            regex = form.find_element_by_xpath('.//tr[2]/td/input').get_attribute('value')
            try:
                shouldReject = form.find_element_by_xpath('.//tr[9]/td')
                shouldReject = re.split(r'REJECT: |ACCEPT: ', shouldReject.text.replace('\n', ''))[1:]
                shouldAccept = form.find_element_by_xpath('.//tr[7]/td')
                shouldAccept = re.split(r'REJECT: |ACCEPT: ', shouldAccept.text.replace('\n', ''))[1:]
            except NoSuchElementException:
                shouldAccept = []
                shouldReject = []
            htmlBuilder = '# {}\nanswer = \'{}\'\n# Test Strings:\ntestStrings={}\nshouldAccept={}\nshouldReject={}' \
                          '\ndisplay(Markdown(test_regex(shouldAccept,shouldReject,testStrings,answer)))'.format(title.text, regex,testString,shouldAccept,shouldReject)

            print(htmlBuilder)
            nb['cells'].append(nbformat.v4.new_code_cell(htmlBuilder))
            htmlBuilder = ""

    nb['cells'].append(nbformat.v4.new_markdown_cell(htmlBuilder))
    nbformat.write(nb, filename)

    driver.close()


scrape_lab7_save_as_jupyter()
