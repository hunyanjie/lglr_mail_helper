import tkinter as tk
from tkinter import colorchooser
from tkinter import font
import re

# 定义暗色主题的颜色
dark_theme_colors = {
    'background': '#0E0E0E',
    'foreground': '#FFFFFF',
    'highlight': '#3A3A3A',
    'selectbackground': '#4A4A4A',
    'selectforeground': '#FFFFFF',
    'insertbackground': '#FFFFFF',  # 设置光标颜色为白色
    'inactiveselectbackground': '#4A4A4A',
    'warning': '#FF0000',
}


# 定义一个函数，用于更改选中文本的颜色
def change_color(event):
    color_code = colorchooser.askcolor(title="选择颜色")[1].upper()
    if color_code:
        # 设置新的前景色
        start_index = input_text.index("sel.first")
        end_index = input_text.index("sel.last")
        for tag in input_text.tag_names():
            print(input_text.tag_ranges(tag))
            input_text.tag_remove(str(tag), str(start_index), str(end_index))  # 删除之前的颜色
        input_text.tag_config(str(color_code), foreground=str(color_code))  # 设置前景色
        input_text.tag_add(str(color_code), str(start_index), str(end_index))

def copy_text():
    # 全选Text组件中的所有文字
    output_text.tag_add('sel', '1.0', 'end')
    output_text.event_generate('<<Copy>>')  # 触发复制操作
    output_text.tag_remove('sel', '1.0', 'end')  # 取消全选

def paste_text():
    output_text.event_generate('<<Paste>>')  # 触发粘贴操作

# 定义函数，用于格式化文本
def output_content():
    处理坐标颜色(input_text, True)
    all_text = {}
    row = 0
    column = 0
    for i in input_text.get(0.0, "end").split("\n")[:-1]:
        row += 1
        column = 0
        for j in i:
            all_text[f"{row}.{column}"] = "#FFFFFF"
            column += 1
        all_text[f"{row}.{column}"] = "#FFFFFF"
    tags = input_text.tag_names()
    for tag in tags:
        if tag != "sel":
            try:
                print(input_text.tag_ranges(tag))
                for i in range(0, len(input_text.tag_ranges(tag)), 2):
                    start_index = input_text.index(input_text.tag_ranges(tag)[i])
                    end_index = input_text.index(input_text.tag_ranges(tag)[i + 1])
                    for i in range(list(all_text.keys()).index(start_index), list(all_text.keys()).index(end_index)):
                        all_text[list(all_text.keys())[i]] = tag
            except:
                pass
    处理坐标颜色(input_text)
    print(all_text)
    # 拼接所有内容
    formatted_content = ""
    现索引位置 = 0
    # 上一个颜色 = "#FFFFFF"
    for i in list(all_text.keys()):
        获取到的文本 = input_text.get(list(all_text.keys())[现索引位置])  # 获取文本内容
        文本颜色 = all_text[list(all_text.keys())[现索引位置]]  # 获取文本颜色
        下一位列表索引值 = 1
        # 合并相同颜色的文本
        while (下一位列表索引值 + list(all_text.keys()).index(list(all_text.keys())[现索引位置])) < len(all_text) and all_text[list(all_text.keys())[下一位列表索引值 + list(all_text.keys()).index(list(all_text.keys())[现索引位置])]] == 文本颜色:  # 如果下一位颜色相同
            获取到的文本 += "\n" * (int(float(list(all_text.keys())[下一位列表索引值 + list(all_text.keys()).index(list(all_text.keys())[现索引位置])])) - int(float(list(all_text.keys())[下一位列表索引值 + list(all_text.keys()).index(list(all_text.keys())[现索引位置]) - 1])) - 1)
            获取到的文本 += input_text.get(list(all_text.keys())[下一位列表索引值 + list(all_text.keys()).index(list(all_text.keys())[现索引位置])])
            下一位列表索引值 += 1
        if 文本颜色 == "#FFFFFF":
            formatted_content += 获取到的文本
        elif 下一位列表索引值 + list(all_text.keys()).index(list(all_text.keys())[现索引位置]) < len(all_text) and all_text[list(all_text.keys())[下一位列表索引值 + list(all_text.keys()).index(list(all_text.keys())[现索引位置])]] == "#FFFFFF":  # 如果下一位颜色为白色
            formatted_content += 文本颜色.replace("#", "#c") + 获取到的文本 + "#n"
        else:
            formatted_content += 文本颜色.replace("#", "#c") + 获取到的文本
        现索引位置 += 下一位列表索引值
        if 现索引位置 >= len(all_text):
            break
    formatted_content = formatted_content.replace("\n", "#r").replace("#c0000FF", "#B").replace("#cFFD700", "#D").replace("#c00FF00", "#G").replace("#c000000", "#K").replace("#cFFA500", "#O").replace("#cFFC0CB", "#P").replace("#cFF0000", "#R").replace("#c800080", "#U").replace("#cFFFFFF", "#W").replace("#cFFFF00", "#Y")
    while formatted_content[-2:] == "#n" or formatted_content[-2:] == "#r":
        formatted_content = formatted_content[:-2]
    output_text.delete("1.0", "end")  # 清空文本框内容
    output_text.insert("1.0", formatted_content)  # 插入格式化后的文本
    count_total_words(None)

