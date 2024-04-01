# Collections

# namedtuple
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)

# deque

from collections import deque

q = deque()
q.append(1)
q.appendleft(0)
q.popleft()
print(q)

# Counter

from collections import Counter

counts = Counter([1, 2, 2, 3, 3, 3])
print(counts[2])

# OrderedDict

from collections import OrderedDict

ordered_dict = OrderedDict()
ordered_dict['a'] = 1
ordered_dict['b'] = 2
print(ordered_dict)

# DefaultDict

from collections import defaultdict

d = defaultdict(int)
d['a'] += 1
print(d)