import argparse
import base64
import json
import html
import time
from typing import Tuple, Dict, List
import urllib

from IPython.core.interactiveshell import InteractiveShell
from IPython import get_ipython
from IPython.display import display, HTML

import notebook

from httpdbg import httprecord


def css() -> str:
    style = """<style>
.httpdbg-block {
    border-style: solid !important;
    border-width: 1px 0px !important;
    border-color: rgb(124, 124, 124) !important;
    width: 100% !important;
}

.httpdbg-url {
    padding: 0px 0px 0px 10px !important;
}

.httpdbg-url-data {
    padding: 0px 0px 0px 10px !important;
}

.httpdbg-url-code {
    padding: 0px 0px 0px 10px !important;
    width: 100% !important;
    background-color: #EEEEEE !important;
    cursor: default !important;
}

.httpdbg-url-code > img {
    max-width: 50% !important;
    height: auto !important;
}

.httpdbg-expand {
    cursor: pointer !important;
}
"""

    if int(notebook.__version__.split(".")[0]) < 7:
        style += """

.httpdbg-expand > summary:before {
    content: '\\229E ' !important;
}

.httpdbg-expand[open] > summary:before {
    content: '\\229F ' !important;
}
    """

    style += """
</style>
"""

    return style


def parse_content_type(content_type: str) -> Tuple[str, Dict[str, str]]:
    s = content_type.split(";")
    media_type = s[0]
    directives = {}
    for directive in s[1:]:
        sp = directive.split("=")
        if len(sp) == 2:
            directives[sp[0].strip()] = sp[1].strip()
    return media_type, directives


def print_body(req, limit: int) -> str:
    if len(req.content) == 0:
        return ""

    preview = req.preview

    if preview.get("image"):
        return f"""<img src="data:{preview["content_type"]};base64,{base64.b64encode(req.content).decode("utf-8")}">"""

    if preview.get("text"):
        txt = preview["text"]
        try:
            txt = json.dumps(json.loads(preview["text"]), indent=4)
        except Exception:
            # query string
            try:
                if (
                    parse_content_type(req.get_header("content_type"))[0]
                    == "application/x-www-form-urlencoded"
                ):
                    qs = []
                    for key, value in urllib.parse.parse_qsl(
                        req.content, strict_parsing=True
                    ):
                        if value:
                            qs.append(f"{key}={value}")
                    if qs:
                        txt = "\n\n".join(qs)
            except Exception:
                pass

        return html.escape(txt)[:limit]

    return "<i> body data not printable </i>"


def print_headers(headers: List[str], limit: int):
    return html.escape(
        "\n".join([f"{header.name}: {header.value}" for header in headers])
    )[:limit]


def httpdbg_magic(line, cell):
    args = read_args([arg for arg in line.strip().split(" ") if arg != ""])

    with httprecord() as records:
        tbegin = time.time()
        get_ipython().run_cell(cell)
        tend = time.time()
        infos = css()
        infos += f"""<details class="httpdbg-block httpdbg-expand"><summary>[httpdbg] {len(records)} requests in {tend-tbegin:.2f} seconds</summary>"""
        for record in records:
            request_headers = print_headers(record.request.headers, args.headers)
            request_body = print_body(
                record.request,
                args.body,
            )
            response_headers = print_headers(record.response.headers, args.headers)
            response_body = print_body(
                record.response,
                args.body,
            )
            infos += f"""<details  class="httpdbg-expand httpdbg-url">
<summary>{html.escape(str(record.status_code))} {html.escape(record.method)} {html.escape(record.url)}</summary>
<details  class="httpdbg-expand httpdbg-url-data"><summary>request</summary><pre class="httpdbg-url-code">{request_headers}\n\n{str(request_body)}</pre></details>
<details  class="httpdbg-expand httpdbg-url-data"><summary>response</summary><pre class="httpdbg-url-code">{response_headers}\n\n{str(response_body)}</pre></details>
</details>"""
        display(HTML(infos))


def read_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="httpdbg",
        description="httdbg - a very simple tool to debug HTTP(S) client requests",
    )

    parser.add_argument(
        "--headers",
        type=int,
        default=1000,
        metavar=1000,
        help="Number of characters to display for the headers.",
    )

    parser.add_argument(
        "--body",
        type=int,
        default=5000,
        metavar=5000,
        help="Number of characters to display for the body.",
    )

    return parser.parse_args(args)


def load_ipython_extension(ipython: InteractiveShell):
    ipython.register_magic_function(httpdbg_magic, "cell", "httpdbg")


def unload_ipython_extension(ipython):
    pass
