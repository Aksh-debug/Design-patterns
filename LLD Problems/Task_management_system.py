# Task Management system

# Requirements

# The task management system should allow users to create, update, and delete tasks.
# Each task should have a title, description, due date, priority, and status (e.g., pending, in progress, completed).
# Users should be able to assign tasks to other users and set reminders for tasks.
# The system should support searching and filtering tasks based on various criteria (e.g., priority, due date, assigned user).
# Users should be able to mark tasks as completed and view their task history.
# The system should handle concurrent access to tasks and ensure data consistency.
# The system should be extensible to accommodate future enhancements and new features.

from typing import List, Optional, Dict
import uuid
import threading
from abc import ABC,abstractmethod
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    PENDING='PENDING'
    IN_PROGRESS='IN_PROGRESS'
    COMPLETED='COMPLETED'

class TaskPriority(Enum):
    LOW=1
    MEDIUM=2
    HIGH=3

class User:
    def __init__(self,name,email):
        self.user_id=str(uuid.uuid4())
        self.name=name
        self.email=email
    def __repr__(self):
        return f"User({self.name})"

# observer pattern : where each observer will listen to the changes via notification service

class TaskObserver(ABC):
    @abstractmethod
    def on_task_update(self,task,message:str):
        pass

class NotificationReminderService(TaskObserver):
    def on_task_update(self, task, message):
        assignee=task.assigned_user.name if task.assigned_user else "Unassigned"
        print(f"Assignee: {assignee} assigned Task: {task.title} ${message}")

class History:
    def __init__(self,description:str):
        self.timestamp=datetime.now()
        self.description=description
    def __repr__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.description}"


class Task:
    def __init__(self,title:str,description:str,due_date:datetime,priority:TaskPriority,createdBy:User):
        self.task_id=str(uuid.uuid4())
        self.title=title
        self.description=description
        self.due_date=due_date
        self.priority=priority
        self.status=TaskStatus.PENDING
        self.createdBy=createdBy
        self.assigned_user:Optional[User]=None

        self._lock=threading.RLock()
        self._observers:List[TaskObserver]=[]
        self._history:List[History]=[History("Task Created")]

    def add_observers(self,observer:TaskObserver):
        with self._lock:
            self._observers.append(observer)

    def _notify(self,message:str):
        for observer in self._observers:
            observer.on_task_update(self,message)
    def assign_to(self,user:User):
        with self._lock:
            self.assigned_user=user
            self._history.append(History(f"Assigned to {user.name}"))
        self._notify(f"Assigned to {user.name}")
    def update_status(self,status:TaskStatus):
        with self._lock:
            old_status=self.status
            self.status=status
            self._history.apepnd(History(f"Updated status from {old_status} -> {status}"))
        self._notify(f"Updated status from {old_status} -> {status}")
    def update_details(self,title:Optional[str],description:Optional[str],priority:Optional[TaskPriority],due_date:Optional[datetime]):
        with self._lock:
            if(title):
                self.title=title
            if(description):
                self.description=description
            if(priority):
                self.priority=priority
            if(due_date):
                self.due_date=due_date
            self._history.append(History("Task details updated"))
        self._notify("Task details updated")
    def mark_completed(self):
        self.update_status(TaskStatus.COMPLETED)
    def get_history(self):
        with self._lock:
            return list(self._history)


# Singleton pattern : One one task manager exists

class TaskManager:
    _instance=None
    _instance_lock=None
    def __new__(cls):
        if(cls._instance is None):
            with cls._instance_lock:
                if(cls._instance is None):
                    cls._instance=super().__new__(cls)
        return cls._instance
    def __init__(self):
        self._tasks:Dict[str,Task]={}
        self._lock=threading.RLock()
    def create_task(self,title:str,description:str,due_date:datetime,priority:TaskPriority,createdBy:User):
        task=Task(title,description,due_date,priority,createdBy)
        with self._lock:
            self._tasks[task.task_id]=task
        return task
    def delete_task(self,task_id:str):
        with self._lock:
            self._tasks.pop(task_id,None) is not None
    def update_task(self,task_id:str,**kwargs):
        task=self._tasks.get(task_id)
        if(not task):
            raise ValueError("Task not found")
        task.update_details(**kwargs)
    def get_task(self,task_id:str):
        with self._lock:
            return self._tasks.get(task_id)
    def assign_task(self,task_id:str,user:User):
        task=self._tasks.get(task_id)
        if(not task):
            raise ValueError("Task not found")
        task.assign_to(user)
    def search_tasks(self,filterFunction:any):
        with self._lock:
            snapshot=list(self._tasks)
        return [t for t in snapshot if filterFunction(t)] # strategy pattern : where the TaskManager is not aware about the strategy to search among the tasks.
