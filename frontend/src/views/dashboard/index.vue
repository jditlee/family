<template>
  <div>
    <div class="pageHeaderContent">
      <div class="avatar">
        <a-avatar size="large" :src="userStore.avatar"/>
      </div>
      <div class="content">
        <div class="contentTitle">
          您好，
          {{ state.user.nickName }}
        </div>
        <div>
          <span></span>
          <span v-if="!sentence">加载中...</span>
          <span v-else>{{ sentence }}</span></div>
        <div v-if="state.user.dept">{{ state.user.dept.deptName }} |{{ state.postGroup }}</div>
      </div>
      <div class="extraContent">
        <div class="statItem">
          <a-statistic title="账户数" :value="12"/>
        </div>
        <div class="statItem">
          <a-statistic title="资产积累进度" :value="sum_current" suffix="/ 1000000"/>
        </div>
        <div class="statItem">
          <a-statistic title="进度百分比" :value="sum_current/1000000*100" suffix="%"/>
        </div>
      </div>
    </div>

    <div style="padding: 10px">
      <a-row :gutter="24">
        <a-col :xl="16" :lg="24" :md="24" :sm="24" :xs="24">
          <a-card
              class="projectList"
              :style="{ marginBottom: '24px' }"
              title="通知公告"
              :bordered="false"
              :loading="false"
              :body-style="{ padding: 0 }"
          >
            <template #extra>
              <a href=""> <span style="color: #1890ff">全部》》</span> </a>
            </template>
            <a-card-grid
                v-for="item in projectNotice"
                :key="item.noticeId"
                class="projectGrid"
            >
              <a-card
                  :body-style="{ padding: 0 }"
                  style="box-shadow: none"
                  :bordered="false"
              >
                <a-card-meta class="w-full">
                  <template #description>
                    <div v-html="item.noticeContent" class="p-notice"></div>
                  </template>
                  <template #title>
                    <div class="cardTitle">
                      <!--                      <a-avatar size="small" :src="item.logo" />-->
                      <a :href="item.href">
                        {{ item.noticeTitle }}
                      </a>
                    </div>
                  </template>
                </a-card-meta>
                <div class="projectItemContent">
                  <a :href="item.memberLink">
                    {{ item.createBy || "" }}
                  </a>
                  <span class="datetime" ml-2 :title="item.createTime">
                    {{ item.createTime }}
                  </span>
                </div>
              </a-card>
            </a-card-grid>
          </a-card>
          <a-card
              :body-style="{ padding: 0 }"
              :bordered="false"
              class="activeCard"
              title="动态"
              :loading="false"
          >
            <a-list :data-source="activities" class="activitiesList">
              <template #renderItem="{ item }">
                <a-list-item :key="item.operId">
                  <a-list-item-meta>
                    <template #title>
                      <span>
                        <a class="username">{{ item.operName }}</a>&nbsp;
                        <span class="event">
                          <span>在</span>&nbsp;
                          <a href="" style="color: #1890ff">
                            {{
                              item.title
                            }} </a>&nbsp; 中进行了<span>{{ operTypeMap[item.operatorType] || item.operatorType }}</span>&nbsp;操作
                        </span>
                      </span>
                    </template>
                    <!--                    <template #avatar>-->
                    <!--                      <a-avatar :src="item.user.avatar" />-->
                    <!--                    </template>-->
                    <template #description>
                      <span class="datetime" :title="item.operTime">
                        {{ item.updatedAt }}
                      </span>
                    </template>
                  </a-list-item-meta>
                </a-list-item>
              </template>
            </a-list>
          </a-card>
        </a-col>
        <a-col :xl="8" :lg="24" :md="24" :sm="24" :xs="24">
          <a-card
              :style="{ marginBottom: '24px' }"
              title="快速开始 / 便捷导航"
              :bordered="false"
              :body-style="{ padding: 0 }"
          >
            <EditableLinkGroup/>
          </a-card>
          <a-card
              :style="{ marginBottom: '24px' }"
              :bordered="false"
              title="XX 指数"
          >
            <div class="chart">
              <div ref="radarContainer"/>
            </div>
          </a-card>
          <a-card
              :body-style="{ paddingTop: '12px', paddingBottom: '12px' }"
              :bordered="false"
              title="团队"
          >
            <div class="members">
              <a-row :gutter="48">
                <a-col
                    v-for="item in projectNotice"
                    :key="`members-item-${item.id}`"
                    :span="12"
                >
                  <a :href="item.href">
                    <a-avatar :src="item.logo" size="small"/>
                    <span class="member">{{ item.member }}</span>
                  </a>
                </a-col>
              </a-row>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script>
import {
  Statistic,
  Row,
  Col,
  Card,
  CardGrid,
  CardMeta,
  List,
  ListItem,
  ListItemMeta,
  Avatar,
} from "ant-design-vue";
import 'ant-design-vue/dist/reset.css';

export default {
  components: {
    AStatistic: Statistic,
    ARow: Row,
    ACol: Col,
    ACard: Card,
    ACardGrid: CardGrid,
    ACardMeta: CardMeta,
    AList: List,
    AListItem: ListItem,
    AListItemMeta: ListItemMeta,
    AAvatar: Avatar,
  },
};
</script>


