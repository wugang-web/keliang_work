import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import ttk
import threading
import subprocess
import time
class SineWaveApp:
    def __init__(self, master):
        self.master = master
        self.amplitude = tk.DoubleVar(value=1.0)

        # 创建Canvas对象并绑定事件处理函数
        self.canvas = tk.Canvas(self.master, width=1200, height=600)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.draw_sine_wave)

        # 创建Label和Entry对象用于输入amplitude的值
        amplitude_label = tk.Label(self.master, text="Amplitude:")
        amplitude_label.place(x=60,y=50)
        amplitude_entry = tk.Entry(self.master, textvariable=self.amplitude)
        amplitude_entry.place(x=60,y=70)

        # 创建按钮
        self.button = tk.Button(self.master, text="生成正弦波数据", command=self.draw_sine_wave)
        self.button.place(x=60,y=110)

    def draw_sine_wave(self, event=None):
        # 获取amplitude的值
        amplitude = self.amplitude.get()

        # 计算正弦波信号
        x_values = np.linspace(0, 2 * np.pi, 1000)
        y_values = amplitude * np.sin(x_values)

        # 将 y_values 存入文本文件 data.txt
        with open('Sine_Wave_output.txt', 'w') as file:
            for value in y_values:
                file.write(f'{value}\n')

        # # # 绘制正弦波图形
        # plt.plot(x_values, y_values)
        # plt.xlabel('x')
        # plt.ylabel('y')
        # plt.title('Sine Wave')
        # plt.grid(True)
        # plt.show()

# 乘法器Mult
class Mult:
    def __init__(self, canvas, x, y):
        self.canvas = canvas

        # 创建标签对象
        self.label1 = tk.Label(canvas, text="Number 1:")
        self.label1.place(x=x+30, y=y)

        # 创建输入框对象
        self.entry1 = tk.Entry(canvas)
        self.entry1.insert(0, "1.0")  # 设置默认值为1.0
        self.entry1.place(x=x+80+30, y=y)

        # 创建标签对象
        self.label2 = tk.Label(canvas, text="Number 2:")
        self.label2.place(x=x+30, y=y+30)

        # 创建输入框对象
        self.entry2 = tk.Entry(canvas)
        self.entry2.insert(0, "1.0")  # 设置默认值为1.0
        self.entry2.place(x=x+80+30, y=y+30)

        # 创建按钮对象
        self.button = tk.Button(canvas, text="生成乘法器数据", command=self.multiply)
        self.button.place(x=x+40+30, y=y+90)

        # 创建输出框对象
        self.output = tk.Label(canvas, text="")
        self.output.place(x=x+40+30+80+40, y=y+90)

        # 创建标签对象
        self.label3 = tk.Label(canvas, text="Number 1:")
        self.label3.place(x=230, y=200)

        # 创建标签对象
        self.label4 = tk.Label(canvas, text="Number 2:")
        self.label4.place(x=230, y=250)



    def multiply(self):
        try:
            print(combo.get())
            print(combo_combobox.get())
            print(combo_combobox_2.get())
            if combo.get() == "组合模式" and combo_combobox.get() != "空.txt" and combo_combobox_2.get() == "空.txt":
                # print(combo_combobox.get())
                data_num1 = np.loadtxt(combo_combobox.get())
                num2 = float(self.entry2.get())
                result = data_num1 * num2
                with open('Mult_data_output.txt', 'w') as file:
                    if type(result) == np.ndarray:
                        for value in result:
                            file.write(f'{value}\n')
                    elif type(result) == np.float64:
                        file.write(f'{result}\n')
            elif combo.get() == "组合模式" and combo_combobox.get() == "空.txt" and combo_combobox_2.get() != "空.txt":
                # print(combo_combobox.get())
                num1 = float(self.entry1.get())
                data_num2 = np.loadtxt(combo_combobox_2.get())
                result = data_num2 * num1
                with open('Mult_data_output.txt', 'w') as file:
                    if type(result) == np.ndarray:
                        for value in result:
                            file.write(f'{value}\n')
                    elif type(result) == np.float64:
                        file.write(f'{result}\n')

            elif combo.get() == "组合模式" and combo_combobox.get() != "空.txt" and combo_combobox_2.get() != "空.txt":
                # print(combo_combobox.get())
                data_num1 = np.loadtxt(combo_combobox.get())
                data_num2 = np.loadtxt(combo_combobox_2.get())
                result = data_num1 * data_num2
                with open('Mult_data_output.txt', 'w') as file:
                    print(type(result))
                    if type(result) == np.ndarray:
                        for value in result:
                            file.write(f'{value}\n')
                    elif type(result) == np.float64:
                        file.write(f'{result}\n')
            else:
                num1 = float(self.entry1.get())
                num2 = float(self.entry2.get())
                result = num1 * num2
                print(result)
            # 将 y_values 存入文本文件 data.txt
                self.output.config(text=f"{result:.2f}")
        except ValueError:
            self.output.config(text="Invalid input")



