# Python初学者练习题参考答案

## 第一部分：基础语法与数据类型

### 练习1：变量和基本数据类型

```python
# 定义不同类型的变量
name = "张三"
age = 25
height = 1.75
like_programming = True
favorite_colors = ['蓝色', '绿色', '红色']

# 打印变量值和类型
print(f"姓名: {name}, 类型: {type(name)}")
print(f"年龄: {age}, 类型: {type(age)}")
print(f"身高: {height}, 类型: {type(height)}")
print(f"喜欢编程: {like_programming}, 类型: {type(like_programming)}")
print(f"喜欢的颜色: {favorite_colors}, 类型: {type(favorite_colors)}")
```

### 练习2：字符串操作

```python
# 定义字符串
text = "Python是一门优秀的编程语言"

# 打印字符串长度
print(f"字符串长度: {len(text)}")

# 转换为大写
print(f"大写: {text.upper()}")

# 转换为小写
print(f"小写: {text.lower()}")

# 检查是否包含"Python"
print(f"包含'Python': {text.find('Python') != -1}")

# 按空格分割
words = text.split()
print(f"分割后的列表: {words}")

# 用"-"重新组合
new_text = "-".join(words)
print(f"重新组合: {new_text}")
```

### 练习3：数字运算

```python
# 定义两个数字
a = 15
b = 4

# 各种运算
print(f"a = {a}, b = {b}")
print(f"加法: {a} + {b} = {a + b}")
print(f"减法: {a} - {b} = {a - b}")
print(f"乘法: {a} * {b} = {a * b}")
print(f"除法: {a} / {b} = {a / b}")
print(f"整除: {a} // {b} = {a // b}")
print(f"取余: {a} % {b} = {a % b}")
print(f"幂运算: {a} ** {b} = {a ** b}")

# 保留2位小数
print(f"除法结果(保留2位小数): {round(a / b, 2)}")
```

## 第二部分：控制结构

### 练习4：条件判断

```python
def grade_score(score):
    """根据分数返回等级"""
    if 0 <= score <= 100:
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "中等"
        elif score >= 60:
            return "及格"
        else:
            return "不及格"
    else:
        return "分数无效"

# 测试函数
test_scores = [95, 85, 75, 65, 55, 105, -5]
for score in test_scores:
    print(f"分数 {score}: {grade_score(score)}")
```

### 练习5：循环结构

```python
# 1. 使用for循环打印1到10
print("1到10的数字:")
for i in range(1, 11):
    print(i, end=" ")
print()

# 2. 使用while循环计算1到100的和
sum_100 = 0
i = 1
while i <= 100:
    sum_100 += i
    i += 1
print(f"1到100的和: {sum_100}")

# 3. 打印九九乘法表（上半部分）
print("九九乘法表（上半部分）:")
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()

# 4. 找出100以内最大的能被7整除的数
max_num = 0
i = 1
while i <= 100:
    if i % 7 == 0:
        max_num = i
    i += 1
print(f"100以内最大的能被7整除的数: {max_num}")
```

### 练习6：列表操作

```python
# 创建学生成绩列表
scores = [85, 92, 78, 96, 88]

print("原始成绩:", scores)

# 计算统计信息
average = sum(scores) / len(scores)
max_score = max(scores)
min_score = min(scores)
sorted_scores = sorted(scores, reverse=True)

print(f"平均分: {average:.2f}")
print(f"最高分: {max_score}")
print(f"最低分: {min_score}")
print(f"成绩排序: {sorted_scores}")

# 添加新学生成绩
scores.append(90)
print(f"添加新成绩后: {scores}")

# 删除最低分
scores.remove(min_score)
print(f"删除最低分后: {scores}")

# 统计及格人数
pass_count = sum(1 for score in scores if score >= 60)
print(f"及格人数: {pass_count}")
```

## 第三部分：函数

### 练习7：函数定义

```python
import math

def calculate_area(radius):
    """计算圆的面积"""
    return math.pi * radius ** 2

def is_prime(n):
    """判断一个数是否为质数"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def reverse_string(text):
    """反转字符串"""
    return text[::-1]

def find_max(numbers):
    """找出列表中的最大值"""
    if not numbers:
        return None
    return max(numbers)

def count_vowels(text):
    """统计字符串中元音字母的个数"""
    vowels = 'aeiouAEIOU'
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

# 测试函数
print(f"圆的面积 (半径=5): {calculate_area(5):.2f}")
print(f"17是质数: {is_prime(17)}")
print(f"反转'hello': {reverse_string('hello')}")
print(f"最大值 [1, 5, 3, 9, 2]: {find_max([1, 5, 3, 9, 2])}")
print(f"元音字母个数 'hello world': {count_vowels('hello world')}")
```

### 练习8：函数进阶

```python
def calculator(operation='+', a=0, b=0):
    """简单计算器函数"""
    try:
        if operation == '+':
            return a + b
        elif operation == '-':
            return a - b
        elif operation == '*':
            return a * b
        elif operation == '/':
            if b == 0:
                return "错误：除数不能为零"
            return a / b
        else:
            return "错误：不支持的运算"
    except Exception as e:
        return f"计算错误: {e}"

# 测试计算器
print(calculator('+', 10, 5))
print(calculator('-', 10, 5))
print(calculator('*', 10, 5))
print(calculator('/', 10, 5))
print(calculator('/', 10, 0))  # 测试除零错误
print(calculator('^', 10, 5))  # 测试不支持的操作
```

## 第四部分：文件操作

### 练习9：文件读写

