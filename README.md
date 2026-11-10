<p align="center">
  <img src="assets/cover.svg" alt="Amazon Listing Forge — 把产品事实，锻造成购买理由" width="100%">
</p>

<p align="center">
  <strong>让买家看懂，让每个卖点有据可查。</strong><br>
  面向 Amazon 卖家的 AI Skill：文案 × FAQ × 图片需求 × 上架检查
</p>

<p align="center">
  <a href="SKILL.md">查看 Skill</a> ·
  <a href="examples/bath-brush-demo.md">看洗澡刷案例</a> ·
  <a href="templates/product-brief.md">复制产品资料模板</a> ·
  <a href="#快速开始">快速开始</a>
</p>

---

**产品资料写了一大堆，买家却还是不知道能不能用。**

Listing Forge 从买家的购买疑问出发，把结构、材质、数量和使用边界，分配到标题、五点、FAQ 与图片。让运营拿得到文案，让设计师接得住图需，让关键宣称追得到来源。

```text
产品事实 → 买家疑问 → 购买理由 → 文案与图片 → 检查与实验
```

## 你会得到什么

| 输入 | 输出 |
| --- | --- |
| 产品规格、说明书、包装清单 | 事实台账与待确认项 |
| 关键词、目标人群、使用场景 | 标题、Item Highlights、五点、描述/A+ |
| 差评、真实客服问题、退货原因 | FAQ 答案与内容补漏清单 |
| 产品参考图、确认过的卖点 | 可交给设计师的图片分镜和英文图上文案 |
| 已有 Listing 和效果数据 | 问题优先级、改写稿与实验建议 |

**三个值得试用的设计：**

- **卖点能追溯。** 数字、材质、结构对应证据；缺资料时列待补项，避免 AI 自动补出“卖点”。
- **表达有边界。** 区分已确认信息与未知特性，不凭外观推断刷毛触感、皮肤适用性或清洁效果。
- **内容互相对得上。** 文案、图片与后台属性使用同一份事实，而不是各写一套。

## 先看一个改写

> 全部案例统一为独立虚构的洗澡刷。不使用真实商家的品牌、型号、参数、图片或经营数据。

**原稿**

```text
Premium Bath Brush, Best Quality, Perfect for Everyone
```

**改写**

```text
Long Handle Bath Brush with Hanging Loop, 1 Count
```

去掉无依据的“适合所有人”和泛泛夸赞，把产品类型、长柄结构、挂绳和数量放到买家最先看到的位置。刷毛软硬、尺寸和材质没有证据时，保留为待确认项。

→ [查看洗澡刷演示资料、五点、FAQ、七图简报和发布判断](examples/bath-brush-demo.md)

## 快速开始

### 1. 获取并安装

下载本仓库 ZIP 或克隆：

```bash
git clone https://github.com/TomorrowLee/amazon-listing-forge.git
```

将包含 `SKILL.md`、`agents/`、`references/`、`templates/`、`examples/` 和 `scripts/` 的整个 `amazon-listing-forge` 文件夹放进你的 Codex 用户技能目录 `~/.agents/skills/`，或项目内的 `.agents/skills/`。使用 `$amazon-listing-forge` 调用；未识别时重启 Codex。目录和调用方式见 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。

其他支持 Markdown Skill 的工具可按各自导入方式加载；本项目未逐一测试其他客户端。运行核心写作流程不需要 Python；仅可选检查工具需要 Python 3.9+，不需要第三方包。

### 2. 贴产品资料，直接开工

```text
使用 $amazon-listing-forge，为这款美国站产品生成 Listing。
根据以下已确认资料写英文成稿，中文解释取舍；
同时输出事实追溯表、FAQ 和图片需求，不知道的参数列待确认。

品牌：...
产品：...
已确认规格与证据：...
使用方式与限制：...
包装清单：...
真实买家问题：...
```

也可以从 [产品资料模板](templates/product-brief.md) 开始。已有的信息直接复用，不需要填满整张表才能起草。

### 3. 只做你需要的那一部分

```text
诊断这版 Listing：先指出最容易造成误购的三处，再给替换稿。
```

```text
把这些脱敏退货原因转成 FAQ，并标出该补到哪条五点、哪张副图。
```

```text
只输出七图需求：每张图回答一个问题，给构图、英文标题、证据和禁改项。
```

```text
根据现有数据设计主图实验，明确主指标、观察条件和回滚标准。
```

## 可选：发布前做一次结构检查

```bash
python scripts/check_listing.py examples/listing.json
python -m unittest discover -s tests -v
```

检查标题/Highlights 的字符数、后台词 UTF-8 字节数、重复五点、联系方式及部分风险词。默认使用美国站非媒体类 75/125 字符快照，可按适用规则覆盖：

```bash
python scripts/check_listing.py your-listing.json --title-limit 75 --highlights-limit 125
```

后台词仅报告字节数；需要强制限制时自行按当前字段要求传 `--search-terms-max-bytes`。`structural_pass` 只表示通过配置的结构检查，不代表事实正确或获得 Amazon 审核。

## 把经验和规则分开

项目采用通用 Listing 写作方法和公开资料，并于 **2026-11-10** 复核部分官方来源。洗澡刷案例独立虚构，不对应任何真实商品。

- 75 字符标题与 125 字符 Highlights 来源于官方公告，使用时仍核对站点和类目。
- 卖家的触发词个案仅作复核线索，不做全站通用禁词表。
- 七图分工是创作方法，可按产品和图位调整。
- FAQ 用于真实产品信息，不用于自问自答或伪造社区内容。
- 主图标识、包装例外和图像真实性按适用官方要求判断。

[查看公开来源、访问限制与适用范围](references/sources-and-policy.md)。项目不分发私有产品文件，不承诺转化率、排名或购物 AI 推荐结果，也不代表 Amazon 官方。

## 项目导航

```text
amazon-listing-forge/
├── SKILL.md                         技能入口
├── agents/openai.yaml               调用信息
├── references/                      文案、FAQ、图片、质检与来源
├── templates/product-brief.md        产品资料模板
├── examples/                        虚构洗澡刷演示与检查输入
├── scripts/check_listing.py          离线结构检查
├── tests/                           检查工具测试
└── assets/cover.svg                  项目封面
```

## English overview

**Turn product facts into buyer-ready listings.** Amazon Listing Forge is a Chinese-first AI skill for evidence-based Amazon copy, buyer FAQs, image briefs, and pre-publication review. It links claims to sources and keeps unverified features out of publication drafts. Listing copy follows the target marketplace language; explanations default to Chinese. All examples use an independently fictional bath brush, with no real merchant product data. Includes a dependency-free Python structure checker.

## 一起改进

欢迎通过 [Issues](https://github.com/TomorrowLee/amazon-listing-forge/issues) 提交脱敏案例、规则变更的官方链接或改进建议。复现文案问题时请附站点、类目、已确认事实、预期结果和实际结果；不要提交买家个人信息或凭证。

如果这套工作流对你有帮助，欢迎点亮 Star，让更多卖家找到它。
