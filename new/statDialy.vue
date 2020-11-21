<template>
  <div class="recharge-list-box">
    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="1400px"
      :before-close="handleClose"
      :close-on-click-modal="false"
      class="el-dialogs"
    >
      <div class="recharge-list-box">
        <!--操作栏-->
        <div class="action-bar">
          <!-- <el-input size="small" clearable placeholder="流水id" v-model="params.id" @keyup.native.enter="getPayHisList('status')" class="param-input" /> -->
          <!-- <el-input size="small" clearable placeholder="用户id" v-model.number="params.uid" @keyup.native.enter="getPayHisList('status')" class="param-input" /> -->
          <el-input
            size="small"
            clearable
            :placeholder="$t('code_0')"
            v-model="params.subDiscCode"
            @change="getStatDailyList('status')"
            class="param-input"
          />
          <el-input
            size="small"
            clearable
            :placeholder="$t('code_1')"
            v-model="params.seqe"
            @change="getStatDailyList('status')"
            class="param-input"
          />
          <!-- <el-select v-model="params.isDirect" clearable size="small" placeholder="用户类型" @change="getPayHisList('status')" >
          <el-option :value="true" label="直推用户"></el-option>
          <el-option :value="false" label="分裂用户"></el-option>
          </el-select>-->
          <el-select
            v-model="params.sysType"
            clearable
            size="small"
            :placeholder="$t('code_2')"
            @change="getStatDailyList('status')"
          >
            <el-option v-for="item in ['android', 'ios']" :value="item" :label="item" :key="item"></el-option>
          </el-select>
          <el-date-picker
            v-model="params.time"
            type="daterange"
            range-separator="至"
            :start-placeholder="$t('code_3')"
            :end-placeholder="$t('code_4')"
            size="small"
            @change="changeTime"
          ></el-date-picker>
          <el-button type="primary" size="small" @click="getStatDailyList('status')">{{$t("code_5")}}</el-button>
          <div>
            <el-checkbox v-model="isDed" :label="$t('code_6')" @click="isExpandOne"></el-checkbox>
            <el-checkbox v-model="isShow" :label="$t('code_7')" @click="isExpand"></el-checkbox>
          </div>
        </div>

        <!--数据表格-->
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          v-loading="loading"
          :element-loading-text="$t('code_8')"
          element-loading-spinner="el-icon-loading"
        >
          <el-table-column fixed prop="sumDate" :label="$t('code_9')" align="center" min-width="100">
            <template slot-scope="scope">
              <span v-if="scope.row.sumDate === '总共'">{{ scope.row.sumDate }}</span>
              <span v-else>{{ scope.row.sumDate | changeDate }}</span>
            </template>
          </el-table-column>
          <el-table-column fixed prop="districtCode" :label="$t('code_0')" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.districtCode || " " }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="sysType" :label="$t('code_10')" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.sysType }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="seqe" :label="$t('code_1')" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.seqe }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="linkRemark" :label="$t('code_11')" align="center" width="150">
            <template slot-scope="scope">
              <span>{{ scope.row.linkRemark }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="dividendRatio" :label="$t('code_12')" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.dividendRatio | filtersDividendRatio }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="name" :label="$t('code_13')" align="center" min-width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="newUIDCount" :label="$t('code_14')" align="center" min-width="140">
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.newUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.newUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="newDirectUIDCount"
            :label="$t('code_15')"
            align="center"
            min-width="100"
            v-if="isShow"
            :key="Math.random()"
          >
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.newDirectUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.newDirectUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="newFissionUIDCount"
            :label="$t('code_16')"
            align="center"
            min-width="100"
            v-if="isShow"
            :key="Math.random()"
          >
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.newFissionUIDCount }}</span>
              <span v-else>{{ scope.row.dailyData.newFissionUIDCount }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="rechargeCompleteOrderCount"
            :label="$t('code_17')"
            align="center"
            min-width="100"
          >
            <template slot-scope="scope">
              <span v-if="isDed">{{ scope.row.dedDailyData.rechargeCompleteOrderCount }}</span>
              <span v-else>{{ scope.row.dailyData.rechargeCompleteOrderCount }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="directRechargePaidOrderCount"
            :label="$t('code_18')"
            align="center"
            min-width="100"
            v-if="isShow"
            :key="Math.random()"
          >
            <template slot-scope="scope">
