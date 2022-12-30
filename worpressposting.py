from requests import get, post
import openai
import base64
from dotenv import load_dotenv
load_dotenv()

with open('assing.txt', 'r+') as file:
    files = file.readlines()
    # r = files.strip('\n')
    # print(files)
i = 0

for f in files:
    r = f.strip('\n')
    # print(r)




#  heading two generte
def wp_h2(text):
  code = f'<!-- wp:heading --><h2>{text}</h2<!-- /wp:heading -->'
  return code
#paragraph generate 
def wp_p(text):
  code = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->' 
  return code  



# start open ai command
import os
openai.api_key = os.getenv('API_KEY_Op')
def opeai_comand(promt):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt= promt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  output=response.get('choices')[0].get('text')
  return output
comand = ('Best pressure Cooker')
promt = f'Write a paragraph about {comand}'
# final = opeai_comand(promt)
contents = wp_p(opeai_comand(f'write short about {comand}').strip().strip('\n'))
# print(contents)
question  = opeai_comand(promt)
# print(question)
question_list = (question.strip().split('\n'))
# print(question_list)
end_line = 'write a pragraph about it'
# print(question_list)   
content_dicts ={}

for q in question_list:
  command = f'{q} {end_line}'
  answer = opeai_comand(command).strip().strip('\n')
  content_dicts[q] = answer
# print(content_dicts)  

for key, value in content_dicts.items():
  qn = wp_h2(key)
  ans = wp_p(value)
  temp  = qn + ans
  # contents+=temp
# print(qn)

title = f'Common question about {comand}'
print(title)

# wordpress post

user = 'admin'
password = 'ADMIN_PASS' 
creadiantial= f'{user}:{password}'
token = base64.b64encode(creadiantial.encode())
headers = {'Authorization': f'Basic {token.decode("utf-8")}'}

data = {
  'title': title.title(),
  'content': contents,
  'slug': comand.replace(' ', '-')
}
site_url =  'https://localhost/chayan/wp-json/wp/v2/posts'

r = post(site_url, data= data, headers= headers, verify= False)
print(r.json())