import sys
from urllib import parse
import re
import aiofiles
import aiohttp
import asyncio
import os

# import time


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/67.0.3396.99 '
                  'Safari/537.36',
    'Host': "www.zhihu.com",
    'Referer': f"https://www.zhihu.com/question/42355466"
}


async def answer(url_):
    async with aiohttp.ClientSession() as session:
        async with session.get(url_, headers=header) as html:
            # print(resp.status)
            response = await html.json(encoding="utf-8")
            # time.sleep(1)
            return response


async def get_questions(url, qid):
    try:
        html = await answer(url)
        answer_total = int(html['paging']['totals'])
        offset = 0
        while offset < answer_total:
            url = f"https://www.zhihu.com/api/v4/questions/{qid}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=" + str(
                offset) + "&platform=desktop&sort_by=default"
            offset += 5
            answer_row = await answer(url)
            data = answer_row['data']
            if data.__len__ == 0:
                break
            else:
                for index, data_ in enumerate(data):
                    # 回答正文
                    answer_content = data[index]['content']
                    # print(author_url)
                    # 使用正则获取图片URL
                    img_urls = re.findall(r'src=\"(https://.*?)"', answer_content)
                    # 去除重复的URL
                    img_urls = list(set(img_urls))
                    # print(json.dumps(img_urls))
                    # 回答中没有图片，跳过
                    if img_urls.__len__() == 0:
                        break

                    with open("zhihu_img.txt", mode="a", encoding="utf-8") as f:
                        f.write("\n".join(img_urls) + "\n")
                    await sava_image(img_urls)
        print("全部图片下载")
    except:
        print("Question ID错误")
        sys.exit()


async def sava_image(img_urls):
    for img_url in img_urls:
        local_path = parse.urlsplit(img_url)[2].replace("/", "")  # 出现类似http://xxxx.com/xx/xxxx.jpg这种URL的处理
        # print(local_path)
        print(img_url)
        dir_path = 'images/'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        async with aiohttp.ClientSession() as session:  # reqs2 = requests.get(line)
            async with session.get(img_url) as reps:
                async with aiofiles.open("images/" + local_path, mode="wb") as f:
                    await f.write(await reps.content.read())
                    # time.sleep(0.2)
    # time.sleep(0.5)
    # print("全部下载完成")


async def main():
    qid = int(input("questionID："))
    url = f"https://www.zhihu.com/api/v4/questions/{qid}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&platform=desktop&sort_by=default"
    await get_questions(url, qid)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
