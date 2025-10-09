import tkinter as tk
from tkinter import colorchooser, font, Menu, messagebox
import re
import threading
import time

THEME = dict(bg='#0E0E0E', fg='#FFFFFF', insert='#FFFFFF', warn='#FF0000')

# ---------- 工具 ----------
def rgb_to_tag(c: str) -> str:          # #12AB34 -> c_12AB34
    return 'c_' + c[1:].upper()

def tag_to_rgb(t: str) -> str:          # c_12AB34 -> #12AB34
    return '#' + t[2:]

def coords_in(text: str):
    return re.findall(r'\(\d+,\d+\)', text)

# ---------- 核心 ----------
class ColorText(tk.Text):
    """带颜色标记的 Text，支持导出/导入 Lagrange 格式"""
    def __init__(self, master, **kw):
        super().__init__(master, wrap='char', undo=True, insertbackground=THEME['insert'], **kw)
        self.bind('<Button-3>', self._on_right)
        self.bind('<KeyRelease>', self._on_key)
        self._tag_coords = 'coords'          # 坐标高亮专用 tag
        self.tag_config(self._tag_coords, foreground='#278451')

    # ---- 右键改色 ----
    def _on_right(self, e):
        if not self.tag_ranges('sel'): return
        c = colorchooser.askcolor(title='选中文本颜色')[1]
        if not c: return
        self.apply_color(c.upper())

    def apply_color(self, color: str):
        tag = rgb_to_tag(color)
        self.tag_config(tag, foreground=color)
        start, end = self.index('sel.first'), self.index('sel.last')
        # 去掉冲突 tag
        for t in self.tag_names(start):
            if t.startswith('c_'):
                self.tag_remove(t, start, end)
        self.tag_add(tag, start, end)

    # ---- 增量坐标高亮 ----
    def _on_key(self, _=None):
        # 防抖 200 ms
        if hasattr(self, '_after'):
            self.after_cancel(self._after)
        self._after = self.after(200, self._highlight_coords)

    def _highlight_coords(self):
        self.tag_remove(self._tag_coords, '1.0', 'end')
        for s, e in self._scan_re(r'\(\d+,\d+\)'):
            self.tag_add(self._tag_coords, s, e)

    def _scan_re(self, pattern):
        """返回 (start_index, end_index) 列表"""
        idx = '1.0'
        out = []
        while True:
            idx = self.search(pattern, idx, regexp=True, stopindex='end')
            if not idx: break
            end = f'{idx}+{len(self.get(idx, f"{idx}+11c"))}c'
            out.append((idx, end))
            idx = end
        return out

    # ---- 导出 Lagrange ----
    def export_lagrange(self) -> str:
        """按拉格朗日协议导出：#r=换行，#cRRGGBB=改色，#n=强制重置为默认色"""
        out, cur_color = [], None
        # 逐字符扫描，先拿到全局索引
        all_text = self.get('1.0', 'end-1c')
        for global_idx, ch in enumerate(all_text):
            # 当前字符的 Text 索引
            tk_idx = f'1.0+{global_idx}c'
            # 取颜色
            tags = [t for t in self.tag_names(tk_idx) if t.startswith('c_')]
            color = tag_to_rgb(tags[0]) if tags else '#FFFFFF'

            # 换行
            if ch == '\n':
                out.append('#r')
                continue

            # 颜色变化才输出控制符
            if color != cur_color:
                if color == '#FFFFFF':  # 回到默认色
                    out.append('#n')
                else:  # 新颜色
                    out.append('#c' + color[1:].upper())
                cur_color = color

            out.append(ch)

        # 清理尾部无用控制符
        while out and out[-1] in ('#n', '#r'):
            out.pop()
        return ''.join(out)

    def _global_idx(self, line_str, char_pos):
        """把行内偏移转成全局偏移"""
        row = self.get('1.0', 'end').splitlines().index(line_str.rstrip('\n')) + 1
        return int(self.index(f'{row}.0').split('.')[1]) + char_pos

    # ---- 导入 Lagrange ----
    def import_lagrange(self, txt: str):
        """把 Lagrange 字符串还原成带颜色 Text"""
        self.delete('1.0', 'end')

        # 1. 先插入纯文本（去掉所有控制符）
        plain = re.sub(r'#c[0-9A-Fa-f]{6}|#n|#r', '', txt.replace('#r', '\n'))
        self.insert('1.0', plain)

        # 2. 再扫描一次，给对应区间上色
        pos_in_lag = 0  # 在 Lagrange 串里的指针
        pos_in_plain = 0  # 在 plain 里的指针
        cur_color = None
        tag_start = None  # 当前颜色块起始（plain 坐标）

        def flush_color():
            nonlocal tag_start, cur_color
            if tag_start is not None and cur_color and cur_color != '#FFFFFF':
                tk_start = f'1.0+{tag_start}c'
                tk_end = f'1.0+{pos_in_plain}c'
                tag = rgb_to_tag(cur_color)
                self.tag_config(tag, foreground=cur_color)
                self.tag_add(tag, tk_start, tk_end)
            tag_start = None

        while pos_in_lag < len(txt):
            if txt.startswith('#r', pos_in_lag):
                pos_in_lag += 2
                pos_in_plain += 1  # 对应 \n
            elif txt.startswith('#n', pos_in_lag):
                flush_color()
                cur_color = None
                pos_in_lag += 2
            elif txt.startswith('#c', pos_in_lag) and len(txt) >= pos_in_lag + 9:
                new_color = '#' + txt[pos_in_lag + 3:pos_in_lag + 9].upper()
                flush_color()
                cur_color = new_color
                tag_start = pos_in_plain
                pos_in_lag += 9
            else:  # 普通字符
                if cur_color and tag_start is None:
                    tag_start = pos_in_plain
                pos_in_lag += 1
                pos_in_plain += 1

        flush_color()  # 收尾
        self._highlight_coords()

