from download.common.insertSql import initSoftPoint, updateDownloadDate, insertSnapshotDate, initDownloadDate, \
    getStatus, getPoint
from download.models import TestCase, CaseResult, TestSoftId
from download.common.rollback import getRebate, rollBackData
from download.common.inserts import insertDate, initDate, initPoint, getbate
from download.common.getCaseAttr import getDownloadId, getNowTime
import time
from Logs.log import get_log

log = get_log("performCase")


# 用例执行函数
def runCase(caseIds, username):
    if caseIds == 'all':
        dicts = TestCase.objects.filter(createuser=username).values()
        for dict in dicts:
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            if dict["point"] == '免费':
                dict["point"] = 0
            elif dict["point"] == '储值':
                dict["point"] = 6
            elif dict["point"] == '第三方':
                dict["point"] = 7
            elif dict["point"] == '高级点':
                dict["point"] = 8
            else:
                dict["point"] = dict["point"]

            if dict["downloadAuthorTypeName"] == "初中高端网校通":
                route = "20"
            elif dict["downloadAuthorTypeName"] == "初中中端网校通":
                route = "21"
            elif dict["downloadAuthorTypeName"] == "初中普通网校通":
                route = "22"
            elif dict["downloadAuthorTypeName"] == "高中高端网校通":
                route = "23"
            elif dict["downloadAuthorTypeName"] == "高中中端网校通":
                route = "24"
            else:
                route = "25"

            if dict["level"] == "是":
                initSoftPoint(dict["point"], dict["softid"], dict["softauthor_id"], dict["softtime"])  # 初始化资料点数、上传时间
                updateDownloadDate(dict["softid"], dict["wxtnumber"], dict["Generalnumber"], dict["QCRnumber"],
                                   dict["point"])  # 初始化资料下载量数据
                guid = insertSnapshotDate(dict["point"], dict["softauthor_id"], dict["softid"],
                                          dict["downloadauthor_id"], dict["softtime"], route)  # 插入快照表下载数据
            else:
                initSoftPoint(dict["point"], dict["softid"], dict["softauthor_id"], dict["softtime"])  # 初始化资料点数、上传时间
                initDownloadDate(dict["softid"], dict["wxtnumber"], dict["Generalnumber"],
                                 dict["QCRnumber"])  # 初始化资料下载量数据
                guid = insertSnapshotDate(dict["point"], dict["softauthor_id"], dict["softid"],
                                          dict["downloadauthor_id"], dict["softtime"], route)  # 插入快照表下载数据
            times = 0
            time.sleep(1)
            while True:
                if getStatus(dict["softid"], nowTime) == 1:
                    if dict["case_version"] == '返利':
                        if getRebate(dict["softid"], dict["softauthor_id"], nowTime) == float(
                                dict['asserContent']):
                            CaseResult.objects.create(
                                case_id=dict["case_id"],
                                case_name=dict["case_name"],
                                asserContent=dict['asserContent'],
                                asserresult=True,
                                executtime=nowTime,
                                executnumber=time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())),
                                details="result:" + str(getRebate(dict["softid"], dict["softauthor_id"],
                                                                  nowTime)) + "--" + "guid:" + str(guid),
                                guid=str(guid)
                            )
                            break
                        else:
                            CaseResult.objects.create(
                                case_id=dict["case_id"],
                                case_name=dict["case_name"],
                                asserContent=dict['asserContent'],
                                asserresult=False,
                                executtime=nowTime,
                                executnumber=time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())),
                                details="result:" + str(getRebate(dict["softid"], dict["softauthor_id"],
                                                                  nowTime)) + "--" + "guid:" + str(guid),
                                guid=str(guid)
                            )
                            break
                    else:
                        if dict["point"] == '免费':
                            dict["point"] = 0
                        else:
                            dict["point"] = dict["point"]
                        if int(getPoint(dict["softid"])) == (int(dict["point"]) + 1):
                            CaseResult.objects.create(
                                case_id=dict["case_id"],
                                case_name=dict["case_name"],
                                asserContent=dict['asserContent'],
                                asserresult=True,
                                executtime=nowTime,
                                executnumber=time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())),
                                details="升点前：{}-后：{}".format(str(dict["point"]),
                                                             str(getPoint(dict["softid"]))) + "返利：{}".format(
                                    getRebate(dict["softid"], dict["softauthor_id"], nowTime)) + \
                                        "--guid:" + str(guid),
                                guid=str(guid)
                            )
                            break
                        else:
                            CaseResult.objects.create(
                                case_id=dict["case_id"],
                                case_name=dict["case_name"],
                                asserContent=dict['asserContent'],
                                asserresult=False,
                                executtime=nowTime,
                                executnumber=time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())),
                                details="升点前：{}-后：{}".format(str(dict["point"]),
                                                             str(getPoint(dict["softid"]))) + "返利：{}".format(
                                    getRebate(dict["softid"], dict["softauthor_id"], nowTime)) + \
                                        "--guid:" + str(guid),
                                guid=str(guid)
                            )
                            break
                else:
                    times += 1
                    time.sleep(0.5)
                if times == 20:
                    CaseResult.objects.create(
                        case_id=dict["case_id"],
                        case_name=dict["case_name"],
                        asserContent=dict['asserContent'],
                        asserresult=False,
                        executtime=nowTime,
                        executnumber=time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())),
                        details="数据处理异常，请联系相关开发人员" + "--" + "guid:" + str(guid)
                    )
                    break
    else:
        ids = caseIds.split(',')
        ids.reverse()
        for caseId in ids:
            try:
                dates = TestCase.objects.filter(caseId=caseId).values()
            except Exception as e:
                log.error(e)
            for d in dates:
                nowTime = getNowTime()
                route = getDownloadId(d['routeType'])
                initSoftPoint(d["softId"], d["softAuthorId"], d["addTime"], d["softPoint"],
                              d["softMoney"], d["softCash"], d["isSupply"], d["backCashRate"], d["backMoneyRate"])
                guid = insertSnapshotDate(d["softPoint"], d["softMoney"], d["isSupply"], d["softCash"],
                                          d["backMoneyRate"],d["softAuthorId"], d["softId"], d["downloadAuthorId"],
                                          d["addTime"], route, d["backCashRate"])
                if d["ifLevel"] == "是":
                    updateDownloadDate(d["softId"], d["wxtDownloadNumber"], d["pointDownloadNumber"],
                                       d["scanCodeDownloadNumber"], d["softPoint"])
                else:
                    initDownloadDate(d["softId"], d["wxtDownloadNumber"], d["pointDownloadNumber"],
                                     d["scanCodeDownloadNumber"])
                times = 0
                time.sleep(1)
                while True:
                    if getStatus(d["softId"], nowTime) == 1:
                        # 返利结果判断
                        if d["functionPoint"] == '返利':
                            if getRebate(d["softId"], d["softAuthorId"], nowTime) == float(d['rebateAmount']):
                                CaseResult.objects.create(
                                    caseId=d["caseId"],
                                    caseName=d["caseName"],
                                    rebateAmount=d['rebateAmount'],
                                    assertResult=True,
                                    executionTime=nowTime,
                                    CaseExecutionResult="返利：{}".format(
                                        getRebate(d["softId"], d["softAuthorId"], nowTime)) + "--guid:" + str(guid),
                                    guid=str(guid),
                                    project=d["project"],
                                    executionUser=username
                                )
                                break
                            else:
                                CaseResult.objects.create(
                                    caseId=d["caseId"],
                                    caseName=d["caseName"],
                                    rebateAmount=d['rebateAmount'],
                                    assertResult=False,
                                    executionTime=nowTime,
                                    CaseExecutionResult="返利：{}".format(
                                        getRebate(d["softId"], d["softAuthorId"], nowTime)) + "--guid:" + str(guid),
                                    guid=str(guid),
                                    project=d["project"],
                                    executionUser=username
                                )
                                break
                        else:  # 升点结果判断
                            if int(getPoint(d["softId"])) == int(d["softPoint"]) + 1:  # 获取升点结果并进行判断
                                # 将结果写入数据库
                                CaseResult.objects.create(
                                    caseId=d["caseId"],
                                    caseName=d["caseName"],
                                    rebateAmount=d['rebateAmount'],
                                    assertResult=True,
                                    executionTime=nowTime,
                                    CaseExecutionResult="升点前：{}-后：{}".format(str(d["softPoint"]),
                                                                             str(getPoint(d["softId"]))) +
                                                        "返利：{}".format(getRebate(d["softId"], d["softAuthorId"],
                                                                                 nowTime)) + "--guid:" + str(guid),
                                    guid=str(guid),
                                    project=d["project"],
                                    executionUser=username
                                )
                                break
                            else:
                                # 将结果写入数据库
                                CaseResult.objects.create(
                                    caseId=d["caseId"],
                                    caseName=d["caseName"],
                                    rebateAmount=d['rebateAmount'],
                                    assertResult=False,
                                    executionTime=nowTime,
                                    CaseExecutionResult="升点前：{}-后：{}".format(str(d["softPoint"]),
                                                                             str(getPoint(d["softId"]))) +
                                                        "返利：{}".format(getRebate(d["softId"], d["softAuthorId"],
                                                                                 nowTime)) + "--guid:" + str(guid),
                                    guid=str(guid),
                                    project=d["project"],
                                    executionUser=username
                                )
                                break
                    else:
                        times += 1
                        time.sleep(0.5)
                    if times == 20:
                        # 服务器处理异常写入数据
                        CaseResult.objects.create(
                            caseId=d["caseId"],
                            caseName=d["caseName"],
                            rebateAmount=d['rebateAmount'],
                            assertResult=False,
                            executionTime=nowTime,
                            CaseExecutionResult="数据处理异常，请联系相关开发人员" + "--" + "guid:" + str(guid),
                            guid=str(guid),
                            project=d["project"],
                            executionUser=username
                        )
                        break


