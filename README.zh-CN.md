# COMSOL Agent Research Workflow

**与 AI Agent 一起建立 COMSOL 模型、开展计算并解释结果。**

这是一个 Skill，让编程 Agent 通过 COMSOL 原生 Java API 和命令行开展仿真。说明你的科研问题，Agent 会建立或检查模型、运行有边界的计算、核对数值，并解释下一步该调整什么。

- **从物理问题出发。** 先明确观测量、边界条件和假设，再选择求解器和作图方式。
- **先试算，再全面计算。** 用代表性工况确定批量规模；逐个工况记录日志和断点，中断的扫描可以续算。
- **先核对，再下结论。** 解释结果前先检查守恒、极限情形和网格敏感性；数值完成、物理自洽与实验吻合分开报告。

![由 AI Agent 主导的科研循环：建模、COMSOL 计算、查看结果、调整模型；查看结果时可退回重算，最终输出图表和报告](assets/workflow.png)

## 示例：边缘电流的收集

采用 Ma 等人提出的边缘电流源与收集模型 [1]，在独立重建的四十字导电结构中应用这套工作流。计算得到的左右对应肩部热点同号，沿沟道经过下、上肩部时，响应呈现重复的正负变化。

![计算得到的扫描电流响应与纵向扫描剖面](examples/edge-current/assets/example-results.png)

**图 1。** **(a)** 底部电极电流随光斑位置的变化。**(b)** x = ±0.7 µm 处的纵向扫描剖面，灰色区域表示横臂所在范围。两图均用完整扫描的最大绝对电流归一化。几何为近似重建，源强用于演示；本例进行定性对照，未标定实验电流。

**[1]** Ma, Q. et al. *Giant intrinsic photoresponse in pristine graphene.* **Nature Nanotechnology 14**, 145–150 (2019). [doi:10.1038/s41565-018-0323-8](https://doi.org/10.1038/s41565-018-0323-8)。

[示例方法、数据与代码 →](examples/edge-current/README.md)

## 开始使用

将完整的 [`comsol-agent-research-workflow`](skills/comsol-agent-research-workflow/) 文件夹复制到 Agent 的 Skill 目录，然后提出任务：

```text
使用 $comsol-agent-research-workflow 检查这个模型，
规划一组对照计算，先运行代表工况，再解释结果。
```

**[安装与使用说明 →](docs/getting-started.md)**

需要可执行本地命令的编程 Agent 和具有许可的 COMSOL。采用原生 Java API 与命令行，无需额外 MCP 服务。配套示例已在 Windows、COMSOL 6.4.0.293 下检查。[验证详情](VALIDATION.md)。

[English](README.md) · [MIT 许可证](LICENSE) · [来源说明](NOTICE.md)
