import urllib.request
import json, sys
import matplotlib.pyplot as plt

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    
def getting_texts(i):

    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-55284725&count=1&offset='+str(i)) 
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    d1 = json.loads(result)
    
    posts1 = d1['response']
    x1 = posts1[1] #промежуточная переменная,которая содержит словарь
    post_id = x1['id'] # id поста
    number_comms = x1['comments']['count'] #кол-во комментариев
    text = x1['text'] #текст поста
    
    f = open('textnaval.txt', 'a', encoding='utf-8')
    f.write(text + '\n' + '\n')
    
    text1 = text.replace('<br>', '')
    text1 = text1.replace('—', '')


    arr_text = text1.split()

    for element in arr_text:
        if element.startswith('vk.com'):
            arr_text.remove(element)
        elif element.startswith('https'):
            arr_text.remove(element)

    length_post = len(arr_text)

    average = 0
    average = getting_comms(post_id)
    

    f.close()



    return length_post, average
          
def getting_comms(post_id):

    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-55284725&count=1')
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    d1 = json.loads(result)

    posts = d1['response']
    x1 = posts[1] # type - dict
 #   post_id = x1['id']
    number_comms = x1['comments']['count']
    
 
    k = 0
    average = 0
    
    while k < number_comms:
        try:
            req_comm = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-55284725&post_id='+str(post_id)+'&count=1&offset='+str(k))
            response_comm = urllib.request.urlopen(req_comm) 
            result_comm = response_comm.read().decode('utf-8')
            d2comm = json.loads(result_comm)
            arr = d2comm['response']
            text_comm = arr[1]['text']
            text_comm_1 = text_comm.translate(non_bmp_map)
            text_comm_arr = text_comm_1.split()
            length_comm = len(text_comm_arr)
            average = average + length_comm
            k += 1
        except:
            break
    average = average/number_comms
    print(average)
    return average


def main():

 #   d = {}
    length_of_posts = []
    average_comm = []
    i = 0
    length_post = 0
    while i < 150:
        length_post, average = getting_texts(i)
        i += 1
        length_of_posts.append(length_post)
        average_comm.append(average)
        


    #for x in range(0, len(length_of_posts)):
#        d[length_of_posts[x]] = average_comm[x]

    plt.scatter(length_of_posts, average_comm)
    plt.title("Длина поста и средняя длина комментария")
    plt.xlabel("длина поста")
    plt.ylabel("средняя длина комментариев")

    plt.show()
           
if __name__ == '__main__':
    main()
    




    


