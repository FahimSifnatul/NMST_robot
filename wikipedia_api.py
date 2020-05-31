import wikipediaapi
    
wiki = wikipediaapi.Wikipedia('en')

page_py = wiki_wiki.page('Pied_Piper_of_Hamelin')
print("Page - Exists: %s" % page_py.exists())
# Page - Exists: True

print("Page - Title: %s" % page_py.title)
# Page - Title: Python (programming language)

print("Page - Summary: %s" % page_py.summary[0:1000])
# Page - Summary: Python is a widely used high-level programming language for
