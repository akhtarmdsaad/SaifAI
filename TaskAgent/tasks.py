from todoist_api_python.api import TodoistAPI
from private import TODOIST_API_KEY

class Tasks:
    def __init__(self, api_key):
        self.tasks = []
        self.api = TodoistAPI(api_key)
        tasks = self.api.get_tasks()
        for task in tasks:
            self.tasks.append({
                'id': task.id, # added 'id' to store the task id from todoist
                'title': task.content,
                'priority': task.priority
            })

    def add_task(self, title, priority):
        if not title:
            return

        # add task to todoist 
        task = self.api.add_task(
            content=title,
            priority=priority,
        )

        task = {
            'id': task.id,
            'title': title,
            'priority': priority
        }
        self.tasks.append(task)
        

    def get_tasks(self):
        return sorted(self.tasks, key=lambda x: x['priority'])

    def close_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.api.close_task(task.id)
                self.tasks.remove(task)
                return True
        return False
    
    def delete_task(self, title):
        for task in self.tasks:
            if task["title"] == title:
                self.api.delete_task(task['id'])
                self.tasks.remove(task)
                return True
        return False
    
    def reopen_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.api.reopen_task(task.id)
                return True
        return False
    
    def update_task(self, title, new_title, new_priority=-1):
        for task in self.tasks:
            if task.title == title:
                if new_priority == -1:
                    new_priority = task.priority
                self.api.update_task(task.id, content=new_title, priority=new_priority)

                task.title = new_title
                if new_priority != -1:
                    task.priority = new_priority
                return True
        return False

# Example usage
if __name__ == "__main__":
    tasks = Tasks(TODOIST_API_KEY)
    # task_list = tasks.get_tasks()
    # for t in task_list:
    #     print(t.get('title'))
    #     print(t)
    #     print("\n\n")
    tasks.delete_task("hwy")
