# encoding=utf-8


from . import jena_sparql_endpoint
from . import question2sparql
import os
from mysite import settings

def kb_query(sentence):
    print (os.getcwd())
    # TODO 连接Fuseki服务器，开始前要进入fuseki目录启动服务器
    fuseki = jena_sparql_endpoint.JenaFuseki()
    # TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
    q2s = question2sparql.Question2Sparql([os.path.join(settings.BASE_DIR, 'movie_title.txt'), os.path.join(settings.BASE_DIR, 'person_name.txt')])

    question = sentence
    ans = []
    my_query = q2s.get_sparql(question.encode('utf-8').decode('utf-8'))
    if my_query is not None:
        result = fuseki.get_sparql_result(my_query)
        value = fuseki.get_sparql_result_value(result)
        # TODO 判断结果是否是布尔值。
        if isinstance(value, bool):
            if value is True:
                ans.append("是的")
            else:
                ans.append("不是")
        else:
            # TODO 查询结果为空，根据OWA，回答“不知道”
            if len(value) == 0:
                ans.append("无结果，请重试")
            # elif len(value) == 1:
            #     ans.append(value[0])
            # else:
            #     output = ''
            #     for v in value:
            #         output += v + u'、'
            #     ans.append(output[0:-1])
            else:
                ans = value

    else:
        # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
        ans.append("无法理解该问题")
    return ans

if __name__ == '__main__':
    kb_query("周星驰是谁？")
