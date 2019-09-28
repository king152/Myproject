import time
import re
import random

from dateutil.parser import parse
from download.models import TestCase
from UserInfo.models import UserSoft
from download.common.getCaseAttr import getDownloadAuthorType, getSoftInfo, isDate
from Logs.log import get_log

log = get_log("caseOperate")


# 用例操作
def caseOperate(req, user):
    print(req.POST)
    author = ['28759649', '28759645', '28755951', '28759633', '28759650']
    downAuthor = ['28763241', '28761551']
    modelWay = req.POST.get("way")

    # 功能点
    if req.POST.get("version") == "1":
        getVersion = "返利"
    else:
        getVersion = "升点"

    # 用例编号
    getCaseId = req.POST.get("caseId")

    # 用例名称
    getCaseName = req.POST.get("caseName")

    # 获取资料点数、返利比例信息
    softAttr = req.POST.get("type")
    attrList = getSoftInfo(softAttr)
    getPoint = attrList[0]
    getMoney = attrList[1]
    getCash = attrList[2]
    getIsSupply = attrList[3]
    getBackMoneyRate = attrList[4]
    getBackCashRate = attrList[5]

    # 资料上传时间
    getSoftTime = req.POST.get("softTime")

    if isDate(getSoftTime):
        pass
    else:
        return '00'

    # 是否连续升点标识
    if req.POST.get("level") == '0':
        getLevel = '是'
    else:
        getLevel = '否'

    # 资料softID、下载次数
    if modelWay == "newCase":

        # 资料id
        try:
            Soft = UserSoft.objects.filter(username=user).first()
        except Exception as e:
            log(e)
            Soft = None
        if Soft:
            softId = Soft.soft
        else:
            return "09"

        if getLevel == '是':
            getSoftId = req.POST.get("softId")
        else:
            getSoftId = softId
            UserSoft.objects.filter(soft=softId).delete()

        # 资料下载次数
        numbers = req.POST.get("number")
        wxtNumber = numbers.split(',')[0]
        generalNumber = numbers.split(',')[1]
        qcrNumber = numbers.split(',')[2]

        # 返利金额
        getRebateAmount = req.POST.get("rebate")
    else:
        # 资料id
        getSoftId = req.POST.get("softId")

        # 获取下载次数
        num = req.POST.get('number').split('-')
        generalNumber = re.findall(r':(.*?)次', num[0])[0]
        wxtNumber = re.findall(r':(.*?)次', num[1])[0]
        qcrNumber = re.findall(r':(.*?)次', num[2])[0]

        getRebateAmount = re.findall(r'(.*?)元', req.POST.get("rebate"))

        if len(getRebateAmount) == 0:
            return "04"
        else:
            getRebateAmount = getRebateAmount[0]

    # 返利金额
    if softAttr == '6':
        getRebateAmount = str(float(getMoney) * float(getBackMoneyRate) / 100.0)
    elif softAttr == '7':
        getRebateAmount = str(float(getCash) * float(getBackCashRate) / 100.0)

    # 获取项目名称
    projectName = req.POST.get("project")

    # 资料作者id
    if req.POST.get("softAuthorId") is '':
        getSoftAuthorId = author[random.randint(0, len(author) - 1)]
    else:
        getSoftAuthorId = req.POST.get("softAuthorId")

    # 用例备注
    if req.POST.get("caseNote") is '':
        caseNote = ""
    else:
        caseNote = req.POST.get("caseNote")

    # 资料下载作者id
    getDownloadAuthor = downAuthor[random.randint(0, len(downAuthor) - 1)]

    # 获取下载用户类型
    downloadAuthorType = getDownloadAuthorType(req.POST.get("downloadId"))

    if modelWay == "newCase":  # 新增用例
        if len(getCaseId) == 0 or len(getCaseName) == 0 or len(numbers) == 0 or len(getSoftTime) == 0 or len(
                getRebateAmount) == 0:
            return "01"
        else:
            TestCase.objects.create(project=projectName,
                                    caseId=getCaseId,
                                    caseName=getCaseName,
                                    softId=getSoftId,
                                    softPoint=getPoint,
                                    softMoney=getMoney,
                                    softCash=getCash,
                                    isSupply=getIsSupply,
                                    pointDownloadNumber=generalNumber,
                                    wxtDownloadNumber=wxtNumber,
                                    scanCodeDownloadNumber=qcrNumber,
                                    addTime=parse(getSoftTime),
                                    softAuthorId=getSoftAuthorId,
                                    rebateAmount=getRebateAmount,
                                    caseNote=caseNote,
                                    downloadAuthorId=getDownloadAuthor,
                                    createTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                    functionPoint=str(getVersion),
                                    ifLevel=getLevel,
                                    newCaseUser=user,
                                    routeType=downloadAuthorType,
                                    backMoneyRate=getBackMoneyRate,
                                    backCashRate=getBackCashRate,
                                    )
        return "02"
    else:  # 修改用例
        if len(generalNumber) == 0 or len(wxtNumber) == 0 or len(qcrNumber) == 0:
            return "03"
        # elif len(getRebateAmount) == 0:
        #     return "04"
        elif len(getSoftId) == 0:
            return "05"
        elif len(getCaseName) == 0:
            return "06"
        elif len(getSoftAuthorId) == 0:
            return "07"
        else:
            TestCase.objects.filter(caseId=getCaseId).update(caseName=getCaseName,
                                                             softId=getSoftId,
                                                             softPoint=getPoint,
                                                             softMoney=getMoney,
                                                             softCash=getCash,
                                                             isSupply=getIsSupply,
                                                             pointDownloadNumber=generalNumber,
                                                             wxtDownloadNumber=wxtNumber,
                                                             scanCodeDownloadNumber=qcrNumber,
                                                             addTime=parse(getSoftTime),
                                                             softAuthorId=getSoftAuthorId,
                                                             rebateAmount=getRebateAmount,
                                                             caseNote=caseNote,
                                                             downloadAuthorId=getDownloadAuthor,
                                                             functionPoint=str(getVersion),
                                                             ifLevel=getLevel,
                                                             newCaseUser=user,
                                                             routeType=downloadAuthorType,
                                                             backMoneyRate=getBackMoneyRate,
                                                             backCashRate=getBackCashRate,
                                                             )
            return "08"