class GainGUI:
    def __init__(self, master):
        self.master = master

        # 创建输入、输出和参数输入框
        self.input_label = tk.Label(master, text="Input:")
        self.input_label.place(x=500,y=30)
        # self.input_label.pack()
        self.input_entry = tk.Entry(master)
        self.input_entry.insert(0, "1.0")  # 设置默认值为1.0
        self.input_entry.place(x=500,y=50)

        self.output_label = tk.Label(master, text="Output:")
        self.output_label.place(x=500,y=70)
        self.output_entry = tk.Entry(master)
        self.output_entry.insert(0, "0.0")  # 设置默认值为1.0
        self.output_entry.place(x=500,y=90)

        self.param_label = tk.Label(master, text="Parameter:")
        self.param_label.place(x=500,y=110)
        self.param_entry = tk.Entry(master)
        self.param_entry.insert(0, "1.0")  # 设置默认值为1.0
        self.param_entry.place(x=500,y=130)
        # 创建输入、输出和参数输入框
        self.input_label_2 = tk.Label(master, text="Input:")
        self.input_label_2.place(x=500,y=200)

        self.param_label = tk.Label(master, text="Parameter:")
        self.param_label.place(x=500,y=260)
        self.combo_combobox_2 = ttk.Combobox(canvas, values=files, state="readonly")
        self.combo_combobox_2.current(0)  # 设置默认选项为第一个选项（索引为0）
        self.combo_combobox_2.place(x=500, y=290)

        # 创建计算按钮
        self.calculate_button = tk.Button(master, text="生成增益器数据", command=self.calculate_gain)
        self.calculate_button.place(x=500,y=150)

    def calculate_gain(self):
        try:
            if combo.get() == "组合模式" and combo_combobox_1.get() != "空.txt" and self.combo_combobox_2.get() == "空.txt":
                # print(combo_combobox.get())
                data_num1 = np.loadtxt(combo_combobox_1.get())
                num2 = float(self.param_entry.get())
                result = data_num1 * num2
                with open('Gain_output.txt', 'w') as file:
                    print(type(result))
                    if type(result) == np.ndarray:
                        for value in result:
                            file.write(f'{value}\n')
                    elif type(result) == np.float64:
                        file.write(f'{result}\n')
            elif combo.get() == "组合模式" and combo_combobox_1.get() == "空.txt" and self.combo_combobox_2.get() != "空.txt":
                # print(combo_combobox.get())
                num1 = float(self.input_entry.get())
                data_num2 = np.loadtxt(self.combo_combobox_2.get())
                result = data_num2 * num1
                with open('Gain_output.txt', 'w') as file:
                    print(type(result))
                    if type(result) == np.ndarray:
                        for value in result:
                            file.write(f'{value}\n')
                    elif type(result) == np.float64:
                        file.write(f'{result}\n')
            elif combo.get() == "组合模式" and combo_combobox_1.get() != "空.txt" and self.combo_combobox_2.get() != "空.txt":
                # print(combo_combobox.get())
                data_num1 = np.loadtxt(combo_combobox_1.get())
                data_num2 = np.loadtxt(self.combo_combobox_2.get())
                result = data_num1 * data_num2
                with open('Gain_output.txt', 'w') as file:
                    print(type(result))
                    if type(result) == np.ndarray:
                        for value in result:
                            file.write(f'{value}\n')
                    elif type(result) == np.float64:
                        file.write(f'{result}\n')

            # # 从输入框中获取输入数和参数
            # if combo.get() == "组合模式" and combo_combobox_1.get() != "空.txt" and self.combo_combobox_2.get() != "空.txt":
            #     # print(combo_combobox.get())
            #     data_num1 = np.loadtxt(combo_combobox_1.get())
            #     print(data_num1)
            #     data_num2 = np.loadtxt(self.combo_combobox_2.get())
            #     result = data_num1 * data_num2
            #     with open('Gain_output.txt', 'w') as file:
            #         for value in result:
            #             file.write(f'{value}\n')
            # elif combo.get() == "组合模式" and combo_combobox_1.get() == "空.txt":
            #     data_num1 = float(self.input_entry.get())
            #     num2 = float(self.param_entry.get())
            #
            #     result = data_num1 * num2
            #     with open('Gain_output.txt', 'w') as file:
            #         file.write(f'{result}\n')
            else:
                input_num = float(self.input_entry.get())
                param = float(self.param_entry.get())

                # 计算并显示输出结果
                output_num = input_num * param
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, str(output_num))
        except ValueError:
            # 如果输入不是数字，则清空输出框
            self.output_entry.delete(0, tk.END)
