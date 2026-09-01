# STACK OVERFLOW

# Requirements

# Users can post questions, answer questions, and comment on questions and answers.
# Users can vote on questions and answers.
# Questions should have tags associated with them.
# Users can search for questions based on keywords, tags, or user profiles.
# The system should assign reputation score to users based on their activity and the quality of their contributions.
# The system should handle concurrent access and ensure data consistency.


# Entities: Question, Answer, User

# Patterns: SystemManager (Singleton), Strategy, Factory

from typing import Dict,List
import uuid
import threading
from enum import Enum
from abc import ABC,abstractmethod

class VoteType(Enum):
    UP_VOTE=1
    DOWN_VOTE=-1

class ReputationScore(Enum):
    POST_QUESTION=1
    VOTE_QUESTION=2
    VOTE_ANSWER=3
    POST_ANSWER=4
    ADD_COMMENT=1

class SearchMode(Enum):
    KEYWORD='keyword'
    TAGS='tags'

class User:
    def __init__(self,name):
        self.userId=str(uuid.uuid4())
        self.name=name
        self.reputationScore=0

class Comment:
    def __init__(self,comment:str,posted_by:User):
        self.commentId=str(uuid.uuid4())
        self.comment=comment
        self.author=posted_by

class Question:
    def __init__(self,question:str,author:User,tags:List[str]):
        self.questionId=str(uuid.uuid4())
        self.text=question
        self.author=author
        self.tags=[t.lower() for t in tags]
        self.comments=[]
        self.answers:List[Answer]=[]
        self.votes=0
        self.voters:Dict[str,VoteType]={}
    def add_comment(self,comment:Comment):
        self.comments.append(comment)

class Answer:
    def __init__(self,answer:str,author:User):
        self.answerId=str(uuid.uuid4())
        self.answer=answer
        self.author=author
        self.comments=[]
        self.votes=0
        self.voters:Dict[str,VoteType]={} # to prevent double voting 
    def add_comment(self,comment:Comment):
        self.comments.append(comment)

# Strategy Pattern

class SearchStrategy(ABC):
    @abstractmethod
    def search(self,questions:List[Question],query:str):
        pass

class KeywordSearch(SearchStrategy):
    def search(self, questions, query):
        if(not query):
            return 
        results=[]
        q=query.lower()
        for question in questions:
            if(q in question.text.lower()):
                results.append(question)
        print(f"{len(results)} results found : {results}")
        
class TagSearch(SearchStrategy):
    def search(self,questions,query):
        if(not query):
            return 
        results=[]
        q=query.lower()
        for question in questions:
            if(q in question.tags):
                results.append(question)
        print(f"{len(results)} results found : {results}")

# Factory Pattern

class SearchFactory:
    _strategies:Dict[str,SearchStrategy]={
        'keyword':KeywordSearch,
        'tags':TagSearch
    }
    def search(self,query,questions,mode):
        search_service = self._strategies.get(mode)
        if(search_service is None):
            raise ValueError("Unknown mode for search")
        return search_service().search(questions,query)

# Singleton pattern

class SystemManager:
    _instance=None
    _instance_lock=threading.Lock()
    def __new__(cls):
        if(cls._instance is None):
            with cls._instance_lock:
                if(cls._instance is None):
                    cls._instance=super().__new__(cls)
                    cls._instance._init()
        return cls._instance
    def _init(self):
        self.questions:Dict[str,Question]={}
        self._lock=threading.RLock()
        self.search_service=SearchFactory()
    def add_question(self,question_text:str,author:User,tags:List[str]):
        with self._lock:
            question=Question(question_text,author,tags)
            self.questions[question.questionId]=question
            author.reputationScore+=ReputationScore.POST_QUESTION.value
    def add_answer(self,question:Question,answer_text:str,posted_by:User):
        with self._lock:
            answer=Answer(answer_text,posted_by)
            question.answers.append(answer)
            posted_by.reputationScore+=ReputationScore.POST_ANSWER.value
    def add_comment_to_question(self,question:Question,comment_text:str,posted_by:User):
        with self._lock:
            comment=Comment(comment_text,posted_by)
            question.add_comment(comment)
            posted_by.reputationScore+=ReputationScore.ADD_COMMENT.value
    def add_comment_to_answer(self,answer:Answer,comment_text:str,posted_by:User):
        with self._lock:
            comment=Comment(comment_text,posted_by)
            answer.add_comment(comment)
            posted_by.reputationScore+=ReputationScore.ADD_COMMENT.value
    def vote_question(self,question:Question,user:User,type:VoteType):
        with self._lock:
            already_voted = question.voters.get(user.userId)
            if(already_voted):
                if(already_voted==type):
                    print("Cannot vote the same again!!")
                    return 
                question.voters[user.userId]=type
                question.votes-=already_voted.value
            else:
                question.voters[user.userId]=type
            question.votes+=type.value
            question.author.reputationScore+=ReputationScore.VOTE_QUESTION.value
    def vote_answer(self,answer:Answer,user:User,type:VoteType):
        with self._lock:
            already_voted = answer.voters.get(user.userId)
            if(already_voted):
                if(already_voted==type):
                    print("Cannot vote the same again!!")
                    return
                answer.voters[user.userId]=type
                answer.votes-=already_voted.value
            else:
                answer.voters[user.userId]=type    
            answer.votes+=type.value
            answer.author.reputationScore+=ReputationScore.VOTE_ANSWER.value
    def search_question(self,query:str,mode:SearchMode):
        questions=list(self.questions.values())
        self.search_service.search(query,questions,mode.value)
            
    


