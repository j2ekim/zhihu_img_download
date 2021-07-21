from urllib import parse
import re
import aiofiles
import aiohttp
import asyncio

try:
    qid = int(input("请输入文章ID："))
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/67.0.3396.99 '
                      'Safari/537.36',
        'Host': "www.zhihu.com",
        'Referer': f"https://www.zhihu.com/question/{qid}"
    }
except:
    print("questionID：")

async def answer(url_):
    async with aiohttp.ClientSession() as session:
        async with session.get(url_, headers=header) as html:
            # print(resp.status)
            response = await html.json(encoding="utf-8")
            # time.sleep(0.2)
            return response

async def get_questions(url,qid):
    html = await answer(url)
    answer_total = int(html['paging']['totals'])
    offset = 0
    #all_url = []   # 多线程用的列表
    while offset < answer_total:
        url = f"https://www.zhihu.com/api/v4/questions/{qid}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=" + str(offset) + "&platform=desktop&sort_by=default"
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

                with open("zhihu_img.txt",mode="a",encoding="utf-8") as f:
                    f.write("\n".join(img_urls)+"\n")
                # 多线程 感觉有点渣
                # all_url.append(img_urls)
                # pool = ThreadPool(1000) #线程个数
                # await pool.map(sava_image, all_url)  # 多线程工作，第一个参数是方法名
                # pool.close() #关闭pool
                # pool.join()#主进程阻塞后，让子进程继续运行完成，子进程运行完后，再把主进程全部关掉。

    # print(all_url)
                await sava_image(img_urls)

async def sava_image(img_urls):
    for img_url in img_urls:
        local_path = parse.urlsplit(img_url)[2].replace("/", "")  # 出现类似http://xxxx.com/xx/xxxx.jpg这种URL的处理
        # print(local_path)
        print(img_url)
        dir_path = 'images/'
        async with aiohttp.ClientSession() as session:  # reqs2 = requests.get(line)
            async with session.get(img_url) as reps:
                async with aiofiles.open(dir_path + local_path, mode="wb") as f:
                    await f.write(await reps.content.read())

async def main():
    url = f"https://www.zhihu.com/api/v4/questions/{qid}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&platform=desktop&sort_by=default"
    await get_questions(url,qid)

if __name__ == '__main__':
    asyncio.run(main())