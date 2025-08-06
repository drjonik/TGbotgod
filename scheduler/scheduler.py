from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from db.database import get_pending_tasks, get_task

class Scheduler:
    def __init__(self, bot):
        self.bot = bot
        self.sched = AsyncIOScheduler()
        self.sched.start()

    async def load_jobs(self):
        tasks = await get_pending_tasks()
        for t in tasks:
            trigger = DateTrigger(run_date=t.date_time)
            self.sched.add_job(self.send_reminder, trigger, args=[t.user_id, t.id])

    async def send_reminder(self, user_id: int, task_id: int):
        task = await get_task(task_id)
        await self.bot.send_message(user_id, f"Reminder: {task.text}")
        # reschedule if repeat
