import os
import boto3
import requests
import json, xmltodict


s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['MORPH_AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['MORPH_AWS_SECRET_KEY'],
    region_name='eu-west-1'
)

r = requests.get('https://syndication.24.com/articles/Fin24/News/newsml',
      auth = (
        os.environ['MORPH_NEWS24_USERNAME'],
        os.environ['MORPH_NEWS24_PASSWORD']
      )
    )


data = [];
xml = xmltodict.parse(r.content)

for index, news_item in enumerate(xml['NewsML']['NewsItem']):
  news_item = news_item['NewsComponent']['NewsComponent']['NewsComponent']
  data.append({
    'title': news_item['NewsLines']['HeadLine'],
    'description': news_item['NewsLines']['SlugLine'],
    'link': news_item['NewsLines']['MoreLink'],
    'img': news_item['ContentItem']['DataContent']['nitf']['body']['body.content']['media']['media-reference']['@source'],
    })

  if index == 5:
    break


s3.put_object(
    Bucket='taxclock-za.codeforafrica.org',
    ACL='public-read',
    Key='data/fin24-news.json',
    Body=json.dumps(data)
)

print "Successfully finished."
