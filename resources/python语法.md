- 列表推导式
    - 解释：是一种用于生成新列表的简洁语法
    - 基本语法：基本语法：列表推导式的基本形式为 [expression for item in iterable if condition]，其中 expression 是对 item 的操作，iterable 是可迭代对象，condition 是可选的过滤条件
    - 示例：
        
```python
# 使用列表推导式转换对象为 dict
data_to_save = [user.model_dump(mode='json') for user in users]
        
# 过程讲解
        
# 假设有两个 User 对象
users = [user1, user2]

# 列表推导式的执行过程相当于：
data_to_save = []  # 创建一个空列表
for user in users:  # 遍历每个 User
    # 每次循环：user.model_dump() 返回一个独立的字典
    dict_item = user.model_dump(mode='json')  # 返回 dict[str, Any]
    data_to_save.append(dict_item)  # 将字典添加到列表中

# 最终结果：
data_to_save = [
    {"name": "张三", "age": 25},  # 第一个字典
    {"name": "李四", "age": 30}   # 第二个字典
]
```
- 四大数据结构
    - Set-集合-无序不重复键值对
    - List-列表-顺序的数据集合-可放任意类型数据，但是不建议这么做
    - Dict-字典-键值对结合--类似java的 HashMap
    - Tuple--元组--类似Java的数组
    - 注意事项：集合和字典均使用花括号{}表示，但使用有差别，如d={}是创建一个空字典，若要创建一个空集合的话则要用d=set()。同样元组使用的小括号()，为避免与普通表达式混淆，在定义只有一个元素的元组时，要在元素后面加逗号如t=(88，)
    - 支持操作：for循环，in判存，len返长

- 在Python中自带json库。通过import json导入

- Python 类型提示 (Type Hints)
  - 解释：一种在代码中显式标注变量、函数参数和返回值“应该是什么类型”的机制，由Python 内置的 typing 模块 基于 使用 “: 类型” 的语法实现