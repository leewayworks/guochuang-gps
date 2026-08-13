<p align="center">
  <img src="assets/gps-title.svg" alt="GPS (Guochuang Preparation Skills)" width="680">
</p>

<p align="center">🧭 <strong>From idea to gold. Navigate your Guochuang journey.</strong></p>

<p align="center"><strong>把散落的项目书、PPT 和调研记录，收束成一条经得起追问的项目主线。</strong></p>

<p align="center">
  <strong>简体中文</strong> ·
  <a href="README.en.md">English</a>
</p>

<p align="center">
  <img src="assets/guochuang-gps-concept.png" alt="Guochuang GPS 概念图" width="100%">
</p>

备赛越往后，材料通常越多。项目书、路演 PPT、实验记录和访谈纪要各自积累了不少内容，**真正要讲的那条主线**却容易被埋住。技术亮点、市场空间、合作经历都在，但评委很难在短时间里看清它们之间的关系。

Guochuang GPS 现在以开源 Skill 的形式发布，面向中国国际大学生创新大赛参赛团队。名字里的 GPS 取自 Guochuang Preparation Skills。使用时，它会先判断**项目走到哪一步**，再把**下一轮最值得做的事**排出来。

GPS 可以在 Codex、Claude Code 等支持 Skills 的 Agent 中运行。它会读取团队已有的材料，梳理项目定位、核心优势、创新价值、市场机会和证据缺口，然后把下一轮修改任务排出先后顺序。

## 先把项目讲清楚

把项目目录交给 GPS 后，你会得到一份可以直接拿去开修改会的 Markdown 报告。报告先收束**一句话定位和前三个卖点**，再检查创新、市场与对应赛道的评分维度，最后整理**证据台账和三项优先行动**。重要判断会回到具体文件和当前证据状态，团队讨论时不用在几版 PPT 之间来回找依据。

完整诊断适合项目盘点和大改。市场分析、创新检查、PPT 审阅、项目书修改和答辩演练也可以单独调用。需要把结果保存到项目目录时，默认文件名是 `项目名-GPS评审.md`。专项报告则使用 `项目名-创新评审.md`、`项目名-PPT评审.md` 这类名称。遇到同名文件，GPS 会顺延为 `-02`、`-03`，不会直接覆盖。

## 三分钟开始

### Codex

使用带有 `codex plugin` 命令的 Codex CLI，在终端执行下面两行。

```text
codex plugin marketplace add leewayworks/guochuang-gps
codex plugin add guochuang-gps@guochuang-gps
```

安装后运行 `codex plugin list`，确认列表中出现 Guochuang GPS。新建一个对话，把项目目录和几项基本信息发给它。

```text
使用 GPS 审阅 G:\path\to\project
申报年份：2026
赛道与组别：高教主赛道创意组
当前阶段：省赛准备
```

也可以先处理眼前最着急的问题。

```text
请用 GPS 梳理这个项目的核心优势和前三个卖点，按高教主赛道创意组逐项指出证据缺口。
```

赛道还没定、材料还没整理完，都可以直接开始。GPS 读完现有内容后，再补问会影响资格判断、评分卡选择和下一步行动的信息。

### Claude Code

把 `skills/` 下的各个目录复制到个人 Skills 目录。

PowerShell

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse -Force .\skills\* "$env:USERPROFILE\.claude\skills\"
claude plugin list
```

macOS 或 Linux

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
claude plugin list
```

复制完成后重新打开 Claude Code 会话。其他支持 Skills 的 Agent 也可以采用相同方式，目标位置以对应工具的说明为准。

## GPS 怎样找到真正的卖点

专利、奖项、市场规模、合作单位和首创声明都值得看，但它们只是线索。GPS 会继续确认**比较对象、适用范围和证据来源**，再决定哪些内容值得进入核心叙事。

一个能放上路演台的卖点，需要把几件事交代清楚。谁遇到了什么问题，团队采取了哪些不同做法，结果在什么条件下成立，又有哪些文件、数据或第三方记录能够证明。适用范围也要说清，这样答辩时才不容易被一个追问打散。

## 从优秀项目里拆出方法

GPS 的方法库建立在 **67 套国金项目样本**之上，覆盖**高教主赛道、青年红色筑梦之旅赛道和产业赛道**。我们逐份梳理了其中的项目书、网评稿、路演 PPT、现场赛终稿和培训课件。

方法库也吸收了 **17 位国金选手**的实战经验和 **5 位专家评委**的评审思路。选手熟悉一套材料怎样反复取舍、逐步成形，评委更清楚**什么内容会被看见，哪些问题会在现场被追问**。GPS 把这两种经验放在一起，形成了自己的项目判断逻辑。

