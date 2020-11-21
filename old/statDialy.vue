<template>
  <div class="recharge-list-box">
    <el-dialog :title="title" :visible.sync="dialogVisible" width="1400px" :before-close="handleClose" :close-on-click-modal="false" class="el-dialogs">
      <div class="recharge-list-box">
        <!--操作栏-->
        <div class="action-bar">
          <!-- <el-input size="small" clearable placeholder="流水id" v-model="params.id" @keyup.native.enter="getPayHisList('status')" class="param-input" /> -->
          <!-- <el-input size="small" clearable placeholder="用户id" v-model.number="params.uid" @keyup.native.enter="getPayHisList('status')" class="param-input" /> -->
          <el-input size="small" clearable placeholder="商区码" v-model="params.subDiscCode" @change="getStatDailyList('status')" class="param-input" />
          <el-input size="small" clearable placeholder="推广序列" v-model="params.seqe" @change="getStatDailyList('status')" class="param-input" />
          <!-- <el-select v-model="params.isDirect" clearable size="small" placeholder="用户类型" @change="getPayHisList('status')" >
          <el-option :value="true" label="直推用户"></el-option>
          <el-option :value="false" label="分裂用户"></el-option>
          </el-select>-->
          <el-select v-model="params.sysType" clearable size="small" placeholder="请选择系统类型" @change="getStatDailyList('status')">
            <el-option v-for="item in ['android', 'ios']" :value="item" :label="item" :key="item"></el-option>
          </el-select>
          <el-date-picker v-model="params.time" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" size="small" @change="changeTime"></el-date-picker>
          <el-button type="primary" size="small" @click="getStatDailyList('status')">搜索</el-button>
          <div>
            <el-checkbox v-model="isDed" label="切换到扣量" @click="isExpandOne"></el-checkbox>
            <el-checkbox v-model="isShow" label="展示直推和裂变" @click="isExpand"></el-checkbox>
          </div>
        </div>

        <!--数据表格-->
        <el-table :data="tableData" border style="width: 100%" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading">
          <el-table-column fixed prop="sumDate" label="日期" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="scope.row.sumDate === '总共'">{{ scope.row.sumDate }}</span>
              <span v-else>{{ scope.row.sumDate | changeDate }}</span>
            </template>
          </el-table-column>
          <el-table-column fixed prop="districtCode" label="商区码" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.districtCode || " " }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="sysType" label="系统类型" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.sysType }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="seqe" label="推广序列" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.seqe }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="linkRemark" label="链接备注" align="center" width="150">
            <template slot-scope="scope">
              <span>{{ scope.row.linkRemark }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="dividendRatio" label="分红比" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.dividendRatio | filtersDividendRatio }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="商区账号" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="newUIDCount" label="注册数" align="center" min-width="140">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.newUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.newUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="newDirectUIDCount" label="直推注册数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.newDirectUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.newDirectUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="newFissionUIDCount" label="分裂注册数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.newFissionUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.newFissionUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="rechargeCompleteOrderCount" label="充值单数" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.rechargeCompleteOrderCount }}</span>
              <span v-else>{{ scope.row.dailyData.rechargeCompleteOrderCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directRechargePaidOrderCount" label="直推充值单数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directRechargePaidOrderCount }}</span>
              <span v-else>{{ scope.row.dailyData.directRechargePaidOrderCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionRechargePaidOrderCount" label="分裂充值单数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionRechargePaidOrderCount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionRechargePaidOrderCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="rechargeCompleteOrderAmount" label="充值金额(元)" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.rechargeCompleteOrderAmount }}</span>
              <span v-else>{{ scope.row.dailyData.rechargeCompleteOrderAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directRechargePaidAmount" label="直推充值金额(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directRechargePaidAmount }}</span>
              <span v-else>{{ scope.row.dailyData.directRechargePaidAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionRechargePaidAmount" label="分裂充值金额(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionRechargePaidAmount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionRechargePaidAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="newAndRechargeOrderCount" label="新增充值单数" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.newAndRechargeOrderCount }}</span>
              <span v-else>{{ scope.row.dailyData.newAndRechargeOrderCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="newAndRechargeOrderYuan" label="新增充值金额(元)" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.newAndRechargeOrderYuan }}</span>
              <span v-else>{{ scope.row.dailyData.newAndRechargeOrderYuan }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="arpu" label="ARPU" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.arpu | iTofixed }}</span>
              <span v-else>{{ scope.row.dailyData.arpu | iTofixed }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="userFissionRatio" label="用户分裂率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.userFissionRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.userFissionRatio + "%" }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="buyVIPCount" label="VIP数" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.buyVIPCount }}</span>
              <span v-else>{{ scope.row.dailyData.buyVIPCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directBuyVIPCount" label="直推VIP数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directBuyVIPCount }}</span>
              <span v-else>{{ scope.row.dailyData.directBuyVIPCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionBuyVIPCount" label="分裂VIP数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionBuyVIPCount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionBuyVIPCount }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="buyVIPAmount" label="VIP金额(元)" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.buyVIPAmount }}</span>
              <span v-else>{{ scope.row.dailyData.buyVIPAmount }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="directBuyVIPAmount" label="直推VIP金额(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directBuyVIPAmount }}</span>
              <span v-else>{{ scope.row.dailyData.directBuyVIPAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionBuyVIPAmount" label="分裂VIP金额(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionBuyVIPAmount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionBuyVIPAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="buyVIPUIDCount" label="VIP用户数" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.buyVIPUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.buyVIPUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directBuyVIPUIDCount" label="直推VIP用户数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directBuyVIPUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.directBuyVIPUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionBuyVIPUIDCount" label="分裂VIP用户数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionBuyVIPUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionBuyVIPUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="buyVIDTaxAmount" label="视频收益(元)" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.buyVIDTaxAmount }}</span>
              <span v-else>{{ scope.row.dailyData.buyVIDTaxAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directBuyVIDTaxAmount" label="直推视频收益(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directBuyVIDTaxAmount }}</span>
              <span v-else>{{ scope.row.dailyData.directBuyVIDTaxAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionBuyVIDTaxAmount" label="分裂视频收益(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionBuyVIDTaxAmount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionBuyVIDTaxAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="consume" label="消费(元)" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.consume }}</span>
              <span v-else>{{ scope.row.dailyData.consume }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directConsume" label="直推消费(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directConsume }}</span>
              <span v-else>{{ scope.row.dailyData.directConsume }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionConsume" label="分裂消费(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionConsume }}</span>
              <span v-else>{{ scope.row.dailyData.fissionConsume }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directARPU" label="直推ARPU" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directARPU | iTofixed }}</span>
              <span v-else>{{ scope.row.dailyData.directARPU | iTofixed }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionARPU" label="分裂ARPU" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionARPU | iTofixed }}</span>
              <span v-else>{{ scope.row.dailyData.fissionARPU | iTofixed }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="withDrawPaidOrderCount" label="出款单数" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.withDrawPaidOrderCount }}</span>
              <span v-else>{{ scope.row.dailyData.withDrawPaidOrderCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directWithDrawPaidOrderCount" label="直推出款单数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directWithDrawPaidOrderCount }}</span>
              <span v-else>{{ scope.row.dailyData.directWithDrawPaidOrderCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionWithDrawPaidOrderCount" label="分裂出款单数" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionWithDrawPaidOrderCount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionWithDrawPaidOrderCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="withDrawPaidAmount" label="出款金额(元)" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.withDrawPaidAmount }}</span>
              <span v-else>{{ scope.row.dailyData.withDrawPaidAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directWithDrawPaidAmount" label="直推出款金额(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directWithDrawPaidAmount }}</span>
              <span v-else>{{ scope.row.dailyData.directWithDrawPaidAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionWithDrawPaidAmount" label="分裂出款金额(元)" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionWithDrawPaidAmount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionWithDrawPaidAmount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="visitUIDCount" label="日活跃" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.visitUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.visitUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directVisitUIDCount" label="直推日活跃" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directVisitUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.directVisitUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionVisitUIDCount" label="分裂日活跃" align="center" min-width="100" v-if="isShow" :key="Math.random()">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionVisitUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.fissionVisitUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="nextDayRetainUIDRatio" label="次日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.nextDayRetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.nextDayRetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="day3RetainUIDRatio" label="3日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.day3RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.day3RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="day7RetainUIDRatio" label="7日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.day7RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.day7RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="day15RetainUIDRatio" label="15日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.day15RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.day15RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="day30RetainUIDRatio" label="30日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.day30RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.day30RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directNextDayRetainUIDRatio" label="直推次日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directNextDayRetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.directNextDayRetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directDay3RetainUIDRatio" label="直推3日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directDay3RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.directDay3RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directDay7RetainUIDRatio" label="直推7日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directDay7RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.directDay7RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directDay15RetainUIDRatio" label="直推15日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directDay15RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.directDay15RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="directDay30RetainUIDRatio" label="直推30日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.directDay30RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.directDay30RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionNextDayRetainUIDRatio" label="分裂次日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionNextDayRetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.fissionNextDayRetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionDay3RetainUIDRatio" label="分裂3日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionDay3RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.fissionDay3RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionDay7RetainUIDRatio" label="分裂7日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionDay7RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.fissionDay7RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionDay15RetainUIDRatio" label="分裂15日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionDay15RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.fissionDay15RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="fissionDay30RetainUIDRatio" label="分裂30日留存率" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.fissionDay30RetainUIDRatio + "%" }}</span>
              <span v-else>{{ scope.row.dailyData.fissionDay30RetainUIDRatio + "%" }}</span>
            </template>
          </el-table-column>
          <!-- <el-table-column label="操作" align="center" fixed="right" width="130">
        <template slot-scope="scope">
          <el-button type="success" size="mini" icon="el-icon-edit" @click="editDesc(scope.row)"></el-button>
        </template>
          </el-table-column>-->
        </el-table>
        <el-pagination :page-sizes="[10, 15, 20, 25]" :current-page="params.pageNumber" :page-size="params.pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total" background v-if="total > 10" @size-change="changeSize" @current-change="changeCurrent"></el-pagination>
      </div>
      <div class="zw"></div>
    </el-dialog>
  </div>
</template>
<script>
import { changeTime } from "@/utils/global"
import local from "@/utils/localStroage"
import API from "@/api"
export default {
  data() {
    return {
      isDed: false, //控制切换扣量
      isShow: false, //控制直推裂变
      sum: {},
      dialogVisible: false,
      title: "每日统计",
      tableData: [],
      showMap: {},
      loading: false,
      rchgordMoney: 0,
      total: 0,
      // 请求订单列表参数
      params: {
        pageNumber: 1,
        pageSize: 10,
        time: "",
        startTime: "",
        endTime: "",
        seqe: "",
        subDiscCode: "", //下级商区码
        discCode: "",
        sysType: "" //系统类型
        // sortKey: '',
        // sortValue: '',
      }
    }
  },
  filters: {
    filtersDividendRatio(params) {
      if (params) {
        return params + "%"
      }
      return ""
    }
  },
  created() {
    let actJson = local.get("userInfo").actJson ? JSON.parse(local.get("userInfo").actJson) : {}
    this.initShowMap(actJson.checked)
    this.initShowMap(actJson.halfChecked)
  },
  methods: {
    //初始化显示项
    initShowMap(actJson) {
      if (!actJson) return false
      for (let k in actJson) {
        let auth = actJson[k]
        if (auth.children) {
          this.initShowMap(auth.children)
        }
        if (typeof auth === "string") {
          this.showMap[auth] = true
        } else {
          this.showMap[auth.name] = true
        }
      }
    },
    //根据勾选权限判断是否显示
    hasItemAuth(key) {
      if (!this.showMap[key]) return false
      return this.showMap[key]
    },

    isExpand() {
      this.isShow = this.isShow ? false : true
    },
    isExpandOne() {
      this.isDed = this.isDed ? false : true
    },
    // 请求订单统计列表
    getStatDailyList(type) {
      if (type === "status") {
        this.params.pageNumber = 1
      }
      this.loading = true
      let params = Object.assign({}, this.params, {
        discCode: this.params.discCode,
        srd: this.hasItemAuth("isRealData1")
      })
      API.getStatDailyList(params)
        .then(res => {
          if (res.code === 200 && res.data.list) {
            // this.tableData = res.data.list
            this.tableData = []
            this.total = res.data.total
            this.sum = {
              sumDate: "总共",
              subDiscCode: "",
              seqe: "",
              dividendRatio: "",
              name: "",
              dailyData: res.data.sum,
              dedDailyData: res.data.dedSum
            }
            this.tableData = res.data.list
            this.tableData.unshift(this.sum)
          } else {
            this.tableData = []
            this.total = 0
          }
          this.loading = false
        })
        .catch(() => {
          this.loading = false
        })
    },

    // 打开弹窗
    open(row) {
      this.dialogVisible = true
      this.params.agent = row.agent
      this.params.discCode = row.districtCode
      this.getStatDailyList()
      this.title = "【商区" + row.districtCode + "】每日统计表单"
    },
    // 关闭弹窗
    handleClose() {
      this.dialogVisible = false
      this.params = {
        pageNumber: 1,
        pageSize: 10,
        startTime: "",
        endTime: "",
        time: "",
        seqe: "",
        discCode: "", //商区码
        sysType: "" //系统类型
      }
    },
    // 分页条数改变回掉
    changeSize(size) {
      this.params.pageSize = size
      this.getStatDailyList()
    },
    // 分页页码改变回掉
    changeCurrent(number) {
      this.params.pageNumber = number
      this.getStatDailyList()
    },
    // 时间选择回掉
    changeTime(time) {
      if (time) {
        this.params.startTime = changeTime(time[0]) || ""
        this.params.endTime = changeTime(time[1]) || ""
      } else {
        this.params.startTime = ""
        this.params.endTime = ""
      }
      this.getStatDailyList("status")
    }
  }
}
</script>
<style lang="scss">
.zw {
  height: 100px;
}
.recharge-list-box tbody tr.el-table__row:first-child {
  background: #ccc;
  font-weight: 700;
}
</style>
