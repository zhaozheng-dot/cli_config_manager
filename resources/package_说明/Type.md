- Type是做什么的：   
  - CLI 是 Command Line Interface（命令行界面）的缩写。简单来说，CLI 应用程序就是一种不需要鼠标点点点，而是通过在终端（Terminal）或控制台（Console）中输入文本命令来运行的程序

- CLI 的核心组成部分
  - 命令 (Command)：你要运行的程序名称。例如 python, git, mkdir。

  - 子命令 (Sub-command)：某些程序下属的功能模块。例如 git push 中的 push。

  - 选项/标志 (Options/Flags)：修改程序行为的开关。通常以 - 或 -- 开头。例如 ls -l 或 git commit -m "message"。

  - 参数 (Arguments)：程序执行的对象。例如 rm file.txt 中的 file.txt。

- 原生python 和Type的关系
  - Typer 完全依赖 Python 原生的类型提示（Type Hints）和 typing 模块来进行“信息提示”。 这种“提示”体现在两个层面：面向开发者（IDE 代码补全）和面向最终用户（生成命令行帮助信息）。

- python 中的fastAPI pydatic Type,这三个包的关联关系讲解下
  - 很多现代 Python 开发者会将这三者结合使用，构建一套完整的生产力工具：

  - Pydantic (数据模型层)：定义核心的数据结构和校验逻辑。这个模型可以被 Web 和 CLI 共用。

  - FastAPI (接口层)：将这些模型暴露给互联网，供前端或其他服务调用。

  - Typer (管理层)：编写一个 CLI 工具来管理你的 FastAPI 服务。例如：一键初始化数据库、创建管理员账号、清理缓存等。