class SumCalculator:

    def __init__(self, window, files=None):
        self.window = window

        self.label_num1 = tk.Label(window, text="第一个数：")
        self.label_num1.place(x=700,y=30)
        self.entry_num1 = tk.Entry(window)
        self.entry_num1.insert(0, "1.0")  # 设置默认值为1.0
        self.entry_num1.place(x=700,y=50)

        self.label_num2 = tk.Label(window, text="第二个数：")
        self.label_num2.place(x=700,y=70)
        self.entry_num2 = tk.Entry(window)
        self.entry_num2.insert(0, "1.0")  # 设置默认值为1.0
        self.entry_num2.place(x=700,y=90)

        self.button_calculate = tk.Button(window, text="加法器数据生成", command=self.calculate_sum)
        self.button_calculate.place(x=700,y=120)

        self.label_result = tk.Label(window, text="结果：")
        self.label_result.place(x=700,y=150)
        self.entry_result = tk.Entry(window)
        self.entry_result.place(x=700,y=180)

        self.label_num1 = tk.Label(window, text="第一个数：")
        self.label_num1.place(x=700,y=200)
        self.combo_combobox = ttk.Combobox(canvas, values=files, state="readonly")
        self.combo_combobox.current(0)  # 设置默认选项为第一个选项（索引为0）
        self.combo_combobox.place(x=700, y=230)

        self.label_num2 = tk.Label(window, text="第二个数：")
        self.label_num2.place(x=700,y=260)
        self.combo_combobox_2 = ttk.Combobox(canvas, values=files, state="readonly")
        self.combo_combobox_2.current(0)  # 设置默认选项为第一个选项（索引为0）
        self.combo_combobox_2.place(x=700, y=290)

    def calculate_sum(self):
        if combo.get() == "组合模式" and self.combo_combobox != "空.txt" and self.combo_combobox_2.get() == "空.txt":
            # print(combo_combobox.get())
            data_num1 = np.loadtxt(combo_combobox_1.get())
            num2 = float(self.entry_num2.get())
            result = data_num1 + num2
            with open('SumCalculator_output.txt', 'w') as file:
                print(type(result))
                if type(result) == np.ndarray:
                    for value in result:
                        file.write(f'{value}\n')
                elif type(result) == np.float64:
                    file.write(f'{result}\n')
        elif combo.get() == "组合模式" and self.combo_combobox.get() == "空.txt" and self.combo_combobox_2.get() != "空.txt":
            # print(combo_combobox.get())
            num1 = float(self.entry_num1.get())
            data_num2 = np.loadtxt(self.combo_combobox_2.get())
            result = data_num2 + num1
            with open('SumCalculator_output.txt', 'w') as file:
                print(type(result))
                if type(result) == np.ndarray:
                    for value in result:
                        file.write(f'{value}\n')
                elif type(result) == np.float64:
                    file.write(f'{result}\n')
        elif combo.get() == "组合模式" and self.combo_combobox.get() != "空.txt" and self.combo_combobox_2.get() != "空.txt":
            # print(combo_combobox.get())
            data_num1 = np.loadtxt(self.combo_combobox.get())
            data_num2 = np.loadtxt(self.combo_combobox_2.get())
            result = data_num1 + data_num2
            with open('SumCalculator_output.txt', 'w') as file:
                print(type(result))
                if type(result) == np.ndarray:
                    for value in result:
                        file.write(f'{value}\n')
                elif type(result) == np.float64:
                    file.write(f'{result}\n')

        # if combo.get() == "组合模式" and self.combo_combobox != "空.txt" and self.combo_combobox_2.get() != "空.txt":
        #     # print(combo_combobox.get())
        #     data_num1 = np.loadtxt(self.combo_combobox.get())
        #     # print(len(data_num1))
        #     num2 = np.loadtxt(self.combo_combobox_2.get())
        #     result = data_num1 + num2
        #     with open('SumCalculator_output.txt', 'w') as file:
        #         for value in result:
        #             file.write(f'{value}\n')
        # elif combo.get() == "组合模式" and self.combo_combobox == "空.txt" and self.combo_combobox_2.get() != "空.txt":
        #     # print(combo_combobox.get())
        #     num1 = float(self.entry_num1.get())
        #     data_num2 = np.loadtxt(self.combo_combobox_2.get())
        #     print(len(data_num2))
        #     result = data_num2 + num1
        #     with open('SumCalculator.txt', 'w') as file:
        #         for value in result:
        #             file.write(f'{value}\n')
        # elif combo.get() == "组合模式" and self.combo_combobox != "空.txt" and self.combo_combobox_2.get() != "空.txt":
        #     # print(combo_combobox.get())
        #     data_num1 = np.loadtxt(self.combo_combobox.get())
        #     data_num2 = np.loadtxt(self.combo_combobox_2.get())
        #     result = data_num1 + data_num2
        #     print(type(data_num2))
        #     with open('SumCalculator.txt', 'w') as file:
        #         for value in result:
        #             file.write(f'{value}\n')
        else:
            num1 = float(self.entry_num1.get())
            num2 = float(self.entry_num2.get())
            result = num1 + num2
            self.entry_result.delete(0, tk.END)
            self.entry_result.insert(tk.END, str(result))


