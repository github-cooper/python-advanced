"""
- Project: python-crash-course
- File:    coroutine.py
- Date:    2023/10/30 20:57
- Author:  WANGHUI
- Desc:    Coroutine / 协程实现
"""
import asyncio

from greenlet import greenlet


def split_line():
    print('-' * 80)


def func1_greenlet():
    print(1)            # step2: 打印 1
    gr2.switch()        # step3: 切换到函数 func2
    print(2)            # step6: 从 func2 返回后继续执行
    gr2.switch()        # step7: 切换到 func2, 从上次执行的位置继续向后执行


def func2_greenlet():
    print(3)            # step4: 打印 3
    gr1.switch()        # step5: 切换到函数 func1 上次执行的位置继续向后执行
    print(4)            # step8：打印 4


def func1_yield():
    yield 1                     # step1: 返回 1
    yield from func2_yield()    # step2 切换到函数 func2_yield()
    yield 2                     # step5: 返回 2


def func2_yield():
    yield 3                     # step3: 返回 3
    yield 4                     # step4: 返回 4


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


def func3():
    """ 执行单个 @asyncio.coroutine 协程函数 """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func1_asyncio())


async def func1_async():
    print(1)                        # step1: 打印 1
    await asyncio.sleep(2)          # step2: 遇到 I/O 耗时操作，自动切换到 tasks 列表中的其他任务
    print(2)                        # step5: 打印 1


async def func2_async():
    print(3)                        # step3: 打印 3
    await asyncio.sleep(2)          # step4: 遇到 I/O 耗时操作，自动切换到 tasks 列表中的其他任务
    print(4)                        # step6: 打印 4


if __name__ == '__main__':
    ''' 1. greenlet 实现协程 '''
    gr1 = greenlet(func1_greenlet)      # 使用 greenlet 封装函数对象
    gr2 = greenlet(func2_greenlet)
    gr1.switch()                        # step1: 执行 func1()
    split_line()

    ''' 2. yield 实现协程（python 生成器）'''
    yield_1 = func1_yield()             # 调用生成器函数返回生成器
    for item in yield_1:                # 遍历此生成器返回值
        print(item)
    split_line()

    ''' 3. asyncio 实现协程，在遇到 I/O 阻塞时会自动进行切换 '''
    asyncio_tasks = [
        asyncio.ensure_future(func1_asyncio()),
        asyncio.ensure_future(func2_asyncio())
    ]
    asyncio_loop = asyncio.get_event_loop()
    asyncio_loop.run_until_complete(asyncio.wait(asyncio_tasks))  # 随机执行任务列表中的函数，无固定顺序
    split_line()

    ''' 4. async & await 关键字实现协程 '''
    async_tasks = [
        asyncio.ensure_future(func1_async()),
        asyncio.ensure_future(func2_async())
    ]
    asyncio_loop = asyncio.get_event_loop()
    asyncio_loop.run_until_complete(asyncio.wait(async_tasks))  # 随机执行任务列表中的函数，无固定顺序
    split_line()
