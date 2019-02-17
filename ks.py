import requests
import os
import json
import process

class KuaiShouCrawler(object):
    def __init__(self, name):
        self.session = requests.Session()
        self.verify = False
        self.name = name
    
    def write_file(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
            'origin': 'https://live.kuaishou.com',
            'referer': 'https://live.kuaishou.com/profile/{}'.format(self.name)
        }
        payloads = {
            "operationName": "ProfileFeeds",
            "variables": {
                "principalId": "{}".format(self.name),
                "privacy": "public",
                "pcursor": "0",
                "count": 100000
            },
            "query": "query ProfileFeeds($principalId: String, $privacy: String, $pcursor: String, $count: Int) {\n  getProfileFeeds(principalId: $principalId, privacy: $privacy, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      ...LiveStreamInfo\n      __typename\n    }\n    list {\n      ...WorkInfo\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment LiveStreamInfo on LiveStream {\n  user {\n    id\n    kwaiId\n    eid\n    profile\n    name\n    living\n    __typename\n  }\n  watchingCount\n  src\n  title\n  gameId\n  gameName\n  categoryId\n  liveStreamId\n  playUrls {\n    quality\n    url\n    __typename\n  }\n  followed\n  type\n  living\n  redPack\n  liveGuess\n  anchorPointed\n  latestViewed\n  expTag\n  __typename\n}\n\nfragment WorkInfo on VideoFeed {\n  photoId\n  caption\n  thumbnailUrl\n  poster\n  viewCount\n  likeCount\n  commentCount\n  timestamp\n  workType\n  type\n  playUrl\n  useVideoPlayer\n  imgUrls\n  imgSizes\n  magicFace\n  musicName\n  location\n  liked\n  onlyFollowerCanComment\n  relativeHeight\n  width\n  height\n  user {\n    id\n    eid\n    name\n    profile\n    __typename\n  }\n  expTag\n  __typename\n}\n"
        }
        r = self.session.post('https://live.kuaishou.com/graphql', headers=headers, json=payloads, stream=True)
        with open('stream.txt', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        r.close()
    
    def download_videos(self, save_dir=''):
        if save_dir == '':
            save_dir = os.path.join(os.getcwd(), self.name)
            if not os.path.isdir(save_dir):
                os.makedirs(save_dir)
        if not os.path.isdir(save_dir):
            raise('your save dir path is not exist!')
        video_dict = {}
        with open('stream.txt', 'r', encoding='UTF-8') as f:
            video_dict = json.load(f)
        os.chdir(save_dir)
        for video in video_dict['data']['getProfileFeeds']['list']:
            if video['useVideoPlayer']:
                video_url = video['playUrl']
                video_name = video_url.rsplit('/', 1)[1]
                if os.path.exists(os.path.join(save_dir, video_name)):
                    continue
                cmd = 'curl -O {}'.format(video_url)
                os.system(cmd)

if __name__ == "__main__":
    name = input('Please input the name: ')
    crawler = KuaiShouCrawler(name)
    crawler.write_file()
    crawler.download_videos()
    process.merge_videos()