class ConstantOutput:
    def __init__(self, window):
        self.window = window

        self.label_param = tk.Label(window, text="参数值：")
        self.label_param.place(x=900,y=30)

        self.entry1 = tk.Entry(window)
        self.entry1.insert(0, "0.0")  # 设置默认值为1.0
        self.entry1.place(x=900,y=60)
        self.entry1.bind("<KeyRelease>", self.output_param)  # 绑定键盘释放事件

        self.label_output = tk.Label(window, text="输出结果：")
        self.label_output.place(x=900,y=140)

        self.label_param_1 = tk.Label(window, text="参数值：")
        self.label_param_1.place(x=900,y=160)

        self.entry2 = tk.Entry(window)
        self.entry2.insert(0, "0.0")  # 设置默认值为1.0
        self.entry2.place(x=900,y=180)
        self.entry2.bind("<KeyRelease>", self.output_param_1)  # 绑定键盘释放事件

        self.label_output_1 = tk.Label(window, text="输出结果：")
        self.label_output_1.place(x=900,y=250)

    def output_param(self, event):
        param = self.entry1.get()
        self.label_output.configure(text=f"输出结果：{param}")
        with open('Constant_output.txt', 'w') as file:
            file.write(f'{param}\n')

    def output_param_1(self, event):
        param = self.entry2.get()
        self.label_output_1.configure(text=f"输出结果：{param}")
        with open('Constant_output_1.txt', 'w') as file:
            file.write(f'{param}\n')

