#计算word error rate，词错误率  最小编辑距离(min edit distance)=min(替代+插入+脱落) wer=(最小编辑距离)/(全部单词数)% 参考：自然语言处理综论p63
import numpy as np
def med(str1,str2):
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

    return matrix_distance[m][n]  

#str1 = ['i','n','t','e','n','t','i','o','n']
#str2 = ['e','x','e','c','u','t','i','o','n']
#str1=['i','um','the','phone','is','i','left','the','portable','phone','upstairs','last','night']
#str2=['i','got','it','to','the','fullest','i','love','to','portable','form','of','stores','last','night']
#c=med(str2,str1)
#print(c,'  ',c/13)
