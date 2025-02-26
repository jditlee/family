<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="账户" prop="accountId">
        <el-select clearable v-model="queryParams.accountId" style="width: 200px" placeholder="请选择账户">
          <el-option
              v-for="dict in accountIds"
              :key="dict.id"
              :label="dict.accounrName"
              :value="dict.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间" prop="createBy">
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
            v-hasPermi="['money:account_transactions:add']"
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
            v-hasPermi="['money:account_transactions:edit']"
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
            v-hasPermi="['money:account_transactions:remove']"
        >删除
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="account_transactionsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="账户" align="center" prop="accounrId" width="130">
        <template #default="scope">
          <span>{{ matchAccount(scope.row.accountId) }} </span>
        </template>
      </el-table-column>
      <el-table-column :style="'background: yellow'" label="当前余额" align="center" prop="currentBalance" width="100"/>
      <el-table-column label="本金差" align="center" prop="diffOri" width="100">
        <template #default="scope">
          <span :style="getCellStyle(scope.row.diffOri)">{{ scope.row.diffOri }} </span>
        </template>
      </el-table-column>
      <el-table-column label="本金差百分比" align="center" prop="raiseOri" width="100">
        <template #default="scope">
          <span :style="getCellStyle(scope.row.raiseOri)">{{ scope.row.raiseOri }} </span>
        </template>
      </el-table-column>
      <el-table-column label="上期差" align="center" prop="diffPre" width="100">
        <template #default="scope">
          <span :style="getCellStyle(scope.row.diffPre)">{{ scope.row.diffPre }} </span>
        </template>
      </el-table-column>
      <el-table-column label="上期差百分比" align="center" prop="raisePre" width="100">
        <template #default="scope">
          <span :style="getCellStyle(scope.row.raisePre)">{{ scope.row.raisePre }} </span>
        </template>
      </el-table-column>
      <el-table-column label="上年最高差" align="center" prop="diffMax" width="100">
        <template #default="scope">
          <span :style="getCellStyle(scope.row.diffMax)">{{ scope.row.diffMax }} </span>
        </template>
      </el-table-column>
      <el-table-column label="上年最高差百分比" align="center" prop="raiseMax" width="100">
        <template #default="scope">
          <span :style="getCellStyle(scope.row.raiseMax)">{{ scope.row.raiseMax }} </span>
        </template>
      </el-table-column>
      <el-table-column label="本金" align="center" prop="principal" width="100"/>
      <el-table-column label="上年度最高余额" align="center" prop="maxBalance" width="100"/>

      <el-table-column label="创建时间" align="center" prop="createTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>

<!--      <el-table-column label="备注" align="center" prop="remark" width="200"/>-->
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                     v-hasPermi="['money:account_transactions:edit']">修改
          </el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                     v-hasPermi="['money:account_transactions:remove']">删除
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
    <el-dialog :title="title" v-model="open" width="850px" append-to-body>
      <el-form ref="account_transactionsRef" :model="form" :rules="rules" label-width="80px">
        <div v-for="(item, index) in form.items" :key="index">
          <el-row :gutter="24" class="mb-8">
            <el-col :span="7">
              <el-form-item
                :label="'账户ID'"
                :prop="'items.' + index + '.accountId'"
                :rules="rules.accountId"
                label-width="80"
              >
                <el-select v-model="item.accountId" placeholder="请选择账户ID" style="width: 100%">
                  <el-option
                    v-for="dict in accountIds"
                    :key="dict.id"
                    :label="dict.accounrName"
                    :value="dict.id"
                  ></el-option>
                </el-select>
              </el-form-item>
              
            </el-col>
            <el-col :span="7">
              <el-form-item
                :label="'当前余额'"
                :prop="'items.' + index + '.currentBalance'"
                :rules="rules.currentBalance"
                label-width="80"
              >
                <el-input-number
                  v-model="item.currentBalance"
                  placeholder="请输入账户当前余额"
                  :precision="2"
                  :step="0.01"
                  controls-position="right"
                  style="width: 100%"
                ></el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="7">
              <el-form-item
                :label="'备注'"
                :prop="'items.' + index + '.remark'"
                label-width="80"
              >
                <el-input v-model="item.remark" placeholder="请输入备注"/>
              </el-form-item>
            </el-col>
            <el-col :span="3" class="pt-4">
              <el-button
                v-if="form.items.length > 1 || index > 0"
                @click="removeRow(index)"
                icon="Delete"
                link
                type="danger"
              />
            </el-col>
          </el-row>
          <el-divider v-if="index < form.items.length - 1"/>
        </div>

        <div class="text-center mt-16" v-show="mode === 'add'">
          <el-button
            type="primary"
            icon="Plus"
            @click="addRow"
            link
          >新增一行</el-button>
        </div>
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