#
# def run():



def read_data_background_SineWaveApp():
    # 模拟读取数据的耗时操作
    temp = combo.get()
    print(temp)
    subprocess.call(['python', r'D:\gugeliulanqi\mycode-mycodetest\all_test\Real_time_read_file_data.py'])
def read_data_background():
    # 模拟读取数据的耗时操作
    temp = combo.get()
    print(temp)
    subprocess.call(['python', r'D:\gugeliulanqi\mycode-mycodetest\all_test\Real_time_read_file_data_finally.py'])
def read_data_background_2():
    # 模拟读取数据的耗时操作
    temp = combo.get()
    # print(temp)
    subprocess.call(['python', r'D:\gugeliulanqi\mycode-mycodetest\all_test\Real_time_read_file_data_finally_gian.py'])

def read_data_background_3():
    # 模拟读取数据的耗时操作
    temp = combo.get()
    # print(temp)
    subprocess.call(['python', r'D:\gugeliulanqi\mycode-mycodetest\all_test\Real_time_read_file_data_finally_SumCalculator.py'])
def start_background_thread():
    # 创建并启动后台线程-正弦
    background_thread_SineWaveApp = threading.Thread(target=read_data_background_SineWaveApp)
    background_thread_SineWaveApp.start()
    # 创建并启动后台线程-乘法器
    background_thread = threading.Thread(target=read_data_background)
    background_thread.start()
    # 创建并启动后台线程-增益器
    background_thread_2 = threading.Thread(target=read_data_background_2)
    background_thread_2.start()
    # 创建并启动后台线程-加法器
    background_thread_3 = threading.Thread(target=read_data_background_3)
    background_thread_3.start()

# 获取文件txt文件
def get_files_in_folder(folder):
    files = []
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path) and item.endswith(".txt"):
            files.append(item)
    return files
def clear_file(files):
    for file_path in files:
        with open(file_path, 'w') as file:
            print(file_path,"文本文件内容已清空")
            file.truncate(0)
            file.write("0")  # 将默认值0写入文件


def add_new_line():
    new_entry = tk.Entry(root)
    new_entry.pack()
    entry_list.append(new_entry)

    if len(entry_list) > 1:
        # 设置新文本框的 insert 索引为第一个文本框文字的最后位置
        last_entry_text = entry_list[-2].get()
        new_entry.insert(0, last_entry_text)

        # # 更新已有按钮的位置
        # for button in button_list:
        #     button.place_configure(y=button.winfo_y() + 30)

def delete_current_line():
    current_entry = root.focus_get()  # 获取当前焦点的文本框

    if current_entry in entry_list:
        # 删除当前文本框
        current_entry.pack_forget()
        entry_list.remove(current_entry)

        # # 更新已有文本框和按钮的位置
        # for entry in entry_list:
        #     entry.pack_forget()
        #     entry.pack()

        # for button in button_list:
        #     button.place_configure(y=button.winfo_y() - 30)

def on_button_click(button_text):
    current_entry = root.focus_get()  # 获取当前焦点的文本框

    if current_entry in entry_list:
        text = current_entry.get()
        if button_text == "增益器":
            text += "增" + " "
        if button_text == "加法器":
            text += "加" + " "
        if button_text == "正弦波":
            text += "正" + " "
        if button_text == "常数器":
            text += "常" + " "
        if button_text == "乘法器":
            text += "乘" + " "
        current_entry.delete(0, tk.END)
        current_entry.insert(0, text)

    # global button_count, current_button_text
    # button_count += 1
    # if button_count >= 2:
    #     current_button_text = ""
    # current_button_text += button_text

    # button.config(text=current_button_text)

def run():
    # 创建执行函数
    num_iterations = int(entry_iterations.get())
    for _ in range(num_iterations):
        for entry in entry_list:
            text = entry.get()
            text_list = text.split(" ")
            time.sleep(2)  # 模拟操作间隔
            for text in text_list:
                if text == "增":
                    gui.calculate_button.invoke()
                if text == "加":
                    Sum.button_calculate.invoke()
                if text == "正":
                    SineWaveApp.button.invoke()
                if text == "常":
                    pass
                if text == "乘":
                    mult_1.button.invoke()