```python
def write_diary(entry):
    """将日记内容写入文件"""
    with open('diary.txt', 'a', encoding='utf-8') as f:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {entry}\n")

def read_diary():
    """读取并显示所有日记"""
    try:
        with open('diary.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            if content:
                print("所有日记:")
                print(content)
            else:
                print("日记文件为空")
    except FileNotFoundError:
        print("日记文件不存在")

def search_diary(keyword):
    """搜索包含关键词的日记"""
    try:
        with open('diary.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            found_entries = []
            for line in lines:
                if keyword.lower() in line.lower():
                    found_entries.append(line.strip())
            
            if found_entries:
                print(f"包含关键词 '{keyword}' 的日记:")
                for entry in found_entries:
                    print(entry)
            else:
                print(f"没有找到包含关键词 '{keyword}' 的日记")
    except FileNotFoundError:
        print("日记文件不存在")

# 测试日记功能
write_diary("今天学习了Python编程，感觉很有趣！")
write_diary("完成了文件操作的练习，掌握了with语句的使用。")
read_diary()
search_diary("Python")
```

## 第五部分：异常处理

### 练习11：异常处理

```python
def safe_divide(a, b):
    """安全的除法运算"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "错误：除数不能为零"
    except TypeError:
        return "错误：参数类型不正确"
    except Exception as e:
        return f"未知错误: {e}"

def safe_int_input():
    """安全地获取用户输入的整数"""
    while True:
        try:
            user_input = input("请输入一个整数: ")
            return int(user_input)
        except ValueError:
            print("输入无效，请输入一个整数")
        except KeyboardInterrupt:
            print("\n程序被用户中断")
            return None

def read_file_safe(filename):
    """安全地读取文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    except FileNotFoundError:
        return f"错误：文件 '{filename}' 不存在"
    except PermissionError:
        return f"错误：没有权限读取文件 '{filename}'"
    except UnicodeDecodeError:
        return f"错误：文件 '{filename}' 编码格式不正确"
    except Exception as e:
        return f"未知错误: {e}"

# 测试异常处理
print("测试安全除法:")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("10", 2))

print("\n测试文件读取:")
print(read_file_safe('nonexistent.txt'))
```

## 第六部分：综合项目

### 练习12：简单游戏

```python
import random

def guess_number_game():
    """猜数字游戏"""
    while True:
        # 生成随机数
        target = random.randint(1, 100)
        attempts = 0
        
        print("\n=== 猜数字游戏 ===")
        print("我已经想好了一个1-100之间的数字，请你来猜！")
        
        while True:
            try:
                guess = int(input("请输入你的猜测: "))
                attempts += 1
                
                if guess < target:
                    print("太小了，再大一点！")
                elif guess > target:
                    print("太大了，再小一点！")
                else:
                    print(f"恭喜你猜对了！答案就是 {target}")
                    print(f"你总共猜了 {attempts} 次")
                    break
                    
            except ValueError:
                print("请输入有效的数字！")
                continue
            except KeyboardInterrupt:
                print("\n游戏被中断")
                return
        
        # 询问是否继续
        play_again = input("是否继续游戏？(y/n): ").lower()
        if play_again != 'y':
            print("谢谢参与，再见！")
            break

# 运行游戏
if __name__ == "__main__":
    guess_number_game()
```

## 第七部分：进阶挑战

### 练习14：面向对象编程

```python
class BankAccount:
    """银行账户类"""
    
    def __init__(self, account_number, name, balance=0):
        self.account_number = account_number
        self.name = name
        self.balance = balance
        print(f"账户 {account_number} 创建成功，户主: {name}")
    
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.balance += amount
            print(f"存款成功: +{amount:.2f}，当前余额: {self.balance:.2f}")
            return True
        else:
            print("存款金额必须大于0")
            return False
    
    def withdraw(self, amount):
        """取款"""
        if amount <= 0:
            print("取款金额必须大于0")
            return False
        
        if self.balance >= amount:
            self.balance -= amount
            print(f"取款成功: -{amount:.2f}，当前余额: {self.balance:.2f}")
            return True
        else:
            print(f"余额不足，当前余额: {self.balance:.2f}")
            return False
    
    def get_balance(self):
        """查询余额"""
        print(f"账户 {self.account_number} 当前余额: {self.balance:.2f}")
        return self.balance
    
    def __str__(self):
        return f"账户号: {self.account_number}, 户主: {self.name}, 余额: {self.balance:.2f}"

# 测试银行账户
def test_bank_account():
    # 创建账户
    account1 = BankAccount("001", "张三", 1000)
    account2 = BankAccount("002", "李四", 500)
    
    print("\n=== 账户操作测试 ===")
    
    # 存款测试
    account1.deposit(500)
    account2.deposit(1000)
    
    # 取款测试
    account1.withdraw(200)
    account2.withdraw(800)
    
    # 余额不足测试
    account1.withdraw(2000)
    
    # 查询余额
    account1.get_balance()
    account2.get_balance()
    
    # 打印账户信息
    print("\n账户信息:")
    print(account1)
    print(account2)

# 运行测试
if __name__ == "__main__":
    test_bank_account()
```

---

## 总结

恭喜你完成了所有练习题！通过这些练习，你已经掌握了：

1. **基础语法**：变量、数据类型、运算符
2. **控制结构**：条件判断、循环
3. **函数编程**：函数定义、参数传递、返回值
4. **文件操作**：读写文件、CSV处理
5. **异常处理**：try-except结构
6. **面向对象**：类定义、方法、属性

### 下一步建议

1. **深入学习**：学习更多Python标准库
2. **项目实践**：尝试开发小项目
3. **框架学习**：学习Django、Flask等Web框架
4. **数据处理**：学习pandas、numpy等库
5. **算法练习**：在LeetCode等平台练习算法

**记住：编程是一门实践的艺术，继续练习，你一定会成为优秀的Python程序员！** 