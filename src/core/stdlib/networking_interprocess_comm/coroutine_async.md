# *协程 & 异步编程*

> 异步非阻塞 asyncio
>
> 使用异步框架提升性能，如 Tornado, FastAPI, Django3.x asgi, aiohttp...
> 
> 示例:
> 
> 1. 协程
>
> 2. asyncio 模块
> 
> 3. 实战
>

<br>

# 1 [协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id3)

协程不是计算机提供，程序员人为创造。

协程（Coroutine），也可以被称为微线程，是一种用户态内的上下文切换技术。简而言之，其实就是通过一个线程实现代码块相互切换执行。例如：

```python
def func1():
    print(1)
    ...
    print(1)

def func2():
    print(2)
    ...
    print(2)

func1()
func2()
```

实现协程的方法
- greenlet
- yield 关键字, python 生成器实现
- asyncio 标准库（>=python3.4）, python 装饰器实现
- async, await 关键字（>=python3.5）

## 1.1 `greenlet` 实现协程
```python
from greenlet import greenlet


def func1():
    print(1, '-' * 10)      # step2: 打印 1
    gr2.switch()            # step3: 切换到函数 func2
    print(2, '-' * 10)      # step6: 从 func2 返回后继续执行
    gr2.switch()            # step7: 切换到 func2, 从上次执行的位置继续向后执行


def func2():
    print(3, '-' * 10)      # step4: 打印 3
    gr1.switch()            # step5: 切换到函数 func1 上次执行的位置继续向后执行
    print(4, '-' * 10)      # step8：打印 4


if __name__ == '__main__':
    ''' 1. greenlet 实现协程 '''
    gr1 = greenlet(func1)   # 使用 greenlet 封装函数对象
    gr2 = greenlet(func2)
    gr1.switch()            # step1: 执行 func1()
```
*Output*:
```text
1
3
2
4
```

## 1.2 `yeild` 关键字实现协程
```python
def func1_yield():
    yield 1                             # step1
    yield from func2_yield()            # step2 跳转 func2_yield()
    yield 2                             # step5


def func2_yield():
    yield 3                             # step3
    yield 4                             # step4


if __name__ == '__main__':
    ''' 2. yield 实现（python 生成器）'''
    yield_1 = func1_yield()             # 调用生成器函数返回生成器
    for item in yield_1:                # 遍历此生成器返回值
        print(item, '-' * 10)
```
*Output*:
```text
1
3
4
2
```

## 1.3 `asyncio` 实现协程(>=python3.4)
```python
@asyncio.coroutine  # "@coroutine" decorator is deprecated since Python 3.8, use "async def" instead
def func1_asyncio():
    print(1)                        # step1: 打印 1
    yield from asyncio.sleep(2)     # step2: 遇到 I/O 耗时操作，自动切换到 tasks 列表中的其他任务
    print(2)                        # step5: 打印 1


@asyncio.coroutine
def func2_asyncio():
    print(3)                        # step3: 打印 3
    yield from asyncio.sleep(2)     # step4: 遇到 I/O 耗时操作，自动切换到 tasks 列表中的其他任务
    print(4)                        # step6: 打印 4


if __name__ == '__main__':
    ''' 3. asyncio 实现协程 '''
    asyncio_tasks = [
        asyncio.ensure_future(func1_asyncio()),
        asyncio.ensure_future(func2_asyncio())
    ]
    asyncio_loop = asyncio.get_event_loop()
    asyncio_loop.run_until_complete(asyncio.wait(asyncio_tasks))  # 随机执行任务列表中的函数，无固定顺序
```
*Output*:
```text
1
3
2
4
```
- Note: 
  - `asyncio` 模块在遇到 I/O 阻塞时会自动进行切换
  - `@coroutine` decorator is deprecated since Python 3.8, use "async def" instead

## 1.4 `async` & `await` 关键字实现协程
```python
async def func1_async():
    print(1)                        # step1: 打印 1
    await asyncio.sleep(2)          # step2: 遇到 I/O 耗时操作，自动切换到 tasks 列表中的其他任务
    print(2)                        # step5: 打印 1


async def func2_async():
    print(3)                        # step3: 打印 3
    await asyncio.sleep(2)          # step4: 遇到 I/O 耗时操作，自动切换到 tasks 列表中的其他任务
    print(4)                        # step6: 打印 4


if __name__ == '__main__':
    ''' 4. async & await 关键字实现协程 '''
    async_tasks = [
        asyncio.ensure_future(func1_async()),
        asyncio.ensure_future(func2_async())
    ]
    asyncio_loop = asyncio.get_event_loop()
    asyncio_loop.run_until_complete(asyncio.wait(async_tasks))  # 随机执行任务列表中的函数，无固定顺序
```


# 2 协程意义

通常在Python中我们进行并发编程一般都是使用多线程或者多进程来实现的，对于 CPU 计算密集型任务由于 GIL 的存在通常使用多进程来实现，而对于 I/O 密集型任务可以通过线程调度来让线程在执行 I/O 任务时让出 GIL，从而实现表面上的并发。

其实对于 I/O 密集型任务我们还有一种选择就是协程。

协程，又称微线程，英文名 *Coroutine*，是运行在单线程中的“并发”，协程相比多线程的一大优势就是省去了多线程之间的切换开销，获得了更高的运行效率。Python 中的异步 I/O 模块 `asyncio` (Lib/asyncio/coroutines.py) 就是基本的协程模块。

- 普通方式下载图片（同步）
- 
- 使用协程下载图片（异步）
```python
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
    
    for _ in urls:
        regular_download(_)

    time.sleep(2)
    print('-' * 80)

    asyncio.run(coroutine_download())

```
