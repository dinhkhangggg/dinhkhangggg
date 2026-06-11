import requests

def get_meme():
    # Fetch a random meme from r/ProgrammerHumor
    response = requests.get('https://meme-api.com/gimme/ProgrammerHumor')
    if response.status_code == 200:
        return response.json().get('url')
    return None

def update_readme(meme_url):
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_tag = '<!-- meme-start -->'
    end_tag = '<!-- meme-end -->'
    
    if start_tag not in content or end_tag not in content:
        print("Could not find tags in README")
        return
        
    before = content.split(start_tag)[0]
    after = content.split(end_tag)[1]
    
    if meme_url:
        meme_html = f'<p align="center"><img src="{meme_url}" width="400" alt="Programming Meme" style="border-radius:10px;"/></p>'
        new_content = f"{before}{start_tag}\n{meme_html}\n{end_tag}{after}"
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("README updated successfully")
    else:
        print("Failed to fetch meme")

if __name__ == '__main__':
    url = get_meme()
    update_readme(url)
