import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import random
import time
from PIL import Image, ImageTk
import pyautogui
import cv2
import threading


class YYSBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("阴阳师自动挂机脚本")
        self.root.geometry("900x750")

        # 默认模板
        self.default_templates = {
            "魂十一": {
                "battle_img": "hun11tz.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "duration": 30,
                "cycles": 100,
                "error_action": "continue",
                "rest_cycles": "8-12",
                "rest_time": "5-10",
                "confidence": 0.8,
                "x_offset": "-30,30",
                "y_offset": "-30,30"
            },
            "御灵": {
                "battle_img": "tz.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "duration": 45,
                "cycles": 50,
                "error_action": "stop",
                "rest_cycles": "4-6",
                "rest_time": "3-5",
                "confidence": 0.75,
                "x_offset": "-20,20",
                "y_offset": "-20,20"
            },
            "结界突破": {
                "battle_img": "tupo1.png",
                "victory_img": "jiesuan.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "duration": 60,
                "cycles": 30,
                "error_action": "continue",
                "rest_cycles": "2-4",
                "rest_time": "2-4",
                "confidence": 0.85,
                "x_offset": "-40,40",
                "y_offset": "-40,40"
            },
            "业原火": {
                "battle_img": "tz.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "duration": 25,
                "cycles": 80,
                "error_action": "continue",
                "rest_cycles": "6-10",
                "rest_time": "3-7",
                "confidence": 0.7,
                "x_offset": "-25,25",
                "y_offset": "-25,25"
            },
            "困难28": {
                "battle_img": "tansuokaishi.png",
                "victory_img": "victory.png",
                "defeat_img": "failure.png",
                "reward_img": "jiesuan.png",
                "duration": 120,
                "cycles": 20,
                "error_action": "continue",
                "rest_cycles": "1-2",
                "rest_time": "10-15",
                "confidence": 0.8,
                "x_offset": "-50,50",
                "y_offset": "-50,50"
            }
        }

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

        # 战斗胜利图片
        ttk.Label(img_frame, text="战斗胜利图片:").grid(
            row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.victory_img_var = tk.StringVar(
            value=self.current_template["victory_img"])
        ttk.Entry(img_frame, textvariable=self.victory_img_var, width=20).grid(
            row=1, column=1, padx=(5, 5), pady=(5, 0))
        ttk.Button(img_frame, text="浏览", command=lambda: self.browse_image(
            "victory_img")).grid(row=1, column=2, padx=(0, 10), pady=(5, 0))
        ttk.Button(img_frame, text="预览", command=lambda: self.preview_image(
            self.victory_img_var.get())).grid(row=1, column=3, pady=(5, 0))

        # 战斗失败图片
        ttk.Label(img_frame, text="战斗失败图片:").grid(
            row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.defeat_img_var = tk.StringVar(
            value=self.current_template["defeat_img"])
        ttk.Entry(img_frame, textvariable=self.defeat_img_var, width=20).grid(
            row=2, column=1, padx=(5, 5), pady=(5, 0))
        ttk.Button(img_frame, text="浏览", command=lambda: self.browse_image(
            "defeat_img")).grid(row=2, column=2, padx=(0, 10), pady=(5, 0))
        ttk.Button(img_frame, text="预览", command=lambda: self.preview_image(
            self.defeat_img_var.get())).grid(row=2, column=3, pady=(5, 0))

        # 战利品结算图片
        ttk.Label(img_frame, text="战利品结算图片:").grid(
            row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.reward_img_var = tk.StringVar(
            value=self.current_template["reward_img"])
        ttk.Entry(img_frame, textvariable=self.reward_img_var, width=20).grid(
            row=3, column=1, padx=(5, 5), pady=(5, 0))
        ttk.Button(img_frame, text="浏览", command=lambda: self.browse_image(
            "reward_img")).grid(row=3, column=2, padx=(0, 10), pady=(5, 0))
        ttk.Button(img_frame, text="预览", command=lambda: self.preview_image(
            self.reward_img_var.get())).grid(row=3, column=3, pady=(5, 0))

        # 参数设置
        param_frame = ttk.Frame(battle_frame)
        param_frame.grid(row=1, column=0, columnspan=4,
                         sticky=(tk.W, tk.E), pady=(10, 0))

        # 模板选择
        ttk.Label(param_frame, text="战斗模式:").grid(row=0, column=0, sticky=tk.W)
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(
            param_frame, textvariable=self.template_var, width=15)
        self.template_combo.grid(row=0, column=1, padx=(5, 10), sticky=tk.W)
        self.template_combo.bind("<<ComboboxSelected>>", self.load_template)
        ttk.Button(param_frame, text="保存为模板", command=self.save_template).grid(
            row=0, column=2, padx=(0, 10))

        # 战斗持续时间
        ttk.Label(param_frame, text="战斗持续时间(秒):").grid(
            row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.duration_var = tk.StringVar(
            value=str(self.current_template["duration"]))
        ttk.Entry(param_frame, textvariable=self.duration_var, width=10).grid(
            row=1, column=1, padx=(5, 0), sticky=tk.W, pady=(5, 0))

        # 战斗循环次数
        ttk.Label(param_frame, text="战斗循环次数:").grid(
            row=1, column=2, sticky=tk.W, pady=(5, 0), padx=(10, 0))
        self.cycles_var = tk.StringVar(
            value=str(self.current_template["cycles"]))
        ttk.Entry(param_frame, textvariable=self.cycles_var, width=10).grid(
            row=1, column=3, padx=(5, 0), sticky=tk.W, pady=(5, 0))

        # 错误处理方式
        ttk.Label(param_frame, text="发生错误时:").grid(
            row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.error_action_var = tk.StringVar(
            value=self.current_template["error_action"])
        error_frame = ttk.Frame(param_frame)
        error_frame.grid(row=2, column=1, columnspan=3,
                         sticky=tk.W, pady=(5, 0))
        ttk.Radiobutton(error_frame, text="继续循环", variable=self.error_action_var,
                        value="continue").pack(side=tk.LEFT)
        ttk.Radiobutton(error_frame, text="停止运行", variable=self.error_action_var,
                        value="stop").pack(side=tk.LEFT, padx=(10, 0))

        # 休息设置
        ttk.Label(param_frame, text="每").grid(
            row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.rest_cycles_var = tk.StringVar(
            value=self.current_template["rest_cycles"])
        ttk.Entry(param_frame, textvariable=self.rest_cycles_var, width=10).grid(
            row=3, column=1, padx=(5, 0), sticky=tk.W, pady=(5, 0))
        ttk.Label(param_frame, text="次战斗后休息").grid(
            row=3, column=1, sticky=tk.W, padx=(70, 0), pady=(5, 0))
        self.rest_time_var = tk.StringVar(
            value=self.current_template["rest_time"])
        ttk.Entry(param_frame, textvariable=self.rest_time_var, width=10).grid(
            row=3, column=2, padx=(5, 0), sticky=tk.W, pady=(5, 0))
        ttk.Label(param_frame, text="秒").grid(row=3,
                                              column=2, sticky=tk.W, padx=(70, 0), pady=(5, 0))

        # 图像识别置信度
        ttk.Label(param_frame, text="图像识别置信度:").grid(
            row=4, column=0, sticky=tk.W, pady=(5, 0))
        self.confidence_var = tk.StringVar(
            value=str(self.current_template["confidence"]))
        ttk.Entry(param_frame, textvariable=self.confidence_var, width=10).grid(
            row=4, column=1, padx=(5, 0), sticky=tk.W, pady=(5, 0))

        # 坐标偏移设置
        offset_frame = ttk.Frame(param_frame)
        offset_frame.grid(row=5, column=0, columnspan=4,
                          sticky=(tk.W, tk.E), pady=(5, 0))
        ttk.Label(offset_frame, text="X坐标偏移:").pack(side=tk.LEFT)
        self.x_offset_var = tk.StringVar(
            value=self.current_template["x_offset"])
        ttk.Entry(offset_frame, textvariable=self.x_offset_var,
                  width=10).pack(side=tk.LEFT, padx=(5, 10))
        ttk.Label(offset_frame, text="Y坐标偏移:").pack(side=tk.LEFT)
        self.y_offset_var = tk.StringVar(
            value=self.current_template["y_offset"])
        ttk.Entry(offset_frame, textvariable=self.y_offset_var,
                  width=10).pack(side=tk.LEFT, padx=(5, 0))

        # 运行日志区域
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="10")
        log_frame.grid(row=1, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        self.log_text = tk.Text(log_frame, height=10, width=60)
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
                self.duration_var.set(template.get("duration", "30"))
                self.cycles_var.set(template.get("cycles", "100"))
                self.error_action_var.set(
                    template.get("error_action", "continue"))
                self.rest_cycles_var.set(template.get("rest_cycles", "8-12"))
                self.rest_time_var.set(template.get("rest_time", "5-10"))
                self.confidence_var.set(template.get("confidence", "0.8"))
                self.x_offset_var.set(template.get("x_offset", "-30,30"))
                self.y_offset_var.set(template.get("y_offset", "-30,30"))

                self.current_template = template
                self.log(f"已加载模板: {template_name}")
        except Exception as e:
            self.log(f"加载模板失败: {str(e)}")

    def save_template(self):
        template_name = self.template_var.get()
        if not template_name:
            template_name = "自定义模板"

        template = {
            "battle_img": self.battle_img_var.get(),
            "victory_img": self.victory_img_var.get(),
            "defeat_img": self.defeat_img_var.get(),
            "reward_img": self.reward_img_var.get(),
            "duration": int(self.duration_var.get()),
            "cycles": int(self.cycles_var.get()),
            "error_action": self.error_action_var.get(),
            "rest_cycles": self.rest_cycles_var.get(),
            "rest_time": self.rest_time_var.get(),
            "confidence": float(self.confidence_var.get()),
            "x_offset": self.x_offset_var.get(),
            "y_offset": self.y_offset_var.get()
        }

        try:
            with open(f"{self.template_dir}/{template_name}.json", "w", encoding="utf-8") as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            self.log(f"模板已保存: {template_name}")
            self.load_templates()  # 重新加载模板列表
        except Exception as e:
            self.log(f"保存模板失败: {str(e)}")

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

    def get_random_offset(self, offset_str):
        try:
            parts = offset_str.split(",")
            if len(parts) == 2:
                min_val = int(parts[0])
                max_val = int(parts[1])
                return random.randint(min_val, max_val)
        except:
            pass
        return 0

    def get_random_mouse_strategy(self):
        strategies = [
            pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad,
            pyautogui.easeInCubic, pyautogui.easeOutCubic, pyautogui.easeInOutCubic,
            pyautogui.easeInQuart, pyautogui.easeOutQuart, pyautogui.easeInOutQuart,
            pyautogui.easeInQuint, pyautogui.easeOutQuint, pyautogui.easeInOutQuint,
            pyautogui.easeInSine, pyautogui.easeOutSine, pyautogui.easeInOutSine,
            pyautogui.easeInExpo, pyautogui.easeOutExpo, pyautogui.easeInOutExpo,
            pyautogui.easeInCirc, pyautogui.easeOutCirc, pyautogui.easeInOutCirc,
            pyautogui.easeInElastic, pyautogui.easeOutElastic, pyautogui.easeInOutElastic,
            pyautogui.easeInBack, pyautogui.easeOutBack, pyautogui.easeInOutBack,
            pyautogui.easeInBounce, pyautogui.easeOutBounce, pyautogui.easeInOutBounce
        ]
        return random.choice(strategies)

    def find_and_click(self, image_path, confidence=0.7, clicks=None, click_when_not_found=True):
        try:
            if not os.path.exists(image_path):
                self.log(f"图片不存在: {image_path}")
                # 如果图片不存在且需要在未找到时点击，则执行随机点击
                if click_when_not_found:
                    self.random_click()
                return False

            pos = pyautogui.locateCenterOnScreen(
                image_path, confidence=confidence)
            if pos:
                # 添加随机偏移
                x_offset = self.get_random_offset(self.x_offset_var.get())
                y_offset = self.get_random_offset(self.y_offset_var.get())

                # 随机点击次数
                if clicks is None:
                    clicks = random.randint(1, 3)

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

                return True
            else:
                # 未找到图片但在屏幕上点击
                if click_when_not_found:
                    self.random_click()
                return False
        except Exception as e:
            self.log(f"查找点击图片时出错: {str(e)}")
            # 出错时也执行随机点击
            if click_when_not_found:
                self.random_click()
            return False

    def random_click(self):
        """
        在当前鼠标位置附近进行随机点击
        """
        try:
            # 获取当前鼠标位置
            current_x, current_y = pyautogui.position()

            # 添加随机偏移
            x_offset = self.get_random_offset(self.x_offset_var.get())
            y_offset = self.get_random_offset(self.y_offset_var.get())

            # 随机点击次数 (1次)
            clicks = 1

            # 随机鼠标移动策略
            move_strategy = self.get_random_mouse_strategy()
            move_duration = random.uniform(0.2, 0.8)

            # 移动到位置
            pyautogui.moveTo(
                current_x + x_offset,
                current_y + y_offset,
                duration=move_duration,
                tween=move_strategy
            )

            # 随机等待后点击
            time.sleep(random.uniform(0.1, 0.3))
            for _ in range(clicks):
                pyautogui.click()
                time.sleep(random.uniform(0.1, 0.2))

            self.log("未找到目标图片，执行随机点击")
        except Exception as e:
            self.log(f"随机点击时出错: {str(e)}")

    def battle_loop(self):
        try:
            # 获取参数
            cycles = int(self.cycles_var.get())
            duration = int(self.duration_var.get())
            confidence = float(self.confidence_var.get())
            rest_cycles_range = self.rest_cycles_var.get()
            rest_time_range = self.rest_time_var.get()
            error_action = self.error_action_var.get()

            self.log("开始自动战斗...")

            for i in range(1, cycles + 1):
                # 检查是否暂停或停止
                if not self.is_running:
                    break
                self.pause_event.wait()  # 如果暂停则等待

                self.log(f"开始第 {i} 次战斗")

                # 查找并点击战斗开始按钮 (找不到则报错处理)
                if not self.find_and_click(self.battle_img_var.get(), confidence, click_when_not_found=False):
                    self.log("未找到战斗开始按钮")
                    if error_action == "stop":
                        break
                    continue

                # 等待战斗结束
                time.sleep(duration)

                # 查找胜利或失败界面
                victory_found = self.find_and_click(
                    self.victory_img_var.get(), confidence, click_when_not_found=False)
                defeat_found = False

                # 如果没有找到胜利图片，则查找失败图片
                if not victory_found:
                    defeat_found = self.find_and_click(
                        self.defeat_img_var.get(), confidence, click_when_not_found=False)

                # 如果既没有找到胜利也没有找到失败图片，则等待结算界面出现
                if not victory_found and not defeat_found:
                    self.log("未检测到战斗结果界面，等待结算界面出现")
                    # 等待一小段时间再尝试查找结算界面
                    time.sleep(1)

                # 查找结算界面
                reward_found = self.find_and_click(
                    self.reward_img_var.get(), confidence, click_when_not_found=False)

                # 如果没有找到战利品结算图片，则在鼠标当前位置随机点击1次
                if not reward_found:
                    self.log("未找到战利品结算界面，执行随机点击")
                    self.random_click()

                # 检查是否需要休息
                rest_cycles = self.get_random_value_from_range(
                    rest_cycles_range)
                if rest_cycles is not None and i % rest_cycles == 0 and i < cycles:
                    rest_time = self.get_random_value_from_range(
                        rest_time_range)
                    if rest_time is None:
                        rest_time = 5  # 默认休息时间

                    self.log(f"第 {i} 次战斗完成，休息 {rest_time} 秒")
                    time.sleep(rest_time)
                else:
                    self.log(f"第 {i} 次战斗完成")

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
