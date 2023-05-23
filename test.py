import requests
from concurrent.futures import ThreadPoolExecutor

token = "ya29.a0AWY7CkkjHGcR6EaKAGI0kc3YzdAeglQbvFoUW4I6gW5Mocn74dHTSZNaRpslxvdjn5rT8edyr7t8h8TgKCStFT_AtNObiRSTsYNaPHfzPPZr-ablSXEs6Qca8-0X53X9mZB4IcSBbxXWF7D3TYEgRMb51ZKh4ExjqAaCgYKAfESARESFQG1tDrphdK2-wRu3mx6_QavgzWBoQ0169"
headers = {"Authorization": "Bearer " + token}
def get_url(url):
    return url['Yext ID'],requests.get(url['url'], headers = headers)

list_of_urls = [{'Yext ID': "12345",'url':"https://mybusiness.googleapis.com/v4/accounts/114683890036704478408/locations/15207521256978509479/reviews"}]*104


total_responses = []
chunks = [list_of_urls[x:x+int(50)] for x in range(0, len(list_of_urls), 50)]
num_chunks = len(chunks)
for count, prep_chunks in enumerate(chunks):
    with ThreadPoolExecutor() as pool:
        response_list = list(pool.map(get_url,prep_chunks))
        for response in response_list:
            print(response)
        print("break")







