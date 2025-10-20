# Mermaid 高级图表测试

## 思维导图 (Mindmap) 测试

### 标准Mindmap语法
```mermaid
mindmap
  root((思维导图))
    分支1
      子分支1.1
      子分支1.2
    分支2
      子分支2.1
      子分支2.2
```

### 替代方案 - 流程图风格
```mermaid
flowchart TD
    A[思维导图] --> B[分支1]
    A --> C[分支2]
    B --> B1[子分支1.1]
    B --> B2[子分支1.2]
    C --> C1[子分支2.1]
    C --> C2[子分支2.2]
```

## 象限图 (Quadrant Chart) 测试

### 标准QuadrantChart语法
```mermaid
quadrantChart
    title 功能优先级分析
    x-axis 低实现成本 --> 高实现成本
    y-axis 低用户价值 --> 高用户价值
    quadrant-1 高价值，低成本
    quadrant-2 高价值，高成本
    quadrant-3 低价值，低成本
    quadrant-4 低价值，高成本
    
    功能A: [0.3, 0.8]
    功能B: [0.7, 0.9]
    功能C: [0.6, 0.4]
```

### 替代方案 - 散点图风格
```mermaid
flowchart LR
    subgraph 高价值
        A[功能A<br/>低成本]
        B[功能B<br/>高成本]
    end
    subgraph 低价值
        C[功能C<br/>高成本]
        D[功能D<br/>低成本]
    end
    
    style A fill:#9f9,stroke:#333,stroke-width:2px
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#f99,stroke:#333,stroke-width:2px
    style D fill:#ff9,stroke:#333,stroke-width:2px
```

## 其他高级图表测试

### 用户旅程图
```mermaid
journey
    title 用户使用体验
    section 发现
      了解产品: 5: 用户
      下载试用: 4: 用户
    section 使用
      初次使用: 3: 用户
      熟练操作: 5: 用户
    section 分享
      推荐给朋友: 4: 用户
      写评价: 3: 用户
```

### 甘特图
```mermaid
gantt
    title 项目开发计划
    dateFormat  YYYY-MM-DD
    section 设计阶段
    需求分析      :done, des1, 2023-01-01, 2023-01-05
    UI设计        :done, des2, after des1, 5d
    section 开发阶段
    前端开发      :active, dev1, after des2, 10d
    后端开发      :dev2, after des1, 15d
    section 测试阶段
    单元测试      :test1, after dev1, 5d
    集成测试      :test2, after dev2, 5d
```

### 状态图
```mermaid
stateDiagram-v2
    [*] --> 待处理
    待处理 --> 处理中: 开始处理
    处理中 --> 已完成: 处理完成
    处理中 --> 待处理: 重置
    已完成 --> [*]: 结束
```

## 故障排除

如果某些图表类型不显示，可能的原因：

1. **版本兼容性**：某些图表类型是较新添加的，可能需要更新Mermaid插件
2. **语法错误**：检查图表语法是否正确
3. **配置问题**：确保VS Code设置中启用了Mermaid支持

### 更新插件命令
```bash
code --update-extension bierner.markdown-mermaid
```

### 查看插件信息
```bash
code --show-versions bierner.markdown-mermaid
```

## 替代方案

如果某些图表类型仍然不显示，可以考虑：

1. 使用流程图模拟思维导图
2. 使用带样式的流程图模拟象限图
3. 使用在线Mermaid编辑器生成图片并嵌入到Markdown中
4. 使用其他图表库如PlantUML