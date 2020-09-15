from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import date
from textwrap import dedent
import datetime

engine = create_engine("sqlite:///todo.db?check_same_thread=False")
Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=date.today())

    def __repr__(self):
        return self.task


def create_session():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


# Menu
class Todolist:
    def __init__(self):
        self.today = datetime.datetime.today()

    def print_all_tasks(self, session):
        rows = session.query(Task).order_by(Task.deadline).all()
        for i, row in enumerate(rows):
            print(f"{i + 1}. {row.task}. {row.deadline.strftime('%#d %b')}")

    def start(self):
        session = create_session()
        while True:
            print(dedent('''
            1) Today's tasks
            2) Week's tasks
            3) All tasks
            4) Missed tasks
            5) Add task
            6) Delete task
            0) Exit
            '''))
            action = input()
            print()

            if action == "0":
                print("Bye!")
                return

            # Today's tasks
            elif action == "1":
                day = self.today.day
                month = self.today.strftime("%b")
                rows = session.query(Task).filter(Task.deadline == self.today.date()).all()
                print(f"Today {day} {month}:")
                if not rows:
                    print("Nothing to do!")
                    continue
                else:
                    for i, row in enumerate(rows):
                        print(f"{i + 1}. {row.task}")
                    continue

            # Week's tasks
            elif action == "2":
                weekly = self.today + datetime.timedelta(days=6)
                rows = session.query(Task).filter(Task.deadline <= weekly).all()
                for i in range(7):
                    print()
                    d = self.today + datetime.timedelta(days=i)
                    print(f"{d.strftime('%A %#d %b')}:")  # Windows
                    tasks = []
                    for row in rows:
                        if row.deadline == d.date():
                            tasks.append(row.task)
                    if not tasks:
                        print("Nothing to do!")
                        continue
                    else:
                        for n, task in enumerate(tasks):
                            print(f"{n + 1}. {task}")
                        print()
                        continue

            # All tasks
            elif action == "3":
                print("All tasks:")
                self.print_all_tasks(session)
                print()
                continue

            # Missed tasks
            elif action == "4":
                print("Missed tasks:")
                rows = session.query(Task).filter(Task.deadline < self.today.date()).order_by(Task.deadline).all()
                for i, row in enumerate(rows):
                    print(f"{i + 1}. {row.task}. {row.deadline.strftime('%#d %b')}")
                print()
                continue

            # Add task
            elif action == "5":
                print("Enter task")
                new_task = input()
                print("Enter deadline")
                deadline = datetime.datetime.strptime(input(), "%Y-%m-%d")
                new_row = Task(task=new_task, deadline=deadline)
                session.add(new_row)
                session.commit()
                print("The task has been added!")
                continue

            # Delete task
            elif action == "6":
                print("Choose the number of the task you want to delete:")
                self.print_all_tasks(session)
                to_delete = int(input())
                rows = session.query(Task).all()
                if not rows:
                    print("Nothing to delete!")
                else:
                    session.query(Task).filter(Task.id == to_delete).delete()
                    session.commit()
                    print("The task has been deleted!", end="\n\n")
                continue
            else:
                continue


Todolist().start()
