% ��ɫ��������
% ��������������ڡ��ͺ����24��ά��֮��Ĺ����̶�
clc
clear
close all
% ��������������
format short;
% ԭʼ����
data = xlsread('data_prepare.xlsx', 'C3:AA18913');  % ���������ڡ�����
data = data';
n1=size(data,1);

% ���ݱ�׼������
for i = 1:n1
    data(i,:) = (data(i,:)-min(data(i,:)))/(max(data(i,:))-min(data(i,:)));%�޸�x(i,:) = x(i,:)/x(i,1);
end

% ����ĸ����
consult=data(1,:);
m1=size(consult,1);
% ����������
compare=data(2:n1,:);
m2=size(compare,1);
for i=1:m1
    for j=1:m2
        t(j,:)=compare(j,:)-consult(i,:);
    end
    min_min=min(min(abs(t')));
    max_max=max(max(abs(t')));  %�õ���������ֵ����Сֵ
    % ͨ���ֱ��ʶ���ȡ0.5
    resolution=0.5;
    % �������ϵ��
    coefficient=(min_min+resolution*max_max)./(abs(t)+resolution*max_max);
    % ���������
    corr_degree=sum(coefficient')/size(coefficient,2);
    r(i,:)=corr_degree;
end

%% ���������ֵ����������ͼ
r  
figure('name', '��ɫ��������')
bar(r, 0.90, 'b');
grid on
axis tight;
n = 24;
profits = {'������','��������λ','��������ʽ','����','�Ƿ���ѹ',...
    '�۸�','������ʽ','ȼ������','����Դ����','�ŷű�׼','�Ƿ�΢��',...
    '�Ƿ����','����','����','������Ť��','����','����','����',...
    '������','��������','��ؿ�','���','ǰ�־�','���־�'};
set(gca, 'Xtick',1:n);
set(gca,'XTickLabel',profits);
xtickangle(40)	%�̶ȱ�ǩ��ʱ����ת

set(gca,'fontname','��������',... %����%times new roman
    'fontsize',12,...
    'FontWeight','bold');         %����
axis([0.5 24.5 0 1])   
ylabel('������')
title('�������������Ļ�ɫ������')