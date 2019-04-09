# encoding=utf-8

"""
设置问题模板，为每个模板设置对应的SPARQL语句。demo提供如下模板：

1. 某演员演了什么电影
2. 某电影有哪些演员出演
3. 演员A和演员B合作出演了哪些电影
4. 某演员参演的评分大于X的电影有哪些
5. 某演员出演过哪些类型的电影
6. 某演员出演的XX类型电影有哪些。
7. 某演员出演了多少部电影。
8. 某演员是喜剧演员吗。

"""
from refo import finditer, Predicate, Star, Any, Disjunction
import re

# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
PREFIX : <http://www.moviekgqa.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
             u"SELECT COUNT({select}) WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
             u"ASK {{\n" + \
             u"{expression}\n" + \
             u"}}\n"


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


class KeywordRule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        if len(matches) == 0:
            return None
        else:
            return self.action()


class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_movie_question(word_objects):
        """
        某演员演了什么电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :actor_actor_chName '{person}'." \
                    u"?s :hasActedIn ?m." \
                    u"?m :movie_movie_chName ?x".format(person=w.token )

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_actor_question(word_objects):
        """
        哪些演员参演了某电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_movie:
                e = u"?m :movie_movie_chName '{movie}'." \
                    u"?m :hasActor ?a." \
                    u"?a :actor_actor_chName ?x".format(movie=w.token )

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break

        return sparql

    @staticmethod
    def has_cooperation_question(word_objects):
        """
        演员A和演员B有哪些合作的电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        person1 = None
        person2 = None

        for w in word_objects:
            if w.pos == pos_person:
                if person1 is None:
                    person1 = w.token
                else:
                    person2 = w.token
        if person1 is not None and person2 is not None:
            e = u"?p1 :actor_actor_chName '{person1}'." \
                u"?p2 :actor_actor_chName '{person2}'." \
                u"?p1 :hasActedIn ?m." \
                u"?p2 :hasActedIn ?m." \
                u"?m :movie_movie_chName ?x".format(person1=person1 , person2=person2 )

            return SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                          select=select,
                                          expression=e)
        else:
            return None

    @staticmethod
    def has_movie_type_question(word_objects):
        """
        某演员演了哪些类型的电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :actor_actor_chName '{person}'." \
                    u"?s :hasActedIn ?m." \
                    u"?m :hasGenre ?g." \
                    u"?g :genre_genre_name ?x".format(person=w.token )

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_specific_type_movie_question(word_objects):
        """
        某演员演了什么类型（指定类型，喜剧、恐怖等）的电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        keyword = None
        for r in genre_keyword_rules:
            keyword = r.apply(word_objects)

            if keyword is not None:
                break

        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :actor_actor_chName '{person}'." \
                    u"?s :hasActedIn ?m." \
                    u"?m :hasGenre ?g." \
                    u"?g :genre_genre_name '{keyword}'." \
                    u"?m :movie_movie_chName ?x".format(person=w.token , keyword=keyword)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_quantity_question(word_objects):
        """
        某演员演了多少部电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :actor_actor_chName '{person}'." \
                    u"?s :hasActedIn ?x.".format(person=w.token )

                sparql = SPARQL_COUNT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                break

        return sparql


    @staticmethod
    def has_basic_person_info_question(word_objects):
        """
        某演员的基本信息是什么
        :param word_objects:
        :return:
        """

        keyword = None
        for r in person_basic_keyword_rules:
            keyword = r.apply(word_objects)
            if keyword is not None:
                break

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :actor_actor_chName '{person}'." \
                    u"?s {keyword} ?x.".format(person=w.token , keyword=keyword)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)

                break

        return sparql

    @staticmethod
    def has_basic_movie_info_question(word_objects):
        """
        某电影的基本信息是什么
        :param word_objects:
        :return:
        """

        keyword = None
        for r in movie_basic_keyword_rules:
            keyword = r.apply(word_objects)
            if keyword is not None:
                break

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_movie:
                e = u"?s :movie_movie_chName '{movie}'." \
                    u"?s {keyword} ?x.".format(movie=w.token , keyword=keyword)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)

                break

        return sparql


class PropertyValueSet:
    def __init__(self):
        pass

    @staticmethod
    def return_adventure_value():
        return u'冒险'

    @staticmethod
    def return_animation_value():
        return u'动画'

    @staticmethod
    def return_drama_value():
        return u'剧情'

    @staticmethod
    def return_thriller_value():
        return u'恐怖'

    @staticmethod
    def return_action_value():
        return u'动作'

    @staticmethod
    def return_comedy_value():
        return u'喜剧'


    @staticmethod
    def return_horror_value():
        return u'惊悚'

    @staticmethod
    def return_crime_value():
        return u'犯罪'

    @staticmethod
    def return_fiction_value():
        return u'科幻'

    @staticmethod
    def return_romance_value():
        return u'爱情'


    @staticmethod
    def return_higher_value():
        return u'>'

    @staticmethod
    def return_lower_value():
        return u'<'

    @staticmethod
    def return_birth_value():
        return u':actor_actor_birthDay'

    @staticmethod
    def return_birth_place_value():
        return u':actor_actor_birthPlace'

    @staticmethod
    def return_english_name_value():
        return u':actor_actor_foreName'

    @staticmethod
    def return_person_introduction_value():
        return u':actor_actor_bio'

    @staticmethod
    def return_movie_introduction_value():
        return u':movie_movie_bio'

    @staticmethod
    def return_release_value():
        return u':movie_movie_releaseTime'

    @staticmethod
    def return_rating_value():
        return u':movieRating'


