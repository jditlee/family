<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="收入账户" prop="acc_id">
        <el-select clearable v-model="queryParams.acc_id" style="width: 200px" placeholder="请选择账户">
          <el-option
              v-for="dict in accountIds"
              :key="dict.id"
              :label="dict.accounrName"
              :value="dict.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="收入类型" prop="type_id">
        <el-select clearable v-model="queryParams.type_id" style="width: 200px" placeholder="请选择收入类型">
          <el-option
              v-for="dict in income_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="收入明细" prop="detail">
        <el-input
            v-model="queryParams.detail"
            placeholder="请输入收入明细"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="入账人" prop="user_id">
        <el-select clearable v-model="queryParams.user_id" style="width: 200px" placeholder="请选择入账人">
          <el-option
              v-for="dict in userListName"
              :key="dict.userId"
              :label="dict.nickName"
              :value="dict.userId"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="收入来源" prop="source_id">
        <el-select v-model="queryParams.source_id" placeholder="请选择收入来源" clearable style="width: 200px">
          <el-option
              v-for="dict in income_source"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="收入时间" prop="income_time">
        <el-date-picker v-model="dateRange" type="daterange" range-separator="至"
                        start-placeholder="开始日期"
                        end-placeholder="结束日期"
                        value-format="YYYY-MM-DD"
                        style="width: 308px">
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
            type="primary"
            plain
            icon="Plus"
            @click="handleAdd"
            v-hasPermi="['money:income:add']"
        >新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
            type="success"
            plain
            icon="Edit"
            :disabled="single"
            @click="handleUpdate"
            v-hasPermi="['money:income:edit']"
        >修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
            type="danger"
            plain
            icon="Delete"
            :disabled="multiple"
            @click="handleDelete"
            v-hasPermi="['money:income:remove']"
        >删除
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="incomeList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="账户" align="center" prop="accId" width="130">
        <template #default="scope">
          <span>{{ matchAccount(scope.row.accId) }} </span>
        </template>
      </el-table-column>
      <el-table-column label="收入类型" align="center" prop="typeId" width="130">
        <template #default="scope">
          <dict-tag :options="income_type" :value="scope.row.typeId"/>
        </template>
      </el-table-column>
      <el-table-column label="收入明细" align="center" prop="detail" :show-overflow-tooltip="true" width="130"/>
      <el-table-column label="收入金额" align="center" prop="amount" width="130">
      </el-table-column>
      <!-- <el-table-column label="货币类型" align="center" prop="currency" width="130">
        <template #default="scope">
          <dict-tag :options="money_type" :value="scope.row.currency"/>
        </template>
      </el-table-column> -->
      <!-- <el-table-column label="支付方式" align="center" prop="paymentMethod" width="130">
        <template #default="scope">
          <dict-tag :options="payment_method" :value="scope.row.paymentMethod"/>
        </template>
      </el-table-column> -->
      <!-- <el-table-column label="入账人" align="center" prop="userId" width="130">
        <template #default="scope">
          <span>{{ matchUserId(scope.row.userId) }}</span>
        </template>
      </el-table-column> -->
      <el-table-column label="收入时间" align="center" prop="incomeTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.incomeTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="收入来源" align="center" prop="sourceId" width="130">
        <template #default="scope">
          <dict-tag :options="income_source" :value="scope.row.sourceId"/>
        </template>
      </el-table-column>
      <!-- <el-table-column label="创建时间" align="center" prop="createTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column> -->
      <el-table-column label="备注" align="center" prop="remark" width="300"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                     v-hasPermi="['money:income:edit']">修改
          </el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                     v-hasPermi="['money:income:remove']">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

     <pagination
        v-show="total > 0"
        :total="total"
        v-model:page="queryParams.page_num"
        v-model:limit="queryParams.page_size"
        @pagination="getList"
    />

    <!-- 添加或修改公告对话框 -->
    <el-dialog :title="title" v-model="open" width="780px" append-to-body>
      <el-form ref="incomeRef" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="入账账户" prop="acc_id">
              <el-select v-model="form.acc_id" placeholder="请选择账户ID" :disabled="mode === 'edit'">
                <el-option
                    v-for="dict in accountIds"
                    :key="dict.id"
                    :label="dict.accounrName"
                    :value="dict.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="收入类型" prop="type_id">
              <el-select v-model="form.type_id" placeholder="请选择收入类型">
                <el-option
                    v-for="dict in income_type"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="收入明细" prop="detail">
              <el-input v-model="form.detail" placeholder="请输入收入明细"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="收入金额" prop="amount">
              <el-input-number
                  placeholder="请输入收入金额"
                  v-model="form.amount"
                  :precision="2"
                  :step="0.01"
                  controls-position="right"
              >
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="货币类型" prop="currency">
              <el-select v-model="form.currency" placeholder="请选择货币类型">
                <el-option
                    v-for="dict in money_type"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="支付方式" prop="payment_method">
              <el-select v-model="form.payment_method" placeholder="请选择货币支付方式">
                <el-option
                    v-for="dict in payment_method"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="入账人" prop="user_id">
              <el-select clearable v-model="form.user_id" placeholder="请选择入账人">
                <el-option
                    v-for="dict in userListName"
                    :key="dict.userId"
                    :label="dict.nickName"
                    :value="dict.userId"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="收入时间" prop="income_time">
              <el-date-picker v-model="form.income_time" align="right" type="date"
                              placeholder="请选择日期"></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="收入来源" prop="source_id">
              <el-select v-model="form.source_id" placeholder="请选择收入来源">
                <el-option
                    v-for="dict in income_source"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="form.remark" type="textarea" placeholder="请输入备注"/>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Income">
