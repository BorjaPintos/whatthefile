from multiprocessing import JoinableQueue


class Queue:

    def __init__(self):
        self._queue = JoinableQueue()

    def put(self, element):
        if self._queue is not None:
            self._queue.put(element)

    def get(self):
        if self._queue is not None:
            try:
                return self._queue.get()
            except:
                return None

    def join(self):
        if self._queue is not None:
            self._queue.join()

    def task_done(self):
        if self._queue is not None:
            self._queue.task_done()

    def unblock_gets(self):
        if self._queue is not None:
            self._queue.close()
            self._queue = JoinableQueue()