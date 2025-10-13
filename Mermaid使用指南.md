# Trae中Mermaid插件使用指南

## 插件安装状态

✅ Mermaid插件已成功安装：`bierner.markdown-mermaid v1.29.0`

## 如何使用

### 1. 创建或打开Markdown文件

在Trae中创建一个新的Markdown文件（.md扩展名）或打开现有的Markdown文件。

### 2. 编写Mermaid图表

在Markdown文件中，使用以下语法嵌入Mermaid图表：

```markdown
```mermaid
[您的Mermaid图表代码]
```
```

### 3. 预览图表

有几种方式可以预览Mermaid图表：

#### 方法一：使用内置预览
1. 打开Markdown文件
2. 按 `Ctrl+Shift+V` 打开预览面板
3. 图表将自动渲染

#### 方法二：使用侧边预览
1. 按 `Ctrl+K` 然后按 `V` 打开侧边预览
2. 图表将在侧边栏中实时渲染

#### 方法三：使用命令面板
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Markdown: 打开预览" 并选择
3. 图表将在预览面板中显示

## 支持的图表类型

Mermaid支持多种图表类型，包括：

1. **流程图** (flowchart)
2. **时序图** (sequenceDiagram)
3. **类图** (classDiagram)
4. **状态图** (stateDiagram)
5. **实体关系图** (erDiagram)
6. **用户旅程图** (journey)
7. **甘特图** (gantt)
8. **饼图** (pie)
9. **象限图** (quadrantChart)
10. **思维导图** (mindmap)

## 示例

### 简单流程图
```mermaid
flowchart TD
    A[开始] --> B{条件判断}
    B -->|是| C[执行操作]
    B -->|否| D[结束]
    C --> D
```

### 时序图
```mermaid
sequenceDiagram
    participant A as 用户
    participant B as 系统
    A->>B: 发送请求
    B-->>A: 返回响应
```

## 常见问题

### 图表不显示
1. 确保使用正确的语法：```mermaid ... ```
2. 检查图表代码是否有语法错误
3. 尝试重新加载预览面板

### 图表显示不完整
1. 检查是否有未闭合的标签
2. 确保图表代码符合Mermaid语法规范

## 更多资源

- [Mermaid官方文档](https://mermaid-js.github.io/mermaid/)
- [Mermaid语法指南](https://mermaid-js.github.io/mermaid/#/)
- [VS Code Markdown预览文档](https://code.visualstudio.com/docs/languages/markdown)

## 项目图表

您可以在以下文件中查看为RedBookCards项目创建的图表：
- `项目图表.md` - 包含9种不同类型的Mermaid图表
- `mermaid测试.md` - 简单的测试图表

现在您可以在Trae中轻松创建和查看各种Mermaid图表了！