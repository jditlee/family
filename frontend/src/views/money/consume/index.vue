<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="消费账户" prop="accId">
        <el-select clearable v-model="queryParams.accId" style="width: 200px" placeholder="请选择账户">
          <el-option
              v-for="dict in accountIds"
              :key="dict.id"
              :label="dict.accounrName"
              :value="dict.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="消费场景" prop="scene">
        <el-select clearable v-model="queryParams.scene" style="width: 200px" placeholder="请选择消费类型">
          <el-option
              v-for="dict in consume_scene"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="消费类型" prop="typeId">
        <el-select clearable v-model="queryParams.typeId" style="width: 200px" placeholder="请选择消费类型">
          <el-option
              v-for="dict in consume_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="消费人" prop="userId">
        <el-select clearable v-model="queryParams.userId" style="width: 200px" placeholder="请选择消费人">
          <el-option
              v-for="dict in userListName"
              :key="dict.userId"
              :label="dict.nickName"
              :value="dict.userId"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="消费状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择消费状态" clearable style="width: 200px">
          <el-option
              v-for="dict in consume_status"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="消费明细" prop="detail">
        <el-input
            v-model="queryParams.detail"
            placeholder="请输入消费明细"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>

      <el-form-item label="消费地点" prop="location">
        <el-input
            v-model="queryParams.location"
            placeholder="请输入地点"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>

      <el-form-item label="消费时间" prop="consumeTime">
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
            v-hasPermi="['money:consume:add']"
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
            v-hasPermi="['money:consume:edit']"
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
            v-hasPermi="['money:consume:remove']"
        >删除
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="consumeList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="账户" align="center" prop="accId" width="130">
        <template #default="scope">
          <span>{{ matchAccount(scope.row.accId) }} </span>
        </template>
      </el-table-column>
      <el-table-column label="消费场景" align="center" prop="scene" width="130">
        <template #default="scope">
          <dict-tag :options="consume_scene" :value="scope.row.scene"/>
        </template>
      </el-table-column>
      <el-table-column label="消费类型" align="center" prop="typeId" width="100">
        <template #default="scope">
          <dict-tag :options="consume_type" :value="scope.row.typeId"/>
        </template>
      </el-table-column>
      <el-table-column label="消费明细" align="center" prop="detail" :show-overflow-tooltip="true" width="130"/>
      <el-table-column label="消费金额" align="center" prop="amount" width="130">
      </el-table-column>

      <el-table-column label="消费时间" align="center" prop="consumeTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.consumeTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="消费地点" align="center" prop="location" width="130"/>
      <el-table-column label="消费人" align="center" prop="userId" width="130">
        <template #default="scope">
          <span>{{ matchUserId(scope.row.userId) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="支付方式" align="center" prop="paymentId" width="130">
        <template #default="scope">
          <dict-tag :options="payment_method" :value="scope.row.paymentId"/>
        </template>
      </el-table-column>
      <el-table-column label="消费状态" align="center" prop="status" width="130">
        <template #default="scope">
          <dict-tag :options="consume_status" :value="scope.row.status"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                     v-hasPermi="['money:consume:edit']">修改
          </el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                     v-hasPermi="['money:consume:remove']">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
        v-show="total > 0"
        :total="total"
        :page="queryParams.pageNum"
        :limit="queryParams.pageSize"
        @pagination="getList"
    />

    <!-- 添加或修改公告对话框 -->
    <el-dialog :title="title" v-model="open" width="780px" append-to-body>
      <el-form ref="consumeRef" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="20">
            <el-form-item label="入账账户" labelWidth="120" prop="accId">
              <el-select v-model="form.accId" placeholder="请选择账户ID">
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
            <el-form-item label="消费时间" prop="consumeTime">
              <el-date-picker v-model="form.consumeTime" align="right" type="date"
                              placeholder="请选择日期"></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="消费地点" prop="location">
              <el-input v-model="form.location" type="" placeholder="请输入消费地点"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="消费场景" prop="scene">
              <el-select v-model="form.scene     " placeholder="请选择消费场景">
                <el-option
                    v-for="dict in consume_scene"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="消费类型" prop="typeId">
              <el-select v-model="form.typeId" placeholder="请选择消费类型">
                <el-option
                    v-for="dict in consume_type"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="消费明细" prop="detail">
              <el-input v-model="form.detail" placeholder="请输入消费明细"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="消费金额" prop="amount">
              <el-input-number placeholder="请输入消费金额" v-model="form.amount" :precision="2" :step="0.01"
                               controls-position="right"></el-input-number>
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
            <el-form-item label="支付方式" prop="paymentId">
              <el-select v-model="form.paymentId" placeholder="请选择货币支付方式">
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
            <el-form-item label="支付状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择支付状态">
                <el-option
                    v-for="dict in consume_status"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="消费人" prop="userId">
              <el-select clearable v-model="form.userId" placeholder="请选择入账人">
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
            <el-form-item label="消费类别" prop="category">
              <el-input v-model="form.category" placeholder="请输入消费类别"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="记录标签" prop="tags">
              <el-input v-model="form.tags" type="" placeholder="请输入消费标签，逗号分开"/>
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

<script setup name="Consume">
import {listConsume, getConsume, delConsume, addConsume, updateConsume,} from "@/api/money/consume";
import {getUserListName, getUserProfile} from '@/api/system/user'
import {listAccountFinance} from "@/api/money/account_finance.js";

const {proxy} = getCurrentInstance();
const {
  consume_scene,
  consume_type,
  consume_status,
  money_type,
  payment_method
} = proxy.useDict("consume_scene", "consume_type", "consume_status", "money_type", "payment_method");

const consumeList = ref([]);
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

const data = reactive({
  form: {},
  queryParams: {
    typeId: '',
    detail: '',
    currency: '',
    category: '',
    scene: '',
    paymentId: '',
    accId: undefined,
    userId: undefined,
    location: undefined,
    tags: undefined,
    status: undefined,
    consumeTime: undefined,
    pageSize: 10,
  },
  rules: {
    detail: [{required: true, message: '消费明细不能为空', trigger: 'blur'}],
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
    ]
  },
});

const {queryParams, form, rules} = toRefs(data);

/** 查询消费列表 */
function getList() {
  loading.value = true;
  listConsume(proxy.addDateRange(queryParams.value, dateRange.value)).then(response => {
    consumeList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 查询用户列表 */
function getUserList() {
  getUserListName({pageNum: 1, pageSize: 30}).then(response => {
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
    typeId: '1',
    detail: '',
    amount: 0,
    currency: '1',
    category: '',
    paymentId: '1',
    status: '1',
    location: '',
    tags: '',
    accId: '',
    userId: currentUser.value,
    consumeTime: new Date(),
    scene: '2',
    remark: ''
  };
  proxy.resetForm("consumeRef");
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
  title.value = "新增消费";
}

/**修改按钮操作 */
function handleUpdate(row) {
  reset();
  const consumeId = row.id || ids.value;
  getConsume(consumeId).then(response => {
    form.value = response.data;
    form.value.typeId = form.value.typeId.toString()
    form.value.currency = form.value.currency.toString()
    form.value.paymentId = form.value.paymentId.toString()
    form.value.scene = form.value.scene.toString()
    form.value.userId = parseInt(form.value.userId)
    open.value = true;
    title.value = "修改消费";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["consumeRef"].validate(valid => {
    if (valid) {
      if (form.value.id != undefined) {
        updateConsume(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addConsume(form.value).then(response => {
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
  const consumeIds = row.id || ids.value
  proxy.$modal.confirm('是否确认删除公告编号为"' + consumeIds + '"的数据项？').then(function () {
    return delConsume(consumeIds);
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
  listAccountFinance().then(response => {
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
