import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
# # 设置字体为SimHei，并将其设置为默认字体
# plt.rcParams['font.family'] = 'SimHei'
# plt.rcParams['font.sans-serif'] = ['SimHei']
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # 创建画布和坐标轴
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        # 获取主窗口的位置和尺寸
        self.master .update_idletasks()  # 更新窗口信息
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()
        root_x = self.master.winfo_rootx()
        root_y = self.master.winfo_rooty()
        #
        # # 计算弹窗的位置
        popup_x = 20  # 加向右
        popup_y = 700

        # 设置弹窗的位置
        self.master.geometry(f"+{popup_x}+{popup_y}")



        # 创建画布控件
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        # 启动定时器
        self.update_chart()

    def update_chart(self):
        try:
            # 读取文件内容
            data = np.loadtxt('Sine_Wave_output.txt')

            # 生成时间戳
            timestamps = np.arange(len(data))

            # 清除原有图形
            self.ax.clear()

            # 绘制新图形
            # self.ax.scatter(timestamps, data)
            self.ax.plot(timestamps, data, '-')

            # 在每个点上添加文本标签
            for x, y in zip(timestamps, data):
                self.ax.text(x, y, f'{y:.2f}', fontsize=0, ha='center', va='bottom')
            # 显示网格线

            self.ax.grid(True)
            self.ax.set_xlabel('Timestamp')
            self.ax.set_ylabel('Data')
            self.ax.set_title('Sine_Wave_output')
            # 更新画布
            self.canvas.draw()


        except Exception as e:
            pass
            # print(e)

        # 下一次更新的时间间隔（单位是毫秒）
        interval = 1

        # 启动下一次定时器
        self.master.after(interval, self.update_chart)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