复盘时，我们会追踪同一个项目在不同版本里**删了什么、保留了什么，证据又被放在什么位置**。这些变化能还原团队怎样找到主线，也能看出一套材料如何逐步靠近评审的阅读顺序。再与评分规则和培训材料互相印证，评委最关心的问题就会清晰许多。

这些观察最终整理成 **9 张[匿名方法卡](skills/positioning/references/case-patterns.md)**。卡片记录的是优秀项目中反复出现的判断方法，包括怎样选主线、怎样组织证据、怎样处理市场和落地，以及怎样把学生团队的真实贡献讲清楚。样本和人员的计数方式统一记录在[方法库来源口径](skills/positioning/references/method-sources.md)中。

## 跟着赛道评分卡查缺补漏

项目一换赛道，评委关注的顺序也会变。GPS 会先确认申报年份、赛道和组别，再调用对应的评分卡。仓库目前收录了中国国际大学生创新大赛 2025 年正式规则对应的**七张评分卡**。

| 赛道 | 组别 |
| --- | --- |
| 高教主赛道 | 创意组、创业组 |
| 青年红色筑梦之旅 | 公益组、创意组、创业组 |
| 产业赛道 | 企业命题组、成果转化组 |

评分卡以[全国大学生创业服务网发布页](https://cy.ncss.cn/en/notifications/2c93f4c696aa01a10196eca57202006a)为正式来源，并用[19 页完整附件镜像](https://www.cupk.edu.cn/cxcy/upload/resources/file/2025/06/23/102490.pdf)逐页核对。版本和来源记录保存在[来源注册表](skills/gps-common/references/source-registry.yaml)中。

当 2026 年正式评审规则尚未发布时，GPS 暂用同赛道、同组别的 2025 评分卡。报告会明确写出 `rubric_version: 2025-05-20`、`rubric_status: historical_baseline` 和 `current_year_rubric_status: pending`，方便团队在新规则发布后重新核对。

报告里有三个常用指标。

| 指标 | 含义 |
| --- | --- |
| `rubric_alignment_score` | 当前材料与评分表一级维度的对齐程度 |
| `gps_readiness` | 项目处于基础整理、证据建设、评审准备或答辩准备中的哪个阶段 |
| `evidence_coverage` | 问题、机制、结果、外部验证和持续性证据覆盖了多少 |

`rubric_alignment_score` 先为每个一级维度使用 0 至 4 的证据就绪锚点，再按官方权重换算为 0 至 100。团队可以用这些数值安排备赛优先级，正式成绩仍以赛事评审为准。校赛和省赛的材料格式、时间与流程以当地通知为准。

## 八个任务 Skill，共用一套路由

GPS 有**八个任务 Skill**，另设一个共用规则目录。完整诊断从 `navigator` 开始，它先盘点材料、确认评分卡，再把问题交给最合适的 Skill。需要核对项目事实时，`evidence` 会回到原始文件查证。

| Skill | 负责什么 |
| --- | --- |
| `navigator` | 材料盘点、评分卡确认、任务分配和结果汇总 |
| `positioning` | 项目定位、候选优势、前三卖点和机会判断 |
| `evidence` | 主张与证据台账、文件核验、矛盾和隐私检查 |
| `innovation` | 技术机制、比较基线、实验和可复现性 |
| `business` | 客户阶段、市场方法、定价、单位经济和交付风险 |
| `proposal` | 项目书结构、章节主张和修改顺序 |
| `deck` | 路演逻辑、页面结论、视觉证据和时间控制 |
| `defense` | 评委问题、回答卡和压力演练 |
| `gps-common` | 共用的路由、来源和输出规则 |

## 在本地跑一个示例

仓库附带了一个合成项目，可以用来查看评分路由和证据识别结果。

```powershell
python scripts/gps_score.py examples/demo-project.json
```

示例故意留下了缺失的证据路径和一条缺少支持的量化主张。运行后可以看到 GPS 怎样标记材料缺口、计算证据覆盖率，并把需要补证的内容排进下一步行动。

## 项目材料放在哪里

项目材料留在团队自己的工作区即可，GPS 会从当前目录读取。数据如何传输和保存，取决于团队所用 Agent 的设置。学生身份信息、客户保密材料、私人联系方式和未公开知识产权继续放在团队内部目录。这个公开仓库只保存匿名方法、规则索引和合成示例。

## 维护与致谢

- [leewayworks](https://github.com/leewayworks) 负责项目方向、领域资料、方法判断和日常维护。
- OpenAI Codex 参与了资料比对、代码实现、测试和中英文文档编辑。

## 许可证

[MIT](LICENSE)