def input_content():
    未处理的文本 = output_text.get(0.0, "end")  # 获取输入框中的所有内容
    待处理的文本 = 未处理的文本.replace("#B", "#c0000FF").replace("#D", "#cFFD700").replace("#D", "#cFFD700").replace("#G", "#c00FF00").replace("#K", "#c000000").replace("#O", "#cFFA500").replace("#P", "#cFFC0CB").replace("#R", "#cFF0000").replace("#U", "#c800080").replace("#W", "#cFFFFFF").replace("#Y", "#cFFFF00")
    for color in re.findall(r'#c[0-9A-Fa-f]{6}', 待处理的文本):
        待处理的文本 = 待处理的文本.replace(color, color.replace("#c", "#"))
    用来显示的文本 = re.sub(r'#[0-9A-Fa-f]{6}', "", 待处理的文本.replace("#n", "").replace("#r", "\n"))
    input_text.delete("1.0", "end")  # 清空输入框内容
    input_text.insert("1.0", 用来显示的文本)  # 插入处理后的文本
    行 = 1
    列 = 0
    文本索引 = 0
    # 上一个颜色 = "#FFFFFF"
    for i in 待处理的文本:
        if 文本索引>= len(待处理的文本):
            break
        现在处理的文本 = 待处理的文本[文本索引]
        if 现在处理的文本 == "#" and 待处理的文本[文本索引 + 1] == "r":
            行 += 1
            列 = 0
            文本索引 += 1
        elif 现在处理的文本 == "#" and re.match(r'^#[0-9A-Fa-f]{6}$', 待处理的文本[文本索引:文本索引 + 7]):
            颜色代码 = re.match(r'^#[0-9A-Fa-f]{6}$', 待处理的文本[文本索引:文本索引 + 7]).group()
            临时文本索引 = 0
            临时行 = 行
            临时列 = 列
            for j in 待处理的文本[文本索引 + 7:-1]:
                if 文本索引 + 7 + 临时文本索引 >= len(待处理的文本):
                    break
                临时处理的文本 = 待处理的文本[文本索引 + 7 + 临时文本索引]
                if 临时处理的文本 == "#" and 待处理的文本[文本索引 + 7 + 临时文本索引 + 1] == "r":
                    行 += 1
                    列 = -1
                    临时文本索引 += 1
                elif 临时处理的文本 == "#" and 待处理的文本[文本索引 + 7 + 临时文本索引 + 1] == "n":
                    文本索引 += 临时文本索引 + 7 + 1
                    break
                elif 现在处理的文本 == "#" and re.match(r'^#[0-9A-Fa-f]{6}$', 待处理的文本[临时文本索引 + 文本索引 + 7:临时文本索引 + 文本索引 + 7 + 7]):
                    文本索引 += 临时文本索引 + 7 - 1
                    break
                列 += 1
                临时文本索引 += 1
            input_text.tag_config(str(颜色代码), foreground=str(颜色代码))  # 设置前景色
            input_text.tag_add(str(颜色代码), str(f"{临时行}.{临时列}"), str(f"{行}.{列}"))
        if 现在处理的文本 != "#":
            列 += 1
        文本索引 += 1
    处理坐标颜色(input_text)

