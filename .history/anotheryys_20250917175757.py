import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import random
import time
from PIL import Image, ImageTk
import pyautogui
import threading
import pygetwindow as gw


class YYSBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("阴阳师自动挂机脚本")
        self.root.geometry("1300x650")

        # 默认模板
        self.default_templates = {
            "魂十一": {
                "name": "魂十一",
                "battle_img": "hun11tz.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "battle_confidence": 0.8,
                "result_confidence": 0.8,
                "reward_confidence": 0.8,
                "cycles": 100,
                "error_action": "continue",
                "rest_cycles": "8-12",
                "rest_time": "5-10",
                "max_wait_time": 60
            },
            "御灵": {
                "name": "御灵",
                "battle_img": "tz.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "battle_confidence": 0.8,
                "result_confidence": 0.8,
                "reward_confidence": 0.8,
                "cycles": 50,
                "error_action": "stop",
                "rest_cycles": "4-6",
                "rest_time": "3-5",
                "max_wait_time": 60
            },
            "组队魂11": {
                "name": "组队魂11",
                "battle_img": "hun11tz.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "battle_confidence": 0.8,
                "result_confidence": 0.8,
                "reward_confidence": 0.8,
                "cycles": 50,
                "error_action": "continue",
                "rest_cycles": "4-6",
                "rest_time": "3-5",
                "max_wait_time": 60,
                "captain_window_title": "阴阳师-网易游戏",  # 队长窗口标题
                "teammate_window_title": "阴阳师-网易游戏"  # 队友窗口标题
            },
            "困难28": {
                "name": "困难28",
                "battle_img": "tansuokaishi.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "kun28_img": "kun28.png",
                "explore_img": "tansuo.png",
                "end_img": "tansuojieshu.png",
                "treasure_img": "zhanlipin.png",
                "battle_confidence": 0.7,
                "result_confidence": 0.8,
                "reward_confidence": 0.8,
                "explore_confidence": 0.8,
                "end_confidence": 0.7,
                "treasure_confidence": 0.8,
                "cycles": 20,
                "error_action": "continue",
                "rest_cycles": "1-2",
                "rest_time": "10-15",
                "max_wait_time": 90
            },
            "结界突破": {
                "name": "结界突破",
                "battle_img": "tupo1.png",
                "victory_img": "jiesuan.png",
                "defeat_img": "failure.png",
                "attack_img": "jingongjiejie.png",
                "battle_confidence": 0.8,
                "result_confidence": 0.8,
                "reward_confidence": 0.7,
                "cycles": 30,
                "error_action": "continue",
                "rest_cycles": "2-4",
                "rest_time": "2-4",
                "max_wait_time": 60
            },
            "业原火": {
                "name": "业原火",
                "battle_img": "tz.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "battle_confidence": 0.7,
                "result_confidence": 0.6,
                "reward_confidence": 0.8,
                "cycles": 80,
                "error_action": "continue",
                "rest_cycles": "6-10",
                "rest_time": "3-7",
                "max_wait_time": 60
            },
            "活动": {
                "name": "活动",
                "battle_img": "huodong.png",
                "victory_img": "jiesuan.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "battle_confidence": 0.8,
                "result_confidence": 0.8,
                "reward_confidence": 0.8,
                "cycles": 50,
                "error_action": "continue",
                "rest_cycles": "5-8",
                "rest_time": "3-6",
                "max_wait_time": 60
            }
        }

        # 添加默认随机点击坐标
        self.default_random_click_pos = {"x": 800, "y": 450}

        # 创建模板目录
        self.template_dir = "templates"
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)

        # 保存模板到文件
        for name, template in self.default_templates.items():
            with open(f"{self.template_dir}/{name}.json", "w", encoding="utf-8") as f:
                json.dump(template, f, indent=2)

        # 当前选中的模板
        self.current_template = self.default_templates["魂十一"]

        # 运行状态
        self.is_running = False
        self.pause_event = threading.Event()
        self.pause_event.set()  # 初始设置为非暂停状态

        self.setup_ui()
        self.load_templates()

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 战斗设置区域
        battle_frame = ttk.LabelFrame(main_frame, text="战斗设置", padding="10")
        battle_frame.grid(row=0, column=0, columnspan=2,
                          sticky=(tk.W, tk.E), pady=(0, 10))

        # 图片设置
        img_frame = ttk.Frame(battle_frame)
        img_frame.grid(row=0, column=0, columnspan=4,
                       sticky=(tk.W, tk.E), pady=(0, 10))

        # 战斗开始图片
        ttk.Label(img_frame, text="战斗开始图片:").grid(row=0, column=0, sticky=tk.W)
        self.battle_img_var = tk.StringVar(
            value=self.current_template["battle_img"])
        ttk.Entry(img_frame, textvariable=self.battle_img_var,
                  width=20).grid(row=0, column=1, padx=(5, 5))
        ttk.Button(img_frame, text="浏览", command=lambda: self.browse_image(
            "battle_img")).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(img_frame, text="预览", command=lambda: self.preview_image(
            self.battle_img_var.get())).grid(row=0, column=3)
        ttk.Label(img_frame, text="置信度:").grid(
            row=0, column=4, sticky=tk.W, padx=(10, 0))
        self.battle_confidence_var = tk.StringVar(
            value=str(self.current_template["battle_confidence"]))
        ttk.Entry(img_frame, textvariable=self.battle_confidence_var,
                  width=8).grid(row=0, column=5, padx=(5, 0))

        # 战斗结果图片
        ttk.Label(img_frame, text="战斗结果图片:").grid(
            row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.result_img_frame = ttk.Frame(img_frame)
        self.result_img_frame.grid(
            row=1, column=1, columnspan=5, sticky=tk.W, pady=(5, 0))

        # 胜利图片
        ttk.Label(self.result_img_frame, text="胜利:").grid(
            row=0, column=0, sticky=tk.W)
        self.victory_img_var = tk.StringVar(
            value=self.current_template["victory_img"])
        ttk.Entry(self.result_img_frame, textvariable=self.victory_img_var, width=15).grid(
            row=0, column=1, padx=(5, 5))
        ttk.Button(self.result_img_frame, text="浏览", command=lambda: self.browse_image(
            "victory_img")).grid(row=0, column=2, padx=(0, 5))
        ttk.Label(self.result_img_frame, text="置信度:").grid(
            row=0, column=3, sticky=tk.W, padx=(5, 0))
        self.victory_confidence_var = tk.StringVar(
            value=str(self.current_template["result_confidence"]))
        ttk.Entry(self.result_img_frame, textvariable=self.victory_confidence_var,
                  width=6).grid(row=0, column=4, padx=(5, 0))

        # 失败图片
        ttk.Label(self.result_img_frame, text="失败:").grid(
            row=0, column=5, sticky=tk.W, padx=(10, 0))
        self.defeat_img_var = tk.StringVar(
            value=self.current_template["defeat_img"])
        ttk.Entry(self.result_img_frame, textvariable=self.defeat_img_var, width=15).grid(
            row=0, column=6, padx=(5, 5))
        ttk.Button(self.result_img_frame, text="浏览", command=lambda: self.browse_image(
            "defeat_img")).grid(row=0, column=7, padx=(0, 5))
        ttk.Label(self.result_img_frame, text="置信度:").grid(
            row=0, column=8, sticky=tk.W, padx=(5, 0))
        self.defeat_confidence_var = tk.StringVar(
            value=str(self.current_template["result_confidence"]))
        ttk.Entry(self.result_img_frame, textvariable=self.defeat_confidence_var,
                  width=6).grid(row=0, column=9, padx=(5, 0))

        # 战利品结算图片
        ttk.Label(img_frame, text="战利品结算图片:").grid(
            row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.reward_img_var = tk.StringVar(
            value=self.current_template["reward_img"])
        ttk.Entry(img_frame, textvariable=self.reward_img_var, width=20).grid(
            row=2, column=1, padx=(5, 5), pady=(5, 0))
        ttk.Button(img_frame, text="浏览", command=lambda: self.browse_image(
            "reward_img")).grid(row=2, column=2, padx=(0, 10), pady=(5, 0))
        ttk.Button(img_frame, text="预览", command=lambda: self.preview_image(
            self.reward_img_var.get())).grid(row=2, column=3, pady=(5, 0))
        ttk.Label(img_frame, text="置信度:").grid(
            row=2, column=4, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        self.reward_confidence_var = tk.StringVar(
            value=str(self.current_template["reward_confidence"]))
        ttk.Entry(img_frame, textvariable=self.reward_confidence_var,
                  width=8).grid(row=2, column=5, padx=(5, 0), pady=(5, 0))

        # 特殊图片设置（根据模板显示）
        self.special_img_frame = ttk.Frame(battle_frame)
        self.special_img_frame.grid(row=3, column=0, columnspan=4,
                                    sticky=(tk.W, tk.E), pady=(5, 10))

        # 参数设置
        param_frame = ttk.Frame(battle_frame)
        param_frame.grid(row=4, column=0, columnspan=4,
                         sticky=(tk.W, tk.E), pady=(10, 0))

        # 在 param_frame 界面设置代码之后添加
        # 随机点击坐标设置
        random_click_frame = ttk.Frame(battle_frame)
        random_click_frame.grid(
            row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Label(random_click_frame, text="随机点击坐标:").grid(
            row=0, column=0, sticky=tk.W)
        ttk.Label(random_click_frame, text="X:").grid(
            row=0, column=1, sticky=tk.W, padx=(10, 0))
        self.random_click_x_var = tk.StringVar(
            value=str(self.default_random_click_pos["x"]))
        ttk.Entry(random_click_frame, textvariable=self.random_click_x_var,
                  width=10).grid(row=0, column=2, padx=(5, 0))

        ttk.Label(random_click_frame, text="Y:").grid(
            row=0, column=3, sticky=tk.W, padx=(10, 0))
        self.random_click_y_var = tk.StringVar(
            value=str(self.default_random_click_pos["y"]))
        ttk.Entry(random_click_frame, textvariable=self.random_click_y_var,
                  width=10).grid(row=0, column=4, padx=(5, 0))

        ttk.Label(random_click_frame, text="(当找不到图片时使用)").grid(
            row=0, column=5, sticky=tk.W, padx=(10, 0))

        # 组队窗口设置
        self.team_window_frame = ttk.Frame(battle_frame)
        self.team_window_frame.grid(
            row=6, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Label(self.team_window_frame, text="队长窗口标题:").grid(
            row=0, column=0, sticky=tk.W)
        self.captain_window_title_var = tk.StringVar(value="阴阳师-网易游戏")
        ttk.Entry(self.team_window_frame, textvariable=self.captain_window_title_var,
                  width=20).grid(row=0, column=1, padx=(5, 10))

        ttk.Label(self.team_window_frame, text="队友窗口标题:").grid(
            row=0, column=2, sticky=tk.W)
        self.teammate_window_title_var = tk.StringVar(value="阴阳师-网易游戏")
        ttk.Entry(self.team_window_frame, textvariable=self.teammate_window_title_var,
                  width=20).grid(row=0, column=3, padx=(5, 0))

        # 模板选择
        ttk.Label(param_frame, text="战斗模式:").grid(row=0, column=0, sticky=tk.W)
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(
            param_frame, textvariable=self.template_var, width=15)
        self.template_combo.grid(row=0, column=1, padx=(5, 10), sticky=tk.W)
        self.template_combo.bind("<<ComboboxSelected>>", self.load_template)
        ttk.Button(param_frame, text="保存为模板", command=self.save_template).grid(
            row=0, column=2, padx=(0, 10))

        # 战斗循环次数
        ttk.Label(param_frame, text="战斗循环次数:").grid(
            row=0, column=3, sticky=tk.W, padx=(10, 0))
        self.cycles_var = tk.StringVar(
            value=str(self.current_template["cycles"]))
        ttk.Entry(param_frame, textvariable=self.cycles_var, width=10).grid(
            row=0, column=4, padx=(5, 0))

        # 错误处理方式
        ttk.Label(param_frame, text="发生错误时:").grid(
            row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.error_action_var = tk.StringVar(
            value=self.current_template["error_action"])
        error_frame = ttk.Frame(param_frame)
        error_frame.grid(row=1, column=1, columnspan=2,
                         sticky=tk.W, pady=(5, 0))
        ttk.Radiobutton(error_frame, text="继续循环", variable=self.error_action_var,
                        value="continue").pack(side=tk.LEFT)
        ttk.Radiobutton(error_frame, text="停止运行", variable=self.error_action_var,
                        value="stop").pack(side=tk.LEFT, padx=(10, 0))

        # 休息设置
        ttk.Label(param_frame, text="每").grid(
            row=1, column=3, sticky=tk.W, pady=(5, 0), padx=(10, 0))
        self.rest_cycles_var = tk.StringVar(
            value=self.current_template["rest_cycles"])
        ttk.Entry(param_frame, textvariable=self.rest_cycles_var, width=10).grid(
            row=1, column=4, padx=(5, 0), pady=(5, 0), sticky=tk.W)
        ttk.Label(param_frame, text="次战斗后休息").grid(
            row=1, column=4, sticky=tk.W, padx=(70, 0), pady=(5, 0))
        self.rest_time_var = tk.StringVar(
            value=self.current_template["rest_time"])
        ttk.Entry(param_frame, textvariable=self.rest_time_var, width=10).grid(
            row=1, column=5, padx=(5, 0), pady=(5, 0))
        ttk.Label(param_frame, text="秒").grid(row=1,
                                              column=5, sticky=tk.W, padx=(70, 0), pady=(5, 0))

        # 最长战斗等待时间设置
        ttk.Label(param_frame, text="最长战斗等待时间:").grid(
            row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.max_wait_time_var = tk.StringVar(
            value=str(self.current_template["max_wait_time"]))
        ttk.Entry(param_frame, textvariable=self.max_wait_time_var, width=10).grid(
            row=2, column=1, padx=(5, 0), pady=(5, 0), sticky=tk.W)
        ttk.Label(param_frame, text="秒").grid(
            row=2, column=1, sticky=tk.W, padx=(70, 0), pady=(5, 0))

        # 运行日志区域
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="10")
        log_frame.grid(row=1, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        self.log_text = tk.Text(log_frame, height=12, width=70)
        log_scroll = ttk.Scrollbar(
            log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 预览窗口
        preview_frame = ttk.LabelFrame(main_frame, text="图片预览", padding="10")
        preview_frame.grid(row=1, column=1, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=(0, 10))

        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.grid(row=0, column=0)

        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.start_btn = ttk.Button(
            button_frame, text="开始战斗", command=self.start_battle)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.pause_btn = ttk.Button(
            button_frame, text="暂停战斗", command=self.pause_battle, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_btn = ttk.Button(
            button_frame, text="结束战斗", command=self.stop_battle, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        # 初始化特殊图片显示
        self.update_special_images()

    def update_special_images(self):
        # 清除之前的特殊图片控件
        for widget in self.special_img_frame.winfo_children():
            widget.destroy()

        # 根据当前模板显示特殊图片设置
        template_name = self.template_var.get()
        if template_name == "困难28":
            # 显示困难28特有的图片设置
            ttk.Label(self.special_img_frame, text="困难28图片:").grid(
                row=0, column=0, sticky=tk.W)
            self.kun28_img_var = tk.StringVar(
                value=self.current_template.get("kun28_img", "kun28.png"))
            ttk.Entry(self.special_img_frame, textvariable=self.kun28_img_var,
                      width=15).grid(row=0, column=1, padx=(5, 5))
            ttk.Button(self.special_img_frame, text="浏览", command=lambda: self.browse_image(
                "kun28_img")).grid(row=0, column=2, padx=(0, 5))
            ttk.Label(self.special_img_frame, text="置信度:").grid(
                row=0, column=3, sticky=tk.W, padx=(5, 0))
            self.kun28_confidence_var = tk.StringVar(
                value=str(self.current_template.get("battle_confidence", 0.8)))
            ttk.Entry(self.special_img_frame, textvariable=self.kun28_confidence_var,
                      width=6).grid(row=0, column=4, padx=(5, 0))

            ttk.Label(self.special_img_frame, text="探索图片:").grid(
                row=0, column=5, sticky=tk.W, padx=(10, 0))
            self.explore_img_var = tk.StringVar(
                value=self.current_template.get("explore_img", "tansuo.png"))
            ttk.Entry(self.special_img_frame, textvariable=self.explore_img_var,
                      width=15).grid(row=0, column=6, padx=(5, 5))
            ttk.Button(self.special_img_frame, text="浏览", command=lambda: self.browse_image(
                "explore_img")).grid(row=0, column=7, padx=(0, 5))
            ttk.Label(self.special_img_frame, text="置信度:").grid(
                row=0, column=8, sticky=tk.W, padx=(5, 0))
            self.explore_confidence_var = tk.StringVar(
                value=str(self.current_template.get("explore_confidence", 0.8)))
            ttk.Entry(self.special_img_frame, textvariable=self.explore_confidence_var,
                      width=6).grid(row=0, column=9, padx=(5, 0))

            ttk.Label(self.special_img_frame, text="结束图片:").grid(
                row=1, column=0, sticky=tk.W, pady=(5, 0))
            self.end_img_var = tk.StringVar(
                value=self.current_template.get("end_img", "tansuojieshu.png"))
            ttk.Entry(self.special_img_frame, textvariable=self.end_img_var,
                      width=15).grid(row=1, column=1, padx=(5, 5), pady=(5, 0))
            ttk.Button(self.special_img_frame, text="浏览", command=lambda: self.browse_image(
                "end_img")).grid(row=1, column=2, padx=(0, 5), pady=(5, 0))
            ttk.Label(self.special_img_frame, text="置信度:").grid(
                row=1, column=3, sticky=tk.W, padx=(5, 0), pady=(5, 0))
            self.end_confidence_var = tk.StringVar(
                value=str(self.current_template.get("end_confidence", 0.7)))
            ttk.Entry(self.special_img_frame, textvariable=self.end_confidence_var,
                      width=6).grid(row=1, column=4, padx=(5, 0), pady=(5, 0))

            ttk.Label(self.special_img_frame, text="战利品图片:").grid(
                row=1, column=5, sticky=tk.W, padx=(10, 0), pady=(5, 0))
            self.treasure_img_var = tk.StringVar(
                value=self.current_template.get("treasure_img", "zhanlipin.png"))
            ttk.Entry(self.special_img_frame, textvariable=self.treasure_img_var,
                      width=15).grid(row=1, column=6, padx=(5, 5), pady=(5, 0))
            ttk.Button(self.special_img_frame, text="浏览", command=lambda: self.browse_image(
                "treasure_img")).grid(row=1, column=7, padx=(0, 5), pady=(5, 0))
            ttk.Label(self.special_img_frame, text="置信度:").grid(
                row=1, column=8, sticky=tk.W, padx=(5, 0), pady=(5, 0))
            self.treasure_confidence_var = tk.StringVar(
                value=str(self.current_template.get("treasure_confidence", 0.8)))
            ttk.Entry(self.special_img_frame, textvariable=self.treasure_confidence_var,
                      width=6).grid(row=1, column=9, padx=(5, 0), pady=(5, 0))
        elif template_name == "结界突破":
            ttk.Label(self.special_img_frame, text="攻击图片:").grid(
                row=0, column=0, sticky=tk.W)
            self.attack_img_var = tk.StringVar(
                value=self.current_template.get("attack_img", "jingongjiejie.png"))
            ttk.Entry(self.special_img_frame, textvariable=self.attack_img_var,
                      width=20).grid(row=0, column=1, padx=(5, 5))
            ttk.Button(self.special_img_frame, text="浏览", command=lambda: self.browse_image(
                "attack_img")).grid(row=0, column=2, padx=(0, 10))
            ttk.Label(self.special_img_frame, text="置信度:").grid(
                row=0, column=3, sticky=tk.W, padx=(5, 0))
            self.attack_confidence_var = tk.StringVar(
                value=str(self.current_template.get("battle_confidence", 0.8)))
            ttk.Entry(self.special_img_frame, textvariable=self.attack_confidence_var,
                      width=8).grid(row=0, column=4, padx=(5, 0))
        elif template_name == "组队魂11":
            self.team_window_frame.grid()  # 显示组队设置
        else:
            self.team_window_frame.grid_remove()  # 隐藏组队设置

    def browse_image(self, img_type):
        file_path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            if img_type == "battle_img":
                self.battle_img_var.set(file_path)
            elif img_type == "victory_img":
                self.victory_img_var.set(file_path)
            elif img_type == "defeat_img":
                self.defeat_img_var.set(file_path)
            elif img_type == "reward_img":
                self.reward_img_var.set(file_path)
            elif img_type == "kun28_img":
                self.kun28_img_var.set(file_path)
            elif img_type == "explore_img":
                self.explore_img_var.set(file_path)
            elif img_type == "end_img":
                self.end_img_var.set(file_path)
            elif img_type == "treasure_img":
                self.treasure_img_var.set(file_path)
            elif img_type == "attack_img":
                self.attack_img_var.set(file_path)

    def preview_image(self, image_path):
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(image)
                self.preview_label.configure(image=photo)
                self.preview_label.image = photo  # 保持引用
            else:
                self.preview_label.configure(image="", text="图片不存在")
        except Exception as e:
            self.preview_label.configure(image="", text=f"预览错误: {str(e)}")

    def load_templates(self):
        templates = list(self.default_templates.keys())
        template_files = os.listdir(self.template_dir)
        for file in template_files:
            if file.endswith(".json"):
                template_name = file[:-5]  # 移除.json后缀
                if template_name not in templates:
                    templates.append(template_name)
        self.template_combo['values'] = templates
        self.template_combo.set("魂十一")

    def load_template(self, event=None):
        template_name = self.template_var.get()
        template_path = f"{self.template_dir}/{template_name}.json"

        try:
            if os.path.exists(template_path):
                with open(template_path, "r", encoding="utf-8") as f:
                    template = json.load(f)
            else:
                template = self.default_templates.get(template_name, {})

            if template:
                self.battle_img_var.set(template.get("battle_img", ""))
                self.victory_img_var.set(template.get("victory_img", ""))
                self.defeat_img_var.set(template.get("defeat_img", ""))
                self.reward_img_var.set(template.get("reward_img", ""))
                self.battle_confidence_var.set(
                    template.get("battle_confidence", "0.8"))
                self.victory_confidence_var.set(
                    template.get("result_confidence", "0.8"))
                self.defeat_confidence_var.set(
                    template.get("result_confidence", "0.8"))
                self.reward_confidence_var.set(
                    template.get("reward_confidence", "0.8"))
                self.cycles_var.set(template.get("cycles", "100"))
                self.error_action_var.set(
                    template.get("error_action", "continue"))
                self.rest_cycles_var.set(template.get("rest_cycles", "8-12"))
                self.rest_time_var.set(template.get("rest_time", "5-10"))
                self.max_wait_time_var.set(template.get("max_wait_time", "60"))
                self.random_click_x_var.set(
                    str(template.get("random_click_x", self.default_random_click_pos["x"])))
                self.random_click_y_var.set(
                    str(template.get("random_click_y", self.default_random_click_pos["y"])))
                # 特殊图片处理
                if template_name == "困难28":
                    if "kun28_img" in template:
                        if hasattr(self, 'kun28_img_var'):
                            self.kun28_img_var.set(
                                template.get("kun28_img", ""))
                            self.kun28_confidence_var.set(
                                template.get("battle_confidence", "0.8"))
                    if "explore_img" in template:
                        if hasattr(self, 'explore_img_var'):
                            self.explore_img_var.set(
                                template.get("explore_img", ""))
                            self.explore_confidence_var.set(
                                template.get("explore_confidence", "0.8"))
                    if "end_img" in template:
                        if hasattr(self, 'end_img_var'):
                            self.end_img_var.set(template.get("end_img", ""))
                            self.end_confidence_var.set(
                                template.get("end_confidence", "0.7"))
                    if "treasure_img" in template:
                        if hasattr(self, 'treasure_img_var'):
                            self.treasure_img_var.set(
                                template.get("treasure_img", ""))
                            self.treasure_confidence_var.set(
                                template.get("treasure_confidence", "0.8"))

                if template_name == "结界突破":
                    if "attack_img" in template and hasattr(self, 'attack_img_var'):
                        self.attack_img_var.set(template.get("attack_img", ""))
                        self.attack_confidence_var.set(
                            template.get("battle_confidence", "0.8"))

                if template_name == "组队魂11":
                    self.captain_window_title_var.set(
                        template.get("captain_window_title", "阴阳师-网易游戏"))
                    self.teammate_window_title_var.set(
                        template.get("teammate_window_title", "阴阳师-网易游戏"))
                    self.team_window_frame.grid()  # 显示组队设置
                else:
                    self.team_window_frame.grid_remove()  # 隐藏组队设置

                self.current_template = template
                self.log(f"已加载模板: {template_name}")
                self.update_special_images()  # 更新特殊图片显示
        except Exception as e:
            self.log(f"加载模板失败: {str(e)}")

    def save_template(self):
        template_name = self.template_var.get()
        if not template_name:
            template_name = "自定义模板"

        template = {
            "name": template_name,
            "battle_img": self.battle_img_var.get(),
            "victory_img": self.victory_img_var.get(),
            "defeat_img": self.defeat_img_var.get(),
            "reward_img": self.reward_img_var.get(),
            "battle_confidence": float(self.battle_confidence_var.get()),
            # 使用胜利图片的置信度作为结果置信度
            "result_confidence": float(self.victory_confidence_var.get()),
            "reward_confidence": float(self.reward_confidence_var.get()),
            "cycles": int(self.cycles_var.get()),
            "error_action": self.error_action_var.get(),
            "rest_cycles": self.rest_cycles_var.get(),
            "rest_time": self.rest_time_var.get(),
            "max_wait_time": int(self.max_wait_time_var.get()),
            "random_click_x": int(self.random_click_x_var.get()),
            "random_click_y": int(self.random_click_y_var.get())
        }

        # 添加特殊图片
        if template_name == "困难28":
            template["kun28_img"] = self.kun28_img_var.get() if hasattr(
                self, 'kun28_img_var') else "kun28.png"
            template["explore_img"] = self.explore_img_var.get() if hasattr(
                self, 'explore_img_var') else "tansuo.png"
            template["end_img"] = self.end_img_var.get() if hasattr(
                self, 'end_img_var') else "tansuojieshu.png"
            template["treasure_img"] = self.treasure_img_var.get() if hasattr(
                self, 'treasure_img_var') else "zhanlipin.png"
            template["battle_confidence"] = float(self.kun28_confidence_var.get()) if hasattr(
                self, 'kun28_confidence_var') else 0.8
            template["explore_confidence"] = float(self.explore_confidence_var.get(
            )) if hasattr(self, 'explore_confidence_var') else 0.8
            template["end_confidence"] = float(self.end_confidence_var.get()) if hasattr(
                self, 'end_confidence_var') else 0.7
            template["treasure_confidence"] = float(self.treasure_confidence_var.get(
            )) if hasattr(self, 'treasure_confidence_var') else 0.8
        elif template_name == "结界突破":
            template["attack_img"] = self.attack_img_var.get() if hasattr(
                self, 'attack_img_var') else "jingongjiejie.png"
            template["battle_confidence"] = float(self.attack_confidence_var.get(
            )) if hasattr(self, 'attack_confidence_var') else 0.8
        elif template_name == "组队魂11":
            template["captain_window_title"] = self.captain_window_title_var.get()
            template["teammate_window_title"] = self.teammate_window_title_var.get()

        try:
            with open(f"{self.template_dir}/{template_name}.json", "w", encoding="utf-8") as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            self.log(f"模板已保存: {template_name}")
            self.load_templates()  # 重新加载模板列表
        except Exception as e:
            self.log(f"保存模板失败: {str(e)}")

            # 设置为新保存的模板
        self.template_combo.set(template_name)
        # 重新加载模板以更新界面
        self.load_template()

    def log(self, message):
        self.log_text.insert(
            tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)

    def parse_range(self, range_str):
        """
        解析范围字符串，如 "5-10"，返回最小值和最大值
        """
        try:
            parts = range_str.split("-")
            if len(parts) == 2:
                min_val = int(parts[0])
                max_val = int(parts[1])
                if min_val <= max_val:
                    return min_val, max_val
        except:
            pass
        return None, None

    def get_random_value_from_range(self, range_str):
        """
        从范围字符串中获取随机值
        """
        min_val, max_val = self.parse_range(range_str)
        if min_val is not None and max_val is not None:
            return random.randint(min_val, max_val)
        return None

    def get_random_mouse_strategy(self):
        strategies = [
            pyautogui.easeInOutElastic, pyautogui.easeInBack, pyautogui.easeInBounce,
            pyautogui.easeInCirc, pyautogui.easeInOutBack, pyautogui.easeInOutCirc,
            pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad
        ]
        return random.choice(strategies)

    def random_click_at_position(self):
        """在指定坐标附近随机点击两次"""
        try:
            x = int(self.random_click_x_var.get())
            y = int(self.random_click_y_var.get())

            # 添加随机偏移量(-50到50像素)
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)

            # 移动到指定位置附近
            target_x = x + offset_x
            target_y = y + offset_y
            pyautogui.moveTo(target_x, target_y,
                             duration=random.uniform(0.5, 1.0))

            # 等待1秒
            time.sleep(1)

            # 点击两次
            for _ in range(2):
                if not self.is_running:
                    break
                self.pause_event.wait()

                pyautogui.click()
                time.sleep(random.uniform(0.1, 0.3))

            self.log(f"在坐标({x}, {y})附近随机点击两次")
        except Exception as e:
            self.log(f"随机点击时出错: {str(e)}")

    def find_image(self, image_path, confidence=0.8, timeout=15):
        """查找图片位置，带超时"""
        try:
            if not os.path.exists(image_path):
                self.log(f"图片不存在: {image_path}")
                self.random_click_at_position()  # 图片不存在时执行随机点击
                return None

            start_time = time.time()
            while time.time() - start_time < timeout and self.is_running:
                self.pause_event.wait()
                pos = pyautogui.locateCenterOnScreen(
                    image_path, confidence=confidence)
                if pos is not None:
                    return pos
                time.sleep(0.01)  # 提高检测频率

            # 超时且未找到图片时执行随机点击
            if self.is_running:
                self.log(f"未找到图片: {image_path}，执行随机点击")
                self.random_click_at_position()
            return None
        except Exception as e:
            self.log(f"查找图片时出错: {str(e)}")
            self.random_click_at_position()  # 出错时也执行随机点击
            return None

    def click_position(self, pos, clicks=1):
        """点击指定位置"""
        if pos:
            # 随机偏移
            x_offset = random.randint(-30, 30)
            y_offset = random.randint(-30, 30)

            # 随机鼠标移动策略
            move_strategy = self.get_random_mouse_strategy()
            move_duration = random.uniform(0.5, 1.5)

            # 移动并点击
            pyautogui.moveTo(
                pos[0] + x_offset,
                pos[1] + y_offset,
                duration=move_duration,
                tween=move_strategy
            )

            # 随机等待后点击
            time.sleep(random.uniform(0.1, 0.5))
            for _ in range(clicks):
                pyautogui.click()
                if clicks > 1:
                    time.sleep(random.uniform(0.1, 0.3))

    def drag_screen(self):
        """滑动屏幕"""
        try:
            pyautogui.moveTo(1400 + random.randint(-50, 50),
                             260 + random.randint(-20, 20))
            pyautogui.dragRel(-800, 0, random.uniform(0.8, 1.5))
        except Exception as e:
            self.log(f"滑动屏幕时出错: {str(e)}")

    def wait_for_battle_result(self, victory_img, defeat_img, reward_img,
                               victory_conf=0.8, defeat_conf=0.8, reward_conf=0.8,
                               max_wait_time=60):
        """
        等待战斗结果，同时检测胜利、失败和奖励图片
        战斗开始后约5秒开始检测，检测频率为0.5秒一次
        如果超过最大等待时间，则在当前位置随机点击两次
        """
        # 等待5秒后开始检测
        time.sleep(5)

        start_time = time.time()
        while self.is_running and (time.time() - start_time) < max_wait_time:
            self.pause_event.wait()

            # 同时检测三种图片
            victory_pos = pyautogui.locateCenterOnScreen(
                victory_img, confidence=victory_conf)
            defeat_pos = pyautogui.locateCenterOnScreen(
                defeat_img, confidence=defeat_conf)
            reward_pos = pyautogui.locateCenterOnScreen(
                reward_img, confidence=reward_conf)

            # 如果检测到任意一种图片，返回其位置
            if victory_pos is not None:
                return "victory", victory_pos
            elif defeat_pos is not None:
                return "defeat", defeat_pos
            elif reward_pos is not None:
                return "reward", reward_pos

            # 每0.5秒检测一次
            time.sleep(0.5)

        # 超时处理
        if self.is_running:
            self.log(f"战斗超时({max_wait_time}秒)，在当前位置随机点击两次")
            # 获取当前鼠标位置
            current_x, current_y = pyautogui.position()

            # 随机点击两次
            for i in range(2):
                if not self.is_running:
                    break
                self.pause_event.wait()

                # 添加随机偏移
                x_offset = random.randint(-50, 50)
                y_offset = random.randint(-50, 50)

                # 点击
                pyautogui.click(current_x + x_offset, current_y + y_offset)
                self.log(f"超时处理：第{i+1}次随机点击")

                # 等待一小段时间
                time.sleep(random.uniform(0.5, 1.0))

            return "timeout", (current_x, current_y)

        return None, None

    """ def click_result_position(self, pos):
        """
    # 在结果位置点击三次，每次间隔0.01~0.2秒
    """
        for _ in range(2):
            if not self.is_running:
                break
            self.pause_event.wait()

            # 点击位置
            self.click_position(pos)

            # 等待0.01~0.2秒
            time.sleep(random.uniform(0.01, 0.2)) """

    def click_result_position(self, pos):

        # 点击位置
        self.click_position(pos)

        # 等待0.01~0.2秒
        time.sleep(random.uniform(0.01, 0.2))

    def activate_window(self, window_title):
        """激活指定标题的窗口"""
        try:
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                window = windows[0]
                window.activate()
                return window
            else:
                self.log(f"未找到窗口: {window_title}")
                return None
        except Exception as e:
            self.log(f"激活窗口时出错: {str(e)}")
            return None

    def find_image_in_window(self, image_path, confidence, window_title, timeout=15):
        """在指定窗口中查找图片"""
        try:
            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                self.log(f"未找到窗口: {window_title}")
                return None

            window = windows[0]

            # 激活窗口
            window.activate()

            # 设置检测区域为窗口区域
            region = (window.left, window.top, window.width, window.height)

            start_time = time.time()
            while time.time() - start_time < timeout and self.is_running:
                self.pause_event.wait()
                try:
                    pos = pyautogui.locateCenterOnScreen(
                        image_path, confidence=confidence, region=region)
                    if pos is not None:
                        return pos
                except:
                    pass
                time.sleep(0.1)

            return None
        except Exception as e:
            self.log(f"在窗口中查找图片时出错: {str(e)}")
            return None

    def click_in_window(self, pos, window_title):
        """在指定窗口中点击"""
        try:
            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                self.log(f"未找到窗口: {window_title}")
                return False

            window = windows[0]

            # 激活窗口
            window.activate()

            # 添加随机偏移
            x_offset = random.randint(-30, 30)
            y_offset = random.randint(-30, 30)

            # 随机鼠标移动策略
            move_strategy = self.get_random_mouse_strategy()
            move_duration = random.uniform(0.5, 1.5)

            # 移动并点击
            pyautogui.moveTo(
                pos[0] + x_offset,
                pos[1] + y_offset,
                duration=move_duration,
                tween=move_strategy
            )

            # 随机等待后点击
            time.sleep(random.uniform(0.1, 0.5))
            pyautogui.click()

            return True
        except Exception as e:
            self.log(f"在窗口中点击时出错: {str(e)}")
            return False

    def team_hun11_strategy(self):
        """组队魂11策略"""
        try:
            cycles = int(self.cycles_var.get())
            error_action = self.error_action_var.get()
            max_wait_time = int(self.max_wait_time_var.get())

            # 获取窗口标题
            captain_title = self.captain_window_title_var.get()
            teammate_title = self.teammate_window_title_var.get()

            # 获取置信度
            battle_confidence = float(self.battle_confidence_var.get())
            victory_confidence = float(self.victory_confidence_var.get())
            defeat_confidence = float(self.defeat_confidence_var.get())
            reward_confidence = float(self.reward_confidence_var.get())

            # 检查窗口是否存在
            captain_windows = gw.getWindowsWithTitle(captain_title)
            teammate_windows = gw.getWindowsWithTitle(teammate_title)

            if not captain_windows:
                self.log(f"未找到队长窗口: {captain_title}")
                return

            if not teammate_windows:
                self.log(f"未找到队友窗口: {teammate_title}")
                return

            self.log(f"找到队长窗口: {captain_title}")
            self.log(f"找到队友窗口: {teammate_title}")

            for i in range(1, cycles + 1):
                if not self.is_running:
                    break
                self.pause_event.wait()

                self.log(f"开始第 {i} 次组队魂11")

                # 在队长窗口中开始战斗（只有队长窗口有战斗开始按钮）
                self.log("激活队长窗口...")
                captain_window = self.activate_window(captain_title)
                if not captain_window:
                    if error_action == "stop":
                        break
                    continue

                # 查找并点击战斗开始按钮（仅在队长窗口）
                battle_pos = self.find_image_in_window(
                    self.battle_img_var.get(), battle_confidence, captain_title, 10)

                if not battle_pos:
                    self.log("队长窗口未找到战斗开始按钮")
                    if error_action == "stop":
                        break
                    continue

                self.click_in_window(battle_pos, captain_title)
                self.log("队长进入战斗，等待战斗结果...")

                # 等待战斗开始
                time.sleep(5)

                # 在队长窗口等待战斗胜利
                self.log("等待队长战斗胜利...")
                victory_pos = self.find_image_in_window(
                    self.victory_img_var.get(), victory_confidence, captain_title, max_wait_time)

                if not victory_pos:
                    self.log("队长窗口未检测到战斗胜利")
                    if error_action == "stop":
                        break
                    continue

                self.click_in_window(victory_pos, captain_title)
                self.log("队长点击战斗胜利确认")

                # 等待战利品结算
                time.sleep(2)
                reward_pos = self.find_image_in_window(
                    self.reward_img_var.get(), reward_confidence, captain_title, 30)

                if reward_pos:
                    self.click_in_window(reward_pos, captain_title)
                    self.log("队长点击战利品结算确认")
                else:
                    self.log("队长窗口未检测到战利品结算界面")

                # 切换到队友窗口处理
                self.log("激活队友窗口...")
                teammate_window = self.activate_window(teammate_title)
                if not teammate_window:
                    if error_action == "stop":
                        break
                    continue

                # 等待并点击队友战斗胜利
                self.log("等待队友战斗胜利...")
                teammate_victory_pos = self.find_image_in_window(
                    self.victory_img_var.get(), victory_confidence, teammate_title, 20)

                if teammate_victory_pos:
                    self.click_in_window(teammate_victory_pos, teammate_title)
                    self.log("队友点击战斗胜利确认")

                    # 等待队友战利品结算
                    time.sleep(2)
                    teammate_reward_pos = self.find_image_in_window(
                        self.reward_img_var.get(), reward_confidence, teammate_title, 20)

                    if teammate_reward_pos:
                        self.click_in_window(
                            teammate_reward_pos, teammate_title)
                        self.log("队友点击战利品结算确认")
                    else:
                        self.log("队友窗口未检测到战利品结算界面")
                else:
                    self.log("队友窗口未检测到战斗胜利")

                # 切换回队长窗口准备下一轮
                self.log("激活队长窗口准备下一轮...")
                self.activate_window(captain_title)

                self.log(f"第 {i} 次组队魂11完成")

                # 检查是否需要休息
                rest_cycles = self.get_random_value_from_range(
                    self.rest_cycles_var.get())
                if rest_cycles is not None and i % rest_cycles == 0 and i < cycles:
                    rest_time = self.get_random_value_from_range(
                        self.rest_time_var.get())
                    if rest_time is None:
                        rest_time = 5
                    self.log(f"休息 {rest_time} 秒")
                    # 分段休息，以便能响应暂停/停止命令
                    for _ in range(rest_time):
                        if not self.is_running:
                            break
                        time.sleep(1)

        except Exception as e:
            self.log(f"组队魂11执行出错: {str(e)}")

    def kun28_strategy(self):
        """困难28策略"""
        try:
            cycles = int(self.cycles_var.get())
            error_action = self.error_action_var.get()
            max_wait_time = int(self.max_wait_time_var.get())

            # 获取置信度
            battle_confidence = float(self.kun28_confidence_var.get()) if hasattr(
                self, 'kun28_confidence_var') else 0.8
            explore_confidence = float(self.explore_confidence_var.get()) if hasattr(
                self, 'explore_confidence_var') else 0.8
            end_confidence = float(self.end_confidence_var.get()) if hasattr(
                self, 'end_confidence_var') else 0.7
            treasure_confidence = float(self.treasure_confidence_var.get()) if hasattr(
                self, 'treasure_confidence_var') else 0.8
            result_confidence = float(self.victory_confidence_var.get())
            reward_confidence = float(self.reward_confidence_var.get())

            for i in range(1, cycles + 1):
                if not self.is_running:
                    break
                self.pause_event.wait()

                self.log(f"开始第 {i} 次困难28")

                # 查找困难28按钮
                kun28_img = self.kun28_img_var.get() if hasattr(
                    self, 'kun28_img_var') else 'kun28.png'
                kun28_pos = self.find_image(kun28_img, battle_confidence)

                start_img = self.battle_img_var.get()
                start_pos = self.find_image(start_img, 0.7)

                if start_pos is None and kun28_pos is not None:
                    self.click_position(kun28_pos)

                # 查找开始按钮
                start_pos = self.find_image(start_img, 0.7)
                if not start_pos:
                    self.log("未找到开始按钮")
                    if error_action == "stop":
                        break
                    continue

                self.click_position(start_pos)

                # 探索过程
                end_img = self.end_img_var.get() if hasattr(
                    self, 'end_img_var') else 'tansuojieshu.png'
                end_pos = self.find_image(end_img, end_confidence)

                while not end_pos and self.is_running:
                    self.pause_event.wait()

                    explore_img = self.explore_img_var.get() if hasattr(
                        self, 'explore_img_var') else 'tansuo.png'
                    explore_pos = self.find_image(
                        explore_img, explore_confidence)

                    if explore_pos is not None:
                        self.click_position(explore_pos)

                        # 等待战斗开始，然后开始检测战斗结果
                        time.sleep(5)

                        # 使用改进的检测方式等待战斗结果
                        result_type, result_pos = self.wait_for_battle_result(
                            self.victory_img_var.get(),
                            self.defeat_img_var.get(),
                            self.reward_img_var.get(),
                            result_confidence,
                            result_confidence,
                            reward_confidence,
                            max_wait_time
                        )

                        if result_pos is None:  # 用户停止了脚本
                            break

                        # 如果不是超时情况，才进行点击操作
                        if result_type != "timeout":
                            self.click_result_position(result_pos)
                            self.log(f"检测到战斗结果({result_type})，点击确认")
                        else:
                            self.log("战斗超时，已进行随机点击处理")

                        time.sleep(2 + random.uniform(0, 1))

                        end_pos = self.find_image(end_img, end_confidence)
                    else:
                        time.sleep(1)
                        end_pos = self.find_image(end_img, end_confidence)
                        if not end_pos:
                            self.drag_screen()

                if end_pos and self.is_running:
                    self.click_position(end_pos)
                    self.log("探索结束，点击确认")
                    time.sleep(2 + random.uniform(0, 1))

                    # 最终结算
                    victory_pos = self.find_image(
                        self.victory_img_var.get(), result_confidence)
                    if victory_pos:
                        self.click_position(victory_pos)
                        time.sleep(2 + random.uniform(0, 1))

                    reward_pos = self.find_image(
                        self.reward_img_var.get(), reward_confidence)
                    if reward_pos:
                        self.click_position(reward_pos)
                        time.sleep(5)

                        # 处理战利品
                        treasure_img = self.treasure_img_var.get() if hasattr(
                            self, 'treasure_img_var') else 'zhanlipin.png'
                        treasure_pos = self.find_image(
                            treasure_img, treasure_confidence)
                        while treasure_pos and self.is_running:
                            self.click_position(treasure_pos)
                            time.sleep(0.5)
                            pyautogui.click(810 + random.randint(-80, 80),
                                            770 + random.randint(-5, 30))
                            time.sleep(1)
                            treasure_pos = self.find_image(
                                treasure_img, treasure_confidence)

                self.log(f"第 {i} 次困难28完成")

                # 检查是否需要休息
                rest_cycles = self.get_random_value_from_range(
                    self.rest_cycles_var.get())
                if rest_cycles is not None and i % rest_cycles == 0 and i < cycles:
                    rest_time = self.get_random_value_from_range(
                        self.rest_time_var.get())
                    if rest_time is None:
                        rest_time = 5
                    self.log(f"休息 {rest_time} 秒")
                    # 分段休息，以便能响应暂停/停止命令
                    for _ in range(rest_time):
                        if not self.is_running:
                            break
                        time.sleep(1)

        except Exception as e:
            self.log(f"困难28执行出错: {str(e)}")

    def jiejietupo_strategy(self):
        """结界突破策略"""
        try:
            cycles = int(self.cycles_var.get())
            error_action = self.error_action_var.get()
            max_wait_time = int(self.max_wait_time_var.get())

            # 获取置信度
            battle_confidence = float(self.battle_confidence_var.get())
            attack_confidence = float(self.attack_confidence_var.get()) if hasattr(
                self, 'attack_confidence_var') else 0.8
            result_confidence = float(self.victory_confidence_var.get())
            defeat_confidence = float(self.defeat_confidence_var.get())
            reward_confidence = float(self.reward_confidence_var.get())

            for i in range(1, cycles + 1):
                if not self.is_running:
                    break
                self.pause_event.wait()

                self.log(f"开始第 {i} 次结界突破")

                # 查找突破按钮
                start_pos = self.find_image(
                    self.battle_img_var.get(), battle_confidence)
                if not start_pos:
                    self.log("未找到突破按钮")
                    if error_action == "stop":
                        break
                    continue

                pyautogui.click(start_pos[0] - 20, start_pos[1])

                # 查找攻击按钮
                attack_img = self.attack_img_var.get() if hasattr(
                    self, 'attack_img_var') else 'jingongjiejie.png'
                attack_pos = self.find_image(attack_img, attack_confidence)
                if not attack_pos:
                    self.log("未找到攻击按钮")
                    if error_action == "stop":
                        break
                    continue

                self.click_position(attack_pos)

                # 等待进入战斗，然后开始检测战斗结果
                time.sleep(5)

                # 使用改进的检测方式等待战斗结果
                result_type, result_pos = self.wait_for_battle_result(
                    self.victory_img_var.get(),
                    self.defeat_img_var.get(),
                    self.reward_img_var.get(),
                    result_confidence,
                    defeat_confidence,
                    reward_confidence,
                    max_wait_time
                )

                if result_pos is None:  # 用户停止了脚本
                    break

                # 如果不是超时情况，才进行点击操作
                if result_type != "timeout":
                    self.click_result_position(result_pos)
                    self.log(f"检测到战斗结果({result_type})，点击确认")
                else:
                    self.log("战斗超时，已进行随机点击处理")

                time.sleep(2 + random.uniform(0, 1))

                self.log(f"第 {i} 次结界突破完成")

                # 检查是否需要休息
                rest_cycles = self.get_random_value_from_range(
                    self.rest_cycles_var.get())
                if rest_cycles is not None and i % rest_cycles == 0 and i < cycles:
                    rest_time = self.get_random_value_from_range(
                        self.rest_time_var.get())
                    if rest_time is None:
                        rest_time = 5
                    self.log(f"休息 {rest_time} 秒")
                    # 分段休息，以便能响应暂停/停止命令
                    for _ in range(rest_time):
                        if not self.is_running:
                            break
                        time.sleep(1)

        except Exception as e:
            self.log(f"结界突破执行出错: {str(e)}")

    def default_strategy(self):
        """改进的默认策略（适用于魂十一、御灵等）"""
        try:
            cycles = int(self.cycles_var.get())
            error_action = self.error_action_var.get()
            max_wait_time = int(self.max_wait_time_var.get())

            # 获取置信度
            battle_confidence = float(self.battle_confidence_var.get())
            victory_confidence = float(self.victory_confidence_var.get())
            defeat_confidence = float(self.defeat_confidence_var.get())
            reward_confidence = float(self.reward_confidence_var.get())

            for i in range(1, cycles + 1):
                if not self.is_running:
                    break
                self.pause_event.wait()

                self.log(f"开始第 {i} 次战斗")

                # 查找并点击战斗开始按钮
                battle_pos = self.find_image(
                    self.battle_img_var.get(), battle_confidence)
                if not battle_pos:
                    self.log("未找到战斗开始按钮")
                    pyautogui.doubleClick()
                    if error_action == "stop":
                        break
                    continue

                self.click_position(battle_pos)
                self.log("进入战斗，等待战斗结果...")

                # 使用改进的检测方式等待战斗结果
                result_type, result_pos = self.wait_for_battle_result(
                    self.victory_img_var.get(),
                    self.defeat_img_var.get(),
                    self.reward_img_var.get(),
                    victory_confidence,
                    defeat_confidence,
                    reward_confidence,
                    max_wait_time
                )

                if result_pos is None:  # 用户停止了脚本
                    break

                # 如果不是超时情况，才进行点击操作
                if result_type != "timeout":
                    # 在结果位置点击三次
                    self.click_result_position(result_pos)
                    self.log(f"检测到战斗结果({result_type})，点击确认")
                else:
                    self.log("战斗超时，已进行随机点击处理")

                self.log(f"第 {i} 次战斗完成")

                # 检查是否需要休息
                rest_cycles = self.get_random_value_from_range(
                    self.rest_cycles_var.get())
                if rest_cycles is not None and i % rest_cycles == 0 and i < cycles:
                    rest_time = self.get_random_value_from_range(
                        self.rest_time_var.get())
                    if rest_time is None:
                        rest_time = 5
                    self.log(f"休息 {rest_time} 秒")
                    # 分段休息，以便能响应暂停/停止命令
                    for _ in range(rest_time):
                        if not self.is_running:
                            break
                        time.sleep(1)

        except Exception as e:
            self.log(f"战斗执行出错: {str(e)}")

    def battle_loop(self):
        try:
            template_name = self.template_var.get()
            self.log(f"开始执行 {template_name} 策略...")

            if template_name == "困难28":
                self.kun28_strategy()
            elif template_name == "结界突破":
                self.jiejietupo_strategy()
            elif template_name == "组队魂11":
                self.team_hun11_strategy()
            else:
                self.default_strategy()

            self.log("自动战斗结束")
        except Exception as e:
            self.log(f"战斗过程中发生错误: {str(e)}")
        finally:
            self.stop_battle()

    def start_battle(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.NORMAL)

            # 在新线程中运行战斗循环
            self.battle_thread = threading.Thread(target=self.battle_loop)
            self.battle_thread.daemon = True
            self.battle_thread.start()

    def pause_battle(self):
        if self.is_running:
            if self.pause_event.is_set():
                self.pause_event.clear()
                self.pause_btn.config(text="继续战斗")
                self.log("战斗已暂停")
            else:
                self.pause_event.set()
                self.pause_btn.config(text="暂停战斗")
                self.log("战斗已继续")

    def stop_battle(self):
        self.is_running = False
        self.pause_event.set()  # 确保不是暂停状态
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED, text="暂停战斗")
        self.stop_btn.config(state=tk.DISABLED)
        self.log("战斗已停止")


if __name__ == "__main__":
    root = tk.Tk()
    app = YYSBotGUI(root)
    root.mainloop()
