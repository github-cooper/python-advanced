"""
- Project: python-crash-course
- File:    demo.py
- Date:    2023/10/31 21:02
- Author:  WANGHUI
- Desc:    Coroutine Demo
"""
import asyncio
import time

import aiohttp
import requests


def regular_download(url: str):
    """ 常规方式从网络下载内容
    Args:
        url:

    Returns:

    """
    print("Start downloading.")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    response = requests.get(url, headers)
    file_name = url.split("/")[-1]
    with open(file_name, mode="wb") as f:
        f.write(response.content)
    print(f"[{file_name}] end downloading.")


async def coroutine_fetch(session, url):
    """ 借助第三方模块 aiohttp 使用协程方式下载
    Args:
        session:
        url:

    Returns:

    """
    print("Sending download requests: ", url)
    # async with session.get(url, verify_ssl=False) as response:
    async with session.get(url) as response:
        content = await response.content.read()
        file_name = f"c-{url.split('/')[-1]}"
        with open(file_name, mode="wb") as f:
            f.write(content)
        print("End downloading: ", file_name)


async def coroutine_download():
    async with aiohttp.ClientSession(trust_env=True) as session:
        urls = [
            "https://bing.com/th?id=OHR.HalloweenCuteAI_ZH-CN1079713117_1920x1080.jpg",
            "https://w.wallhaven.cc/full/d6/wallhaven-d6o77l.jpg",
            "https://w.wallhaven.cc/full/jx/wallhaven-jxyopy.png",
            "https://w.wallhaven.cc/full/ex/wallhaven-ex9gwo.png"
        ]
        tasks = [asyncio.create_task(coroutine_fetch(session, url)) for url in urls]
        await asyncio.wait(tasks)


if __name__ == '__main__':
    urls = [
        "https://bing.com/th?id=OHR.HalloweenCuteAI_ZH-CN1079713117_1920x1080.jpg",
        "https://w.wallhaven.cc/full/d6/wallhaven-d6o77l.jpg",
        "https://w.wallhaven.cc/full/jx/wallhaven-jxyopy.png",
        "https://w.wallhaven.cc/full/ex/wallhaven-ex9gwo.png"
    ]

    time.sleep(2)
    print('-' * 80)

    asyncio.run(coroutine_download())
