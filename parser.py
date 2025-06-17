import requests, json, re

headers = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://www.tiktok.com/explore',
  'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

def get_comments(video_url):
    post_url = requests.get(video_url)
    post_id = re.search(r'/video/(\d+)', post_url.url).group(1)
    all_comments = []
    cursor = 0

    def req(post_id, cursor):
        url = f"https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={post_id}&count=50&cursor={cursor}"
        r = requests.get(url, proxies={
                                    "http": "http://ozmduwem:oe77z2d8b4a9@198.23.239.134:6540/",
                                    "https": "http://ozmduwem:oe77z2d8b4a9@198.23.239.134:6540/"
                                },headers = headers)
        return json.loads(r.text)


    def reply_req(comment_id ,post_id, cursor):
        url = f"https://www.tiktok.com/api/comment/list/reply/?aid=1988&comment_id={comment_id}&cursor={cursor}&count=50&item_id={post_id}"
        r = requests.get(url, proxies={
                                    "http": "http://ozmduwem:oe77z2d8b4a9@198.23.239.134:6540/",
                                    "https": "http://ozmduwem:oe77z2d8b4a9@198.23.239.134:6540/"
                                },headers = headers)
        return json.loads(r.text)

    def parser(data, post_id):
        comments = []
        for el in data['comments']:
            comment_user_id = el['user']['unique_id']
            comment_user_nik = el['user']['nickname']
            comment_user_url = f"https://www.tiktok.com/@{comment_user_id}"
            comment_text = el['text'] or el.get('desk', '')
            comments.append([comment_text, comment_user_id, comment_user_nik, comment_user_url])
            comment_cid = el['cid']
            comment_reply = el['reply_comment_total']
            if comment_reply>0:
                reply_data = reply_req(comment_cid,post_id , cursor=0)
                for reply_el in reply_data['comments']:
                    comment_user_id = reply_el['user']['unique_id']
                    comment_user_nik = reply_el['user']['nickname']
                    comment_user_url = f"https://www.tiktok.com/@{comment_user_id}"
                    comment_text = reply_el['text'] or reply_el.get('desk', '')
                    comments.append([comment_text, comment_user_id, comment_user_nik, comment_user_url])
        return comments

    while True:
        data = req(post_id, cursor)
        all_comments.extend(parser(data, post_id))
        if data.get('has_more') == 1:
            cursor += 50
        else:
            break

    return all_comments
