# 齐禾Miseq-IGDB二代测序数据分析脚本 - 用户指南

## 概述

齐禾Miseq-IGDB二代测序数据分析脚本是一个结合了文件分类和数据整理功能的综合工具。它首先将输入的数据文件按照文件名分类放入对应文件夹，然后处理每个文件夹中的数据以得到编辑效率和InDel结果。

## 使用前置条件

### 1. 安装Python环境
- Python 3.6 或更高版本
- 必需的包：pandas, os, shutil
- 安装 pandas：`pip install pandas`

### 2. 自备文件
- `relationship.csv` 文件
- 源数据文件（Excel .xls 或 CSV 文件）由齐禾结果下载得到，一般为Detail_result文件夹

### 3. 目录结构
- 自定义源目录与输出目录
- 所有输出文件将保存到同一输出目录

## 输入数据格式

### 1. RELATIONSHIP.CSV 文件格式
必须包含以下三列：
- **Name**：与源文件名匹配的分类名称。如样品名为"OSD1-1-01"至"OSD1-1-96"则填入"OSD1"
  > **注意！！** 一个Name匹配一个比对序列，若同一基因名有多个序列比对则需要区分，如"OSD1-1"和"OSD1-2"

- **Case**：要么是 "point mutation" 要么是 "others"
  > 按照IGDB分析方法，Detail文件中只有点突变类型，其余突变类型在IndelDetail文件中

- **Target_Sequence**：对应基因名称在数据文件中需要比对的编辑后序列
  > **注意！！** Target_Sequence为编辑后序列，Case是point mutation时固定为sample sheet中目的序列的长度，包含Sample-sheet中的目的序列点突变。Case是others时不固定长度，由Sample-sheet中的目的序列更改

**relationship.csv 示例：**
```csv
Name,Case,Target_Sequence
OSD1,point mutation,GATAAAGAACCCACCACCCG
PAIR1,point mutation,CGCGTCGGCTTCCGGTTCCG
REC8,others,CGAGCTTGTCAAGCTTC
```

### 2. 源数据文件命名约定
文件必须遵循以下模式之一（在提交给齐禾的sample sheet 里命名）：

**模式 1（连字符分隔）：** `"Name-number-label.filetype"`
- 示例：`OSD1-4-A01.IGDB.detail.csv`, `OSD1-01.IGDB.detail.csv`

**模式 2（下划线分隔）：** `"prefix_Name_suffix.filetype"`
- 示例：`0414_APP_OT1_1.IGDB.Indeldetail.csv`, `0414_APP_01.IGDB.Indeldetail.csv`

### 3. 支持的文件类型
- `.xls`（Excel 文件）
- `.csv`（逗号分隔值）

### 4. 必需的文件类型标识符
源文件名必须包含以下标识符之一：
- `.detail`（用于 detail 文件）
- `.Indeldetail`（用于 Indeldetail 文件）
- `.Count`（用于 count 文件 - 处理后删除，可不删）
- `.Percent`（用于 percent 文件 - 处理后删除，可不删）

### 5. CSV 数据结构要求
CSV 文件必须包含：
- 包含序列数据的 "Key" 列
- "Ratio" 列（用于 Indeldetail 文件）
- "Ratio(%)" 列（用于包含点突变的 detail 文件）

## 使用方法

### 步骤 1：准备数据
1. 将源数据文件放置在任意路径，格式如：`C:/Users/lkmbi/Desktop/0617-WS1`
2. 填写 `relationship.csv` 文件，并确定路径，格式如：`C:/Users/lkmbi/Desktop/relationship.csv`
3. 验证所有文件都遵循必需的命名约定

### 步骤 2：运行脚本
1. 打开命令提示符或 PowerShell
2. 导航到包含 `Data arrangement Version4.py` 的目录
3. 运行命令：`python "Data arrangement Version4.py"`

### 步骤 3：监控进度
脚本将显示进度消息：

- "Starting file classification process..."（开始文件分类过程）
- Enter the input (source) directory containing the data files: `C:/Users/lkmbi/Desktop/0617-WS1`（输入源数据文件路径）
- Enter the path to the relationship CSV file: `C:/Users/lkmbi/Desktop/relationship.csv`（输入relationship文件夹路径）
- Enter the output directory for the results: `C:/Users/lkmbi/Desktop/0617-WS1`（输出文件路径）
- 文件移动确认
- 文件夹删除确认
- "File classification completed!"（文件分类完成）
- "Starting data arrangement process..."（开始数据整理过程）
- 单个结果文件创建确认
- "All combined results saved to: [path]"（所有组合结果已保存到：[路径]）
- "Combined processing completed successfully!"（组合处理成功完成）

