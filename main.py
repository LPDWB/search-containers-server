from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pathlib import Path

app = FastAPI()

DATA_FILE = Path("containers.txt")

def load_containers():
    if DATA_FILE.exists():
        return set(DATA_FILE.read_text(encoding="utf-8").splitlines())
    return set()

def save_containers(containers):
    DATA_FILE.write_text("\n".join(sorted(containers)), encoding="utf-8")

# В памяти
containers = load_containers()

@app.get("/containers")
def get_containers():
    return JSONResponse(list(containers))

@app.post("/add")
def add_container(name: str = Form(...)):
    for part in name.strip().split():
        containers.add(part)
    save_containers(containers)
    return RedirectResponse("/", status_code=302)

@app.post("/delete")
def delete_container(name: str = Form(...)):
    containers.discard(name.strip())
    save_containers(containers)
    return RedirectResponse("/", status_code=302)

@app.get("/", response_class=HTMLResponse)
def form_page():
    html = """
    <html>
        <head>
            <title>Список сеток</title>
            <style>
                body { font-family: sans-serif; margin: 40px; }
                input[type='text'] { padding: 5px; width: 200px; }
                button { padding: 5px 10px; margin-left: 5px; }
                table { margin-top: 20px; border-collapse: collapse; }
                th, td { padding: 8px 12px; border: 1px solid #ccc; }
            </style>
        </head>
        <body>
            <h2>Добавить сетку</h2>
            <form action="/add" method="post">
                <input type="text" name="name" required>
                <button type="submit">Добавить</button>
            </form>

            <h3>Текущие сетки</h3>
            <table>
                <tr><th>Сетка</th><th>Действие</th></tr>
    """
    for name in sorted(containers):
        html += f"""
        <tr>
            <td>{name}</td>
            <td>
                <form action="/delete" method="post" style="display:inline;">
                    <input type="hidden" name="name" value="{name}">
                    <button type="submit">Удалить</button>
                </form>
            </td>
        </tr>
        """
    html += "</table></body></html>"
    return html
