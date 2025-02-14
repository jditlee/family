<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="账户名称" prop="accounrName">
        <el-input
            v-model="queryParams.accounrName"
            placeholder="请输入账户名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="账户类型" prop="typeId">
        <el-select clearable v-model="queryParams.typeId" style="width: 200px" placeholder="请选择账户类型">
          <el-option
              v-for="dict in account_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="账户人" prop="userId">
        <el-select clearable v-model="queryParams.userId" style="width: 200px" placeholder="请选择消费人">
          <el-option
              v-for="dict in userListName"
              :key="dict.userId"
              :label="dict.nickName"
              :value="dict.userId"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间" prop="createTime">
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
            v-hasPermi="['money:account_finance:add']"
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
            v-hasPermi="['money:account_finance:edit']"
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
            v-hasPermi="['money:account_finance:remove']"
        >删除
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="account_financeList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="账户名称" align="center" prop="accounrName" :show-overflow-tooltip="true" width="130"/>
      <el-table-column label="账户类型" align="center" prop="typeId" width="100">
        <template #default="scope">
          <dict-tag :options="account_type" :value="scope.row.typeId"/>
        </template>
      </el-table-column>
      <el-table-column label="历史最高资金" align="center" prop="maxBalance" :show-overflow-tooltip="true" width="160"/>
      <el-table-column label="账户本金" align="center" prop="principal" width="130"></el-table-column>
      <el-table-column label="账户人" align="center" prop="userId" width="130">
        <template #default="scope">
          <span>{{ matchUserId(scope.row.userId) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="createTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="更新时间" align="center" prop="updateTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.updateTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="备注" align="center" prop="remark" width="200"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                     v-hasPermi="['money:account_finance:edit']">修改
          </el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                     v-hasPermi="['money:account_finance:remove']">删除
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
      <el-form ref="account_financeRef" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="账户名称" prop="accounrName">
              <el-input v-model="form.accounrName" type="" placeholder="请输入账户名称"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="账户类型" prop="typeId">
              <el-select v-model="form.typeId" placeholder="请选择账户类型">
                <el-option
                    v-for="dict in account_type"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="历史最高资金" label-width="100" prop="maxBalance">
              <el-input-number placeholder="请输入历史最高资金" v-model="form.maxBalance" :precision="2" :step="0.01"
                               controls-position="right"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="账户本金" prop="principal">
              <el-input-number placeholder="请输入账户本金" v-model="form.principal" :precision="2" :step="0.01"
                               controls-position="right"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="账户人" prop="userId">
              <el-select clearable v-model="form.userId" placeholder="请选择账户人">
                <el-option
                    v-for="dict in userListName"
                    :key="dict.userId"
                    :label="dict.nickName"
                    :value="dict.userId"
                ></el-option>
              </el-select>
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

<script setup name="AccountFinance">
import {
  listAccountFinance,
  getAccountFinance,
  delAccountFinance,
  addAccountFinance,
  updateAccountFinance,
} from "@/api/money/account_finance";
import {getUserListName, getUserProfile} from '@/api/system/user'

const {proxy} = getCurrentInstance();
const {
  account_type,
  money_type,
  payment_method
} = proxy.useDict("account_type", "money_type", "payment_method");

const account_financeList = ref([]);
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

const data = reactive({
  form: {},
  queryParams: {
    accounrName: '',
    typeId: '',
    userId: undefined,
    pageNum: 1,
    pageSize: 10,
  },
  rules: {
    detail: [{required: true, message: '账户明细不能为空', trigger: 'blur'}],
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
    //  location: [{ required: true, message: '账户地点不能为空', trigger: 'blur'}],
  },
});

const {queryParams, form, rules} = toRefs(data);

/** 查询账户列表 */
function getList() {
  loading.value = true;
  listAccountFinance(proxy.addDateRange(queryParams.value, dateRange.value)).then(response => {
    account_financeList.value = response.rows;
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
    accounrName: '',
    maxBalance: undefined,
    principal: undefined,
    userId: currentUser.value,
    typeId: '1',
    remark: ''
  };
  proxy.resetForm("account_financeRef");
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
  open.value = true;
  title.value = "新增账户";
}

/**修改按钮操作 */
function handleUpdate(row) {
  reset();
  const account_financeId = row.id || ids.value;
  getAccountFinance(account_financeId).then(response => {
    form.value = response.data;
    form.value.typeId = form.value.typeId.toString()
    open.value = true;
    title.value = "修改账户";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["account_financeRef"].validate(valid => {
    if (valid) {
      if (form.value.id != undefined) {
        updateAccountFinance(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAccountFinance(form.value).then(response => {
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
  const account_financeIds = row.id || ids.value
  proxy.$modal.confirm('是否确认删除公告编号为"' + account_financeIds + '"的数据项？').then(function () {
    return delAccountFinance(account_financeIds);
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

getUser();
getList();
getUserList();
</script>
