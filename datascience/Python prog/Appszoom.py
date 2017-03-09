from bs4 import BeautifulSoup
import urllib2
import multiprocessing
import MySQLdb
import time
import  requests
import thread
def CallThread(url):
    connection=MySQLdb.connect("localhost","root","root","demo")
    cursor = connection.cursor()
    user_agent = 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1'
    headers = {'User-Agent' : user_agent}
    #request = urllib2.Request(url, None, headers)
    #response = urllib2.urlopen(request)
    proxies = {
               "http": "178.48.2.237:8080",
               "https": "77.78.255.14:8080",
               }

    try:
        time.sleep(2)
        r= requests.get(url, proxies=proxies)
        site = r.text.encode('utf-8')
        soup = BeautifulSoup(site)
        ul = soup.find('ul',{'class':'search'})
        elemA = ul.find_all('a',{'class':'goTo'})
        for x in elemA:
            title = x.contents[0].encode("utf-8")
            link = x['href']
            cursor.execute('INSERT INTO app_name_link (name,link) VALUES (%s,%s)',(str(title),str(link)))
            connection.commit()
        print 'Done ::'+  url, time.ctime(time.time())
    except:
        print 'Error ::'+  url, time.ctime(time.time())
    
if __name__ == '__main__':
      
    #CallThread('Page 1','http://www.appszoom.com/android_games/arcade_and_action')
    l = 58
    for j in range(10):
        h = l + 10
        for i in range(l,h):
            k = i*10
            url = 'http://www.appszoom.com/android_games/arcade_and_action?p='
            url = url+str(k)
            CallThread(url)
            #p = multiprocessing.Process(target=CallThread,args=("Page"+str(i+1), url))
            #p.start()
            
            #p.join()
        l = h