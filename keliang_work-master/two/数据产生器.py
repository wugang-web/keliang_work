import numpy as np
import time
from datetime import datetime
import rethinkdb as r

# 连接到 RethinkDB
conn = r.connect(host='127.0.0.1', port=28015, db='test')

# # 创建数据库和表格
# r.db_create('test').run(conn)
# r.db('test').table_create('sin_data_100Hz').run(conn)
# r.db('test').table_create('sin_data_1000Hz').run(conn)
# r.db('test').table_create('sin_data_500Hz').run(conn)
# r.db("test").table("sin_data_100Hz").delete().run(conn)
# r.db("test").table("sin_data_1000Hz").delete().run(conn)
# r.db("test").table("sin_data_500Hz").delete().run(conn)

def generate_sine_wave_data(freq, duration, sampling_rate):
    """生成指定频率、时长和采样率的正弦波数据"""
    total_samples = int(duration * sampling_rate)
    time_array = np.linspace(0, duration, total_samples)
    data = np.sin(2 * np.pi * freq * time_array)
    return data

# 设置总时长
total_duration = 3600   # 总时长为1秒

# 三个正弦波的频率和采样率
freqs = [100, 1000, 500]
sampling_rates = [20000, 20000, 20000]

# 生成三个不同频率的正弦波数据
data = [generate_sine_wave_data(f, total_duration, sr) for f, sr in zip(freqs, sampling_rates)]

# 设置曲线名称
legend_names = ["sensors_1_100Hz", "sensors_2_1000Hz", "sensors_3_500Hz"]

i = 0
while True:
    try:
        # 获取当前时间戳（精确到毫秒）
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # 将数据插入数据库
        for j in range(3):
            r.table(f'sin_data_{freqs[j]}Hz').insert({'timestamp': timestamp_str, 'data': data[j][i], 'legend_name': legend_names[j]}).run(conn)
        for j in range(3):
            if len(list(r.db("test").table(f'sin_data_{freqs[j]}Hz').order_by("timestamp").run(conn))) > 200:
                r.db("test").table(f'sin_data_{freqs[j]}Hz').order_by("timestamp").limit(100).delete().run(conn)

        # 等待一段时间，根据每个正弦波的采样率来决定
        time.sleep(1 / min(sampling_rates))
        i += 1
        time.sleep(1.5)

    except KeyboardInterrupt:
        break

# 关闭连接
conn.close()
