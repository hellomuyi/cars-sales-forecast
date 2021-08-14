% 灰色关联分析
% 计算销量与除日期、型号外的24个维度之间的关联程度
clc
clear
close all
% 控制输出结果精度
format short;
% 原始数据
data = xlsread('data_prepare.xlsx', 'C3:AA18913');  % 不包含日期、车型
data = data';
n1=size(data,1);

% 数据标准化处理
for i = 1:n1
    data(i,:) = (data(i,:)-min(data(i,:)))/(max(data(i,:))-min(data(i,:)));%修改x(i,:) = x(i,:)/x(i,1);
end

% 分离母因素
consult=data(1,:);
m1=size(consult,1);
% 分离子因素
compare=data(2:n1,:);
m2=size(compare,1);
for i=1:m1
    for j=1:m2
        t(j,:)=compare(j,:)-consult(i,:);
    end
    min_min=min(min(abs(t')));
    max_max=max(max(abs(t')));  %得到矩阵的最大值和最小值
    % 通常分辨率都是取0.5
    resolution=0.5;
    % 计算关联系数
    coefficient=(min_min+resolution*max_max)./(abs(t)+resolution*max_max);
    % 计算关联度
    corr_degree=sum(coefficient')/size(coefficient,2);
    r(i,:)=corr_degree;
end

%% 输出关联度值并绘制柱形图
r  
figure('name', '灰色关联分析')
bar(r, 0.90, 'b');
grid on
axis tight;
n = 24;
profits = {'车厢数','变速器档位','变速器形式','排量','是否增压',...
    '价格','驱动形式','燃料类型','新能源类型','排放标准','是否微客',...
    '是否豪华','功率','缸数','发动机扭矩','车长','车宽','车高',...
    '总质量','整备质量','额定载客','轴距','前轮矩','后轮距'};
set(gca, 'Xtick',1:n);
set(gca,'XTickLabel',profits);
xtickangle(40)	%刻度标签逆时针旋转

set(gca,'fontname','华文宋体',... %字体%times new roman
    'fontsize',12,...
    'FontWeight','bold');         %粗体
axis([0.5 24.5 0 1])   
ylabel('关联度')
title('各特征与销量的灰色关联度')