## 处理步骤

### 阶段 1：文件分类
1. 扫描源目录中的 .xls 和 .csv 文件
2. 从文件名中提取分类名称
3. 识别文件类型（detail, Indeldetail, Count, Percent）
4. 创建文件夹结构：`[SourceDir]/[Classification]/[FileType]/`
5. 将文件移动到相应的文件夹
6. 删除 Count 和 Percent 文件夹

### 阶段 2：数据整理
1. 读取 `relationship.csv` 文件
2. 对于每个关系条目：
   - 根据案例类型处理比对结果
   - 计算总比对比率
   - 处理 Indeldetail 文件夹中的总和结果
   - 组合比对和总和数据
   - 保存单个组合结果文件
3. 将所有单个结果合并到最终的综合文件中

## 输出文件

### 1. 组织的文件夹结构
```
C:/Users/lkmbi/Desktop/0617-WS1/
├── [Classification1]/
│   ├── detail/
│   │   └── [detail 文件]
│   └── Indeldetail/
│       └── [Indeldetail 文件]
├── [Classification2]/
│   ├── detail/
│   └── Indeldetail/
└── ...
```

### 2. 单个结果文件
- `[Classification]_combined_results.csv`
- 包含列：Filename Alignment, Total Alignment Ratio, Total Sum Ratio, Filename Sum

### 3. 最终综合文件
- `all_combined_results.csv`
- 包含所有单个结果加上 "Name" 列
- 位置：`C:/Users/lkmbi/Desktop/0617-WS1/all_combined_results.csv`

## 输出数据格式

最终的 `all_combined_results.csv` 包含：
- **Filename Alignment**：处理的比对文件名
- **Total Alignment Ratio**：目标序列的比对比率总和
- **Total Sum Ratio**：Indeldetail 文件中所有比率的总和
- **Filename Sum**：处理的求和文件名
- **Name**：分类名称（文件夹名）

## 错误处理

脚本处理各种错误情况：
1. 跳过不符合命名约定的文件
2. 自动创建缺失的文件夹
3. 将非数字比率值转换为 0
4. 优雅地处理缺失的列
5. 捕获并报告文件读取错误

**常见错误消息：**
- "Skipping [filename]: No underscore or hyphen found in filename"（跳过 [文件名]：文件名中未找到下划线或连字符）
- "Skipping [filename]: No recognized file type pattern found"（跳过 [文件名]：未找到可识别的文件类型模式）
- "Error processing [filename]: [error details]"（处理 [文件名] 时出错：[错误详情]）

## 故障排除

### 1. "File not found" 错误：
- 检查 `relationship.csv` 是否存在于指定路径
- 验证源目录路径是否正确

### 2. "No files processed"：
- 确保源文件遵循命名约定
- 检查文件扩展名（.xls 或 .csv）

### 3. "Empty results"：
- 验证 CSV 文件包含必需的列（Key, Ratio, Ratio(%)）
- 检查目标序列是否存在于数据中

### 4. "Permission errors"：
- 确保对源目录有写入权限
- 运行脚本前关闭任何打开的 Excel 文件

## 自定义

要修改路径或行为：
1. 编辑脚本中的 source_directory 变量
2. 编辑脚本中的 relationship_file 路径
3. 在 `classify_files()` 函数中修改文件类型标识符
4. 在 `process_alignment_results()` 和 `process_sum_results()` 中调整列名

## 支持

如有问题或疑问：
1. 检查控制台输出中的错误消息
2. 验证所有输入文件都遵循必需格式
3. 确保满足所有先决条件
4. 检查文件权限和路径
5. 实在解决不了就问chatGPT

## 版本信息

- **脚本**：`Data arrangement Version4.py`
- **功能**：文件分类和数据整理
- **依赖项**：pandas, os, shutil
- **兼容性**：Python 3.6+

---

**开发者**：Li KA MING

## 许可证

本项目采用 MIT 许可证。详情请参见 LICENSE 文件。

版权 © 2024 Li KA MING。保留所有权利。
