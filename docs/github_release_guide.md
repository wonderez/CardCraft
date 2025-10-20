# GitHub 发布指南 - v1.0.4

## 提交代码更改

执行以下Git命令将更改提交到GitHub仓库：

```bash
# 确保在正确的仓库目录下
cd d:\CardCraft-1.0.1.0

# 添加所有更改的文件
git add .

# 提交更改，添加描述信息
git commit -m "发布 v1.0.4 版本 - 修复图片显示问题"

# 推送更改到远程仓库
git push origin main
```

## 创建版本标签

为新版本创建Git标签：

```bash
# 创建带注释的标签
git tag -a v1.0.4 -m "CardCraft v1.0.4 发布 - 图片显示优化"

# 推送标签到远程仓库
git push origin v1.0.4
```

## 创建GitHub Release

1. 登录GitHub账户
2. 导航到项目仓库：https://github.com/wonderez/CardCraft
3. 点击上方导航栏中的 "Releases" 或 "Tags"
4. 点击 "Draft a new release" 或 "Create a new release"

### 填写发布信息

- **Tag version**: `v1.0.4`（确保与创建的Git标签名称完全一致）
- **Target**: 选择 `main` 分支
- **Release title**: `CardCraft v1.0.4 - 图片显示优化`

### 发布说明

复制以下内容到描述框中：

```markdown
## v1.0.4 更新内容 (2025-10-14)

### 🖼️ 图片显示优化

- **长图片显示问题修复**: 解决了长图片（如800x1200等非标准比例）被截断的问题
- **CSS样式优化**: 
  - 将.content类的样式修改为`min-height: 100%`和`overflow: visible !important`
  - 保持img标签的响应式设置`max-width: 100%; height: auto`
- **JavaScript改进**: 在ensureContentFit函数中设置`content.style.maxHeight = 'none'`和`content.style.overflow = 'visible'`
- **预览组件优化**: 优化了generate_fit_html方法中的缩放逻辑，确保图片完整显示

### 🔧 技术改进

- **CSS优化**: 移除了不必要的内容高度限制
- **JavaScript优化**: 改进了内容适应逻辑，确保真正的所见即所得
- **响应式设计**: 增强了图片的自适应布局能力

### 📝 文档更新

- 更新README.md，添加图片显示优化功能说明
- 更新版本号为1.0.4
```

### 上传可执行文件

构建完成后，上传以下文件：
- `CardCraft.exe` - 主程序可执行文件
- `requirements.txt` - 依赖列表（可选）

### 发布选项

- 可以选择是否将此版本标记为"Latest release"
- 可以选择是否将此版本标记为"Pre-release"（通常稳定版本不勾选）

## 构建可执行文件

在发布前，建议重新构建应用程序以确保包含所有最新更改：

```bash
# 运行构建脚本
python scripts/build.py --mode onefile --shortcut
```

构建完成后，可执行文件将位于输出目录中，准备上传到GitHub Release。

## 验证发布

发布完成后，验证以下内容：

1. 确认新版本标签出现在GitHub仓库的标签列表中
2. 确认Release页面显示了完整的发布说明
3. 确认可执行文件已成功上传并可以下载
4. 测试下载的可执行文件，确保图片显示问题已修复

## 宣传更新

（可选）在项目README中添加最新版本的链接，并在社交媒体上宣布更新。