# 虚拟事件对象
class Event:
    pass

if __name__ == "__main__":
    # 创建主窗口
    # 获取文件夹中的以".txt"结尾的文件列表
    folder_path = r"D:\gugeliulanqi\mycode-mycodetest\all_test"  # 替换为你的文件夹路径
    files = get_files_in_folder(folder_path)


    try:
        clear_file(files)
        print("文本文件内容全部已清空")
    except Exception as e:
        print("清空文本文件内容时出现错误：", e)

    root = tk.Tk()
    entry_list = []  # 用于保存所有的文本框
    button_count = 0  # 记录按钮点击次数
    current_button_text = ""  # 记录当前按钮文字
    root.title("问题1")

    # 创建画布
    canvas = tk.Canvas(root, width=1200, height=900)
    canvas.pack()

    # 正弦波
    SineWaveApp = SineWaveApp(canvas)

    # 创建乘法器对象
    mult_1 = Mult(canvas, 200, 50)

    # 文本创建拖动
    # name = data_state(canvas, 1000, 1000).in_f_txt()
    # 创建 Combobox 组件并设置下拉选项
    combo = ttk.Combobox(canvas, values=["组合模式", "单独模式"])
    combo.current(0)  # 设置默认选项为第一个选项（索引为0）
    combo.place(x=60,y=250)



    # 增益器
    gui = GainGUI(root)
    # 求和
    Sum = SumCalculator(root, files=get_files_in_folder(folder_path))
    # # 常量
    Constant = ConstantOutput(root)
    # 创建按钮来启动后台线程
    start_button = ttk.Button(canvas, text="开启数据监控", command=start_background_thread)
    start_button.place(x=250, y=300)

    # 组合
    # 创建Combobox并设置选项值
    combo_combobox = ttk.Combobox(canvas, values=files, state="readonly")
    combo_combobox.current(0)  # 设置默认选项为第一个选项（索引为0）
    combo_combobox.place(x=300, y=200)
    combo_combobox_2 = ttk.Combobox(canvas, values=files, state="readonly")
    combo_combobox_2.current(0)  # 设置默认选项为第一个选项（索引为0）
    combo_combobox_2.place(x=300, y=250)

    # 增益器
    # 创建Combobox并设置选项值
    combo_combobox_1 = ttk.Combobox(canvas, values=files, state="readonly")
    combo_combobox_1.current(0)  # 设置默认选项为第一个选项（索引为0）
    combo_combobox_1.place(x=500, y=230)


    button_texts = ["增益器", "正弦波", "加法器", "乘法器", "常数器"]
    button_positions = [(100, 500), (150, 500), (200, 500), (250, 500), (300, 500)]

    # 创建初始的一行文本框和按钮
    initial_entry = tk.Entry(root)
    initial_entry.pack()
    entry_list.append(initial_entry)

    button_list = []
    for i in range(len(button_texts)):
        button = tk.Button(root, text=button_texts[i], command=lambda text=button_texts[i]: on_button_click(text))
        button.place(x=button_positions[i][0], y=button_positions[i][1])
        button_list.append(button)

    # 新增一行按钮
    button_add_line = tk.Button(root, text="新增一行", command=add_new_line)
    button_add_line.place(x=350, y=500)

    # 删除当前行按钮
    button_delete_line = tk.Button(root, text="删除当前行", command=delete_current_line)
    button_delete_line.place(x=500, y=500)

    # 创建输入执行次数的输入框和执行按钮
    label_iterations = tk.Label(root, text="执行次数:")
    label_iterations.place(x=650, y=500)
    entry_iterations = tk.Entry(root)
    entry_iterations.insert(0,"1")
    entry_iterations.place(x=740, y=500)

    delete_button = tk.Button(root, text="执行", command=run)
    delete_button.place(x=600, y=500)
    # run()
    root.mainloop()