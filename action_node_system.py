import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import os
import sys
import time
import ctypes
from PIL import Image, ImageTk
# 调整导入方式，使用当前目录导入而不是相对导入
from keyboard_shortcut_node import KeyboardShortcutNode
from button_click_node import ButtonClickNode


# 主程序类
class ActionNodeSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("动作节点系统")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # 设置中文字体
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TRadiobutton", font=("SimHei", 10))
        
        # 基础节点类数组
        self.action_nodes = []
        
        # 当前选中的节点索引
        self.selected_index = -1
        
        # 创建UI
        self._create_ui()
        
        # 预设快捷键列表
        self.common_keys = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
            'Space', 'Enter', 'Esc', 'Tab', 'Delete', 'BackSpace',
            'PageUp', 'PageDown', 'Home', 'End', 'Insert',
            'Left', 'Right', 'Up', 'Down'
        ]
    
    def _create_ui(self):
        """创建用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建左侧动作节点列表
        left_frame = ttk.LabelFrame(main_frame, text="动作节点列表", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 创建右侧详情页
        right_frame = ttk.LabelFrame(main_frame, text="动作节点详情", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # 左侧列表部分
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建动作列表
        self.action_listbox = tk.Listbox(list_frame, font=("SimHei", 10), selectmode=tk.SINGLE)
        self.action_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.action_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.action_listbox.config(yscrollcommand=scrollbar.set)
        
        # 绑定列表选择事件
        self.action_listbox.bind("<<ListboxSelect>>", self._on_select_node)
        
        # 按钮部分
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 添加快捷键按钮
        add_keyboard_button = ttk.Button(button_frame, text="添加快捷键", command=self._add_keyboard_node)
        add_keyboard_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 添加按钮点击按钮
        add_button_button = ttk.Button(button_frame, text="添加按钮点击", command=self._add_button_node)
        add_button_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 删除按钮
        delete_button = ttk.Button(button_frame, text="删除", command=self._delete_node)
        delete_button.pack(side=tk.LEFT)
        
        # 播放按钮
        play_button = ttk.Button(button_frame, text="播放动作流", command=self._play_action_flow)
        play_button.pack(side=tk.RIGHT)
        
        # 右侧详情页部分
        self.detail_frame = ttk.Frame(right_frame)
        self.detail_frame.pack(fill=tk.BOTH, expand=True)
        
        # 初始显示空状态
        self._show_empty_detail()
    
    def _show_empty_detail(self):
        """显示空详情页"""
        # 清空详情页
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        
        # 显示提示信息
        empty_label = ttk.Label(self.detail_frame, text="请选择一个动作节点查看详情", font=("SimHei", 12))
        empty_label.pack(expand=True)
    
    def _on_select_node(self, event):
        """选择节点时的处理"""
        selection = self.action_listbox.curselection()
        if not selection:
            self.selected_index = -1
            self._show_empty_detail()
            return
        
        self.selected_index = selection[0]
        if 0 <= self.selected_index < len(self.action_nodes):
            self._show_node_detail(self.action_nodes[self.selected_index])
    
    def _show_node_detail(self, node):
        """显示节点详情"""
        # 清空详情页
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        
        # 根据节点类型显示不同的详情
        if isinstance(node, KeyboardShortcutNode):
            self._show_keyboard_detail(node)
        elif isinstance(node, ButtonClickNode):
            self._show_button_detail(node)
    
    def _show_keyboard_detail(self, node):
        """显示快捷键节点详情"""
        # 显示当前快捷键
        current_label = ttk.Label(self.detail_frame, text="当前快捷键:", font=("SimHei", 10, "bold"))
        current_label.pack(anchor=tk.W, pady=(0, 5))
        
        value_label = ttk.Label(self.detail_frame, text=node.shortcut or "未设置", font=("SimHei", 10))
        value_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 预设快捷键选择
        preset_label = ttk.Label(self.detail_frame, text="选择预设快捷键:", font=("SimHei", 10, "bold"))
        preset_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 创建滚动框架来放置预设快捷键
        preset_frame = ttk.Frame(self.detail_frame)
        preset_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建画布和滚动条
        canvas = tk.Canvas(preset_frame)
        scrollbar = ttk.Scrollbar(preset_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建修饰键选择
        modifier_frame = ttk.LabelFrame(scrollable_frame, text="修饰键")
        modifier_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.ctrl_var = tk.BooleanVar(value=False)
        self.alt_var = tk.BooleanVar(value=False)
        self.shift_var = tk.BooleanVar(value=False)
        self.win_var = tk.BooleanVar(value=False)
        
        ctrl_check = ttk.Checkbutton(modifier_frame, text="Ctrl", variable=self.ctrl_var)
        ctrl_check.pack(side=tk.LEFT, padx=10, pady=5)
        
        alt_check = ttk.Checkbutton(modifier_frame, text="Alt", variable=self.alt_var)
        alt_check.pack(side=tk.LEFT, padx=10, pady=5)
        
        shift_check = ttk.Checkbutton(modifier_frame, text="Shift", variable=self.shift_var)
        shift_check.pack(side=tk.LEFT, padx=10, pady=5)
        
        win_check = ttk.Checkbutton(modifier_frame, text="Win", variable=self.win_var)
        win_check.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 创建预设快捷键按钮网格
        grid_frame = ttk.Frame(scrollable_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # 每行显示10个按钮
        row, col = 0, 0
        for key in self.common_keys:
            btn = ttk.Button(grid_frame, text=key, width=10,
                            command=lambda k=key: self._update_keyboard_shortcut(node, k))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky=tk.NSEW)
            col += 1
            if col >= 10:
                col = 0
                row += 1
        
        # 添加自定义快捷键输入
        custom_frame = ttk.Frame(scrollable_frame)
        custom_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(custom_frame, text="或自定义输入:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.custom_key_var = tk.StringVar(value="")
        custom_entry = ttk.Entry(custom_frame, textvariable=self.custom_key_var, width=20)
        custom_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        apply_custom_button = ttk.Button(custom_frame, text="应用",
                                       command=lambda: self._update_keyboard_shortcut(node, self.custom_key_var.get()))
        apply_custom_button.pack(side=tk.LEFT)
    
    def _update_keyboard_shortcut(self, node, key):
        """更新快捷键"""
        # 获取修饰键
        modifiers = []
        if self.ctrl_var.get():
            modifiers.append("Ctrl")
        if self.alt_var.get():
            modifiers.append("Alt")
        if self.shift_var.get():
            modifiers.append("Shift")
        if self.win_var.get():
            modifiers.append("Win")
        
        # 构建快捷键字符串
        if modifiers and key:
            shortcut = "+" .join(modifiers) + "+" + key
        else:
            shortcut = key
        
        # 更新节点
        node.shortcut = shortcut
        
        # 更新列表
        self._update_action_list()
        
        # 重新显示详情
        self._show_keyboard_detail(node)
    
    def _show_button_detail(self, node):
        """显示按钮点击节点详情"""
        # 显示图片路径
        path_frame = ttk.Frame(self.detail_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(path_frame, text="图片路径:", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        path_var = tk.StringVar(value=node.image_path)
        path_entry = ttk.Entry(path_frame, textvariable=path_var, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ttk.Button(path_frame, text="浏览", command=lambda: self._browse_image(path_var, node))
        browse_button.pack(side=tk.RIGHT)
        
        # 添加点击次数设置
        click_count_frame = ttk.Frame(self.detail_frame)
        click_count_frame.pack(fill=tk.X, pady=(10, 10))
        
        ttk.Label(click_count_frame, text="点击次数:", font=("SimHei", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        count_frame = ttk.Frame(click_count_frame)
        count_frame.pack(anchor=tk.W)
        
        count_var = tk.IntVar(value=node.click_count)
        count_entry = ttk.Entry(count_frame, textvariable=count_var, width=5)
        count_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        apply_count_button = ttk.Button(count_frame, text="应用", 
                                       command=lambda: self._update_click_count(node, count_var))
        apply_count_button.pack(side=tk.LEFT)
        
        # 显示图片预览
        preview_frame = ttk.LabelFrame(self.detail_frame, text="图片预览")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.image_label = ttk.Label(preview_frame)
        self.image_label.pack(expand=True)
        
        # 显示当前图片
        self._update_image_preview(node.image_path)
    
    def _update_click_count(self, node, count_var):
        """更新点击次数"""
        try:
            click_count = max(1, int(count_var.get()))
            node.click_count = click_count
            self._update_action_list()
        except ValueError:
            # 输入不是有效数字时，恢复原值
            count_var.set(node.click_count)
    
    def _browse_image(self, path_var, node):
        """浏览并选择图片"""
        file_path = filedialog.askopenfilename(
            title="选择按钮图片",
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        
        if file_path:
            path_var.set(file_path)
            node.image_path = file_path
            self._update_action_list()
            self._update_image_preview(file_path)
    
    def _update_image_preview(self, image_path):
        """更新图片预览"""
        # 清空之前的图片
        self.image_label.config(image="")
        
        if image_path and os.path.exists(image_path):
            try:
                # 打开图片并调整大小以适应预览区域
                image = Image.open(image_path)
                # 计算合适的尺寸
                max_width = 300
                max_height = 300
                image.thumbnail((max_width, max_height))
                
                # 转换为Tkinter可用的图像
                photo = ImageTk.PhotoImage(image)
                
                # 显示图片
                self.image_label.config(image=photo)
                self.image_label.photo = photo  # 保持引用，防止被垃圾回收
            except Exception as e:
                self.image_label.config(text=f"无法加载图片: {str(e)}")
        else:
            self.image_label.config(text="未选择图片或图片不存在")
    
    def _add_keyboard_node(self):
        """添加快捷键节点"""
        node = KeyboardShortcutNode()
        self.action_nodes.append(node)
        self._update_action_list()
        # 选中新添加的节点
        self.selected_index = len(self.action_nodes) - 1
        self.action_listbox.selection_set(self.selected_index)
        self.action_listbox.see(self.selected_index)
        self._show_node_detail(node)
    
    def _add_button_node(self):
        """添加按钮点击节点"""
        node = ButtonClickNode()
        self.action_nodes.append(node)
        self._update_action_list()
        # 选中新添加的节点
        self.selected_index = len(self.action_nodes) - 1
        self.action_listbox.selection_set(self.selected_index)
        self.action_listbox.see(self.selected_index)
        self._show_node_detail(node)
    
    def _delete_node(self):
        """删除节点"""
        if 0 <= self.selected_index < len(self.action_nodes):
            del self.action_nodes[self.selected_index]
            self._update_action_list()
            self.selected_index = -1
            self._show_empty_detail()
    
    def _update_action_list(self):
        """更新动作列表"""
        self.action_listbox.delete(0, tk.END)
        for i, node in enumerate(self.action_nodes):
            self.action_listbox.insert(tk.END, f"{i+1}. {node.get_description()}")
    
    def _play_action_flow(self):
        """播放动作流"""
        for node in self.action_nodes:
            try:
                time.sleep(1)
                node.execute()
            except Exception as e:
                print(f"执行动作时出错: {e}")
                # 可以选择继续执行下一个动作或停止
                continue


def run_as_admin():
    """以管理员权限重新运行程序"""
    if is_admin():
        # 已经是管理员，直接返回
        return True
    else:
        # 重新以管理员权限启动
        script = sys.argv[0]
        params = ' '.join([f'"{x}"' for x in sys.argv[1:]])
        
        try:
            # 请求管理员权限
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}" {params}', None, 1
            )
            sys.exit(0)  # 退出当前实例
        except Exception as e:
            print(f"请求管理员权限失败: {e}")
            return False
            

def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if not is_admin():
        print("需要管理员权限，正在请求...")
        run_as_admin()
    else:
        print("已具有管理员权限")
        # 你的主程序代码
    root = tk.Tk()
    app = ActionNodeSystem(root)
    root.mainloop()