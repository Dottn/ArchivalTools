from lxml import html
from os.path import basename
from posixpath import basename,dirname
from yurl import URL
import requests
import os

# This script crawls through the artist page of a specified artist on natalie.mu, and downloads every single picture from the linked article galleries.
# The artist_id value is the last number of the URL to the artist page.
# The pages value is how many pages back you want to crawl (I did not bother automating this bit). It will go through page 1 to the specified page number.
# To only check the newest articles, set pages to 1.
#
# Pictures will be downloaded to ./natalie/$artist_id/$article_id
# If the path already exist, the script will skip that article.
#
# Sakura Gakuin has artist id 8935
# At time of writing, the oldest natalie articles of SG were on page 14
# SG Artist page: https://natalie.mu/eiga/news/list/page/1/artist_id/8935


artist_id = 8935
pages = 1
print('Artist ID: {0}'.format(artist_id))
print('Number of pages to check: {0}'.format(pages))


# Checks if the path ./natalie/$artist_id exists. If not, creates it.
if not os.path.exists('natalie'):
    os.mkdir("natalie")
if not os.path.exists('natalie/{}'.format(artist_id)):
    os.mkdir("natalie/{}".format(artist_id))
os.chdir("natalie/{}".format(artist_id))

# Starting on page 1, to $pages, find all linked articles
for i in range(pages):
    print('Page {0}'.format(i + 1))

    page = requests.get('https://natalie.mu/eiga/news/list/page/{0}/artist_id/{1}'.format(i + 1 ,artist_id))
    tree = html.fromstring(page.content)

    ul = tree.xpath('//ul[@class="NA_articleList clearfix"]')[0]

    # For all linked articles on the current page
    for li in ul:
        url = li[0].get("href")

        # Find article ID, check if article folder already exists.
        # If it does, skip to next article.
        dirname=basename(URL(url).path)

        print('Article {0}'.format(dirname))

        if os.path.exists(dirname):
            print("Article folder exists")
            continue
        os.mkdir(dirname)

        article = requests.get(url)
        articleTree = html.fromstring(article.content)

        # Get the NA_imageList objects from the page source
        # Here there's some logic around whether a gallery exists or not.
        # If there's a gallery, there are 2 NA_imageList objects, and we want the first.
        imageList = articleTree.xpath('//ul[@class="NA_imageList clearfix"]')
        if len(imageList) > 1:
            imageList = imageList[0]
        # If there's only one NA_imageList, that's a sidebar thing, and we want to try getting the NA_articleBanner instead (included in gallery if exists)
        # Some articles don't have a banner, but have an included NA_articleFigure,
        # If neither of these exists, assume there's no images, and go to next article.
        else:
            try:
                imageList = articleTree.xpath('//div[@class="NA_articleBanner"]')[0][0]
            except:
                try:
                    imageList = articleTree.xpath('//div[@class="GAE_newsMainImage NA_articleFigure"]')[0][0][0]
                except:
                    continue

        # Sort out which tag-property contains the ogre.natalie.mu URL
        if imageList.tag == "ul":
            tagProperty = "data-bg"
        else:
            tagProperty = "src"
            imageList = [[imageList[0]]]

        # For all images in the gallery/article banner/article figure, download the linked resource without the query parameters, i.e. get the original.
        for image in imageList:
            # having 'impolicy=' as the url query ensures download of the largest resolution version of the image
            imageUrl = URL(image[0][0].get(tagProperty)).replace(query='impolicy=')
            try:
                imageData=requests.get(imageUrl).content
                filname='{0}/{1}'.format(dirname, basename(imageUrl.path))
                print(imageUrl)
                print(filname)
                output=open(filname,'wb')
                output.write(imageData)
                output.close()
            except:
                pass
