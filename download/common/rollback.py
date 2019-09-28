# coding=utf-8
from download.common.sqlOprate import MySqlServer
from download.common.stepmodel import RecordBookShopLog, RecordConsumeLog,RecordDowninterfaceHits,\
    RecordFlowLogAfterSoftPointIncre, RecordFreePointDownFeeBackLog, RecordIncrePointFlowLog, \
    RecordMonthlyExcellentDownFeeBackLog, RecordSellIncomeLog, RecordUserGivePoint, \
    RecordSoftPointIncreInfoLogAndUpdateDownNum, UpdateDownInfoStatus, UpdateSoftDownloadHit, UpdateSoftPoint, \
    UpdateUserDown, GetFeedbackShieledUserGroupInfo, GetIncrePointRuleInfo, GetIncrePointShieledGroupInfo, \
    AddSettlementLog, AsserIncreasedForNormalFeeBack, AssetIncreasedMonthlyExcellentDown, FeeBackLogForMonthly, \
    FeeBackLogForNormal, HighWXTConsumeLog, HighWxtDownLoadStatisticsLog
from download.common.insertSql import getRebate, getPoint, getStatus
import time
from Logs.log import get_log

log = get_log("rollback")


# 获取执行结果
def getResult(softid, nowtime, funcPoint, softauthor, AddTime):
    """
    :param softid: 资料softid
    :param nowtime: 获取结果执行时间
    :param funcPoint: 功能，返利、升点
    :param softauthor: 资料作者
    :param AddTime: 正常执行时间
    :return:
    """
    times = 0
    while True:
        if getStatus(softid, AddTime) == 1:
            if funcPoint == '返利':
                print("获取时间：", nowtime)
                amount = getRebate(Softid=softid, Userid=softauthor, exectime=nowtime)
                return ["返利", amount]
            else:
                print("获取时间：", nowtime)
                amount = getRebate(Softid=softid, Userid=softauthor, exectime=nowtime)
                point = getPoint(softid)
                return ["升点", amount, point]
        else:
            times += 1
            time.sleep(0.5)
        if times == 10:
            return ["服务器出现异常！"]


