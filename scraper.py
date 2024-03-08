from bs4 import BeautifulSoup
from collections import defaultdict
from requests_futures.sessions import FuturesSession


urls = []
html_text = ""
athar = []
for page in range(1, 51):
    urls.append(f"https://www.sayingsofthesalaf.net/page/{page}")
    
with FuturesSession() as session:
    futures = [session.get(url) for url in urls]
    for future in futures:
        response = future.result()
        html_text += response.text
    
soup = BeautifulSoup(html_text, "html.parser")
narrations = soup.find_all("article", class_="type-post")

for narration in narrations:
    title = narration.find("h1").text
    article = narration.find("div", class_="post-content").text
        
    tags = [tag.text for tag in narration.find("div", class_="post-tags").find_all("a")]
    categories = [category.text for category in narration.find("div", class_="post-cats").find_all("a")]
    athar.append({
        "title": title,
        "articles": article,
        "tags": tags,
        "categories": categories
    })
    
def get_categories():
    categories_dict = defaultdict(list)
    unique_categories = list({category for item in athar for category in item['categories']})

    for category in unique_categories:
        categories_dict[category[0].upper()].append(category)

    sorted_keys = sorted(categories_dict.keys())

    return [{key: categories_dict[key]} for key in sorted_keys]\
    
def get_tags():
    unique_tags = {tag for item in athar for tag in item['tags']}

    tags_dict = defaultdict(list)

    for tag in unique_tags:
        tags_dict[tag[0].upper()].append(tag)

    sorted_keys = sorted(tags_dict.keys())

    return [{key: tags_dict[key]} for key in sorted_keys]