import pkgutil
import importlib
import inspect
import html
import os


def build_html_tree(package_name):
    """
    指定したパッケージのモジュール・クラス・関数の構造を
    折り畳み可能なHTMLツリー形式で返す。
    """
    html_lines = [f"<details open><summary><b>{package_name}</b></summary><ul>"]
    try:
        package = importlib.import_module(package_name)

        for _, modname, _ in pkgutil.walk_packages(
            package.__path__, package.__name__ + "."
        ):
            try:
                module = importlib.import_module(modname)
                html_lines.append(f"<li><details><summary>{modname}</summary><ul>")

                items = inspect.getmembers(
                    module, lambda obj: inspect.isfunction(obj) or inspect.isclass(obj)
                )
                items.sort(key=lambda x: x[0])

                for name, obj in items:
                    safe_name = html.escape(name)
                    html_lines.append(f"<li>{safe_name}</li>")

                html_lines.append("</ul></details></li>")
            except Exception as e:
                html_lines.append(
                    f"<li><b>{modname}</b> - Error: {html.escape(str(e))}</li>"
                )
    except Exception as e:
        html_lines.append(f"<li>Error: {html.escape(str(e))}</li>")
    html_lines.append("</ul></details>")
    return "\n".join(html_lines)


def save_html_tree(package_name, output_dir="structure"):
    """
    指定したパッケージ名のHTMLツリーを生成し
    output_dir に保存する。
    """
    os.makedirs(output_dir, exist_ok=True)
    html_content = build_html_tree(package_name)
    filename = f"{package_name}.html"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("<html><body>\n" + html_content + "\n</body></html>")
    return filepath