def rollBackData(step, guid, softpoint, funcPoint, SchoolDown, PointDown, QCRdown, softauthor):
    """
    :param funcPoint: 功能点：返利、提成
    :param step: 步骤名称
    :param guid: 快照表DownInfoID
    :param softpoint: 资料点数
    :param SchoolDown: 网校通下载量
    :param PointDown: 点数下载量
    :param QCRdown: 扫码下载量
    :param softauthor: 资料作者
    :return:
    """
    STEP = MySqlServer("10.1.5.70", 'zxxktest', '123456', 'ZxxkDownload')
    # 获取快照表数据
    q_sql = "SELECT *FROM dbo.Cl_DownInfo WHERE ID='{}'".format(guid)

    data = STEP.query_sql(q_sql)

    for d in data:
        if len(d) == 0:
            log.error("获取快照表数据异常！")
            return ["服务器出现异常！"]
        AddTime = d[6]
        softId = str(d[3])
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("执行时间：", nowTime)
    if step == "消费日志":  # RecordConsumeLog  消费日志
        RecordConsumeLog(DownInfoID=guid, Status=2, InfoID=softId, consumetime=AddTime)
        RecordBookShopLog(Status=0, DownInfoID=guid)
        RecordDowninterfaceHits(InfoID=softId, SchoolDown=SchoolDown, PointDown=PointDown, QCRdown=QCRdown,
                                softpoint=softpoint, Status=0, DownInfoID=guid)
        RecordIncrePointFlowLog(InfoID=softId, SoftPoint=softpoint, Status=0, DownInfoID=guid)
        UpdateSoftDownloadHit(softId, Status=0, DownInfoID=guid)
        GetFeedbackShieledUserGroupInfo(Status=0, DownInfoID=guid)
        RecordFreePointDownFeeBackLog(UserID=softauthor, AddTime=AddTime, Status=0, DownInfoID=guid)
        RecordMonthlyExcellentDownFeeBackLog(softId, Status=0, DownInfoID=guid)
        AssetIncreasedMonthlyExcellentDown(Status=0, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u'书城日志':  # RecordBookShopLog  书城日志
        RecordBookShopLog(Status=2, DownInfoID=guid)
        RecordDowninterfaceHits(InfoID=softId, SchoolDown=SchoolDown, PointDown=PointDown, QCRdown=QCRdown,
                                softpoint=softpoint, Status=0, DownInfoID=guid)
        RecordIncrePointFlowLog(InfoID=softId, SoftPoint=softpoint, Status=0, DownInfoID=guid)
        UpdateSoftDownloadHit(softId, Status=0, DownInfoID=guid)
        GetFeedbackShieledUserGroupInfo(Status=0, DownInfoID=guid)
        RecordFreePointDownFeeBackLog(UserID=softauthor, AddTime=AddTime, Status=0, DownInfoID=guid)
        RecordMonthlyExcellentDownFeeBackLog(softId, Status=0, DownInfoID=guid)
        AssetIncreasedMonthlyExcellentDown(Status=0, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"通道类型下载量":  # RecordDowninterfaceHits 通道类型下载量
        RecordDowninterfaceHits(InfoID=softId, SchoolDown=SchoolDown, PointDown=PointDown, QCRdown=QCRdown,
                                softpoint=softpoint, Status=2, DownInfoID=guid)
        RecordIncrePointFlowLog(InfoID=softId, SoftPoint=softpoint, Status=0, DownInfoID=guid)
        UpdateSoftDownloadHit(softId, Status=0, DownInfoID=guid)
        GetFeedbackShieledUserGroupInfo(Status=0, DownInfoID=guid)
        RecordFreePointDownFeeBackLog(UserID=softauthor, AddTime=AddTime, Status=0, DownInfoID=guid)
        RecordMonthlyExcellentDownFeeBackLog(softId, Status=0, DownInfoID=guid)
        AssetIncreasedMonthlyExcellentDown(Status=0, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"资料升点下载量日志流水记录":  # RecordIncrePointFlowLog 资料升点下载量日志流水记录
        RecordIncrePointFlowLog(InfoID=softId, SoftPoint=softpoint, Status=2, DownInfoID=guid)
        UpdateSoftDownloadHit(softid=softId, Status=0, DownInfoID=guid)
        GetFeedbackShieledUserGroupInfo(Status=0, DownInfoID=guid)
        RecordFreePointDownFeeBackLog(UserID=softauthor, AddTime=AddTime, Status=0, DownInfoID=guid)
        RecordMonthlyExcellentDownFeeBackLog(softId, Status=0, DownInfoID=guid)
        AssetIncreasedMonthlyExcellentDown(Status=0, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"更新资料下载量":  # UpdateSoftDownloadHit 更新资料下载量
        UpdateSoftDownloadHit(softid=softId, Status=2, DownInfoID=guid)
        GetFeedbackShieledUserGroupInfo(Status=0, DownInfoID=guid)
        RecordFreePointDownFeeBackLog(UserID=softauthor, AddTime=AddTime, Status=0, DownInfoID=guid)
        RecordMonthlyExcellentDownFeeBackLog(softId, Status=0, DownInfoID=guid)
        AssetIncreasedMonthlyExcellentDown(Status=0, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"不发放奖励的用户群组":  # GetFeedbackShieledUserGroupInfo 不发放奖励的用户群组
        GetFeedbackShieledUserGroupInfo(Status=2, DownInfoID=guid)
        RecordFreePointDownFeeBackLog(UserID=softauthor, AddTime=AddTime, Status=0, DownInfoID=guid)
        RecordMonthlyExcellentDownFeeBackLog(softId, Status=0, DownInfoID=guid)
        AssetIncreasedMonthlyExcellentDown(Status=0, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"记录免费和点数资料批量":  # RecordFreePointDownFeeBackLog 记录免费和点数资料批量
        RecordFreePointDownFeeBackLog(UserID=softauthor, AddTime=AddTime, Status=2, DownInfoID=guid)
        RecordMonthlyExcellentDownFeeBackLog(softId, Status=0, DownInfoID=guid)
        AssetIncreasedMonthlyExcellentDown(Status=0, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"记录月度优秀下载奖励批次":  # RecordMonthlyExcellentDownFeeBackLog 记录月度优秀下载奖励批次
        RecordMonthlyExcellentDownFeeBackLog(softid=softId, Status=2, DownInfoID=guid)
        AssetIncreasedMonthlyExcellentDown(Status=0, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"月度优秀下载奖励发放":  # AssetIncreasedMonthlyExcellentDown 月度优秀下载奖励发放
        AssetIncreasedMonthlyExcellentDown(Status=2, DownInfoID=guid)
        AsserIncreasedForNormalFeeBack(Status=0, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"下载提成发放":  # AsserIncreasedForNormalFeeBack 下载提成发放
        AsserIncreasedForNormalFeeBack(Status=2, DownInfoID=guid)
        FeeBackLogForMonthly(Status=0, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"月度优秀下载返利日志记录":  # FeeBackLogForMonthly 月度优秀下载返利日志记录
        FeeBackLogForMonthly(Status=2, DownInfoID=guid, Softid=softId)
        FeeBackLogForNormal(Status=0, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"普通下载提成返利日志记录":  # FeeBackLogForNormal 普通下载提成返利日志记录
        FeeBackLogForNormal(Status=2, DownInfoID=guid, Softid=softId)
        RecordSellIncomeLog(Status=0, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"精品销售记录":  # RecordSellIncomeLog 精品销售记录
        RecordSellIncomeLog(Status=2, DownInfoID=guid)
        RecordUserGivePoint(Status=0, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"贡献点":  # RecordUserGivePoint 贡献点
        RecordUserGivePoint(Status=2, DownInfoID=guid)
        GetIncrePointShieledGroupInfo(Status=0, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"获取涨点屏蔽群组信息":  # GetIncrePointShieledGroupInfo 获取涨点屏蔽群组信息
        GetIncrePointShieledGroupInfo(Status=2, DownInfoID=guid)
        GetIncrePointRuleInfo(Status=0, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"获取升点规则信息":  # GetIncrePointRuleInfo 获取升点规则信息
        GetIncrePointRuleInfo(Status=2, DownInfoID=guid)
        UpdateSoftPoint(Status=0, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"更新资料点数":  # UpdateSoftPoint 更新资料点数
        UpdateSoftPoint(Status=2, DownInfoID=guid, flag=funcPoint, softID=softId, SoftPoint=softpoint)
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=0, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"涨点日志记录":  # RecordSoftPointIncreInfoLogAndUpdateDownNum 涨点日志记录
        RecordSoftPointIncreInfoLogAndUpdateDownNum(Status=2, DownInfoID=guid, softid=softId)
        RecordFlowLogAfterSoftPointIncre(Status=0, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"升点后记录下载量升点日志":  # RecordFlowLogAfterSoftPointIncre 升点后记录下载量升点日志
        RecordFlowLogAfterSoftPointIncre(Status=2, DownInfoID=guid)
        UpdateUserDown(Status=0, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"更新用户下载量":  # UpdateUserDown 更新用户下载量
        UpdateUserDown(Status=2, DownInfoID=guid)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == "高端网校通下载储值":
        HighWXTConsumeLog(Status=2, DownInfoID=guid, InfoID=softId)
        HighWxtDownLoadStatisticsLog(Status=0, DownInfoID=guid, InfoID=softId)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == "高端网校通下载统计日志":
        HighWxtDownLoadStatisticsLog(Status=2, DownInfoID=guid, InfoID=softId)
        AddSettlementLog(Status=0, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"添加结算日志":  # AddSettlementLog 添加结算日志
        AddSettlementLog(Status=2, DownInfoID=guid)
        UpdateDownInfoStatus(DownInfoID=guid, Status=0)

    elif step == u"更新快照信息状态":  # UpdateDownInfoStatus 更新快照信息状态
        UpdateDownInfoStatus(DownInfoID=guid, Status=2)
        # 获取执行结果

    else:
        print("传参错误！")

    return getResult(softId, nowTime, funcPoint, softauthor, AddTime)
