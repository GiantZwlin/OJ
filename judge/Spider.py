import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

from problems.models import Problem
from submission.models import Submission, JudgeStatus
from users.models import User


class Spider(object):
    def __init__(self, username):
        self.username = username

    def check_database(self):
        """
        check the database to confirm all the submissions have been judged
        :return: the list of unfinished submissions
        """
        raise NotImplementedError

    def get_result(self, *args, **kwargs):
        raise NotImplementedError


class HduSpider(Spider):

    def check_database(self):
        submissions = Submission.objects.filter(
            result__in=[
                JudgeStatus.STATUS[JudgeStatus.QUEUING],
                JudgeStatus.STATUS[JudgeStatus.COMPILING],
                JudgeStatus.STATUS[JudgeStatus.RUNNING],
            ]
        )
        print(submissions)
        if submissions:
            return self.get_result(submissions)
        else:
            return 1000

    def get_result(self, dest):
        url = 'http://acm.hdu.edu.cn/status.php?user=' + self.username
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.findAll('table')[-2].findAll("tr")
        tds = BeautifulSoup(str(trs), 'lxml').findAll('td')
        cnt = dest.count()
        print(url)
        for i in range(9, len(tds), 9):
            print(i)
            run_id = tds[i].string
            judge_status = tds[i + 2].string
            exe_time = tds[i + 4].string
            exe_memory = tds[i + 5].string
            code_len = tds[i + 6].string
            obj = dest.filter(hdusubmission__hdu_run_id=run_id)
            if obj.count():
                print(obj)
                problem = obj[0].problem
                obj.update(
                    result=judge_status,
                    exe_memory=exe_memory,
                    exe_time=exe_time,
                    code_len=code_len)
                cnt -= 1
                problem.submitted += 1
                if judge_status == "Accepted":
                    user = User.objects.get(submission__hdusubmission__hdu_run_id=run_id)
                    user.problem_solved += 1
                    user.save()
                    problem.accepted += 1
                problem.save()
        return cnt
