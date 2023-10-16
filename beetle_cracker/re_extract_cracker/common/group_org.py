#!/usr/bin/env python
# -*- coding: utf-8 -*-



def across_exam(target_list, exam_list):
    """
    Compare 2 lists and REMOVE the duplicate item from exam_list
    Usually daili list is the target list, zhaobiao list is the exam list
    """
    new_exam_value = exam_list.copy()
    for target_item in target_list:
        target_value = target_item.get('value', '')
        for index, exam_item in enumerate(exam_list):
            exam_value = exam_item.get('value', '')
            if target_value == exam_value:
                new_exam_value.pop(index)
    return new_exam_value


def group_by_org(name_list, contact_name_list, contact_phone_list, _type):
    """
                数据结构
                [
                    {
                        "name":"xxx",
                        "contact":[
                                {"contact_phone":"xxx","contact_name":"xxx"}
                            ]
                    }
                ]
                """
    res = []
    max_contact_name_phone_distance = 100
    max_name_phone_distance = 250
    distance = 10000000
    # 舍弃 代理主体后有多个联系方式 的数据
    if _type == 'daili' and len(name_list) == 1:
        ent_index_ls = name_list[0].get("indexs", [])
        if ent_index_ls:
            ent_index_last = ent_index_ls[-1]
            count_ent_contact = 0
            for contact_phone_item in contact_phone_list:
                if not contact_phone_item.get("value", ""):
                    continue
                for contact_phone_index in contact_phone_item.get("indexs", []):
                    if contact_phone_index > ent_index_last:
                        count_ent_contact += 1
                        break
            if count_ent_contact > 1:
                return []
    if len(name_list) == 0:
        pass
    elif len(name_list) == 1:  # 企业名只有一个时，只取里主体最近的一组联系人&电话
        name = name_list[0].get("value", "")
        if name:
            item = {"name": name}
            contact_name = ''
            contact_phone = ''
            phone_distance = 10000000
            name_distance = 10000000
            for ent_index in name_list[0].get("indexs", []):
                for contact_phone_item in contact_phone_list:
                    if not contact_phone_item.get("value", ""):
                        continue
                    for contact_phone_index in contact_phone_item.get("indexs", []):
                        now_distance = contact_phone_index - ent_index
                        if 0 < now_distance < phone_distance and now_distance < max_name_phone_distance:
                            contact_phone = contact_phone_item.get("value", "")
                            phone_distance = now_distance
                for item_contact_name in contact_name_list:
                    if not item_contact_name.get("value", ""):
                        continue
                    for contact_name_index in item_contact_name.get("indexs", []):
                        now_distance = contact_name_index - ent_index
                        if 0 < now_distance < name_distance and now_distance < max_name_phone_distance:
                            contact_name = item_contact_name.get("value", "")
                            name_distance = now_distance
            contact = {}
            if contact_name:
                contact['contact_name'] = contact_name
            if contact_phone:
                contact["contact_phone"] = contact_phone
            if contact:
                item["contact"] = [contact]
            res.append(item)
        # if len(contact_phone_list) <= 1:  # 联系方式小于等于一个
        #     name = name_list[0].get("value", "")
        #     if name:
        #         item = {"name": name}
        #         if len(contact_phone_list) == 1:
        #             contact_phone = contact_phone_list[0].get("value", "")
        #             if contact_phone:
        #                 contact = {"contact_phone": contact_phone}
        #                 contact_name = ""
        #                 for item_contact_name in contact_name_list:
        #                     for contact_name_index in item_contact_name.get("indexs", []):
        #                         for contact_phone_index in contact_phone_list[0].get("indexs", []):
        #                             now_distance = contact_phone_index - contact_name_index
        #                             if now_distance < distance:
        #                                 contact_name = item_contact_name.get("value", "")
        #                                 distance = now_distance
        #                 if contact_name and distance <= max_contact_name_phone_distance:
        #                     contact['contact_name'] = contact_name
        #                 item["contact"] = [contact]
        #         res.append(item)
        # else:  # 联系方式大于一个
        #     name = name_list[0].get("value", "")
        #     if name:
        #         item = {"name": name}
        #         contact = []
        #         for item_contact_phone in contact_phone_list:
        #             contact_phone = item_contact_phone.get("value", "")
        #             if contact_phone:
        #                 contact.append({"contact_phone": contact_phone})
        #         if contact:
        #             item["contact"] = contact
        #         res.append(item)
    elif len(name_list) != len(contact_phone_list):  # 企业名有多个
        if _type in ["zhaobiao", "daili", "zhongbiao"]:
            if len(name_list) == 2:
                if name_list[1].get("value", "") in name_list[0].get("value", ""):
                    item = {"name": name_list[0].get("value", "")}
                    indexs = name_list[0].get("indexs", [])
                else:
                    item = {"name": name_list[-1].get("value", "")}
                    indexs = name_list[-1].get("indexs", [])
            else:
                item = {"name": name_list[0].get("value", "")}
                indexs = name_list[0].get("indexs", [])
            contact_phone = ""
            for item_contact_phone in contact_phone_list:
                for contact_phone_index in item_contact_phone.get("indexs", []):
                    for name_index in indexs:
                        now_distance = contact_phone_index - name_index
                        if now_distance < distance:
                            contact_phone = item_contact_phone.get("value", "")
                            distance = now_distance
            if contact_phone and distance <= max_name_phone_distance:
                item["contact"] = [{
                    "contact_phone": contact_phone
                }]
            res.append(item)
    else:
        for i in range(0, len(contact_phone_list)):
            name_indexes = name_list[i].get("indexs", [])
            phone_indexes = contact_phone_list[i].get("indexs", [])

            found_item_nearby = False
            for n_i in name_indexes:
                for p_i in phone_indexes:
                    if abs(n_i - p_i) < max_name_phone_distance:
                        found_item_nearby = True
            if found_item_nearby:
                res.append({
                    "name": name_list[i].get("value", ""),
                    "contact": [{"contact_phone": contact_phone_list[i].get("value", '')}]
                })
        # elif _type in ["zhongbiao"]:
        #     for item_name in name_list:
        #         item = {"name": item_name.get("value", "")}
        #         res.append(item)
    return res


if __name__ == "__main__":
    name_list = [{'value': '天津市众志成商贸有限公司', 'indexs': [2379, 3157]}]
    contact_phone_list = [{'value': '022-28775832', 'indexs': [7685, 100]},
                          {'value': '023-28775832', 'indexs': [7685, 100]}]
    contact_name_list = [{'value': '陈老师', 'indexs': [8090, 50]}]
    group_by_org(name_list, contact_phone_list, contact_name_list, _type="zhaobiao")
