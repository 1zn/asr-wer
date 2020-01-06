#计算word error rate，词错误率  最小编辑距离(min edit distance)=min(替代+插入+脱落) wer=(最小编辑距离)/(全部单词数)% 参考：自然语言处理综论p63
import numpy as np

def med(str1,str2):
    '''
    str1:正确字符串
    str2：预测字符串
    '''
    m = len(str1)#字符序列长度
    n = len(str2)
    matrix_distance = np.zeros((m+1,n+1))#距离矩阵
    for i in range(m+1):
        matrix_distance[i][0] = i#初始化
    for i in range(n+1):
        matrix_distance[0][i] = i

    for i in range(1,n+1):
        for j in range(1,m+1):
            if str1[j-1] == str2[i-1]:#如果两个字符相等代价为0，否则代价为1，即替换了一次
                sub_distance = 0
            else:
                sub_distance = 1
            #每次计算最小的代价
            matrix_distance[j][i] = min(matrix_distance[j-1][i]+1,matrix_distance[j][i-1]+1,matrix_distance[j-1][i-1]+sub_distance)
    wer = matrix_distance[m][n]/m
    return wer

def med_backoff(str1,str2,mode):
    '''
    str1:正确字符串
    str2：预测字符串
    '''
    m = len(str1)#字符序列长度
    n = len(str2)
    matrix_distance = np.zeros((m+1,n+1))#距离矩阵
    for i in range(m+1):
        matrix_distance[i][0] = i#初始化
    for i in range(n+1):
        matrix_distance[0][i] = i

    for i in range(1,n+1):
        for j in range(1,m+1):
            if str1[j-1] == str2[i-1]:#如果两个字符相等代价为0，否则代价为1，即替换了一次
                sub_distance = 0
            else:
                sub_distance = 1
            #每次计算最小的代价
            matrix_distance[j][i] = min(matrix_distance[j-1][i]+1,matrix_distance[j][i-1]+1,matrix_distance[j-1][i-1]+sub_distance)
    deletion_num=0
    substitution_num=0
    insertion_num=0
    x_index=n
    y_index=m
    while (x_index>0 and y_index>0):
        n_x_index=x_index-1
        n_y_index=y_index-1
        cost_now=matrix_distance[y_index][x_index]
        cost_up=matrix_distance[n_y_index][x_index]
        cost_left=matrix_distance[y_index][n_x_index]
        cost_leftcorner=matrix_distance[n_y_index][n_x_index]
        if str1[n_y_index] == str2[n_x_index]:#始终替换优先
            x_index=n_x_index
            y_index=n_y_index
        elif cost_now>cost_leftcorner:
            x_index=n_x_index
            y_index=n_y_index
            substitution_num+=1
        elif cost_now<=cost_leftcorner:
            if mode==1:#插入优先
                if cost_now>cost_up:
                    y_index=n_y_index
                    insertion_num+=1
                else:
                    x_index=n_x_index
                    deletion_num+=1
            if mode==2:#删除优先
                if cost_now>cost_left:
                    x_index=n_x_index
                    deletion_num+=1
                else:
                    y_index=n_y_index
                    insertion_num+=1
    if(y_index==0 and x_index!=0):
        for i in range(x_index):
            deletion_num+=1
            x_index-=1
    if(y_index!=0 and x_index==0):
        for i in range(y_index):
            insertion_num+=1
            y_index-=1
    if(y_index!=0 and x_index!=0):
        raise RuntimeError('wrong')


    wer = matrix_distance[m][n]/m
    s_wer=substitution_num/m
    i_wer=insertion_num/m 
    d_wer=deletion_num/m

    return wer,s_wer,i_wer,d_wer