# 异常步骤用例执行函数
def stepRunCase(Step, caseId):
    try:
        case = TestCase.objects.filter(caseId=caseId).values().first()
    except Exception as e:
        log.error(e)
    try:
        Guid = CaseResult.objects.filter(caseId=caseId).order_by("-executionTime").values().first()
    except Exception as e:
        log.error(e)

    result = rollBackData(step=Step, guid=Guid["guid"], softpoint=case["point"], funcPoint=case["case_version"], \
                          SchoolDown=case["wxtnumber"], PointDown=case["Generalnumber"], QCRdown=case["QCRnumber"], \
                          softauthor=case["softauthor_id"])

    if result[0] == "返利":
        CaseResult.objects.filter(guid=Guid["guid"]).update(redetails="返利" + str(result[1]))
    elif result[0] == "升点":
        CaseResult.objects.filter(guid=Guid["guid"]).update(
            redetails="提成：" + str(result[1]) + "-升点：" + str(result[2]))
    else:
        CaseResult.objects.filter(guid=Guid["guid"]).update(redetails=result[0])


# 多线程执行
def runGetid(lock, start, end):
    i = start
    while i < end:
        lock.acquire()
        Soft = TestSoftId.objects.get(id=i)
        Id = Soft.softid
        print(Id)
        initPoint(Id)
        initDate(Id)
        guid = insertDate(Id)
        TestSoftId.objects.filter(id=i).update(guid=guid)
        lock.release()
        i += 1


# 多线程查询结果
def getResult(lock, start, end):
    i = start
    while i < end:
        lock.acquire()
        Soft = TestSoftId.objects.get(id=i)
        Id = Soft.softid
        rd = getbate(str(Id))
        print("资料id为：{}---返利金额：{}".format(Id, rd))
        TestSoftId.objects.filter(id=i).update(result=rd)
        TestSoftId.objects.bulk_update()
        lock.release()
        i += 1
