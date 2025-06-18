# 100囚徒问题模拟实验

这个项目实现了100囚徒问题的模拟实验，包括两种策略的对比和可视化分析。

## 问题描述

100名囚犯，编号1-100。房间内有100个盒子，每个盒子随机放入一张囚犯编号的纸条（编号不重复）。
囚犯依次进入房间，每人最多可以打开50个盒子寻找自己的编号。
若所有囚犯都在50次尝试中找到自己的编号，则全体获释；否则全员失败。

## 实验内容

1. 对比两种策略的成功率：
   - 策略1：随机策略（每个囚犯随机打开50个盒子）
   - 策略2：循环策略（囚犯从自己编号的盒子开始，根据盒内纸条跳转）
2. 分析不同参数（囚犯数量N，尝试次数K）对成功率的影响
3. 通过大量模拟实验，观察成功率的分布情况

## 环境要求

- Python 3.6+
- 依赖包：numpy, matplotlib, seaborn, tqdm

## 安装步骤

1. 克隆或下载本项目
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

直接运行Python脚本：
```bash
python prisoner_simulation.py
```

程序会：
1. 使用默认参数（N=100, K=50）运行10000次模拟实验
2. 显示两种策略的成功率对比图
3. 显示循环策略的成功人数分布图
4. 分析不同参数组合下的成功率

### 修改参数

如需修改实验参数，可以编辑`prisoner_simulation.py`文件中的主程序部分：

```python
if __name__ == '__main__':
    # 设置随机种子
    np.random.seed(42)
    random.seed(42)
    
    # 修改这些参数
    n, k, trials = 100, 50, 10000  # 可以调整这些值
    random_results, cycle_results = run_simulation(n, k, trials)
    plot_results(random_results, cycle_results, n, k, trials)
    
    # 分析参数影响
    analyze_parameters()
```

## 文件说明

- `prisoner_simulation.py`: 主程序文件，包含所有功能实现
- `requirements.txt`: 项目依赖列表
- `README.md`: 项目说明文档

## 实验结果

通过大量模拟实验，我们发现：

1. 循环策略的成功率显著高于随机策略
2. 当K/N接近0.5时，循环策略的成功率最高
3. 随着囚犯数量N的增加，循环策略的成功率会逐渐趋于一个稳定值
4. 随机策略的成功率随着N的增加而急剧下降

这些结果验证了循环策略的优越性，特别是在大规模囚犯数量的情况下。

## 代码结构

`prisoner_simulation.py` 包含以下主要函数：

- `generate_boxes(n)`: 生成随机排列的盒子内容
- `random_strategy(boxes, prisoner_num, max_attempts)`: 实现随机策略
- `cycle_strategy(boxes, prisoner_num, max_attempts)`: 实现循环策略
- `simulate_round(n, k, strategy)`: 模拟一轮实验
- `run_simulation(n, k, trials)`: 运行多次模拟实验
- `plot_results(random_results, cycle_results, n, k, trials)`: 绘制实验结果
- `analyze_parameters()`: 分析不同参数对成功率的影响 