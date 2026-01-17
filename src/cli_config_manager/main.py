import typer
import sys
from pathlib import Path
from typing import Annotated

# 引入 Rich 库用于终端美化 (类似 Java 的 Jansi 但功能更强)
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# 引入内部模块
from cli_config_manager.processor import DataProcessor

# 初始化 Typer 应用对象
# Java 类比: SpringApplication 或 Picocli 的 CommandLine 对象
app = typer.Typer(
    help="AI Agent 数据清洗与校验工具",
    add_completion=False  # 关闭 shell 自动补全脚本安装提示
)

# 初始化 Rich 控制台
console = Console()


# -----------------------------------------------------------------------------
# 命令定义 (Command Definition)
# @app.command() 装饰器将函数注册为一个 CLI 命令
#
# Java 类比: Picocli 的 @Command class CleanCommand implements Runnable
# -----------------------------------------------------------------------------
@app.command()
def clean(

        # 1、Annotated[T, metadata] 是 Python 3.9+ 引入的类型注解语法
        #T2、 是参数的实际类型（如 Path, str, int 等）
        #3、metadata 是 Typer 的配置信息（如 typer.Argument() 或 typer.Option()）

        # 参数定义：使用 Annotated + typer.Argument/Option
        # input_file 是位置参数 (Argument)，必须提供
        input_file: Annotated[Path, typer.Argument(help="输入文件路径")],
        # output_file 是选项参数 (Option)，有默认值
        output_file: Annotated[
            Path,
            typer.Option(
                "--output", "-o",  # 命令行标志
                help="清洗后数据的输出路径"
            )
        ] = Path("cleaned_data.json"),
        # verbose 是布尔开关 (Flag) # 标志参数
        verbose: bool = typer.Option(False, "--verbose", "-v", help="显示详细日志")
):
    """
    执行数据清洗主流程。# 这个文档字符串会成为命令描述
    """
    # 打印分割线
    console.rule("[bold blue]Data Cleaner Engine[/bold blue]")

    # 1. 初始化处理器
    # Typer 已经帮我们将 input_file (str) 转为了 Path 对象
    processor = DataProcessor(input_file)

    # 2. 执行处理
    console.print(f"正在读取文件: [yellow]{input_file}[/yellow]...")
    try:
        valid_users, errors = processor.process_data()
    except Exception as e:
        console.print(f"[bold red]致命错误:[/bold red] {e}")
        # typer.Exit 类似于 System.exit(1)
        raise typer.Exit(code=1)

    # 3. 输出摘要
    console.print(f"处理完成. 合法数据: [green]{len(valid_users)}[/green] | 违规数据: [red]{len(errors)}[/red]")

    # 4. 打印错误报告 (如果存在)
    if errors:
        console.print("\n[bold red]发现数据校验错误:[/bold red]")

        # 创建一个表格用于展示错误
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("行号", style="dim", width=10)
        table.add_column("原始数据片段", width=40)
        table.add_column("违规详情")

        for err in errors:
            # 格式化 Pydantic 的错误信息
            # loc 表示 location (字段名), msg 表示 message
            msgs = [f"{e['loc']}: {e['msg']}" for e in err['errors']]

            table.add_row(
                str(err['index']),
                str(err['raw_data']),
                "\n".join(msgs)
            )

        console.print(table)

    # 5. 保存结果
    if valid_users:
        processor.save_cleaned_data(valid_users, output_file)
        console.print(f"\n[bold green]成功![/bold green] 清洗后的数据已保存至: {output_file}")
    else:
        console.print("\n[bold yellow]警告:[/bold yellow] 没有产生有效的输出文件。")


# -----------------------------------------------------------------------------
# 程序入口
# Java 类比: public static void main(String args)
# -----------------------------------------------------------------------------

"""
这个代码片段是 Python 程序的入口点，相当于 Java 中的 public static void main(String[] args) 方法。

具体作用：

条件执行：if __name__ == "__main__": 确保这段代码只在直接运行此脚本时执行，而不是在被导入为模块时执行。

启动 CLI 应用：app() 调用 Typer 应用对象，它会：

解析命令行参数
根据用户输入的命令（如 
clean
）执行对应的函数
处理参数验证和错误信息
提供帮助信息（当用户输入 --help 时）
"""

if __name__ == "__main__":
    app()

##################################编程疑问记录###################################################


# 问：为什么我执行 python src\cli_config_manager\main.py input.yaml 函数后默认执行 Clean方法？
"""
  答：Typer 底层使用 Click 库，当只有一个命令时，Click 会将其设为默认命令。
        在你的代码中，clean函数是唯一被 @app.command() 装饰的函数，所以它成为了默认命令。
 
        当存在两个时候，使用命令执行时候，必须显式的给出 option，或者 修改typer.Typer()配置来强制显式调用option
"""