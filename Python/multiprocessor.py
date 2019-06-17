
# coding: utf-8

# In[ ]:


'''
Python Multiprocessing 패키지로 분산처리

주의: Jupyter Notebook에서는 사용 불가!
'''

from multiprocessing import Pool


def f(x):
    return x*x

if __name__ == '__main__':
    p = Pool(5)
    print(p.map(f, [1, 2, 3]))

