# noise_analysis_visualization.py
import matplotlib.pyplot as plt
import numpy as np

# 데이터 준비
# Total Noise, FPN, Temporal Noise 값은 이전 코드에서 계산한 결과를 사용합니다.
red_total_noise = [np.random.uniform(5, 10) for _ in range(20)]  # 예제 데이터
green_total_noise = [np.random.uniform(4, 9) for _ in range(20)]  # 예제 데이터
blue_total_noise = [np.random.uniform(6, 11) for _ in range(20)]  # 예제 데이터

red_fpn = np.random.uniform(2, 4)  # 예제 데이터
green_fpn = np.random.uniform(1, 3)  # 예제 데이터
blue_fpn = np.random.uniform(3, 5)  # 예제 데이터

red_temporal_noise = np.random.uniform(2, 3)  # 예제 데이터
green_temporal_noise = np.random.uniform(1.5, 2.5)  # 예제 데이터
blue_temporal_noise = np.random.uniform(2.5, 3.5)  # 예제 데이터

# 시각화 1: Total Noise (각 프레임)
# 프레임별 Total Noise를 선 그래프로 시각화합니다.
plt.figure(figsize=(10, 6))
plt.plot(range(1, 21), red_total_noise, label='Red Total Noise', color='red', marker='o')
plt.plot(range(1, 21), green_total_noise, label='Green Total Noise', color='green', marker='o')
plt.plot(range(1, 21), blue_total_noise, label='Blue Total Noise', color='blue', marker='o')
plt.title('Total Noise Across Frames')
plt.xlabel('Frame Number')  # x축: 프레임 번호
plt.ylabel('Total Noise')  # y축: Total Noise 값
plt.legend()
plt.grid()
plt.show()

# Total Noise 설명:
# Total Noise는 각 채널 내에서 픽셀 값의 전체적인 변동성을 나타냅니다.
# 이는 각 프레임별로 계산된 노이즈 값입니다.

# 시각화 2: Fixed Pattern Noise (FPN)
# Fixed Pattern Noise를 원형 차트로 시각화합니다.
plt.figure(figsize=(8, 6))
channels = ['Red', 'Green', 'Blue']  # 채널명
fpn_values = [red_fpn, green_fpn, blue_fpn]  # FPN 값
plt.pie(fpn_values, labels=channels, autopct='%1.1f%%', colors=['red', 'green', 'blue'])
plt.title('Fixed Pattern Noise (FPN)')
plt.show()

# FPN 설명:
# Fixed Pattern Noise는 픽셀 위치에 따라 고정된 잡음을 나타냅니다.
# 특정 픽셀 위치에서의 평균 밝기값이 전체 평균에서 얼마나 벗어나는지를 측정합니다.
# 예를 들어, 센서의 특정 영역이 다른 영역보다 일관되게 어두운 경우 FPN이 큽니다.

# 시각화 3: Temporal Noise
# Temporal Noise를 레이더 차트로 시각화합니다.
from math import pi

# 레이더 차트를 위한 데이터 준비
categories = ['Red', 'Green', 'Blue']  # 채널명
temporal_noise_values = [red_temporal_noise, green_temporal_noise, blue_temporal_noise]  # Temporal Noise 값
N = len(categories)  # 레이더 차트의 축 개수

# 레이더 차트를 위한 각 축의 각도 계산
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]  # 레이더 차트는 시작점과 끝점이 동일해야 함

# Temporal Noise 데이터를 레이더 차트용으로 준비
values = temporal_noise_values + temporal_noise_values[:1]

# 레이더 차트 그리기
plt.figure(figsize=(8, 6))
ax = plt.subplot(111, polar=True)
plt.xticks(angles[:-1], categories)  # 각 축에 채널명 표시

# 데이터 플롯
ax.plot(angles, values, linewidth=2, linestyle='solid', label='Temporal Noise')
ax.fill(angles, values, alpha=0.4)

plt.title('Temporal Noise')
plt.legend(loc='upper right')
plt.show()

# Temporal Noise 설명:
# Temporal Noise는 동일한 픽셀에서 시간에 따라 발생하는 밝기값의 변동성을 나타냅니다.
# 센서가 시간적으로 안정적으로 작동하지 않을 경우 Temporal Noise가 증가합니다.

"""
노이즈의 의미
1. Total Noise:
각 프레임에서 채널별 픽셀 값의 변동성(전체적인 밝기값의 변화)을 나타냅니다.
높은 Total Noise는 이미지 전체에서 큰 변동성을 의미합니다.

2. Fixed Pattern Noise (FPN):
특정 픽셀 위치에서 고정적으로 발생하는 밝기값의 차이를 나타냅니다.
이는 이미지 센서의 제조 결함이나 하드웨어 문제로 인해 발생할 수 있습니다.

3. Temporal Noise:
동일한 픽셀에서 시간에 따라 발생하는 밝기값의 변동성을 측정합니다.
Temporal Noise가 높으면 센서가 시간적으로 안정적이지 않다는 것을 의미합니다.
"""