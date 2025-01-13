from sqlalchemy.ext.asyncio import AsyncSession
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.consume_dao import ConsumeDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.consume_vo import DeleteConsumeModel, ConsumeModel, ConsumePageQueryModel
from utils.common_util import SqlalchemyUtil


class ConsumeService:
    """
    开支记录管理模块服务层
    """

    @classmethod
    async def get_consume_list_services(
            cls, query_db: AsyncSession, query_object: ConsumePageQueryModel, is_page: bool = True
    ):
        """
        获取开支记录列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 开支记录列表信息对象
        """
        consume_list_result = await ConsumeDao.get_consume_list(query_db, query_object, is_page)

        return consume_list_result

    @classmethod
    async def add_consume_services(cls, query_db: AsyncSession, page_object: ConsumeModel):
        """
        新增通开支记录信息service

        :param query_db: orm对象
        :param page_object: 新增开支记录对象
        :return: 新增开支记录校验结果
        """
        try:
            await ConsumeDao.add_consume_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_consume_services(cls, query_db: AsyncSession, page_object: ConsumeModel):
        """
        编辑开支记录信息service

        :param query_db: orm对象
        :param page_object: 编辑开支记录对象
        :return: 编辑开支记录校验结果
        """
        edit_consume = page_object.model_dump(exclude_unset=True)
        consume_info = await cls.consume_detail_services(query_db, page_object.id)
        if consume_info.id:
            try:
                await ConsumeDao.edit_consume_dao(query_db, edit_consume)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='开支记录不存在')

    @classmethod
    async def delete_consume_services(cls, query_db: AsyncSession, page_object: DeleteConsumeModel):
        """
        删除开支记录信息service

        :param query_db: orm对象
        :param page_object: 删除开支记录对象
        :return: 删除开支记录校验结果
        """
        if page_object.ids:
            consume_id_list = page_object.ids.split(',')
            try:
                for consume_id in consume_id_list:
                    await ConsumeDao.delete_consume_dao(query_db, ConsumeModel(id=consume_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入开支记录id为空')

    @classmethod
    async def consume_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取开支记录详细信息service

        :param query_db: orm对象
        :param id: 开支记录id
        :return: 开支记录id对应的信息
        """
        consume = await ConsumeDao.get_consume_detail_by_id(query_db, id=id)
        if consume:
            result = ConsumeModel(**SqlalchemyUtil.serialize_result(consume))
        else:
            result = ConsumeModel(**dict())

        return result
