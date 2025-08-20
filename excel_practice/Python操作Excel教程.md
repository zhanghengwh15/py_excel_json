# Python操作Excel教程

## 目录
1. [Excel操作库介绍](#1-excel操作库介绍)
2. [openpyxl库详解](#2-openpyxl库详解)
3. [pandas库操作Excel](#3-pandas库操作excel)
4. [xlrd/xlwt库](#4-xlrdxlwt库)
5. [实际案例](#5-实际案例)
6. [最佳实践](#6-最佳实践)
7. [常见问题解决](#7-常见问题解决)

## 1. Excel操作库介绍

### 1.1 主流库对比

| 库名 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **openpyxl** | 功能强大、支持新格式、读写操作完整 | 内存占用较大 | 现代Excel文件(.xlsx) |
| **pandas** | 数据处理能力强、语法简洁 | 对Excel格式支持有限 | 数据分析、批量处理 |
| **xlrd/xlwt** | 轻量级、速度快 | 不支持.xlsx格式 | 旧版Excel文件(.xls) |
| **xlsxwriter** | 写入性能好、格式控制精确 | 只支持写入 | 生成报表、模板 |

### 1.2 安装依赖

```bash
# 安装主要库
pip install openpyxl pandas xlrd xlwt xlsxwriter

# 或者使用requirements.txt
pip install -r requirements.txt
```

## 2. openpyxl库详解

### 2.1 基础操作

#### 2.1.1 创建工作簿和工作表

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

# 创建工作簿
wb = Workbook()

# 获取活动工作表
ws = wb.active
ws.title = "数据表"

# 创建新的工作表
ws2 = wb.create_sheet("统计表", 1)  # 插入到第二个位置
```

#### 2.1.2 写入数据

```python
# 写入单个单元格
ws['A1'] = "姓名"
ws['B1'] = "年龄"
ws['C1'] = "成绩"

# 写入多行数据
data = [
    ["张三", 18, 85],
    ["李四", 19, 92],
    ["王五", 18, 78]
]

for row in data:
    ws.append(row)

# 使用坐标写入
ws.cell(row=5, column=1, value="赵六")
ws.cell(row=5, column=2, value=20)
ws.cell(row=5, column=3, value=88)
```

#### 2.1.3 读取数据

```python
from openpyxl import load_workbook

# 加载现有工作簿
wb = load_workbook('data.xlsx')

# 获取工作表
ws = wb['数据表']

# 读取单元格值
cell_value = ws['A1'].value
print(f"A1单元格的值: {cell_value}")

# 读取整行
row_data = []
for cell in ws[1]:  # 第一行
    row_data.append(cell.value)
print(f"第一行数据: {row_data}")

# 读取整列
col_data = []
for cell in ws['A']:  # A列
    col_data.append(cell.value)
print(f"A列数据: {col_data}")

# 读取指定范围
for row in ws.iter_rows(min_row=2, max_row=5, min_col=1, max_col=3):
    for cell in row:
        print(cell.value, end='\t')
    print()
```

### 2.2 格式设置

#### 2.2.1 字体和样式

```python
# 设置字体
header_font = Font(name='微软雅黑', size=12, bold=True, color="FF0000")
ws['A1'].font = header_font

# 设置填充颜色
header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
ws['A1'].fill = header_fill

# 设置对齐方式
header_alignment = Alignment(horizontal="center", vertical="center")
ws['A1'].alignment = header_alignment

# 合并单元格
ws.merge_cells('A1:C1')
```

#### 2.2.2 列宽和行高

```python
# 设置列宽
ws.column_dimensions['A'].width = 15
ws.column_dimensions['B'].width = 10
ws.column_dimensions['C'].width = 12

# 设置行高
ws.row_dimensions[1].height = 25
```

### 2.3 保存文件

```python
# 保存工作簿
wb.save('output.xlsx')

# 注意：保存后工作簿对象会被关闭
# 如果需要继续操作，需要重新加载
```

## 3. pandas库操作Excel

### 3.1 读取Excel文件

```python
import pandas as pd

# 读取Excel文件
df = pd.read_excel('data.xlsx', sheet_name='数据表')

# 指定列名
df = pd.read_excel('data.xlsx', sheet_name=0, header=0)

# 跳过行
df = pd.read_excel('data.xlsx', skiprows=2)

# 只读取指定列
df = pd.read_excel('data.xlsx', usecols=['A', 'B', 'C'])

# 读取多个工作表
all_sheets = pd.read_excel('data.xlsx', sheet_name=None)
```

### 3.2 数据处理

```python
# 查看数据基本信息
print(df.info())
print(df.describe())

# 数据筛选
filtered_df = df[df['成绩'] > 80]

# 数据排序
sorted_df = df.sort_values('成绩', ascending=False)

# 数据分组统计
grouped = df.groupby('年龄')['成绩'].mean()

# 数据透视表
pivot_table = df.pivot_table(index='年龄', columns='姓名', values='成绩', aggfunc='mean')
```

### 3.3 写入Excel文件

```python
# 写入单个工作表
df.to_excel('output.xlsx', sheet_name='处理结果', index=False)

# 写入多个工作表
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='原始数据', index=False)
    filtered_df.to_excel(writer, sheet_name='筛选结果', index=False)
    grouped.to_excel(writer, sheet_name='统计结果')
```

## 4. xlrd/xlwt库

### 4.1 读取旧版Excel文件

```python
import xlrd

# 打开工作簿
workbook = xlrd.open_workbook('old_data.xls')

# 获取工作表
sheet = workbook.sheet_by_index(0)  # 第一个工作表
sheet = workbook.sheet_by_name('数据表')

# 读取单元格
cell_value = sheet.cell_value(0, 0)  # 第一行第一列

# 读取整行
row_values = sheet.row_values(0)

# 读取整列
col_values = sheet.col_values(0)
```

### 4.2 写入旧版Excel文件

```python
import xlwt

# 创建工作簿
workbook = xlwt.Workbook()

# 创建工作表
worksheet = workbook.add_sheet('数据表')

# 写入数据
worksheet.write(0, 0, '姓名')
worksheet.write(0, 1, '年龄')
worksheet.write(0, 2, '成绩')

# 保存文件
workbook.save('output.xls')
```

## 5. 实际案例

### 5.1 学生成绩管理系统

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import pandas as pd

class StudentGradeManager:
    def __init__(self, filename):
        self.filename = filename
        self.wb = None
        self.ws = None
    
    def create_template(self):
        """创建成绩表模板"""
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "学生成绩表"
        
        # 设置表头
        headers = ["学号", "姓名", "语文", "数学", "英语", "总分", "平均分", "排名"]
        for col, header in enumerate(headers, 1):
            cell = self.ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="CCCCCC", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        # 设置列宽
        column_widths = [10, 12, 10, 10, 10, 10, 10, 8]
        for col, width in enumerate(column_widths, 1):
            self.ws.column_dimensions[get_column_letter(col)].width = width
        
        self.save()
    
    def add_student(self, student_id, name, chinese, math, english):
        """添加学生成绩"""
        if not self.wb:
            self.load_workbook()
        
        # 计算总分和平均分
        total = chinese + math + english
        average = round(total / 3, 2)
        
        # 找到下一行
        next_row = self.ws.max_row + 1
        
        # 写入数据
        data = [student_id, name, chinese, math, english, total, average, ""]
        for col, value in enumerate(data, 1):
            self.ws.cell(row=next_row, column=col, value=value)
        
        self.save()
    
    def calculate_ranking(self):
        """计算排名"""
        if not self.wb:
            self.load_workbook()
        
        # 读取所有数据（跳过表头）
        data = []
        for row in range(2, self.ws.max_row + 1):
            student_id = self.ws.cell(row=row, column=1).value
            total = self.ws.cell(row=row, column=6).value
            data.append((row, student_id, total))
        
        # 按总分排序
        data.sort(key=lambda x: x[2], reverse=True)
        
        # 写入排名
        for rank, (row, student_id, total) in enumerate(data, 1):
            self.ws.cell(row=row, column=8, value=rank)
        
        self.save()
    
    def generate_report(self):
        """生成统计报告"""
        if not self.wb:
            self.load_workbook()
        
        # 使用pandas读取数据进行分析
        df = pd.read_excel(self.filename, sheet_name='学生成绩表')
        
        # 创建统计工作表
        if '统计报告' in self.wb.sheetnames:
            self.wb.remove(self.wb['统计报告'])
        
        ws_report = self.wb.create_sheet('统计报告')
        
        # 写入统计信息
        stats = [
            ["统计项目", "数值"],
            ["总人数", len(df)],
            ["语文平均分", round(df['语文'].mean(), 2)],
            ["数学平均分", round(df['数学'].mean(), 2)],
            ["英语平均分", round(df['英语'].mean(), 2)],
            ["总分平均分", round(df['总分'].mean(), 2)],
            ["最高分", df['总分'].max()],
            ["最低分", df['总分'].min()]
        ]
        
        for row, (item, value) in enumerate(stats, 1):
            ws_report.cell(row=row, column=1, value=item)
            ws_report.cell(row=row, column=2, value=value)
        
        self.save()
    
    def load_workbook(self):
        """加载工作簿"""
        try:
            self.wb = openpyxl.load_workbook(self.filename)
            self.ws = self.wb['学生成绩表']
        except FileNotFoundError:
            print(f"文件 {self.filename} 不存在，请先创建模板")
    
    def save(self):
        """保存文件"""
        self.wb.save(self.filename)

# 使用示例
if __name__ == "__main__":
    manager = StudentGradeManager('学生成绩.xlsx')
    
    # 创建模板
    manager.create_template()
    
    # 添加学生数据
    students = [
        ("001", "张三", 85, 92, 78),
        ("002", "李四", 92, 88, 95),
        ("003", "王五", 78, 85, 82),
        ("004", "赵六", 95, 90, 88),
        ("005", "钱七", 88, 92, 85)
    ]
    
    for student in students:
        manager.add_student(*student)
    
    # 计算排名
    manager.calculate_ranking()
    
    # 生成报告
    manager.generate_report()
    
    print("学生成绩表创建完成！")
```

### 5.2 批量处理Excel文件

```python
import os
import pandas as pd
from openpyxl import load_workbook
import glob

class ExcelBatchProcessor:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def merge_excel_files(self, pattern="*.xlsx"):
        """合并多个Excel文件"""
        # 获取所有匹配的文件
        files = glob.glob(os.path.join(self.input_dir, pattern))
        
        if not files:
            print(f"在 {self.input_dir} 中没有找到 {pattern} 文件")
            return
        
        # 读取所有文件
        all_data = []
        for file in files:
            try:
                df = pd.read_excel(file)
                df['来源文件'] = os.path.basename(file)
                all_data.append(df)
                print(f"已读取: {file}")
            except Exception as e:
                print(f"读取文件 {file} 时出错: {e}")
        
        if all_data:
            # 合并数据
            merged_df = pd.concat(all_data, ignore_index=True)
            
            # 保存合并后的文件
            output_file = os.path.join(self.output_dir, '合并结果.xlsx')
            merged_df.to_excel(output_file, index=False)
            print(f"合并完成，保存至: {output_file}")
            
            return merged_df
        else:
            print("没有成功读取任何文件")
            return None
    
    def split_excel_by_column(self, input_file, split_column, output_prefix="分表"):
        """按列值分割Excel文件"""
        try:
            df = pd.read_excel(input_file)
            
            if split_column not in df.columns:
                print(f"列 '{split_column}' 不存在")
                return
            
            # 获取唯一值
            unique_values = df[split_column].unique()
            
            # 按值分割并保存
            for value in unique_values:
                if pd.isna(value):
                    continue
                
                # 筛选数据
                subset = df[df[split_column] == value]
                
                # 生成文件名
                safe_value = str(value).replace('/', '_').replace('\\', '_')
                output_file = os.path.join(self.output_dir, f"{output_prefix}_{safe_value}.xlsx")
                
                # 保存文件
                subset.to_excel(output_file, index=False)
                print(f"已保存: {output_file} (记录数: {len(subset)})")
        
        except Exception as e:
            print(f"处理文件时出错: {e}")
    
    def add_summary_sheet(self, input_file, output_file=None):
        """为Excel文件添加汇总表"""
        if output_file is None:
            output_file = input_file
        
        try:
            # 读取Excel文件
            wb = load_workbook(input_file)
            
            # 创建汇总表
            if '汇总' in wb.sheetnames:
                wb.remove(wb['汇总'])
            
            ws_summary = wb.create_sheet('汇总')
            
            # 为每个工作表创建汇总信息
            summary_data = [["工作表名", "行数", "列数", "数据范围"]]
            
            for sheet_name in wb.sheetnames:
                if sheet_name == '汇总':
                    continue
                
                ws = wb[sheet_name]
                row_count = ws.max_row
                col_count = ws.max_column
                data_range = f"A1:{get_column_letter(col_count)}{row_count}"
                
                summary_data.append([sheet_name, row_count, col_count, data_range])
            
            # 写入汇总数据
            for row, data in enumerate(summary_data, 1):
                for col, value in enumerate(data, 1):
                    ws_summary.cell(row=row, column=col, value=value)
            
            # 保存文件
            wb.save(output_file)
            print(f"汇总表已添加到: {output_file}")
        
        except Exception as e:
            print(f"添加汇总表时出错: {e}")

# 使用示例
if __name__ == "__main__":
    # 设置目录
    input_dir = "input_excel"
    output_dir = "output_excel"
    
    processor = ExcelBatchProcessor(input_dir, output_dir)
    
    # 合并Excel文件
    merged_data = processor.merge_excel_files()
    
    if merged_data is not None:
        # 按来源文件分割
        processor.split_excel_by_column(
            os.path.join(output_dir, '合并结果.xlsx'),
            '来源文件',
            '按文件分割'
        )
        
        # 添加汇总表
        processor.add_summary_sheet(
            os.path.join(output_dir, '合并结果.xlsx')
        )
```

## 6. 最佳实践

### 6.1 性能优化

```python
# 1. 批量写入数据
def batch_write_data(ws, data, start_row=1):
    """批量写入数据，提高性能"""
    for row_idx, row_data in enumerate(data, start_row):
        for col_idx, value in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=value)

# 2. 使用生成器处理大文件
def read_large_excel(filename, chunk_size=1000):
    """分块读取大Excel文件"""
    for chunk in pd.read_excel(filename, chunksize=chunk_size):
        yield chunk

# 3. 避免重复打开文件
class ExcelHandler:
    def __init__(self, filename):
        self.filename = filename
        self._wb = None
    
    @property
    def workbook(self):
        if self._wb is None:
            self._wb = load_workbook(self.filename)
        return self._wb
    
    def save(self):
        if self._wb:
            self._wb.save(self.filename)
    
    def close(self):
        if self._wb:
            self._wb.close()
            self._wb = None
```

### 6.2 错误处理

```python
import logging
from pathlib import Path

def safe_excel_operation(func):
    """Excel操作的安全装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logging.error(f"文件未找到: {e}")
            raise
        except PermissionError as e:
            logging.error(f"文件被占用，无法访问: {e}")
            raise
        except Exception as e:
            logging.error(f"Excel操作失败: {e}")
            raise
    return wrapper

@safe_excel_operation
def read_excel_safe(filename):
    """安全读取Excel文件"""
    if not Path(filename).exists():
        raise FileNotFoundError(f"文件 {filename} 不存在")
    
    return pd.read_excel(filename)
```

### 6.3 数据验证

```python
def validate_excel_data(df, required_columns, data_types):
    """验证Excel数据格式"""
    errors = []
    
    # 检查必需列
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        errors.append(f"缺少必需列: {missing_columns}")
    
    # 检查数据类型
    for col, expected_type in data_types.items():
        if col in df.columns:
            actual_type = str(df[col].dtype)
            if expected_type not in actual_type:
                errors.append(f"列 {col} 数据类型不匹配，期望: {expected_type}，实际: {actual_type}")
    
    # 检查空值
    for col in required_columns:
        if col in df.columns and df[col].isnull().any():
            null_count = df[col].isnull().sum()
            errors.append(f"列 {col} 包含 {null_count} 个空值")
    
    return errors

# 使用示例
required_cols = ['姓名', '年龄', '成绩']
expected_types = {'姓名': 'object', '年龄': 'int64', '成绩': 'float64'}

df = pd.read_excel('data.xlsx')
validation_errors = validate_excel_data(df, required_cols, expected_types)

if validation_errors:
    print("数据验证失败:")
    for error in validation_errors:
        print(f"- {error}")
else:
    print("数据验证通过")
```

## 7. 常见问题解决

### 7.1 文件格式问题

```python
# 问题：无法读取.xls文件
# 解决：使用xlrd库
import xlrd
workbook = xlrd.open_workbook('file.xls')

# 问题：无法写入.xlsx文件
# 解决：确保使用openpyxl引擎
df.to_excel('output.xlsx', engine='openpyxl')
```

### 7.2 内存问题

```python
# 问题：大文件占用内存过多
# 解决：分块读取
def process_large_file(filename):
    chunk_size = 1000
    for chunk in pd.read_excel(filename, chunksize=chunk_size):
        # 处理每个数据块
        process_chunk(chunk)
        del chunk  # 释放内存
```

### 7.3 编码问题

```python
# 问题：中文显示乱码
# 解决：指定编码
df = pd.read_excel('file.xlsx', encoding='utf-8')

# 写入时指定编码
df.to_excel('output.xlsx', encoding='utf-8')
```

### 7.4 日期格式问题

```python
# 问题：日期格式不正确
# 解决：指定日期列
df = pd.read_excel('file.xlsx', parse_dates=['日期列'])

# 或者手动转换
df['日期列'] = pd.to_datetime(df['日期列'])
```

## 总结

本教程涵盖了Python操作Excel的主要方法和最佳实践：

1. **选择合适的库**：根据需求选择openpyxl、pandas等
2. **掌握基础操作**：读写、格式设置、数据处理
3. **学习实际案例**：学生成绩管理、批量处理等
4. **遵循最佳实践**：性能优化、错误处理、数据验证
5. **解决常见问题**：格式、内存、编码、日期等问题

通过本教程的学习，您应该能够熟练使用Python处理各种Excel文件，并能够根据实际需求选择合适的工具和方法。

## 练习建议

1. 尝试创建自己的Excel模板
2. 处理实际的数据文件
3. 实现数据分析和可视化
4. 构建自动化报表系统
5. 处理复杂的Excel公式和图表

记住：实践是最好的学习方式，多动手操作才能真正掌握这些技能！
