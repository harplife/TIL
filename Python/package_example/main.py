'''
Using examples from an article explaining __init__.
link: https://towardsdatascience.com/whats-init-for-me-d70a312da583
'''

# the "online shopping" approach,
# __init__ doesn't do much
from expackage import foo
from expackage import bar
from expackage import baz

foo.foo_func()
bar.bar_func()
baz.baz_func()

# the "general store" approach,
# modules are imported at __init__
import expackage
expackage.foo_func()
expackage.bar_func()
expackage.baz_func()

# pd is imported at __init__,
# and it has become an attribute of the package
temp = [
    {'a': 1, 'b': 2, 'c': 3, 'd': 4},
    {'a': 5, 'b': 6, 'c': 7, 'd': 8}
    ]
df = expackage.pd.DataFrame(temp)
print(df)
