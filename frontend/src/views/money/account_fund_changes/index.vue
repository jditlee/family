<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="入账账户id" prop="inAccountId">
        <el-select clearable v-model="queryParams.inAccountId" style="width: 200px" placeholder="请选择入账账户">
          <el-option
              v-for="dict in accountIds"
              :key="dict.id"
              :label="dict.accounrName"
              :value="dict.id"
          ></el-option>
        </el-select>
        

      </el-form-item>
      <el-form-item label="出账账户id" prop="outAccountId">
          <el-select clearable v-model="queryParams.outAccountId" style="width: 200px" placeholder="请选择出账账户">
          <el-option
              v-for="dict in accountIds"
              :key="dict.id"
              :label="dict.accounrName"
              :value="dict.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="交易类型" prop="transactionTypeId">
        <el-select v-model="queryParams.transactionTypeId" placeholder="交易类型" clearable style="width: 200px">
          <el-option
              v-for="dict in transaction_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="记录时间" prop="createTime">
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
            v-hasPermi="['money:account_fund_changes:add']"
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
            v-hasPermi="['money:account_fund_changes:edit']"
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
            v-hasPermi="['money:account_fund_changes:remove']"
        >删除
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>
    <!--      列表展示-->
    <el-table v-loading="loading" :data="accountFundChangesList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      
      <el-table-column label="序号" align="center" prop="id" width="100"/>
      <el-table-column label="入账账户" align="center" prop="inAccountId" width="130">
        <template #default="scope">
          <span>{{ matchAccount(scope.row.inAccountId) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="出账账户" align="center" prop="outAccountId" width="130">
        <template #default="scope">
          <span>{{ matchAccount(scope.row.outAccountId) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="交易类型" align="center" prop="transactionTypeId" width="100">
        <template #default="scope">
          <dict-tag :options="transaction_type" :value="scope.row.transactionTypeId"/>
        </template>
      </el-table-column>
      <el-table-column label="交易金额" align="center" prop="amount" width="130">
      </el-table-column>
      <el-table-column label="账户余额" align="center" prop="balanceAfter" width="130">
      </el-table-column>
      <el-table-column label="记录人" align="center" prop="createBy" width="130">
        <template #default="scope">
          <span>{{ matchUserId(scope.row.createBy) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="记录时间" align="center" prop="createTime" width="100">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="备注" align="center" prop="remark" width="200"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                     v-hasPermi="['money:account_fund_changes:edit']">修改
          </el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                     v-hasPermi="['money:account_fund_changes:remove']">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
        v-show="total > 0"
        :total="total"
        v-model:page="queryParams.pageNum"
        v-model:limit="queryParams.pageSize"
        @pagination="getList"
    />

    <!-- 添加或修改公告对话框 -->
    <el-dialog :title="title" v-model="open" width="780px" append-to-body>
      <el-form ref="accountFundChangesRef" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="入账账户" prop="inAccountId">
              <el-select v-model="form.inAccountId" placeholder="请选择入账账户">
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
            <el-form-item label="出账账户" prop="outAccountId">
              <el-select clearable v-model="form.outAccountId"  placeholder="请选择出账账户">
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
            <el-form-item label="交易类型" prop="transactionTypeId">
              <el-select v-model="form.transactionTypeId" placeholder="请选择">
                <el-option
                    v-for="dict in transaction_type"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="交易金额" prop="amount">
              <el-input-number placeholder="请输入交易金额" v-model="form.amount" :precision="2" :step="0.01"
                               controls-position="right" ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="账户余额" prop="balanceAfter">
              <el-input-number placeholder="请输入账户余额" v-model="form.balanceAfter" :precision="2" :step="0.01"
                               controls-position="right" ></el-input-number>
            </el-form-item>
          </el-col>
           <el-col :span="24">
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

<script setup name="Account_fund_changes">
import {
  listAccountFundChanges,
  getAccountFundChanges,
  delAccountFundChanges,
  addAccountFundChanges,
  updateAccountFundChanges
} from "@/api/money/account_fund_changes";
import { listAccountFinance} from "@/api/money/account_finance";
import {getUserListName} from "@/api/system/user.js";

const {proxy} = getCurrentInstance();
const {transaction_type,} = proxy.useDict("transaction_type",);
const userListName = ref([])
const accountIds = ref([])

const accountFundChangesList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const dateRange = ref([]);

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    inAccountId: undefined,
    outAccountId: undefined,
    transactionTypeId: undefined
  },
  // rules: {
  //   noticeTitle: [{ required: true, message: "公告标题不能为空", trigger: "blur" }],
  //   noticeType: [{ required: true, message: "公告类型不能为空", trigger: "change" }]
  // },
});

const {queryParams, form, rules} = toRefs(data);

/** 查询公告列表 */
function getList() {
  loading.value = true;
  listAccountFundChanges(queryParams.value, dateRange.value).then(response => {
    accountFundChangesList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
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
    inAccountId: undefined,
    outAccountId: undefined,
    transactionTypeId: undefined,
    amount: 0,
    balanceAfter: 0,
    remark: undefined,
  };
  proxy.resetForm("accountFundChangesRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
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
  title.value = "添加交易记录";
}

/**修改按钮操作 */
function handleUpdate(row) {
  reset();
  const accountFundChangesId = row.id || ids.value;
  getAccountFundChanges(accountFundChangesId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改交易记录";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["accountFundChangesRef"].validate(valid => {
    if (valid) {
      if (form.value.id != undefined) {
        updateAccountFundChanges(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAccountFundChanges(form.value).then(response => {
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
  const accountFundChangesId = row.id || ids.value
  proxy.$modal.confirm('是否确认删除id为"' + accountFundChangesId + '"的数据项？').then(function () {
    return delAccountFundChanges(accountFundChangesId);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {
  });
}
function getUserList() {
  getUserListName({pageNum: 1, pageSize: 30}).then(response => {
    userListName.value = response.rows;
  })
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

/** 匹配账户 */
function getAccountList() {
  listAccountFinance({pageNum: 1, pageSize: 30}).then(response => {
    accountIds.value = response.rows;
  })
}

function matchAccount(accountId) {
  if(accountId) {
    let account = []
     account = accountIds.value.find((el) => {
      return el.id == accountId
    })
    return account.length == 0 ? accountId : account.accounrName
  }
}

getAccountList()
getList();
getUserList();

</script>
