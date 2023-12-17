import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os

class Application(tk.Frame):
    def __init__(self, master=None, txt='Sine_Wave_output.txt'):
        super().__init__(master)
        self.master = master
        self.pack()
        self.txt = txt
        self.data = None  # 存储所有数据
        self.line = None  # 存储绘制的线条
        self.last_modified_time = 0  # 上次文件的最后修改时间
        self.create_widgets()

    def create_widgets(self):
        # 创建画布和坐标轴
        self.fig, self.ax = plt.subplots(figsize=(8, 6))

        # 设置弹窗的位置
        popup_x = 1500  # 加向右
        popup_y = 400
        self.master.geometry(f"+{popup_x}+{popup_y}")
        # 设置窗口标题
        self.master.title(self.txt)
        # 创建画布控件
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        # 读取数据
        self.read_data()
        # 绘制空的线条
        if self.data is not None:
            self.line, = self.ax.plot([], [], '-')
            self.ax.set_xlabel('Timestamp')
            self.ax.set_ylabel('Data')
            self.ax.set_title(self.txt)
            self.ax.grid(True)

            # 更新画布
            self.canvas.draw()

        # 启动定时器
        self.update_chart()

    def read_data(self):
        try:
            # 读取文件内容
            self.data = np.loadtxt(self.txt)

        except Exception as e:
            # 处理异常，避免程序崩溃
            pass

    def update_chart(self):
        try:
            if self.data is not None:
                # 获取当前线条上已经绘制的数据点数
                num_points = len(self.line.get_xdata())
                # 如果还有数据点没有绘制，则继续添加新的数据点
                if num_points < len(self.data):
                    # 获取下一个数据点的坐标
                    x = [num_points]
                    y = [self.data[num_points]]
                    # 添加到线条中
                    self.line.set_xdata(np.concatenate([self.line.get_xdata(), x]))
                    self.line.set_ydata(np.concatenate([self.line.get_ydata(), y]))
                    # 调整坐标轴范围
                    self.ax.relim()
                    self.ax.autoscale_view()
                    self.canvas.draw()

                # 检查文件是否有修改并更新数据
                self.check_file_changes()

        except Exception as e:
            # 处理异常，避免程序崩溃
            pass

        # 下一次更新的时间间隔（单位是毫秒）
        interval = 1  # 设置为100毫秒

        # 启动下一次定时器
        self.master.after(interval, self.update_chart)

    def check_file_changes(self):
        try:
            # 获取文件的最后修改时间
            current_modified_time = os.path.getmtime(self.txt)

            # 如果文件的最后修改时间与之前保存的时间不同，则进行数据的重新读取和图表的更新
            if current_modified_time != self.last_modified_time:
                # 保存当前的最后修改时间
                self.last_modified_time = current_modified_time

                # 重新读取数据
                self.read_data()

                # 清空线条上已绘制的数据点
                self.line.set_data([], [])

                # 更新画布
                self.canvas.draw()

        except Exception as e:
            # 处理异常，避免程序崩溃
            pass

if __name__ == '__main__':
    # 获取命令行参数
    if len(sys.argv) > 1:
        txt_file = sys.argv[1]
    else:
        txt_file = 'Sine_Wave_output.txt'

    root = tk.Tk()
    app = Application(master=root, txt=txt_file)
    app.mainloop()
