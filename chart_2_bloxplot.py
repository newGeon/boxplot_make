import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from tqdm import tqdm

# 아웃라이어 제거
def fn_remove_outliers(list_data):
    cleaned_data = []
    
    q_l_case = np.percentile(list_data, 5)
    q_u_case = np.percentile(list_data, 85)
    
    cleaned_data = [x for x in list_data if x >= q_l_case]
    cleaned_data = [x for x in cleaned_data if x <= q_u_case]

    return cleaned_data


def fn_make_boxplot(json_data, list_column, data_type):

    data_case = []
    data_control = []
    
    for val_column in list_column:
        
        val_column = val_column.split('.')[1].strip()
        
        list_case = json_data[val_column]['case']
        list_control = json_data[val_column]['control']

        print("{} : mean값 >> case = {}, control = {}".format(val_column, np.mean(list_case), np.mean(list_control)))              

        # 원본 데이터
        data_case.append(list_case)
        data_control.append(list_control)

        """
        # 데이터 정규화
        normalized_case = []
        normalized_control = []
        
        for value in tqdm(list_case):
            normalized = (value - np.mean(list_case)) / np.std(list_case)
            normalized_case.append(normalized)
        
        for value in tqdm(list_control):
            normalized = (value - np.mean(list_control)) / np.std(list_control)
            normalized_control.append(normalized)
        
        data_case.append(normalized_case)
        data_control.append(normalized_control)
        """
        
        """
        # 아웃라리어 제거
        clean_case = fn_remove_outliers(list_case)
        clean_control = fn_remove_outliers(list_control)

        data_case.append(clean_case)
        data_control.append(clean_control)
        """
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    # Figure와 두 개의 서브플롯 생성
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 16))

    # Boxplot 생성
    ax1.boxplot(data_case, vert=False, widths=0.6, patch_artist=True)
    ax1.set_xlim(-150, 1000)
    ax1.set_title("Case 그래프")

    # 두 번째 서브플롯에 Boxplot 추가
    ax2.boxplot(data_control, vert=False, widths=0.6, patch_artist=True)
    ax2.set_xlim(-150, 1000)
    ax2.set_title("Control 그래프")
        
    ax1.set_yticklabels(list_column)  # 첫 번째 그래프의 y축 레이블
    
    # 그래프 간 간격 조절
    plt.subplots_adjust(wspace=0.2)
    plt.suptitle("{} 데이터 비교 (Case군 vs Control군)".format(data_type), fontsize=15, fontweight='bold')

    # 그래프 표시
    plt.show()

    # 그래프 저장
    plt.savefig('./chart/0_ALL_boxplot_{}3.png'.format(data_type))
    plt.clf()


if __name__ == '__main__':
    
    list_vitals = [
        '1. sysbp', '2. diabp', '3. meanbp', '4. resprate', '5. heartrate', '6. spo2_pulsoxy', '7. tempc', '8. cardiacoutput', 
        '9. tvset', '10. tvobserved', '11. tvspontaneous', '12. peakinsppressure', '13. totalpeeplevel', '14. o2flow', '15. fio2'        
    ]

    list_labs = [
        '1. aniongap', '2. albumin', '3. bands', '4. bicarbonate', '5. bilirubin', '6. creatinine', '7. chloride', '8. glucose', 
        '9. hematocrit', '10. hemoglobin', '11. lactate', '12. platelet', '13. potassium', '14. ptt', '15. inr', '16.pt', 
        '17. sodium', '18. bun', '19. wbc', '20. creatinekinase', '21. ck_mb', '22. fibrinogen', '23. ldh', '24. magnesium', 
        '25. calcium_free', '26. po2_bloodgas', '27. ph_bloodgas', '28. pco2_bloodgas', '29. so2_bloodgas', '30. troponin_t'
    ]
    
    with open('./data_dump/result_mean.json', 'r') as f:
        load_data = json.load(f)
    
    fn_make_boxplot(load_data, list_vitals, 'Vitals')
    fn_make_boxplot(load_data, list_labs, 'Labs')

    print('----------------------------------------------------------------------------------------')
    print('--- SUCESS -----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------------------')
    
