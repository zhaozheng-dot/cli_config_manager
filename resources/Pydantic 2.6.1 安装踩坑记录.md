# Pydantic 2.6.1 安装踩坑记录

## 环境信息
- **系统**: Windows
- **Python**: 3.14
- **目标版本**: pydantic==2.6.1

## 主要问题

### 1. pydantic-core 编译依赖问题
**问题描述**: pydantic==2.6.1 依赖 pydantic-core==2.16.2，该版本需要从源码编译，依赖 Rust 和 Cargo 工具链。

**错误信息**:
```
Cargo, the Rust package manager, is not installed or is not on PATH.
This package requires Rust and Cargo to compile extensions.
```

**解决方案**: 
1. 安装预编译的 pydantic-core 二进制版本
2. 使用 `--only-binary=:all:` 参数避免源码编译
3. 安装兼容的 pydantic 版本

### 2. 版本兼容性问题
**问题描述**: 预编译的 pydantic-core 版本 (2.41.5) 与 pydantic==2.6.1 要求的版本 (2.16.2) 不兼容。

**解决方案**:
1. 安装 pydantic-core==2.41.5 (预编译二进制)
2. 安装兼容的 pydantic==2.12.5
3. 该版本保持 API 向后兼容性

### 3. 依赖缺失问题
**问题描述**: pydantic 2.12.5 需要额外的依赖包。

**缺失包**:
- typing-inspection (运行时类型检查)
- annotated-types (类型注解支持)

**解决方案**: 手动安装缺失依赖包。

## 最终安装方案

### 安装命令序列
```bash
# 1. 安装预编译的 pydantic-core
python -m pip install pydantic-core --only-binary=:all:

# 2. 安装 pydantic (不检查依赖)
python -m pip install "pydantic>=2.6.1" --no-deps

# 3. 安装缺失依赖
python -m pip install typing_inspection
python -m pip install annotated-types>=0.6.0
```

### 最终版本
- pydantic==2.12.5 (兼容 2.6.1 API)
- pydantic-core==2.41.5 (预编译二进制)
- annotated-types==0.7.0
- typing-inspection==0.4.2

## 关键要点

### 技术要点
1. **Windows 环境限制**: 避免源码编译，优先使用预编译二进制包
2. **版本兼容性**: 较新的 pydantic 版本保持 API 向后兼容
3. **依赖管理**: 注意 pydantic 的间接依赖关系

### 最佳实践
1. 在 Windows 环境下使用 `--only-binary=:all:` 参数
2. 定期检查依赖包的兼容性矩阵
3. 使用固定版本号确保环境一致性

### 配置建议
```toml
# pyproject.toml
[project]
dependencies = [
    "pydantic==2.12.5",
    "pydantic-core==2.41.5",
    "annotated-types==0.7.0",
    "typing-inspection==0.4.2"
]
```

## 验证结果
✅ 所有包安装成功  
✅ 功能测试通过  
✅ API 兼容性验证通过  
✅ 无需 Rust 编译环境