<script setup name="AccountTransactions">
import {
  listAccountTransactions,
  getAccountTransactions,
  delAccountTransactions,
  addAccountTransactions,
  updateAccountTransactions,
} from "@/api/money/account_transactions";
import {getUserListName, getUserProfile} from '@/api/system/user'
import {listAccountFinance} from '@/api/money/account_finance'
import { onMounted } from "vue";
import { getCellStyle } from '@/utils/ruoyi'

const {proxy} = getCurrentInstance();
const {
  money_type,
  payment_method
} = proxy.useDict("money_type", "payment_method");

const account_transactionsList = ref([]);
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

const mode = ref('add') // 添加模式状态

const data = reactive({
  form: {
    items: [] // 修改为数组结构存储多行数据
  },
  queryParams: {
    accountId: '',
    pageNum: 1,
    pageSize: 10,
  },
  rules: {
    accountId: [
      { required: true, message: '请选择账户', trigger: 'blur' }
    ],
    currentBalance: [
      { required: true, message: '收入金额不能为空' },
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
    ]
  },
});

const {queryParams, form, rules} = toRefs(data);

/** 查询消费列表 */
function getList() {
  loading.value = true;
  listAccountTransactions(proxy.addDateRange(queryParams.value, dateRange.value)).then(response => {
    account_transactionsList.value = response.rows;
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
// 表单重置
function reset() {
  form.value.items = [{
    accountId: '',
    currentBalance: '',
    remark: ''
  }];
  proxy.resetForm("account_transactionsRef");
}

// 新增行
function addRow() {
  form.value.items.push({
    accountId: '',
    currentBalance: '',
    remark: ''
  });
}

// 删除行
function removeRow(index) {
  form.value.items.splice(index, 1);
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
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
  mode.value = 'add'
  open.value = true;
  title.value = "新增消费";
}

/**修改按钮操作 */

// 修改按钮操作
function handleUpdate(row) {
  mode.value = 'edit'
  reset();
  const account_transactionsId = row.id || ids.value;
  getAccountTransactions(account_transactionsId).then(response => {
    form.value.items = [response.data]; // 修改为数组形式
    open.value = true;
    title.value = "修改流水";
  });
}

/** 提交按钮 */

// 提交按钮
async function submitForm() {
  proxy.$refs["account_transactionsRef"].validate(async valid => {
    if (valid) {
      try {
        if (mode.value === 'edit') {
          await updateAccountTransactions(form.value.items[0]);
          proxy.$modal.msgSuccess("修改成功");
        } else {
          for (const item of form.value.items) {
            await addAccountTransactions(item);
          }
          proxy.$modal.msgSuccess(`成功添加${form.value.items.length}条记录`);
        }
        open.value = false;
        getList();
      } catch (err) {
        proxy.$modal.msgError(err.message || '操作失败');
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const account_transactionsIds = row.id || ids.value
  proxy.$modal.confirm('是否确认删除公告编号为"' + account_transactionsIds + '"的数据项？').then(function () {
    return delAccountTransactions(account_transactionsIds);
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

/** 获取账户列表 */
function getAccountList() {
  listAccountFinance({pageNum: 1, pageSize: 300}).then(response => {
    accountIds.value = response.rows
  });
}

function matchAccount(accountId) {
  console.log(accountId)
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
<style scoped>
.mt-16 {
  margin-top: 16px;
}
.pt-4 {
  padding-top: 4px;
}
/* ::v-deep .el-table .el-table__cell {
  padding: 0
} */
</style>