import {listIncome, getIncome, delIncome, addIncome, updateIncome,} from "@/api/money/income";
import {getUserListName, getUserProfile} from '@/api/system/user'
import {listAccountFinance} from "@/api/money/account_finance.js";

const {proxy} = getCurrentInstance();
const {
  income_source,
  income_type,
  money_type,
  payment_method
} = proxy.useDict("income_source", "income_type", "money_type", "payment_method");

const incomeList = ref([]);
const userListName = ref([])
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const dateRange = ref([]);
const currentUser = ref("")
const accountIds = ref([])
const mode = ref("")


const data = reactive({
  form: {
    amount: 0 // 设置默认值为0，确保它是数字类型
  },
  queryParams: {
    type_id: '',
    detail: '',
    user_id: undefined,
    acc_id: undefined,
    income_type: undefined,
    income_time: undefined,
    source_id: undefined,
    page_num: 1,
    page_size: 10,
  },
  rules: {
    amount: [
      {required: true, message: '收入金额不能为空'},
      {
        validator: (rule, value, callback) => {
          if (value === '' || value <= 0) {
            callback(new Error('收入金额必须大于 0'));
          } else {
            callback();
          }
        },
        trigger: 'blur'
      }
    ],
    acc_id: [{required: true, message: '入账账户不能为空'}]

    
  },
});

const {queryParams, form, rules} = toRefs(data);

/** 查询公告列表 */
function getList() {
  loading.value = true;
  listIncome(queryParams.value, dateRange.value).then(response => {
    incomeList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 查询用户列表 */
function getUserList() {
  getUserListName({pageNum: 1, pageSize: 300}).then(response => {
    userListName.value = response.rows;
  })
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    id: undefined,
    type_id: '1',
    detail: '',
    amount: 0,
    currency: '1',
    payment_method: '1',
    user_id: currentUser.value,
    acc_id: '',
    income_time: new Date(),
    source_id: '1',
    remark: ''
  };
  proxy.resetForm("incomeRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.page_num = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  dateRange.value = []
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 多选框选中数据 */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "新增收入";
  mode.value = 'add'
}

/**修改按钮操作 */
function handleUpdate(row) {
  reset();
  const incomeId = row.id || ids.value;
  getIncome(incomeId).then(response => {
    form.value = response.data;
    form.value.type_id = form.value.type_id.toString()
    form.value.currency = form.value.currency.toString()
    form.value.payment_method = form.value.payment_method.toString()
    form.value.source_id = form.value.source_id.toString()

    open.value = true;
    title.value = "修改收入";
    mode.value = 'edit'
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["incomeRef"].validate(valid => {
    if (valid) {
      if (form.value.id != undefined) {
        updateIncome(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addIncome(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const incomeIds = row.id || ids.value
  proxy.$modal.confirm('是否确认删除id为"' + incomeIds + '"的数据项？').then(function () {
    return delIncome(incomeIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {
  });
}

/** 匹配user */
function matchUserId(userId) {
  if (userId) {
    let user = userListName.value.find((el) => {
      return el.userId == Number(userId)
    })
    return user.nickName || 'admin'
  }
  return 'admin'
}

function getUser() {
  getUserProfile().then(response => {
    currentUser.value = response.data.userId
  });
}

function getAccountList() {
  listAccountFinance({pageNum: 1, pageSize: 300}).then(response => {
    accountIds.value = response.rows
  });
}

function matchAccount(accountId) {
  if (accountId) {
    let account = accountIds.value.find((el) => {
      return el.id == accountId
    })
    return account.accounrName
  }
}

getAccountList();
getUser();
getList();
getUserList();
</script>
