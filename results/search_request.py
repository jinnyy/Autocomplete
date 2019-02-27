import requests
import json




def print_result(parsed_data):
    for data in parsed_data['hits']['hits']:
        print(data['_source']['name'])

URL = 'http://106.10.42.5:9200/autocomplete_jaso/_search' 



while True:
    gender = input("성별(f/m or 남/여): ")
    if gender=="여":
        gender = "f"
    elif gender=="남":
        gender = "m"
    if gender=="f" or gender=="m":
        break
    else:
        print("다시 입력해 주세요")

while True:
    age = input("나이(ex: 20세-->20): ")
    # 10세 미만일 시 10대와 동일시
    if int(age)<10:
        age = "10"
    # 50세 초과시 40대와 동일시
    elif int(age)>50:
        age = "40"
    if age.isnumeric():
        break
    else:
        print("숫자로 입력해주세요")

input_name = input("검색어를 입력하세요: ")



body = {
            "sort":[
                {"counts."+age[0]+gender:{"order":"desc"}},
                "_score"
            ],
            "size":10,
            "query": {
                "match": {
                  "name": {
                      "query": input_name,
                      "fuzziness":"AUTO"
                  }
                }
              }
            }

response = requests.get(URL, 
                        data= json.dumps(body),
                        headers={"Content-Type": "application/json"}) 

if(response.status_code==200):
    data = response.text
    parsed_data = json.loads(data)
    print("===============================")
    print_result(parsed_data)
else:
    print(response.status_code)
    print(response.json())
