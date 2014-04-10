from __future__ import absolute_import

from apscheduler.executors.base import BaseExecutor, run_job


class TwistedExecutor(BaseExecutor):
    """Runs jobs in the reactor's thread pool."""

    def start(self, scheduler):
        super(TwistedExecutor, self).start(scheduler)
        self._reactor = scheduler._reactor

    def _do_submit_job(self, job, run_times):
        def callback(success, result):
            if success:
                self._run_job_success(job.id, result)
            else:
                self._run_job_error(job.id, result.type, result.value, result.tb)

        self._reactor.getThreadPool().callInThreadWithCallback(callback, run_job, job, run_times)