# TODO 定义关键词
pos_person = "nr"
pos_movie = "nz"
pos_number = "m"

person_entity = (W(pos=pos_person))
movie_entity = (W(pos=pos_movie))
number_entity = (W(pos=pos_number))

adventure = W("冒险")
animation = (W("动画") | W("动画片"))
drama = (W("剧情") | W("剧情片"))
thriller = (W("恐怖") | W("恐怖片"))
action = (W("动作") | W("动作片"))
comedy = (W("喜剧") | W("喜剧片"))
horror = (W("惊悚") | W("惊悚片"))
crime = (W("犯罪") | W("犯罪片"))
science_fiction = (W("科幻") | W("科幻片"))
romance = (W("爱情") | W("爱情片"))
genre = (adventure  | animation | drama | thriller | action
         | comedy | horror | crime | 
         science_fiction | romance )


actor = (W("演员") | W("艺人") | W("表演者"))
movie = (W("电影") | W("影片") | W("片子") | W("片") | W("剧"))
category = (W("类型") | W("种类"))
several = (W("多少") | W("几部"))

higher = (W("大于") | W("高于"))
lower = (W("小于") | W("低于"))
compare = (higher | lower)

birth = (W("生日") | W("出生") + W("日期") | W("出生"))
birth_place = (W("出生地") | W("出生"))
english_name = (W("英文名") | W("英文") + W("名字"))
introduction = (W("介绍") | W("是") + W("谁") | W("简介"))
person_basic = (birth | birth_place | english_name | introduction)

rating = (W("评分") | W("分") | W("分数"))
release = (W("上映"))
movie_basic = (rating | introduction | release)

when = (W("何时") | W("时候"))
where = (W("哪里") | W("哪儿") | W("何地") | W("何处") | W("在") + W("哪"))

# TODO 问题模板/匹配规则

rules = [
    Rule(condition_num=2, condition=person_entity + Star(Any(), greedy=False) + movie + Star(Any(), greedy=False), action=QuestionSet.has_movie_question),
    Rule(condition_num=2, condition=(movie_entity + Star(Any(), greedy=False) + actor + Star(Any(), greedy=False)) | (actor + Star(Any(), greedy=False) + movie_entity + Star(Any(), greedy=False)), action=QuestionSet.has_actor_question),
    Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + person_entity + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=QuestionSet.has_cooperation_question), 
    Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + category + Star(Any(), greedy=False) + movie, action=QuestionSet.has_movie_type_question),
    Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + genre + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=QuestionSet.has_specific_type_movie_question),
    Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + several + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=QuestionSet.has_quantity_question), 
    Rule(condition_num=3, condition=(person_entity + Star(Any(), greedy=False) + (when | where) + person_basic + Star(Any(), greedy=False)) | (person_entity + Star(Any(), greedy=False) + person_basic + Star(Any(), greedy=False)), action=QuestionSet.has_basic_person_info_question),
    Rule(condition_num=2, condition=movie_entity + Star(Any(), greedy=False) + movie_basic + Star(Any(), greedy=False), action=QuestionSet.has_basic_movie_info_question)
]

# TODO 具体的属性词匹配规则
genre_keyword_rules = [
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + adventure + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_adventure_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + fantasy + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_fantasy_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + animation + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_animation_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + drama + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_drama_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + thriller + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_thriller_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + action + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_action_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + comedy + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_comedy_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + history + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_history_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + western + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_western_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + horror + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_horror_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + crime + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_crime_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + documentary + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_documentary_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + science_fiction + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_fiction_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + mystery + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_mystery_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + music + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_music_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + romance + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_romance_value)
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + family + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_family_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + war + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_war_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + TV + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_tv_value)
]

compare_keyword_rules = [
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + higher + number_entity + Star(Any(), greedy=False) + movie + Star(Any(), greedy=False), action=PropertyValueSet.return_higher_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + lower + number_entity + Star(Any(), greedy=False) + movie + Star(Any(), greedy=False), action=PropertyValueSet.return_lower_value)
]

person_basic_keyword_rules = [
    KeywordRule(condition=(person_entity + Star(Any(), greedy=False) + where + birth_place + Star(Any(), greedy=False)) | (person_entity + Star(Any(), greedy=False) + birth_place + Star(Any(), greedy=False)), action=PropertyValueSet.return_birth_place_value),
    KeywordRule(condition=person_entity + Star(Disjunction(Any(), where), greedy=False) + birth + Star(Any(), greedy=False), action=PropertyValueSet.return_birth_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + english_name + Star(Any(), greedy=False), action=PropertyValueSet.return_english_name_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + introduction + Star(Any(), greedy=False), action=PropertyValueSet.return_person_introduction_value)
]

movie_basic_keyword_rules = [
    KeywordRule(condition=movie_entity + Star(Any(), greedy=False) + introduction + Star(Any(), greedy=False), action=PropertyValueSet.return_movie_introduction_value),
    KeywordRule(condition=movie_entity + Star(Any(), greedy=False) + release + Star(Any(), greedy=False), action=PropertyValueSet.return_release_value),
    KeywordRule(condition=movie_entity + Star(Any(), greedy=False) + rating + Star(Any(), greedy=False), action=PropertyValueSet.return_rating_value),
]