def 处理坐标颜色(Text控件标签, 按下=False):
    # 处理坐标颜色
    if 按下:
        for 匹配到的坐标内容 in re.findall(r'\(\d+,\d+\)', Text控件标签.get("1.0", "end")):
            index = Text控件标签.search(匹配到的坐标内容, "1.0", "end")
            if index:
                # 获取匹配的起始和结束索引
                start_index = Text控件标签.index(f"{index}+0c")
                end_index = Text控件标签.index(f"{index}+11c")
                Text控件标签.tag_remove("#278451", start_index, end_index)
    else:
        Text控件标签.tag_config("#278451", foreground="#278451")  # 设置前景色
        for 匹配到的坐标内容 in re.findall(r'\(\d+,\d+\)', Text控件标签.get("1.0", "end")):
            index = Text控件标签.search(匹配到的坐标内容, "1.0", "end")
            if index:
                # 获取匹配的起始和结束索引
                start_index = Text控件标签.index(f"{index}+0c")
                end_index = Text控件标签.index(f"{index}+11c")
                Text控件标签.tag_add("#278451", start_index, end_index)

def count_total_words(event):
    text_len = len(output_text.get("1.0", "end")) - 1
    if text_len > 300:
        total_text_show.config(text="文本长度：" + str(text_len) + "/300", fg=dark_theme_colors['warning'])
    else:
        total_text_show.config(text="文本长度：" + str(text_len) + "/300", fg=dark_theme_colors['foreground'])



# 创建一个新窗口
root = tk.Tk()
root.title("无尽的拉格朗日多色文本编辑器v1.0 | 制作者：魂魇桀（梦岛）")

# 设置窗口的背景颜色
root.configure(bg=dark_theme_colors['background'])

# 创建一个字体对象
text_font = font.Font(family="等线", size=14, weight="normal")

# 创建一个Text组件

input_text_frame = tk.Frame(root)
input_text = tk.Text(input_text_frame, wrap="char", undo=True, bg=dark_theme_colors['background'], fg=dark_theme_colors['foreground'], font=text_font, width=70, height=10)
input_text.pack(expand=True, side="left", fill="both")
input_text_scrollbar_y = tk.Scrollbar(input_text_frame, orient='vertical', command=input_text.yview, bg=dark_theme_colors['background'], troughcolor=dark_theme_colors['background'])
input_text_scrollbar_y.pack(side="right", fill="y")
input_text.config(yscrollcommand=input_text_scrollbar_y.set)
input_text_frame.pack(expand=True, side="top", fill="both")

# input_text = tk.Text(root, wrap="char", undo=True, bg=dark_theme_colors['background'], fg=dark_theme_colors['foreground'], font=text_font, width=70, height=10)
# input_text.pack(expand=True, side="top", fill="both")
# 设置光标颜色
input_text.config(insertbackground=dark_theme_colors['insertbackground'])
input_text.bind("<3>", change_color)
input_text.bind("<KeyPress>", lambda event: 处理坐标颜色(input_text, True))
input_text.bind("<KeyRelease>", lambda event: 处理坐标颜色(input_text))

# 创建按钮，用于格式化文本
input_output_format = tk.Frame(root)
output_bottom = tk.Button(input_output_format, text="导出↓", command=output_content, bg=dark_theme_colors['background'], fg=dark_theme_colors['foreground'])
output_bottom.pack(expand=True, side="left", fill="both")
input_bottom = tk.Button(input_output_format, text="↑导入", command=input_content, bg=dark_theme_colors['background'], fg=dark_theme_colors['foreground'])
input_bottom.pack(expand=True, side="right", fill="both")
input_output_format.pack(fill="x")

# 创建一个Text组件用于显示格式化后的文本
output_text = tk.Text(root, wrap="char", undo=True, bg=dark_theme_colors['background'], fg=dark_theme_colors['foreground'], font=text_font, width=70, height=10)
output_text.pack(expand=True, side="top", fill="both")
# 设置光标颜色
output_text.config(insertbackground=dark_theme_colors['insertbackground'])

# 字数显示
total_text_show = tk.Label(root, text="文本长度：-/300", bg=dark_theme_colors['background'], fg=dark_theme_colors['foreground'])
total_text_show.pack(expand=True, fill="x")
output_text.bind('<Motion>', count_total_words)
output_text.bind("<Key>", count_total_words)

# 提示
hint_show = tk.Label(root, text="提示：选择文本后右键即可选择要更改的颜色", bg=dark_theme_colors['background'], fg=dark_theme_colors['foreground'])
hint_show.pack(expand=True, fill="x")

# 创建右键菜单
right_click_menu = tk.Menu(root, tearoff=0)
right_click_menu.add_command(label="全部复制", command=copy_text)
right_click_menu.add_command(label="粘贴", command=paste_text)

# 绑定右键点击事件
def on_right_click(event):
    right_click_menu.post(event.x_root, event.y_root)

output_text.bind("<Button-3>", on_right_click)  # 绑定右键点击事件

# 运行主循环
root.mainloop()
