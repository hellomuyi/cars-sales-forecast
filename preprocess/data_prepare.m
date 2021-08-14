% 预处理数据
% 缺失值填充，对连续型数据均值代替缺失值，对离散型数据简单删除缺失值记录
%{
   日期         车型           销量	    车厢数(3)	    变速器档位(10)	   
  变速器形式(7)	 排量(19)	  是否增压(2)	  价格	       驱动形式(3)	      
  燃料类型(8)	新能源类型(4)排放标准(4)  是否微客(2)	   是否豪华(2)	      
   功率	      缸数(4)	    发动机扭矩	   车长	           车宽	        
   车高	      总质量	    整备质量	 额定载客(10)	     轴距	       、
 前轮矩	     后轮距
%}
clc
clear
idx = [1, 2, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15, 17, 24];    % 离散数据索引
data = xlsread('(new) yancheng_train_20171226.xlsx', 'A3:AA20159');
len = length(data(1, :));     % 获取矩阵列数 
for i = 1:len
    [p, ~] = find(1 == isnan(data(:, i)));
    if isempty(p)
        continue;
    end
    if ismember(i, idx)
        data(p, :) = [];    % 对离散型缺失值进行删除
    else
        data(p, i) = nanmean(data(:, i));   % 对连续型缺失值用均值代替
    end
end
xlswrite('data_prepare.xlsx', data)