<script setup>
import {Radar} from "@antv/g2plot";
import EditableLinkGroup from "./editable-link-group.vue";
import {getUserListName, getUserProfile} from "@/api/system/user.js";
import {listNotice} from "@/api/system/notice";
import {onMounted, ref} from 'vue';
import axios from "axios";
import {list} from "@/api/monitor/operlog";
import {sumTransactions} from "@/api/money/account_transactions.js";
import useUserStore from "@/store/modules/user.js";

const {proxy} = getCurrentInstance();
const {sys_oper_type, sys_common_status} = proxy.useDict("sys_oper_type", "sys_common_status");

// 添加句子响应式变量
const userStore = useUserStore()
const sentence = ref('');
const operTypeMap = computed(() =>
    sys_oper_type.value.reduce((acc, curr) => {
      acc[curr.value] = curr.label;
      return acc;
    }, {})
);
// 获取句子方法
const fetchSentence = async () => {
  try {
    const response = await axios.get('https://v1.hitokoto.cn/?encode=text');
    sentence.value = response.data;
  } catch (error) {
    console.error('请求句子失败', error);
    sentence.value = '祝你开心每一天！'; // 失败时使用默认值
  }
};

defineOptions({
  name: "DashBoard",
});
const state = reactive({
  user: {},
  roleGroup: {},
  postGroup: {}
});

const currentUser = {
  avatar: "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
  name: state.user.userName,
  userid: state.user.id,
  email: "antdesign@alipay.com",
  signature: "海纳百川，有容乃大",
  title: "交互专家",
  group: "蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED",
};

const projectNotice = ref([]);
//     [
//   {
//     id: "xxx1",
//     title: "Alipay",
//     logo: "https://gw.alipayobjects.com/zos/rmsportal/WdGqmHpayyMjiEhcKoVE.png",
//     description: "那是一种内在的东西，他们到达不了，也无法触及的",
//     updatedAt: "几秒前",
//     member: "科学搬砖组",
//     href: "",
//     memberLink: "",
//   },
// ];

const activities = ref([]);
//     [
//   {
//     id: "trend-1",
//     updatedAt: "几秒前",
//     user: {
//       name: "曲丽丽",
//       avatar:
//         "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
//     },
//     group: {
//       name: "高逼格设计天团",
//       link: "http://github.com/",
//     },
//     project: {
//       name: "六月迭代",
//       link: "http://github.com/",
//     },
//     template1: "在",
//     template2: "新建项目",
//   },
// ];

const sum_current = ref();

const radarContainer = ref();
const radarData = [
  {
    name: "个人",
    label: "引用",
    value: 10,
  },
  {
    name: "个人",
    label: "口碑",
    value: 8,
  },
  {
    name: "个人",
    label: "产量",
    value: 4,
  },
  {
    name: "个人",
    label: "贡献",
    value: 5,
  },
  {
    name: "个人",
    label: "热度",
    value: 7,
  },
  {
    name: "团队",
    label: "引用",
    value: 3,
  },
  {
    name: "团队",
    label: "口碑",
    value: 9,
  },
  {
    name: "团队",
    label: "产量",
    value: 6,
  },
  {
    name: "团队",
    label: "贡献",
    value: 3,
  },
  {
    name: "团队",
    label: "热度",
    value: 1,
  },
  {
    name: "部门",
    label: "引用",
    value: 4,
  },
  {
    name: "部门",
    label: "口碑",
    value: 1,
  },
  {
    name: "部门",
    label: "产量",
    value: 6,
  },
  {
    name: "部门",
    label: "贡献",
    value: 5,
  },
  {
    name: "部门",
    label: "热度",
    value: 7,
  },
];
let radar;
onMounted(() => {
  fetchSentence();
  radar = new Radar(radarContainer.value, {
    data: radarData,
    xField: "label",
    yField: "value",
    seriesField: "name",
    point: {
      size: 4,
    },
    legend: {
      layout: "horizontal",
      position: "bottom",
    },
  });
  radar.render();
});

onBeforeUnmount(() => {
  radar?.destroy?.();
});

//获取通知列表
function getNoticeList() {
  listNotice({pageNum: 1, pageSize: 6}).then(response => {
    projectNotice.value = response.rows;
  })
}

getNoticeList()

// 获取当前用户信息
function getUser() {
  getUserProfile().then(response => {
    state.user = response.data;
    state.roleGroup = response.roleGroup;
    state.postGroup = response.postGroup;
  });
};

getUser();

//获取通知列表
function getLogList() {
  list({pageNum: 1, pageSize: 10}).then(response => {
    activities.value = response.rows;
  })
}

getLogList()

//获取通知列表
function getSumTransactions() {
  sumTransactions().then(response => {
    sum_current.value = response.data;
  })
}

getSumTransactions()


</script>

<style scoped lang="less">
.textOverflow() {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  word-break: break-all;
}

