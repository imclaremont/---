# ar0544_noise_analysis.py
import cv2
import numpy as np
import os

# 함수 정의: Total Noise 계산
def calculate_total_noise(channel):
    """
    Total Noise 계산:
    픽셀 값에서 전체 평균을 뺀 후, 차이를 제곱하여 평균을 내고 제곱근을 취합니다.
    이는 채널 내 픽셀 값의 전반적인 변동성을 나타냅니다.
    """
    mean_pixel = np.mean(channel)  # 전체 평균값 계산
    total_noise = np.sqrt(np.mean((channel - mean_pixel) ** 2))  # 총 노이즈 계산
    return total_noise

# 함수 정의: Fixed Pattern Noise(FPN) 계산
def calculate_fpn(channel):
    """
    Fixed Pattern Noise(FPN) 계산:
    각 열별 평균값과 전체 평균값 간의 차이를 기반으로 계산합니다.
    이는 고정된 패턴 잡음을 측정합니다.
    """
    pixel_means = np.mean(channel, axis=0)  # 각 열의 평균값 계산
    global_mean = np.mean(pixel_means)      # 전체 평균 계산
    fpn = np.sqrt(np.mean((pixel_means - global_mean) ** 2))  # 고정 패턴 노이즈 계산
    return fpn

# 함수 정의: Temporal Noise 계산
def calculate_temporal_noise(frames):
    """
    Temporal Noise 계산:
    다중 프레임 데이터에서 시간에 따른 픽셀 값의 변동성을 계산합니다.
    """
    frame_means = np.mean(frames, axis=(1, 2))  # 각 프레임의 평균값 계산
    temporal_noise = np.sqrt(np.mean((frames - frame_means[:, None, None]) ** 2))  # 시간적 노이즈 계산
    return temporal_noise

# Step 1: 이미지 디렉터리 경로 및 파일 로드
# 분석할 이미지가 저장된 디렉터리 경로와 파일명 정의
image_dir = "./image/"  # 이미지 디렉터리 경로
num_images = 20  # 분석할 이미지 개수
image_files = [os.path.join(image_dir, f"{i}.png") for i in range(1, num_images + 1)]  # 1.png ~ 20.png 파일 목록 생성

# Step 2: 이미지 데이터를 저장할 리스트 생성
# 각 프레임 데이터를 저장할 리스트를 초기화
frames = []

# Step 3: 이미지 로드 및 Bayer 패턴 분리
# 각 이미지를 불러와 Bayer 패턴의 Red, Green, Blue 채널로 분리
for file in image_files:
    # 이미지 로드
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)  # 이미지를 흑백 모드로 로드
    
    # Bayer 패턴 채널 분리
    red_channel = image[1::2, 1::2]    # Red 채널 (홀수 행, 홀수 열)
    # GreenR과 GreenB를 결합하여 Green 채널을 통합
    green_channel = np.vstack((image[0::2, 1::2], image[1::2, 0::2]))  # Green 채널 통합
    blue_channel = image[0::2, 0::2]   # Blue 채널 (짝수 행, 짝수 열)
    
    # 각 프레임 데이터를 딕셔너리 형태로 저장
    frames.append({
        "red": red_channel,
        "green": green_channel,
        "blue": blue_channel
    })

# Step 4: 전체 프레임 데이터를 numpy 배열로 변환 (Temporal Noise 계산용)
# 다중 프레임 데이터를 채널별로 numpy 배열로 변환
red_frames = np.array([frame["red"] for frame in frames])      # Red 채널 프레임 배열
green_frames = np.array([frame["green"] for frame in frames])  # Green 채널 프레임 배열
blue_frames = np.array([frame["blue"] for frame in frames])    # Blue 채널 프레임 배열

# Step 5: Total Noise 및 FPN 계산
# Total Noise는 각 프레임별로 계산하여 리스트에 저장
red_total_noise = [calculate_total_noise(frame["red"]) for frame in frames]
green_total_noise = [calculate_total_noise(frame["green"]) for frame in frames]
blue_total_noise = [calculate_total_noise(frame["blue"]) for frame in frames]

# Fixed Pattern Noise(FPN)는 첫 번째 프레임을 기준으로 계산
red_fpn = calculate_fpn(red_frames[0])  # Red 채널의 FPN
green_fpn = calculate_fpn(green_frames[0])  # Green 채널의 FPN
blue_fpn = calculate_fpn(blue_frames[0])  # Blue 채널의 FPN

# Step 6: Temporal Noise 계산
# Temporal Noise는 모든 프레임 데이터를 사용하여 계산
red_temporal_noise = calculate_temporal_noise(red_frames)      # Red 채널의 Temporal Noise
green_temporal_noise = calculate_temporal_noise(green_frames)  # Green 채널의 Temporal Noise
blue_temporal_noise = calculate_temporal_noise(blue_frames)    # Blue 채널의 Temporal Noise

# Step 7: 결과 출력
# 각 채널별 Total Noise의 평균값, FPN, Temporal Noise 값을 출력
print("=== Total Noise ===")
print("Red Total Noise (avg):", np.mean(red_total_noise))  # Red 채널의 Total Noise 평균 출력
print("Green Total Noise (avg):", np.mean(green_total_noise))  # Green 채널의 Total Noise 평균 출력
print("Blue Total Noise (avg):", np.mean(blue_total_noise))  # Blue 채널의 Total Noise 평균 출력

print("\n=== Fixed Pattern Noise (FPN) ===")
print("Red FPN:", red_fpn)  # Red 채널의 FPN 출력
print("Green FPN:", green_fpn)  # Green 채널의 FPN 출력
print("Blue FPN:", blue_fpn)  # Blue 채널의 FPN 출력

print("\n=== Temporal Noise ===")
print("Red Temporal Noise:", red_temporal_noise)  # Red 채널의 Temporal Noise 출력
print("Green Temporal Noise:", green_temporal_noise)  # Green 채널의 Temporal Noise 출력
print("Blue Temporal Noise:", blue_temporal_noise)  # Blue 채널의 Temporal Noise 출력