# ---------- UI ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('无尽的拉格朗日多色文本编辑器 v3.0 | 制作者：魂魇桀（梦岛）')
        self.configure(bg=THEME['bg'])
        self.font = font.Font(family='等线', size=14)

        # 输入区
        frm = tk.Frame(self, bg=THEME['bg'])
        frm.pack(fill='both', expand=True, padx=5, pady=5)
        self.input = ColorText(frm, bg=THEME['bg'], fg=THEME['fg'], font=self.font, width=70, height=10)
        scroll = tk.Scrollbar(frm, orient='vertical', command=self.input.yview)
        self.input.config(yscrollcommand=scroll.set)
        self.input.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

        # 按钮区
        btn_bar = tk.Frame(self, bg=THEME['bg'])
        btn_bar.pack(fill='x', padx=5, pady=2)
        tk.Button(btn_bar, text='导出↓', command=self.on_export, bg=THEME['bg'], fg=THEME['fg']).pack(side='left', fill='x', expand=True)
        tk.Button(btn_bar, text='↑导入', command=self.on_import, bg=THEME['bg'], fg=THEME['fg']).pack(side='left', fill='x', expand=True)

        # 输出区
        frm2 = tk.Frame(self, bg=THEME['bg'])
        frm2.pack(fill='both', expand=True, padx=5, pady=5)
        self.output = tk.Text(frm2, wrap='char', bg=THEME['bg'], fg=THEME['fg'], font=self.font, width=70, height=10)
        scroll2 = tk.Scrollbar(frm2, orient='vertical', command=self.output.yview)
        self.output.config(yscrollcommand=scroll2.set)
        self.output.pack(side='left', fill='both', expand=True)
        scroll2.pack(side='right', fill='y')
        self.output.bind('<KeyRelease>', self.on_len)
        self.output.bind('<Motion>', self.on_len)

        # 状态栏
        self.status = tk.Label(self, text='文本长度：0/300', bg=THEME['bg'], fg=THEME['fg'])
        self.status.pack(fill='x')

        # 输出区右键菜单
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label='全部复制', command=self.copy_output)
        self.menu.add_command(label='粘贴', command=lambda: self.output.event_generate('<<Paste>>'))
        self.output.bind('<Button-3>', lambda e: self.menu.post(e.x_root, e.y_root))

    # ---- 事件 ----
    def on_export(self):
        try:
            self.output.delete('1.0', 'end')
            self.output.insert('1.0', self.input.export_lagrange())
            self.on_len()
        except Exception as e:
            messagebox.showerror('导出失败', str(e))

    def on_import(self):
        try:
            self.input.import_lagrange(self.output.get('1.0', 'end-1c'))
        except Exception as e:
            messagebox.showerror('导入失败', str(e))

    def on_len(self, _=None):
        n = len(self.output.get('1.0', 'end-1c'))
        self.status.config(text=f'文本长度：{n}/300',
                           fg=THEME['warn'] if n > 300 else THEME['fg'])

    def copy_output(self):
        self.output.tag_add('sel', '1.0', 'end')
        self.output.event_generate('<<Copy>>')
        self.output.tag_remove('sel', '1.0', 'end')

if __name__ == '__main__':
    App().mainloop()