// mixins for clearfix
// ------------------------
.clearfix() {
  zoom: 1;
  &::before,
  &::after {
    display: table;
    content: " ";
  }
  &::after {
    clear: both;
    height: 0;
    font-size: 0;
    visibility: hidden;
  }
}

.activitiesList {
  padding: 0 24px 8px 24px;

  .username {
    color: rgba(0, 0, 0, 0.65);
  }

  .event {
    font-weight: normal;
  }
}

.pageHeaderContent {
  display: flex;
  padding: 12px;
  margin-bottom: 24px;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;

  .avatar {
    flex: 0 1 72px;

    & > span {
      display: block;
      width: 72px;
      height: 72px;
      border-radius: 72px;
    }
  }

  .content {
    position: relative;
    top: 4px;
    flex: 1 1 auto;
    margin-left: 24px;
    color: rgba(0, 0, 0, 0.45);
    line-height: 22px;

    .contentTitle {
      margin-bottom: 12px;
      color: rgba(0, 0, 0, 0.85);
      font-weight: 500;
      font-size: 20px;
      line-height: 28px;
    }
  }
}

.extraContent {
  .clearfix();

  float: right;
  white-space: nowrap;

  .statItem {
    position: relative;
    display: inline-block;
    padding: 0 32px;

    > p:first-child {
      margin-bottom: 4px;
      color: rgba(0, 0, 0, 0.45);
      font-size: 14px;
      line-height: 22px;
    }

    > p {
      margin: 0;
      color: rgba(0, 0, 0, 0.85);
      font-size: 30px;
      line-height: 38px;

      > span {
        color: rgba(0, 0, 0, 0.45);
        font-size: 20px;
      }
    }

    &::after {
      position: absolute;
      top: 8px;
      right: 0;
      width: 1px;
      height: 40px;
      background-color: #e8e8e8;
      content: "";
    }

    &:last-child {
      padding-right: 0;

      &::after {
        display: none;
      }
    }
  }
}

.members {
  a {
    display: block;
    height: 24px;
    margin: 12px 0;
    color: rgba(0, 0, 0, 0.65);
    transition: all 0.3s;
    .textOverflow();

    .member {
      margin-left: 12px;
      font-size: 14px;
      line-height: 24px;
      vertical-align: top;
    }

    &:hover {
      color: #1890ff;
    }
  }
}

.projectList {
  :deep(.ant-card-meta-description) {
    height: 100px;
    overflow: hidden;
    color: rgba(0, 0, 0, 0.45);
    line-height: 12px;
  }

  .cardTitle {
    font-size: 0;

    a {
      display: inline-block;
      height: 26px;
      margin-left: 12px;
      color: rgba(0, 0, 0, 0.85);
      font-size: 16px;
      line-height: 24px;
      vertical-align: top;

      &:hover {
        color: #1890ff;
      }
    }
  }

  .projectGrid {
    width: 33.33%;
  }

  .projectItemContent {
    display: flex;
    flex-basis: 100%;
    height: 20px;
    margin-top: 8px;
    overflow: hidden;
    font-size: 12px;
    line-height: 20px;
    .textOverflow();

    a {
      display: inline-block;
      flex: 1 1 0;
      color: rgba(0, 0, 0, 0.45);
      .textOverflow();

      &:hover {
        color: #1890ff;
      }
    }

    .datetime {
      flex: 0 0 auto;
      float: right;
      color: rgba(0, 0, 0, 0.25);
    }
  }
}

.datetime {
  color: rgba(0, 0, 0, 0.25);
}

@media screen and (max-width: 1200px) and (min-width: 992px) {
  .activeCard {
    margin-bottom: 24px;
  }

  .members {
    margin-bottom: 0;
  }

  .extraContent {
    margin-left: -44px;

    .statItem {
      padding: 0 16px;
    }
  }
}

@media screen and (max-width: 992px) {
  .activeCard {
    margin-bottom: 24px;
  }

  .members {
    margin-bottom: 0;
  }

  .extraContent {
    float: none;
    margin-right: 0;

    .statItem {
      padding: 0 16px;
      text-align: left;

      &::after {
        display: none;
      }
    }
  }
}

@media screen and (max-width: 768px) {
  .extraContent {
    margin-left: -16px;
  }

  .projectList {
    .projectGrid {
      width: 50%;
    }
  }
}

@media screen and (max-width: 576px) {
  .pageHeaderContent {
    display: block;

    .content {
      margin-left: 0;
    }
  }

  .extraContent {
    .statItem {
      float: none;
    }
  }
}

@media screen and (max-width: 480px) {
  .projectList {
    .projectGrid {
      width: 100%;
    }
  }
}

//.p-notice {
//  //p {
//    display: inline-block;
//    white-space: nowrap;
//    margin: 0;
//    padding: 0;
//  font-size: inherit;     /* 继承父级字体大小 */
//  font-weight: normal;    /* 清除默认粗体效果 */
//  line-height: normal;    /* 重置行高 */
//  color: inherit;         /* 继承父级字体颜色 */
//  /* 可选：溢出处理 */
//  overflow: hidden;
//  text-overflow: ellipsis; /* 文字溢出显示省略号 */
//  max-width: 200px;
//  //}
//}
</style>